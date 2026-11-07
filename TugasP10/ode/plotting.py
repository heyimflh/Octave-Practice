import os
from typing import Any, Callable, Dict, List


def is_matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot
        return True
    except ImportError:
        return False


def plot_comparison(
    exact_func: Callable[[float], float],
    iterations_dict: Dict[str, List[Dict[str, Any]]],
    x0: float,
    b: float,
    output_path: str
) -> bool:
    if not is_matplotlib_available():
        print("[PERINGATAN]: Pustaka 'matplotlib' tidak ditemukan. Pembuatan grafik perbandingan dilewati.")
        return False

    import matplotlib.pyplot as plt

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(9, 6), dpi=300)

    num_points = 200
    x_dense = [x0 + i * (b - x0) / (num_points - 1) for i in range(num_points)]
    y_dense = [exact_func(x) for x in x_dense]
    plt.plot(x_dense, y_dense, "k-", linewidth=2.0, label="Solusi Eksak (Analitik)", zorder=1)

    styles = {
        "Euler": {"color": "#e74c3c", "marker": "s", "linestyle": "--", "label": "Euler (Orde-1)"},
        "Heun": {"color": "#3498db", "marker": "^", "linestyle": "-.", "label": "Heun (Orde-2)"},
        "Runge-Kutta 4": {"color": "#2ecc71", "marker": "o", "linestyle": ":", "label": "RK4 (Orde-4)"},
    }

    for name, iters in iterations_dict.items():
        xs = [step["x"] for step in iters]
        ys = [step["y"] for step in iters]
        style = styles.get(name, {"color": "gray", "marker": "x", "linestyle": "-", "label": name})
        plt.plot(
            xs,
            ys,
            color=style["color"],
            marker=style["marker"],
            linestyle=style["linestyle"],
            linewidth=1.5,
            markersize=5,
            alpha=0.9,
            label=style["label"],
            zorder=2,
        )

    plt.title("Perbandingan Solusi PDB: dy/dx = (4x³ − 2x + 1)/(2 + y),  y(0) = 1", fontsize=12, fontweight="bold")
    plt.xlabel("Variabel Bebas (x)", fontsize=11)
    plt.ylabel("Variabel Terikat (y)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left", framealpha=0.9)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    return True


def plot_errors(
    exact_func: Callable[[float], float],
    iterations_dict: Dict[str, List[Dict[str, Any]]],
    output_path: str
) -> bool:
    if not is_matplotlib_available():
        print("[PERINGATAN]: Pustaka 'matplotlib' tidak ditemukan. Pembuatan grafik galat dilewati.")
        return False

    import matplotlib.pyplot as plt

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(9, 6), dpi=300)

    styles = {
        "Euler": {"color": "#e74c3c", "marker": "s", "linestyle": "-", "label": "Galat Absolut Euler"},
        "Heun": {"color": "#3498db", "marker": "^", "linestyle": "-", "label": "Galat Absolut Heun"},
        "Runge-Kutta 4": {"color": "#2ecc71", "marker": "o", "linestyle": "-", "label": "Galat Absolut RK4"},
    }

    for name, iters in iterations_dict.items():
        xs = [step["x"] for step in iters]
        errors = [max(abs(exact_func(step["x"]) - step["y"]), 1e-16) for step in iters]
        style = styles.get(name, {"color": "gray", "marker": "x", "linestyle": "-", "label": name})
        plt.semilogy(
            xs,
            errors,
            color=style["color"],
            marker=style["marker"],
            linestyle=style["linestyle"],
            linewidth=1.5,
            markersize=5,
            label=style["label"],
        )

    plt.title("Galat Absolut Tiap Langkah (|y_eksak − y_aprok|)", fontsize=12, fontweight="bold")
    plt.xlabel("Variabel Bebas (x)", fontsize=11)
    plt.ylabel("Galat Absolut (Skala Logaritmik)", fontsize=11)
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend(loc="upper left", framealpha=0.9)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    return True
