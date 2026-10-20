import os
import sys
import argparse
import unittest
import matplotlib.pyplot as plt

from test.test_algorithms import TestCommonElementAlgorithms
from benchmark import (
    ALGOS,
    make_symmetric_data,
    make_asymmetric_data,
    get_repeats,
    time_func,
    save_csv,
)


def run_tests():
    print("=== Запуск тестов ===")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCommonElementAlgorithms)
    runner = unittest.TextTestRunner(verbosity=1)
    res = runner.run(suite)
    return res.wasSuccessful()


def run_benchmark(max_power=7, no_gui=False):
    os.makedirs("results", exist_ok=True)
    os.makedirs("graphics", exist_ok=True)

    sizes = [10**p for p in range(0, max_power + 1)]
    results = {name: [] for name, *_ in ALGOS}
    measured = []

    # Настройка графика для live-отрисовки
    fig, ax, lines = None, None, {}
    if not no_gui:
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("Сравнение алгоритмов (M = N, худший случай)")
        ax.set_xlabel("Размер массивов (N)")
        ax.set_ylabel("Время (мс)")
        ax.grid(True, which="both", ls="--", alpha=0.5)

        for name, _, color, marker in ALGOS:
            (line,) = ax.plot([], [], label=name, color=color, marker=marker, linewidth=2)
            lines[name] = line
        ax.legend()
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.1)

    print("\n=== Замер M = N ===")
    for sz in sizes:
        reps = get_repeats(sz)
        a, b = make_symmetric_data(sz)
        row = [f"N={sz:<9}"]

        for name, func, *_ in ALGOS:
            ms = time_func(func, a, b, reps)
            results[name].append(ms)
            row.append(f"{name}: {ms:.4f} ms")
            if not no_gui and fig:
                lines[name].set_data(measured + [sz], results[name])

        measured.append(sz)
        print(" | ".join(row))

        if not no_gui and fig:
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.01)

        del a, b

    save_csv("results/benchmark_symmetric.csv", measured, results)

    # Сохраняем график M = N
    if no_gui or fig is None:
        fig_sym, ax_sym = plt.subplots(figsize=(10, 6))
        ax_sym.set_xscale("log"); ax_sym.set_yscale("log")
        ax_sym.set_title("Сравнение алгоритмов (M = N, худший случай)")
        ax_sym.set_xlabel("Размер массивов (N)"); ax_sym.set_ylabel("Время (мс)")
        ax_sym.grid(True, which="both", ls="--", alpha=0.5)
        for name, _, color, marker in ALGOS:
            ax_sym.plot(measured, results[name], label=name, color=color, marker=marker, linewidth=2)
        ax_sym.legend()
        plt.tight_layout()
        fig_sym.savefig("graphics/benchmark_symmetric.png", dpi=300)
        plt.close(fig_sym)
    else:
        fig.savefig("graphics/benchmark_symmetric.png", dpi=300)

    # Асимметричный замер M = 100 << N
    print("\n=== Замер M = 100 << N ===")
    sizes_asym = [10**p for p in range(2, max_power + 1)]
    res_asym = {name: [] for name, *_ in ALGOS}

    for sz in sizes_asym:
        reps = get_repeats(sz)
        a, b = make_asymmetric_data(100, sz)
        row = [f"N={sz:<9}"]
        for name, func, *_ in ALGOS:
            ms = time_func(func, a, b, reps)
            res_asym[name].append(ms)
            row.append(f"{name}: {ms:.4f} ms")
        print(" | ".join(row))
        del a, b

    save_csv("results/benchmark_asymmetric.csv", sizes_asym, res_asym)

    # График M = 100 << N
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_title("Сравнение алгоритмов при M=100 << N")
    ax2.set_xlabel("Размер большего массива (N)"); ax2.set_ylabel("Время (мс)")
    ax2.grid(True, which="both", ls="--", alpha=0.5)
    for name, _, color, marker in ALGOS:
        ax2.plot(sizes_asym, res_asym[name], label=name, color=color, marker=marker, linewidth=2)
    ax2.legend()
    plt.tight_layout()
    fig2.savefig("graphics/benchmark_asymmetric.png", dpi=300)
    plt.close(fig2)

    print("\n[+] Графики сохранены в graphics/, данные в results/")

    if not no_gui:
        plt.ioff()
        print("[+] Закройте окно графика для завершения программы.")
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-power", type=int, default=7)
    parser.add_argument("--no-gui", action="store_true")
    args = parser.parse_args()

    if run_tests():
        run_benchmark(max_power=args.max_power, no_gui=args.no_gui)
