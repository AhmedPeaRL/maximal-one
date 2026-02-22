import math

def divisor_count(n):
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i * i == n else 2
        i += 1
    return count

def run(limit=20000):
    worst_ratio = 0
    worst_k = 1

    for k in range(1, limit+1):
        d = divisor_count(k)
        ratio = d / (2 * math.sqrt(k))
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_k = k

        if d > 2 * math.sqrt(k):
            raise ValueError(f"Bound violated at k={k}")

    print("Divisor bound verified.")
    print("Worst ratio:", worst_ratio)
    print("Worst k:", worst_k)

if __name__ == "__main__":
    run()
