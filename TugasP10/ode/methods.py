from typing import Any, Callable, Dict, List
from .problem import validate_inputs


def euler(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    b: float,
    n: int
) -> List[Dict[str, Any]]:
    validate_inputs(x0, y0, b, n)
    h = (b - x0) / n
    results: List[Dict[str, Any]] = []

    y = float(y0)
    for i in range(n):
        x = x0 + i * h
        k1 = f(x, y)
        results.append({
            "i": i,
            "x": x,
            "y": y,
            "k1": k1,
        })
        y = y + h * k1

    results.append({
        "i": n,
        "x": float(b),
        "y": y,
        "k1": None,
    })

    return results


def heun(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    b: float,
    n: int
) -> List[Dict[str, Any]]:
    validate_inputs(x0, y0, b, n)
    h = (b - x0) / n
    results: List[Dict[str, Any]] = []

    y = float(y0)
    for i in range(n):
        x = x0 + i * h
        k1 = f(x, y)
        x_next = float(b) if i == n - 1 else x0 + (i + 1) * h
        y_predictor = y + k1 * h
        k2 = f(x_next, y_predictor)

        results.append({
            "i": i,
            "x": x,
            "y": y,
            "k1": k1,
            "k2": k2,
        })
        y = y + (h / 2.0) * (k1 + k2)

    results.append({
        "i": n,
        "x": float(b),
        "y": y,
        "k1": None,
        "k2": None,
    })

    return results


def rk4(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    b: float,
    n: int
) -> List[Dict[str, Any]]:
    validate_inputs(x0, y0, b, n)
    h = (b - x0) / n
    results: List[Dict[str, Any]] = []

    y = float(y0)
    for i in range(n):
        x = x0 + i * h
        half_h = 0.5 * h
        x_mid = x + half_h
        x_next = float(b) if i == n - 1 else x0 + (i + 1) * h

        k1 = f(x, y)
        k2 = f(x_mid, y + 0.5 * k1 * h)
        k3 = f(x_mid, y + 0.5 * k2 * h)
        k4 = f(x_next, y + k3 * h)

        results.append({
            "i": i,
            "x": x,
            "y": y,
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
        })
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    results.append({
        "i": n,
        "x": float(b),
        "y": y,
        "k1": None,
        "k2": None,
        "k3": None,
        "k4": None,
    })

    return results
