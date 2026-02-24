import numpy as np
import json

def load_config():
    with open("adversarial/adversarial_config.json") as f:
        return json.load(f)

def generate_sample(n=1000000):
    return np.random.normal(0, 1, n)

def apply_adversarial(data, config):
    if config["heavy_tail_noise"]:
        t_noise = np.random.standard_t(
            config["student_t_df"],
            size=len(data)
        )
        data += t_noise * 0.1

    if config["input_shift"]:
        data += config["input_shift"]

    if config["scale_perturbation"]:
        data *= config["scale_perturbation"]

    return data

if __name__ == "__main__":
    config = load_config()
    data = generate_sample()
    adv_data = apply_adversarial(data, config)
    np.save("current_sample.npy", adv_data)
