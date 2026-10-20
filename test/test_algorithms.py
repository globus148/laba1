import unittest
import random

from two_points import two_points
from binary_search import binary_search
from exponential_search import exponential_search
from double_binary import double_binary


class TestCommonElementAlgorithms(unittest.TestCase):
    def setUp(self):
        self.algorithms = [
            ("Two Pointers", two_points),
            ("Binary Search", binary_search),
            ("Exponential Search", exponential_search),
            ("Double Binary", double_binary),
        ]

    def _run_all(self, a, b, expected):
        for name, func in self.algorithms:
            with self.subTest(algorithm=name, a=a, b=b):
                self.assertEqual(
                    func(a, b),
                    expected,
                    f"Algorithm {name} failed on inputs a={a}, b={b}"
                )
                # Симметрия: смена порядка аргументов должна давать тот же результат
                self.assertEqual(
                    func(b, a),
                    expected,
                    f"Algorithm {name} failed on reversed inputs b={b}, a={a}"
                )

    def test_assignment_examples(self):
        """Примеры из условия лабораторной работы."""
        self._run_all([1, 2, 3], [3, 4, 5], True)
        self._run_all([2, 4, 6], [3, 5, 7], False)
        self._run_all([], [], False)

    def test_empty_arrays(self):
        """Тесты с пустыми массивами."""
        self._run_all([], [1, 2, 3], False)
        self._run_all([1, 2, 3], [], False)
        self._run_all([], [], False)

    def test_single_element_arrays(self):
        """Массивы из одного элемента."""
        self._run_all([1], [1], True)
        self._run_all([1], [2], False)
        self._run_all([5], [1, 3, 5, 7], True)
        self._run_all([4], [1, 3, 5, 7], False)

    def test_match_positions(self):
        """Общий элемент в начале, в середине или в конце."""
        # В начале
        self._run_all([1, 10, 20], [1, 2, 3], True)
        # В конце
        self._run_all([1, 10, 20], [15, 18, 20], True)
        # В середине
        self._run_all([1, 10, 20], [5, 10, 15], True)

    def test_completely_disjoint(self):
        """Полностью непересекающиеся массивы (четные и нечетные)."""
        even = list(range(0, 100, 2))
        odd = list(range(1, 100, 2))
        self._run_all(even, odd, False)

    def test_duplicate_elements(self):
        """Массивы с повторяющимися элементами."""
        self._run_all([2, 2, 2], [2], True)
        self._run_all([1, 1, 1], [2, 2, 2], False)
        self._run_all([1, 2, 2, 3], [2, 2, 4], True)

    def test_different_sizes(self):
        """Разные соотношения длин массивов (M << N)."""
        small = [500]
        large = list(range(1000))
        self._run_all(small, large, True)

        small_absent = [-1]
        self._run_all(small_absent, large, False)

        small_absent_large = [2000]
        self._run_all(small_absent_large, large, False)

    def test_random_fuzz(self):
        """Стресс-тест на 2000 случайных пар массивов."""
        rng = random.Random(42)
        for _ in range(2000):
            len_a = rng.randint(0, 60)
            len_b = rng.randint(0, 60)
            a = sorted(rng.sample(range(200), len_a)) if len_a <= 200 else sorted([rng.randint(0, 200) for _ in range(len_a)])
            b = sorted(rng.sample(range(200), len_b)) if len_b <= 200 else sorted([rng.randint(0, 200) for _ in range(len_b)])
            expected = bool(set(a) & set(b))
            self._run_all(a, b, expected)


if __name__ == "__main__":
    unittest.main()
