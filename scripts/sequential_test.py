import numpy as np

ALPHA = 0.01
THRESHOLD = 3.5

def sequential_check(data_stream):
    for i, value in enumerate(data_stream):
        if abs(value) > THRESHOLD:
            print(f"Sequential breach at index {i}")
            return False
    return True

if __name__ == "__main__":
    data = np.load("current_sample.npy")
    result = sequential_check(data)
    if not result:
        exit(1)
    print("Sequential stability confirmed.")
