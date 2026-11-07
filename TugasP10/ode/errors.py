from typing import Optional


def absolute_error(exact: float, approx: float) -> float:
    return abs(exact - approx)


def relative_error(exact: float, approx: float) -> float:
    abs_exact = abs(exact)
    abs_err = abs(exact - approx)
    if abs_exact < 1e-15:
        return 0.0 if abs_err < 1e-15 else float("inf")
    return abs_err / abs_exact


def relative_error_percent(exact: float, approx: float) -> float:
    return relative_error(exact, approx) * 100.0


def format_value(val: Optional[float], precision: int = 8) -> str:
    if val is None:
        return "-"
    return f"{val:.{precision}f}"


def format_error(val: Optional[float], precision: int = 8, scientific_thresh: float = 1e-4) -> str:
    if val is None:
        return "-"
    abs_val = abs(val)
    if abs_val == 0.0:
        return f"{0.0:.{precision}f}"
    if abs_val < scientific_thresh:
        return f"{val:.4e}"
    return f"{val:.{precision}f}"
