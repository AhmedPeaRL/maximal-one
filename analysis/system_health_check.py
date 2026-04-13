import os, psutil, sys

print("=== SYSTEM HEALTH CHECK ===")

mem = psutil.virtual_memory()
cpu = psutil.cpu_percent(interval=1)

print(f"Memory usage: {mem.percent}%")
print(f"CPU usage: {cpu}%")

if mem.percent > 90:
    print("❌ Memory overload")
    sys.exit(1)

if cpu > 95:
    print("⚠️ CPU stress")

print("✅ System healthy")
