import numpy as np
import json
import os


def recurrence_matrix(x, eps):

    N = len(x)

    R = np.zeros((N, N))

    for i in range(N):
        for j in range(N):

            if abs(x[i] - x[j]) < eps:
                R[i, j] = 1

    return R


def recurrence_rate(R):

    return np.sum(R) / (R.shape[0] ** 2)


def determinism(R):

    N = R.shape[0]

    det = 0
    total = np.sum(R)

    for i in range(N-2):
        for j in range(N-2):

            if R[i,j] and R[i+1,j+1] and R[i+2,j+2]:
                det += 3

    if total == 0:
        return 0

    return det / total


def main():

    x = np.random.randn(1000)

    R = recurrence_matrix(x, eps=0.5)

    rr = recurrence_rate(R)

    det = determinism(R)

    result = {
        "recurrence_rate": rr,
        "determinism": det
    }

    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/rqa.json","w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
