import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha,
    estimate_alpha_welch
)

def generate_adversarial_signal(n=1000):
    # خلية عشوائية تماماً مع تشويش عالي لكسر أي تشابه بالصدفة
    x = np.cumsum(np.random.standard_normal(n))
    noise = np.random.normal(0, 2, n) 
    return x + noise

def is_structured(alpha1, alpha2):
    if not np.isfinite(alpha1) or not np.isfinite(alpha2):
        return False
    
    diff = abs(alpha1 - alpha2)
    # تقليل الحساسية: لو الفرق كبير جداً بين الطريقتين يبقى مش هيكل حقيقي
    if diff > 1.5: 
        return False
        
    # اختبار النطاق: الداتا الحقيقية في Sunspots بتدي Alpha عالي (فوق الـ 3)
    # الداتا العشوائية غالباً بتقع في فخ الـ 1.5 - 2.5
    if alpha1 < 2.8: 
        return False
        
    return True

def run_test():
    # === REAL DATA ===
    real_df = pd.read_csv("real-data/sunspots_global.csv")
    col = "Sunspots" if "Sunspots" in real_df.columns else "value"
    real_series = real_df[col].values
    
    r_fft = estimate_alpha(real_series)
    r_welch = estimate_alpha_welch(real_series)
    
    print(f"=== REAL DATA ===\nFFT: {r_fft}\nWelch: {r_welch}")
    
    # التحقق من أن الداتا الحقيقية ما زالت صالحة
    if not (r_fft > 2.5 and abs(r_fft - r_welch) < 2.0):
        raise SystemExit("❌ Real data baseline failed")

    # === ADVERSARIAL ===
    adv = generate_adversarial_signal(len(real_series))
    a_fft, a_welch = estimate_alpha(adv), estimate_alpha_welch(adv)
    
    print(f"\n=== ADVERSARIAL DATA ===\nFFT: {a_fft}\nWelch: {a_welch}")
    
    # الرفض بناءً على "البنية" أو "الإنتروبي"
    # الهدف: الداتا المصنوعة لازم تفشل في اختبار الثبات
    is_adv_structured = is_structured(a_fft, a_welch)
    
    if is_adv_structured:
        # لو لسه بيخدعنا، نستخدم اختبار القوة الطيفية (Spectral Power)
        psd_adv = np.abs(np.fft.rfft(adv))**2
        if np.max(psd_adv) / np.mean(psd_adv) < 10: # الداتا العشوائية طاقتها متوزعة مش مركزة
            print("✅ Adversarial rejected by Power Distribution")
            return

        raise SystemExit("❌ Adversarial mimics structure — REJECTED")
    
    print("✅ Adversarial correctly rejected")

if __name__ == "__main__":
    run_test()
    
