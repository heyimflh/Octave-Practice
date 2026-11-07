import math

DEFAULT_X0: float = 0.0
DEFAULT_Y0: float = 1.0
DEFAULT_B: float = 2.0
DEFAULT_N: int = 15
DEFAULT_PRECISION: int = 8


def f(x: float, y: float) -> float:
    denominator = 2.0 + y
    if abs(denominator) < 1e-15:
        raise ZeroDivisionError(
            f"Pembagi bernilai nol pada f({x}, {y}): 2 + y = 0 (singularitas pada y = -2)."
        )
    numerator = 4.0 * (x ** 3) - 2.0 * x + 1.0
    return numerator / denominator


def y_exact(x: float) -> float:
    radicand = 2.0 * (x ** 4) - 2.0 * (x ** 2) + 2.0 * x + 9.0
    if radicand < 0.0:
        raise ValueError(
            f"Radikan negatif di bawah tanda akar untuk x = {x}: {radicand} < 0."
        )
    return -2.0 + math.sqrt(radicand)


def validate_inputs(x0: float, y0: float, b: float, n: int) -> None:
    if not isinstance(n, int):
        raise TypeError(f"Jumlah langkah n harus berupa bilangan bulat (int), didapat {type(n).__name__}.")
    if n <= 0:
        raise ValueError(f"Jumlah langkah n harus bernilai bulat positif (> 0), didapat {n}.")
    if abs(b - x0) < 1e-15:
        raise ValueError(f"Titik akhir b ({b}) tidak boleh sama dengan titik awal x0 ({x0}).")
    if abs(2.0 + y0) < 1e-15:
        raise ZeroDivisionError(f"Kondisi awal y0={y0} menyebabkan pembagian dengan nol (2 + y0 = 0).")
