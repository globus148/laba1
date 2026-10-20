import time
import csv
from two_points import two_points
from binary_search import binary_search
from exponential_search import exponential_search
from double_binary import double_binary

ALGOS = [
    ("Два указателя", two_points, "#0984e3", "o"),
    ("Бинарный поиск", binary_search, "#d63031", "s"),
    ("Экспоненциальный", exponential_search, "#00b894", "^"),
    ("Двойной бинарный", double_binary, "#6c5ce7", "D"),
]


def make_symmetric_data(n):
    # Худший случай: четные в a, нечетные в b (общих элементов нет)
    return list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))


def make_asymmetric_data(m, n):
    # m четных чисел равномерно распределены по диапазону b
    step = max(2, (2 * n) // m)
    a = [(i * step) & ~1 for i in range(m)]
    b = list(range(1, 2 * n, 2))
    return a, b


def get_repeats(size):
    if size <= 100:
        return 500
    if size <= 1000:
        return 100
    if size <= 10000:
        return 20
    if size <= 100000:
        return 10
    if size <= 1000000:
        return 5
    return 2


def time_func(func, a, b, repeats):
    t0 = time.perf_counter()
    for _ in range(repeats):
        func(a, b)
    return ((time.perf_counter() - t0) / repeats) * 1000.0


def save_csv(path, sizes, results):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["N"] + [name for name, *_ in ALGOS])
        for i, sz in enumerate(sizes):
            writer.writerow([sz] + [f"{results[name][i]:.6f}" for name, *_ in ALGOS])
