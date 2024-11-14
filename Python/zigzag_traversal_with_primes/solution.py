def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def zigzag_traverse_and_primes(matrix):
    n = len(matrix)

    results = []
    for i in range(n):
        if i % 2 == 0:
            results.extend(matrix[i][j] for j in range(n))
        else:
            results.extend(matrix[i][j] for j in reversed(range(n)))
    return {k + 1: v for k, v in enumerate(results) if is_prime(v)}