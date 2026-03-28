import numpy as np

def entropy(x, bins=50):
    hist, _ = np.histogram(x, bins=bins, density=True)
    hist = hist + 1e-12
    return -np.sum(hist * np.log(hist))

def mutual_information(x, y, bins=50):
    joint_hist, _, _ = np.histogram2d(x, y, bins=bins)
    joint_hist = joint_hist + 1e-12
    joint_prob = joint_hist / np.sum(joint_hist)

    px = np.sum(joint_prob, axis=1)
    py = np.sum(joint_prob, axis=0)

    mi = 0
    for i in range(len(px)):
        for j in range(len(py)):
            mi += joint_prob[i,j] * np.log(joint_prob[i,j] / (px[i]*py[j]))

    return mi

def info_gain(history, pred):
    target = np.array(history[1:])
    source = np.array(history[:-1])

    baseline = mutual_information(source, target)
    enhanced = mutual_information(source, pred[:len(source)])

    return float(enhanced - baseline)
