import math
import os
import sys
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

@dataclass
class IterationRow:
    iteration: int
    a: float
    b: float
    fa: float
    fb: float
    c: float
    fc: float
    error: Optional[float]
    half_width: float

@dataclass
class SolverResult:
    method_name: str
    problem_id: int
    problem_title: str
    equation_str: str
    a0: float
    b0: float
    root: Optional[float]
    f_root: Optional[float]
    iterations: int
    final_error: Optional[float]
    converged: bool
    stopping_reason: str
    history: List[IterationRow]


@dataclass
class ProblemConfig:
    problem_id: int
    title: str
    original_eq: str
    target_eq: str
    residual_eq_str: str
    func: Callable[[float], float]
    single_func: Callable[[float], float]
    single_target_val: float
    single_curve_label: str
    single_target_label: str
    double_func1: Callable[[float], float]
    double_func2: Callable[[float], float]
    double_label1: str
    double_label2: str
    x_plot_min: float
    x_plot_max: float
    default_intervals: List[Tuple[float, float]]
    domain_description: str
    domain_validator: Callable[[float], bool]
    notes: str

def f1_residual(x: float) -> float:
    return 3.0 * (x ** 3) - 5.0 * (x ** 2) + 4.0 * x - 8.0

def f1_original(x: float) -> float:
    return 3.0 * (x ** 3) - 5.0 * (x ** 2) + 4.0 * x - 7.0

def f2_residual(x: float) -> float:
    try:
        return math.exp(x) - (x ** 2)
    except OverflowError:
        return float('inf')

def f2_exp(x: float) -> float:
    try:
        return math.exp(x)
    except OverflowError:
        return float('inf')

def f2_poly(x: float) -> float:
    return x ** 2

def f3_residual(x: float) -> float:
    if x + 2.0 <= 0.0:
        raise ValueError(f"Domain error: Argumen logaritma (x + 2 = {x + 2.0}) <= 0 pada x = {x}. Domain sah: x > -2.")
    return math.log10(x + 2.0) + 2.0 * x - 3.0

def f3_curve1(x: float) -> float:
    if x + 2.0 <= 0.0:
        raise ValueError(f"Domain error: x + 2 <= 0 pada x = {x}")
    return math.log10(x + 2.0) + 2.0 * x

def f3_curve2(x: float) -> float:
    return 3.0

PROBLEMS: dict[int, ProblemConfig] = {
    1: ProblemConfig(
        problem_id=1,
        title="Soal 1: Polinomial Kubik",
        original_eq="y = 3x^3 - 5x^2 + 4x - 7",
        target_eq="y = 1",
        residual_eq_str="f1(x) = 3x^3 - 5x^2 + 4x - 8 = 0",
        func=f1_residual,
        single_func=f1_original,
        single_target_val=1.0,
        single_curve_label="y = 3x^3 - 5x^2 + 4x - 7",
        single_target_label="Target y = 1",
        double_func1=f1_original,
        double_func2=lambda x: 1.0,
        double_label1="y1 = 3x^3 - 5x^2 + 4x - 7",
        double_label2="y2 = 1",
        x_plot_min=-2.0,
        x_plot_max=4.0,
        default_intervals=[(1.0, 2.0)],
        domain_description="Semua bilangan real (x in R)",
        domain_validator=lambda x: True,
        notes="Target persamaan di slide adalah y = 1, sehingga residual f(x) = 0 diperoleh dengan mengurangkan 1 (konstanta menjadi -8)."
    ),
    2: ProblemConfig(
        problem_id=2,
        title="Soal 2: Eksponensial & Kuadrat",
        original_eq="y = e^x - x^2",
        target_eq="y = 0",
        residual_eq_str="f2(x) = exp(x) - x^2 = 0",
        func=f2_residual,
        single_func=f2_residual,
        single_target_val=0.0,
        single_curve_label="y = exp(x) - x^2",
        single_target_label="Target y = 0 (Sumbu-X)",
        double_func1=f2_exp,
        double_func2=f2_poly,
        double_label1="y1 = exp(x)",
        double_label2="y2 = x^2",
        x_plot_min=-3.0,
        x_plot_max=3.0,
        default_intervals=[(-1.0, 0.0)],
        domain_description="Semua bilangan real (x in R)",
        domain_validator=lambda x: True,
        notes=(
            "Catatan Matematis Soal 2: Turunan f'(x) = exp(x) - 2x > 0 untuk seluruh x real "
            "(nilai minimum f'(x) adalah 2 - 2*ln(2) ~ 0.6137 > 0), sehingga fungsi strictly monotonically "
            "increasing dan memiliki tepat 1 akar real di x ~ -0.703467. "
            "Program mendukung pemindaian dan penyelesaian interval terpisah untuk akar berbeda jika dikonfigurasi."
        )
    ),
    3: ProblemConfig(
        problem_id=3,
        title="Soal 3: Logaritma & Linier",
        original_eq="y = log(x + 2) + 2x - 3",
        target_eq="y = 0",
        residual_eq_str="f3(x) = log10(x + 2) + 2x - 3 = 0",
        func=f3_residual,
        single_func=f3_residual,
        single_target_val=0.0,
        single_curve_label="y = log10(x + 2) + 2x - 3",
        single_target_label="Target y = 0 (Sumbu-X)",
        double_func1=f3_curve1,
        double_func2=f3_curve2,
        double_label1="y1 = log10(x + 2) + 2x",
        double_label2="y2 = 3",
        x_plot_min=-1.9,
        x_plot_max=4.0,
        default_intervals=[(1.0, 2.0)],
        domain_description="x > -2 (argumen logaritma x + 2 harus bernilai positif)",
        domain_validator=lambda x: x > -2.0,
        notes="Asumsi PRD: Notasi 'log' pada slide merujuk pada basis 10 (log10). Domain x > -2 divalidasi ketat."
    )
}

def validate_interval(func: Callable[[float], float],
                      a: float,
                      b: float,
                      domain_validator: Optional[Callable[[float], bool]] = None) -> Tuple[bool, str, float, float]:
    if a >= b:
        return False, f"Batas kiri 'a' ({a}) harus lebih kecil dari batas kanan 'b' ({b}).", 0.0, 0.0

    if domain_validator is not None:
        if not domain_validator(a):
            return False, f"Batas 'a' = {a} berada di luar domain sah fungsi!", 0.0, 0.0
        if not domain_validator(b):
            return False, f"Batas 'b' = {b} berada di luar domain sah fungsi!", 0.0, 0.0

    try:
        fa = func(a)
    except Exception as e:
        return False, f"Gagal mengevaluasi f(a) pada x = {a}: {e}", 0.0, 0.0

    try:
        fb = func(b)
    except Exception as e:
        return False, f"Gagal mengevaluasi f(b) pada x = {b}: {e}", 0.0, 0.0

    if math.isnan(fa) or math.isinf(fa):
        return False, f"Nilai f(a) pada x = {a} tidak valid ({fa}).", fa, fb
    if math.isnan(fb) or math.isinf(fb):
        return False, f"Nilai f(b) pada x = {b} tidak valid ({fb}).", fa, fb

    if fa * fb > 0.0:
        msg = (
            f"Interval [{a}, {b}] TIDAK MENGURUNG AKAR! "
            f"f(a) = {fa:+.6f} dan f(b) = {fb:+.6f} memiliki tanda yang sama (f(a) * f(b) > 0). "
            f"Metode bracket memerlukan tanda berlawanan agar konvergensi terjamin."
        )
        return False, msg, fa, fb

    return True, "Interval valid dan mengurung akar.", fa, fb

def bisection(func: Callable[[float], float],
              a: float,
              b: float,
              tol: float = 1e-4,
              max_iter: int = 20,
              domain_validator: Optional[Callable[[float], bool]] = None,
              problem_id: int = 1,
              problem_title: str = "",
              equation_str: str = "") -> SolverResult:
    valid, err_msg, fa, fb = validate_interval(func, a, b, domain_validator)
    if not valid:
        return SolverResult(
            method_name="Biseksi",
            problem_id=problem_id,
            problem_title=problem_title,
            equation_str=equation_str,
            a0=a,
            b0=b,
            root=None,
            f_root=None,
            iterations=0,
            final_error=None,
            converged=False,
            stopping_reason=f"Validasi Gagal: {err_msg}",
            history=[]
        )
    if abs(fa) < 1e-15:
        return SolverResult(
            method_name="Biseksi",
            problem_id=problem_id,
            problem_title=problem_title,
            equation_str=equation_str,
            a0=a,
            b0=b,
            root=a,
            f_root=fa,
            iterations=0,
            final_error=0.0,
            converged=True,
            stopping_reason="Batas kiri 'a' adalah akar eksak.",
            history=[]
        )
    if abs(fb) < 1e-15:
        return SolverResult(
            method_name="Biseksi",
            problem_id=problem_id,
            problem_title=problem_title,
            equation_str=equation_str,
            a0=a,
            b0=b,
            root=b,
            f_root=fb,
            iterations=0,
            final_error=0.0,
            converged=True,
            stopping_reason="Batas kanan 'b' adalah akar eksak.",
            history=[]
        )

    history: List[IterationRow] = []
    c_prev: Optional[float] = None
    curr_a = a
    curr_b = b
    curr_fa = fa
    curr_fb = fb

    converged = False
    stopping_reason = ""
    final_root = 0.0
    final_fc = 0.0
    final_err: Optional[float] = None

    for i in range(1, max_iter + 1):
        c = (curr_a + curr_b) / 2.0
        try:
            fc = func(c)
        except Exception as e:
            stopping_reason = f"Terjadi kesalahan saat evaluasi f(c) pada iterasi {i}: {e}"
            break

        error = abs(c - c_prev) if c_prev is not None else None
        half_w = abs(curr_b - curr_a) / 2.0

        history.append(IterationRow(
            iteration=i,
            a=curr_a,
            b=curr_b,
            fa=curr_fa,
            fb=curr_fb,
            c=c,
            fc=fc,
            error=error,
            half_width=half_w
        ))

        final_root = c
        final_fc = fc
        final_err = error

        if abs(fc) < 1e-15:
            converged = True
            stopping_reason = f"Akar eksak ditemukan pada iterasi ke-{i} (f(c) = 0)."
            break

        if error is not None and error < tol:
            converged = True
            stopping_reason = f"Toleransi selisih akar terpenuhi: |c_k - c_{{k-1}}| = {error:.6e} < {tol} (Iterasi ke-{i})."
            break

        if abs(fc) < tol:
            converged = True
            stopping_reason = f"Toleransi nilai fungsi terpenuhi: |f(c)| = {abs(fc):.6e} < {tol} (Iterasi ke-{i})."
            break

        if curr_fa * fc < 0.0:
            curr_b = c
            curr_fb = fc
        else:
            curr_a = c
            curr_fa = fc

        c_prev = c

    if not converged and not stopping_reason:
        stopping_reason = f"Batas maksimum iterasi ({max_iter}) tercapai tanpa memenuhi toleransi {tol}."

    return SolverResult(
        method_name="Biseksi",
        problem_id=problem_id,
        problem_title=problem_title,
        equation_str=equation_str,
        a0=a,
        b0=b,
        root=final_root,
        f_root=final_fc,
        iterations=len(history),
        final_error=final_err,
        converged=converged,
        stopping_reason=stopping_reason,
        history=history
    )

def regula_falsi(func: Callable[[float], float],
                 a: float,
                 b: float,
                 tol: float = 1e-4,
                 max_iter: int = 20,
                 domain_validator: Optional[Callable[[float], bool]] = None,
                 problem_id: int = 1,
                 problem_title: str = "",
                 equation_str: str = "") -> SolverResult:

    valid, err_msg, fa, fb = validate_interval(func, a, b, domain_validator)
    if not valid:
        return SolverResult(
            method_name="Regula-Falsi",
            problem_id=problem_id,
            problem_title=problem_title,
            equation_str=equation_str,
            a0=a,
            b0=b,
            root=None,
            f_root=None,
            iterations=0,
            final_error=None,
            converged=False,
            stopping_reason=f"Validasi Gagal: {err_msg}",
            history=[]
        )

    if abs(fa) < 1e-15:
        return SolverResult(
            method_name="Regula-Falsi",
            problem_id=problem_id,
            problem_title=problem_title,
            equation_str=equation_str,
            a0=a,
            b0=b,
            root=a,
            f_root=fa,
            iterations=0,
            final_error=0.0,
            converged=True,
            stopping_reason="Batas kiri 'a' adalah akar eksak.",
            history=[]
        )
    if abs(fb) < 1e-15:
        return SolverResult(
            method_name="Regula-Falsi",
            problem_id=problem_id,
            problem_title=problem_title,
            equation_str=equation_str,
            a0=a,
            b0=b,
            root=b,
            f_root=fb,
            iterations=0,
            final_error=0.0,
            converged=True,
            stopping_reason="Batas kanan 'b' adalah akar eksak.",
            history=[]
        )

    history: List[IterationRow] = []
    c_prev: Optional[float] = None
    curr_a = a
    curr_b = b
    curr_fa = fa
    curr_fb = fb

    converged = False
    stopping_reason = ""
    final_root = 0.0
    final_fc = 0.0
    final_err: Optional[float] = None

    for i in range(1, max_iter + 1):
        denom = curr_fb - curr_fa
        if abs(denom) < 1e-14:
            stopping_reason = f"Error Numerik: Penyebut f(b) - f(a) bernilai nol/sangat kecil ({denom}) pada iterasi {i}."
            break

        c = (curr_a * curr_fb - curr_b * curr_fa) / denom
        try:
            fc = func(c)
        except Exception as e:
            stopping_reason = f"Terjadi kesalahan saat evaluasi f(c) pada iterasi {i}: {e}"
            break

        error = abs(c - c_prev) if c_prev is not None else None
        half_w = abs(curr_b - curr_a) / 2.0

        history.append(IterationRow(
            iteration=i,
            a=curr_a,
            b=curr_b,
            fa=curr_fa,
            fb=curr_fb,
            c=c,
            fc=fc,
            error=error,
            half_width=half_w
        ))

        final_root = c
        final_fc = fc
        final_err = error
        if abs(fc) < 1e-15:
            converged = True
            stopping_reason = f"Akar eksak ditemukan pada iterasi ke-{i} (f(c) = 0)."
            break
        if error is not None and error < tol:
            converged = True
            stopping_reason = f"Toleransi selisih akar terpenuhi: |c_k - c_{{k-1}}| = {error:.6e} < {tol} (Iterasi ke-{i})."
            break
        if abs(fc) < tol:
            converged = True
            stopping_reason = f"Toleransi nilai fungsi terpenuhi: |f(c)| = {abs(fc):.6e} < {tol} (Iterasi ke-{i})."
            break
        if curr_fa * fc < 0.0:
            curr_b = c
            curr_fb = fc
        else:
            curr_a = c
            curr_fa = fc
        c_prev = c

    if not converged and not stopping_reason:
        stopping_reason = f"Batas maksimum iterasi ({max_iter}) tercapai tanpa memenuhi toleransi {tol}."

    return SolverResult(
        method_name="Regula-Falsi",
        problem_id=problem_id,
        problem_title=problem_title,
        equation_str=equation_str,
        a0=a,
        b0=b,
        root=final_root,
        f_root=final_fc,
        iterations=len(history),
        final_error=final_err,
        converged=converged,
        stopping_reason=stopping_reason,
        history=history
    )

def scan_graphic_roots(func: Callable[[float], float],
                       x_min: float,
                       x_max: float,
                       steps: int = 500,
                       domain_validator: Optional[Callable[[float], bool]] = None) -> List[Tuple[float, float, float]]:
    xs = np.linspace(x_min, x_max, steps)
    detected: List[Tuple[float, float, float]] = []

    prev_x: Optional[float] = None
    prev_y: Optional[float] = None

    for x in xs:
        if domain_validator and not domain_validator(float(x)):
            prev_x, prev_y = None, None
            continue
        try:
            y = func(float(x))
            if math.isnan(y) or math.isinf(y):
                prev_x, prev_y = None, None
                continue
        except Exception:
            prev_x, prev_y = None, None
            continue

        if prev_x is not None and prev_y is not None:
            if prev_y * y <= 0.0:
                if abs(y - prev_y) > 1e-12:
                    c_est = prev_x - prev_y * (x - prev_x) / (y - prev_y)
                else:
                    c_est = (prev_x + x) / 2.0
                detected.append((prev_x, float(x), float(c_est)))

        prev_x = float(x)
        prev_y = y

    return detected

def plot_single_graph(prob: ProblemConfig,
                      estimated_root: Optional[float] = None,
                      save_path: Optional[str] = None,
                      show_plot: bool = False) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=120)

    xs = np.linspace(prob.x_plot_min, prob.x_plot_max, 400)
    ys = []
    valid_xs = []
    for x in xs:
        if prob.domain_validator(float(x)):
            try:
                val = prob.single_func(float(x))
                if not (math.isnan(val) or math.isinf(val)):
                    valid_xs.append(x)
                    ys.append(val)
            except Exception:
                pass

    ax.plot(valid_xs, ys, label=prob.single_curve_label, color="#1f77b4", linewidth=2.0)
    ax.axhline(prob.single_target_val, color="#d62728", linestyle="--", linewidth=1.8,
               label=f"{prob.single_target_label} (y = {prob.single_target_val:.1f})")

    ax.axhline(0, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)
    ax.axvline(0, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)

    if estimated_root is not None:
        try:
            y_at_root = prob.single_func(estimated_root)
            ax.scatter([estimated_root], [y_at_root], color="#2ca02c", s=80, zorder=5,
                       label=f"Estimasi Titik Potong/Akar (~{estimated_root:.4f})")
            ax.annotate(
                f"Akar ~ {estimated_root:.4f}\n(x={estimated_root:.4f}, y={y_at_root:.2f})",
                xy=(estimated_root, y_at_root),
                xytext=(estimated_root + 0.35 * (prob.x_plot_max - prob.x_plot_min) / 5.0,
                        y_at_root + 0.15 * (max(ys) - min(ys)) if ys else y_at_root + 1),
                arrowprops=dict(facecolor="#2ca02c", shrink=0.08, width=1.5, headwidth=6),
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="#2ca02c", facecolor="#f0fff0", alpha=0.9),
                fontsize=9
            )
        except Exception:
            pass

    ax.set_title(f"{prob.title} --- Pendekatan Grafik Tunggal\nPersamaan: {prob.original_eq} | Target: {prob.target_eq}",
                 fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Sumbu x", fontsize=10, fontweight="semibold")
    ax.set_ylabel("Sumbu y", fontsize=10, fontweight="semibold")
    ax.grid(True, linestyle="--", alpha=0.55)
    ax.legend(loc="best", frameon=True, framealpha=0.9)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    if show_plot:
        try:
            plt.show()
        except Exception as e:
            print(f"  [Catatan Tampilan] Jendela grafik tidak dapat dibuka interaktif: {e}")

    return fig

def plot_double_graph(prob: ProblemConfig,
                      estimated_root: Optional[float] = None,
                      save_path: Optional[str] = None,
                      show_plot: bool = False) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=120)

    xs = np.linspace(prob.x_plot_min, prob.x_plot_max, 400)
    y1_vals = []
    y2_vals = []
    valid_xs = []

    for x in xs:
        if prob.domain_validator(float(x)):
            try:
                v1 = prob.double_func1(float(x))
                v2 = prob.double_func2(float(x))
                if not (math.isnan(v1) or math.isinf(v1) or math.isnan(v2) or math.isinf(v2)):
                    valid_xs.append(x)
                    y1_vals.append(v1)
                    y2_vals.append(v2)
            except Exception:
                pass

    ax.plot(valid_xs, y1_vals, label=prob.double_label1, color="#1f77b4", linewidth=2.0)
    ax.plot(valid_xs, y2_vals, label=prob.double_label2, color="#ff7f0e", linewidth=2.0, linestyle="--")

    ax.axhline(0, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)
    ax.axvline(0, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)

    if estimated_root is not None:
        try:
            y_intersect = prob.double_func1(estimated_root)
            ax.scatter([estimated_root], [y_intersect], color="#d62728", s=85, zorder=5,
                       label=f"Titik Potong y1 = y2 (~{estimated_root:.4f})")
            ax.annotate(
                f"Perpotongan di x ~ {estimated_root:.4f}\n(y = {y_intersect:.4f})",
                xy=(estimated_root, y_intersect),
                xytext=(estimated_root + 0.35 * (prob.x_plot_max - prob.x_plot_min) / 5.0,
                        y_intersect + 0.15 * (max(y1_vals) - min(y1_vals)) if y1_vals else y_intersect + 1),
                arrowprops=dict(facecolor="#d62728", shrink=0.08, width=1.5, headwidth=6),
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="#d62728", facecolor="#fff5f5", alpha=0.9),
                fontsize=9
            )
        except Exception:
            pass

    ax.set_title(f"{prob.title} --- Pendekatan Grafik Ganda\nPerpotongan {prob.double_label1} dan {prob.double_label2}",
                 fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Sumbu x", fontsize=10, fontweight="semibold")
    ax.set_ylabel("Sumbu y", fontsize=10, fontweight="semibold")
    ax.grid(True, linestyle="--", alpha=0.55)
    ax.legend(loc="best", frameon=True, framealpha=0.9)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    if show_plot:
        try:
            plt.show()
        except Exception as e:
            print(f"  [Catatan Tampilan] Jendela grafik tidak dapat dibuka interaktif: {e}")

    return fig

def plot_combined_summary(all_results: dict[int, Tuple[ProblemConfig, List[Tuple[float, float, float]]]],
                          save_path: str = "grafik_semua_soal.png") -> plt.Figure:
    fig, axes = plt.subplots(3, 2, figsize=(15, 14), dpi=120)

    for idx, pid in enumerate([1, 2, 3]):
        prob, scanned_roots = all_results[pid]
        est_root = scanned_roots[0][2] if scanned_roots else None

        ax_l = axes[idx, 0]
        xs = np.linspace(prob.x_plot_min, prob.x_plot_max, 300)
        valid_xs, ys = [], []
        for x in xs:
            if prob.domain_validator(float(x)):
                try:
                    v = prob.single_func(float(x))
                    if not (math.isnan(v) or math.isinf(v)):
                        valid_xs.append(x)
                        ys.append(v)
                except Exception:
                    pass

        ax_l.plot(valid_xs, ys, label=prob.single_curve_label, color="#1f77b4", linewidth=1.8)
        ax_l.axhline(prob.single_target_val, color="#d62728", linestyle="--", linewidth=1.5,
                     label=f"{prob.single_target_label} ({prob.single_target_val:.1f})")
        ax_l.axhline(0, color="gray", linestyle=":", linewidth=0.6, alpha=0.6)
        if est_root is not None:
            try:
                y_r = prob.single_func(est_root)
                ax_l.scatter([est_root], [y_r], color="#2ca02c", s=60, zorder=5)
            except Exception:
                pass
        ax_l.set_title(f"{prob.title} - Grafik Tunggal", fontsize=10, fontweight="bold")
        ax_l.grid(True, linestyle="--", alpha=0.5)
        ax_l.legend(fontsize=8, loc="best")

        ax_r = axes[idx, 1]
        valid_xs, y1_s, y2_s = [], [], []
        for x in xs:
            if prob.domain_validator(float(x)):
                try:
                    v1 = prob.double_func1(float(x))
                    v2 = prob.double_func2(float(x))
                    if not (math.isnan(v1) or math.isinf(v1) or math.isnan(v2) or math.isinf(v2)):
                        valid_xs.append(x)
                        y1_s.append(v1)
                        y2_s.append(v2)
                except Exception:
                    pass

        ax_r.plot(valid_xs, y1_s, label=prob.double_label1, color="#1f77b4", linewidth=1.8)
        ax_r.plot(valid_xs, y2_s, label=prob.double_label2, color="#ff7f0e", linewidth=1.8, linestyle="--")
        ax_r.axhline(0, color="gray", linestyle=":", linewidth=0.6, alpha=0.6)
        if est_root is not None:
            try:
                y_int = prob.double_func1(est_root)
                ax_r.scatter([est_root], [y_int], color="#d62728", s=60, zorder=5)
            except Exception:
                pass
        ax_r.set_title(f"{prob.title} - Grafik Ganda", fontsize=10, fontweight="bold")
        ax_r.grid(True, linestyle="--", alpha=0.5)
        ax_r.legend(fontsize=8, loc="best")

    plt.suptitle("Visualisasi Komparasi Sistem Persamaan Non-Linear (Tugas P7 - Kelas B)",
                 fontsize=14, fontweight="bold", y=0.995)
    plt.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    return fig

def print_separator(char: str = "=", width: int = 100) -> None:
    print(char * width)

def print_iteration_table(res: SolverResult) -> None:
    print()
    print(f"  [TABEL ITERASI: METODE {res.method_name.upper()}]")
    print(f"  Persamaan     : {res.equation_str}")
    print(f"  Interval Awal : [{res.a0}, {res.b0}]")
    print(f"  Toleransi     : 0.0001 (1e-4) | Maksimal Iterasi: 20")
    print("  " + "-" * 105)
    print(f"  {'Iterasi':^8} | {'a':^12} | {'b':^12} | {'f(a)':^13} | {'f(b)':^13} | {'c':^12} | {'f(c)':^13} | {'Error (|c-c_prev|)':^16}")
    print("  " + "-" * 105)

    if not res.history:
        print(f"  {'Tidak ada data iterasi (validasi gagal atau akar langsung ditemukan di batas awal).':^105}")
        print("  " + "-" * 105)
        return

    for row in res.history:
        err_str = "N/A" if row.error is None else f"{row.error:15.6e}"
        print(f"  {row.iteration:^8d} | {row.a:12.6f} | {row.b:12.6f} | {row.fa:13.6e} | {row.fb:13.6e} | {row.c:12.6f} | {row.fc:13.6e} | {err_str:>16}")

    print("  " + "-" * 105)
    status_label = "KONVERGEN" if res.converged else "BELUM / TIDAK KONVERGEN"
    print(f"  Status        : {status_label}")
    print(f"  Keterangan    : {res.stopping_reason}")
    print()

def print_summary_card(res_bisection: SolverResult, res_regula: SolverResult, prob: ProblemConfig) -> None:
    print_separator("=", 95)
    print(f"  RINGKASAN HASIL PERHITUNGAN: {prob.title.upper()}")
    print_separator("-", 95)
    print(f"  Bentuk Persamaan Asli : {prob.original_eq} (dengan target {prob.target_eq})")
    print(f"  Fungsi Residual       : {prob.residual_eq_str}")
    print(f"  Domain Fungsi         : {prob.domain_description}")
    print()

    print(f"  [1] METODE BISEKSI")
    print(f"      Interval awal   : [{res_bisection.a0}, {res_bisection.b0}]")
    if res_bisection.root is not None:
        print(f"      Akar pendekatan : {res_bisection.root:.8f}")
        print(f"      f(akar)         : {res_bisection.f_root:.8e}")
    else:
        print(f"      Akar pendekatan : Gagal ditemukan")
        print(f"      f(akar)         : N/A")
    print(f"      Jumlah iterasi  : {res_bisection.iterations} iterasi")
    final_err_bi = f"{res_bisection.final_error:.8e}" if res_bisection.final_error is not None else "N/A"
    print(f"      Error terakhir  : {final_err_bi}")
    print(f"      Status          : {'Konvergen' if res_bisection.converged else 'Tidak konvergen'}")
    print(f"      Alasan berhenti : {res_bisection.stopping_reason}")
    print()

    print(f"  [2] METODE REGULA-FALSI")
    print(f"      Interval awal   : [{res_regula.a0}, {res_regula.b0}]")
    if res_regula.root is not None:
        print(f"      Akar pendekatan : {res_regula.root:.8f}")
        print(f"      f(akar)         : {res_regula.f_root:.8e}")
    else:
        print(f"      Akar pendekatan : Gagal ditemukan")
        print(f"      f(akar)         : N/A")
    print(f"      Jumlah iterasi  : {res_regula.iterations} iterasi")
    final_err_rf = f"{res_regula.final_error:.8e}" if res_regula.final_error is not None else "N/A"
    print(f"      Error terakhir  : {final_err_rf}")
    print(f"      Status          : {'Konvergen' if res_regula.converged else 'Tidak konvergen'}")
    print(f"      Alasan berhenti : {res_regula.stopping_reason}")
    print()

    print(f"  [3] ANALISIS PERBANDINGAN METODE")
    if res_bisection.converged and res_regula.converged:
        selisih_akar = abs((res_bisection.root or 0.0) - (res_regula.root or 0.0))
        print(f"      - Kedua metode berhasil konvergen ke akar yang konsisten (selisih = {selisih_akar:.4e}).")
        if res_regula.iterations < res_bisection.iterations:
            print(f"      - Regula-Falsi konvergen LEBIH CEPAT ({res_regula.iterations} iterasi) "
                  f"dibanding Biseksi ({res_bisection.iterations} iterasi) karena memanfaatkan gradien fungsi.")
        elif res_regula.iterations > res_bisection.iterations:
            print(f"      - Biseksi konvergen lebih cepat ({res_bisection.iterations} iterasi) "
                  f"karena Regula-Falsi mengalami kondisi stagnant bracket (satu ujung terperangkap).")
        else:
            print(f"      - Kedua metode memerlukan jumlah iterasi yang sama ({res_bisection.iterations} iterasi).")
    elif res_bisection.converged and not res_regula.converged:
        print("      - Biseksi berhasil konvergen, sedangkan Regula-Falsi belum memenuhi batas toleransi pada 20 iterasi.")
    elif not res_bisection.converged and res_regula.converged:
        print("      - Regula-Falsi berhasil konvergen, sedangkan Biseksi belum memenuhi batas toleransi pada 20 iterasi.")
    else:
        print("      - Kedua metode belum konvergen pada batas 20 iterasi atau interval awal tidak valid.")

    if prob.notes:
        print(f"\n  Catatan Tambahan:")
        print(f"  * {prob.notes}")

    print_separator("=", 95)
    print()

def solve_problem(prob: ProblemConfig,
                  custom_interval: Optional[Tuple[float, float]] = None,
                  show_plots: bool = True) -> Tuple[SolverResult, SolverResult]:
    print_separator("#", 95)
    print(f"  MEMPROSES {prob.title.upper()}")
    print_separator("#", 95)
    print(f"  Persamaan Asli        : {prob.original_eq} (target: {prob.target_eq})")
    print(f"  Bentuk Residual       : {prob.residual_eq_str}")
    print(f"  Domain Fungsi         : {prob.domain_description}")
    print()

    scanned = scan_graphic_roots(prob.func, prob.x_plot_min, prob.x_plot_max, steps=400,
                                 domain_validator=prob.domain_validator)
    print(f"  [LANGKAH 1: ANALISIS GRAFIK]")
    print(f"  Rentang pemindaian plot: [{prob.x_plot_min}, {prob.x_plot_max}]")
    if scanned:
        print(f"  Perubahan tanda terdeteksi pada grafik:")
        for idx, (sub_a, sub_b, c_est) in enumerate(scanned, 1):
            print(f"    - Kandidat {idx}: x in [{sub_a:.4f}, {sub_b:.4f}], Perkiraan Akar Grafik ~ {c_est:.4f}")
    else:
        print("  Peringatan: Tidak terdeteksi perubahan tanda pada rentang plot default.")

    primary_est_root = scanned[0][2] if scanned else None

    single_img_path = f"soal{prob.problem_id}_grafik_tunggal.png"
    double_img_path = f"soal{prob.problem_id}_grafik_ganda.png"

    print(f"\n  [LANGKAH 2: MEMBUAT DAN MENYIMPAN GRAFIK]")
    plot_single_graph(prob, estimated_root=primary_est_root, save_path=single_img_path, show_plot=show_plots)
    print(f"  [+] Grafik Tunggal berhasil disimpan ke : '{single_img_path}'")

    plot_double_graph(prob, estimated_root=primary_est_root, save_path=double_img_path, show_plot=show_plots)
    print(f"  [+] Grafik Ganda berhasil disimpan ke   : '{double_img_path}'")

    if custom_interval:
        a_use, b_use = custom_interval
        print(f"\n  [LANGKAH 3: PENGUJIAN INTERVAL (KUSTOM)]")
        print(f"  Menggunakan interval kustom: [{a_use}, {b_use}]")
    else:
        a_use, b_use = prob.default_intervals[0]
        print(f"\n  [LANGKAH 3: PENGUJIAN INTERVAL (DEFAULT TUGAS)]")
        print(f"  Menggunakan interval rekomendasi: [{a_use}, {b_use}]")

    res_bisection = bisection(
        func=prob.func,
        a=a_use,
        b=b_use,
        tol=1e-4,
        max_iter=20,
        domain_validator=prob.domain_validator,
        problem_id=prob.problem_id,
        problem_title=prob.title,
        equation_str=prob.residual_eq_str
    )
    print_iteration_table(res_bisection)

    res_regula = regula_falsi(
        func=prob.func,
        a=a_use,
        b=b_use,
        tol=1e-4,
        max_iter=20,
        domain_validator=prob.domain_validator,
        problem_id=prob.problem_id,
        problem_title=prob.title,
        equation_str=prob.residual_eq_str
    )
    print_iteration_table(res_regula)

    print_summary_card(res_bisection, res_regula, prob)

    return res_bisection, res_regula


def run_all_problems(show_plots: bool = False) -> None:
    print_separator("=", 105)
    print("  MEMPROSES SELURUH SOAL SPNL (SOAL 1, SOAL 2, DAN SOAL 3)")
    print_separator("=", 105)

    all_scanned = {}
    master_results: List[Tuple[ProblemConfig, SolverResult, SolverResult]] = []

    for pid in [1, 2, 3]:
        prob = PROBLEMS[pid]
        scanned = scan_graphic_roots(prob.func, prob.x_plot_min, prob.x_plot_max, steps=400,
                                     domain_validator=prob.domain_validator)
        all_scanned[pid] = (prob, scanned)

        res_bi, res_rf = solve_problem(prob, custom_interval=None, show_plots=show_plots)
        master_results.append((prob, res_bi, res_rf))

    combined_img = "grafik_semua_soal.png"
    plot_combined_summary(all_scanned, save_path=combined_img)
    print(f"  [+] Lembar Grafik Gabungan Seluruh Soal (3x2) disimpan ke: '{combined_img}'")

    print_separator("=", 110)
    print("  TABEL REKAPITULASI DAN EVALUASI SELURUH SOAL SPNL")
    print_separator("-", 110)
    print(f"  {'Soal':<8} | {'Metode':<13} | {'Interval [a, b]':<16} | {'Akar Pendekatan':<16} | {'f(Akar)':<14} | {'Iterasi':<8} | {'Status':<12}")
    print_separator("-", 110)

    for prob, res_bi, res_rf in master_results:
        r_bi_str = f"{res_bi.root:.8f}" if res_bi.root is not None else "N/A"
        f_bi_str = f"{res_bi.f_root:.2e}" if res_bi.f_root is not None else "N/A"
        st_bi = "Konvergen" if res_bi.converged else "Belum Konvergen"
        print(f"  Soal {prob.problem_id:<3} | {'Biseksi':<13} | [{res_bi.a0:>5.1f}, {res_bi.b0:>5.1f}]     | {r_bi_str:<16} | {f_bi_str:<14} | {res_bi.iterations:<8} | {st_bi:<12}")

        r_rf_str = f"{res_rf.root:.8f}" if res_rf.root is not None else "N/A"
        f_rf_str = f"{res_rf.f_root:.2e}" if res_rf.f_root is not None else "N/A"
        st_rf = "Konvergen" if res_rf.converged else "Belum Konvergen"
        print(f"  Soal {prob.problem_id:<3} | {'Regula-Falsi':<13} | [{res_rf.a0:>5.1f}, {res_rf.b0:>5.1f}]     | {r_rf_str:<16} | {f_rf_str:<14} | {res_rf.iterations:<8} | {st_rf:<12}")
        print("  " + "-" * 110)

    print_separator("=", 110)
    print("  Catatan Evaluasi Umum:")
    print("  1. Seluruh soal diselesaikan dengan batas maksimum 20 iterasi dan batas toleransi 0.0001 (1e-4).")
    print("  2. Pada Soal 1, 2, dan 3, metode Regula-Falsi memerlukan iterasi lebih sedikit daripada Biseksi.")
    print("  3. Semua grafik tunggal dan ganda telah disimpan sebagai file PNG beresolusi tinggi di direktori kerja.")
    print_separator("=", 110)
    print()

def prompt_problem_interval(prob: ProblemConfig) -> Optional[Tuple[float, float]]:
    default_a, default_b = prob.default_intervals[0]
    print(f"\n  Pilihan Interval Awal untuk {prob.title}:")
    print(f"    [1] Gunakan interval rekomendasi tugas: [{default_a}, {default_b}] (Default)")
    print(f"    [2] Masukkan interval kustom sendiri (untuk pengujian batas/error)")
    pilihan = input("  Masukkan pilihan [1/2, default 1]: ").strip()

    if pilihan == "2":
        try:
            inp_a = float(input("    Masukkan nilai batas bawah (a): ").strip())
            inp_b = float(input("    Masukkan nilai batas atas  (b): ").strip())
            return inp_a, inp_b
        except ValueError:
            print("  [!] Input tidak valid! Kembali menggunakan interval rekomendasi default.")
            return None
    return None

def main() -> None:
    while True:
        print_separator("=", 80)
        print("  PROGRAM SISTEM PERSAMAAN NONLINEAR (SPNL) DENGAN PYTHON")
        print("  Metode Biseksi & Regula-Falsi | Visualisasi Grafik Tunggal & Ganda")
        print("  Acuan: Slide Halaman 18 - Kelas B (Praktikum Komputasi Numerik)")
        print_separator("=", 80)
        print("  MENU PILIHAN:")
        print("  1. Soal 1 : y = 3x^3 - 5x^2 + 4x - 7, target y = 1")
        print("  2. Soal 2 : y = e^x - x^2, target y = 0")
        print("  3. Soal 3 : y = log10(x + 2) + 2x - 3, target y = 0")
        print("  4. Jalankan seluruh soal (Soal 1, 2, dan 3)")
        print("  5. Keluar")
        print_separator("-", 80)

        pilihan = input("  Pilih menu [1-5]: ").strip()

        if pilihan == "1":
            prob = PROBLEMS[1]
            custom_int = prompt_problem_interval(prob)
            solve_problem(prob, custom_interval=custom_int, show_plots=True)
            input("  Tekan [Enter] untuk kembali ke menu utama...")

        elif pilihan == "2":
            prob = PROBLEMS[2]
            print(f"\n  * {prob.notes}")
            custom_int = prompt_problem_interval(prob)
            solve_problem(prob, custom_interval=custom_int, show_plots=True)
            input("  Tekan [Enter] untuk kembali ke menu utama...")

        elif pilihan == "3":
            prob = PROBLEMS[3]
            print(f"\n  * {prob.notes}")
            custom_int = prompt_problem_interval(prob)
            solve_problem(prob, custom_interval=custom_int, show_plots=True)
            input("  Tekan [Enter] untuk kembali ke menu utama...")

        elif pilihan == "4":
            print("\n  Memproses seluruh soal secara komprehensif...")
            run_all_problems(show_plots=False)
            input("  Tekan [Enter] untuk kembali ke menu utama...")

        elif pilihan == "5":
            print("\n  Terima kasih telah menggunakan program SPNL. Program selesai.")
            break

        else:
            print("\n  [!] Input tidak dikenal. Silakan pilih angka 1 sampai 5!")
            print()

if __name__ == "__main__":
    main()
