import csv
import os
from typing import Any, Callable, Dict, List
from .errors import absolute_error, format_error, format_value, relative_error, relative_error_percent


def print_header(x0: float, y0: float, b: float, n: int, h: float) -> None:
    print("=" * 80)
    print(" PROGRAM PENYELESAIAN PERSAMAAN DIFERENSIAL BIASA (PDB) - METODE NUMERIK")
    print(" Persamaan: dy/dx = (4x^3 - 2x + 1) / (2 + y), dengan kondisi awal y(0) = 1")
    print(f" Target   : Menghitung y({b}) dengan n = {n} langkah, h = {h:.8f}")
    print("-" * 80)
    print(" [CATATAN ASUMSI]:")
    print(" Istilah 'galat abstrak' pada soal tugas diasumsikan sebagai galat absolut")
    print(" (|y_eksak - y_aprok|), sesuai kaidah baku analisis metode numerik.")
    print("=" * 80)
    print()


def print_iteration_table(
    method_name: str,
    iterations: List[Dict[str, Any]],
    y_exact_func: Callable[[float], float],
    precision: int = 8
) -> None:
    print(f"--- TABEL ITERASI DETAIL: METODE {method_name.upper()} ---")

    has_k1 = "k1" in iterations[0]
    has_k2 = "k2" in iterations[0]
    has_k3 = "k3" in iterations[0]
    has_k4 = "k4" in iterations[0]

    headers = ["i", "x_i", "y_i"]
    if has_k1:
        headers.append("k1")
    if has_k2:
        headers.append("k2")
    if has_k3:
        headers.append("k3")
    if has_k4:
        headers.append("k4")
    headers.extend(["y_eksak(x_i)", "Galat Absolut"])

    rows: List[List[str]] = []
    for step in iterations:
        x_i = step["x"]
        y_i = step["y"]
        y_ex = y_exact_func(x_i)
        err = absolute_error(y_ex, y_i)

        row = [
            str(step["i"]),
            format_value(x_i, precision),
            format_value(y_i, precision),
        ]
        if has_k1:
            row.append(format_value(step.get("k1"), precision))
        if has_k2:
            row.append(format_value(step.get("k2"), precision))
        if has_k3:
            row.append(format_value(step.get("k3"), precision))
        if has_k4:
            row.append(format_value(step.get("k4"), precision))
        row.append(format_value(y_ex, precision))
        row.append(format_error(err, precision))
        rows.append(row)

    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            if len(cell) > col_widths[idx]:
                col_widths[idx] = len(cell)

    col_widths = [w + 2 for w in col_widths]

    sep_line = "+" + "+".join("-" * w for w in col_widths) + "+"
    header_line = "|" + "|".join(f" {h}".ljust(w) for h, w in zip(headers, col_widths)) + "|"

    print(sep_line)
    print(header_line)
    print(sep_line)
    for row in rows:
        line = "|" + "|".join(f" {c}".ljust(w) for c, w in zip(row, col_widths)) + "|"
        print(line)
    print(sep_line)
    print()


def print_summary_table(
    summary_data: List[Dict[str, Any]],
    target_x: float,
    precision: int = 8
) -> None:
    print(f"============================ TABEL RINGKASAN HASIL y({target_x}) ============================")
    headers = ["Metode", f"y({target_x}) Aproksimasi", "Galat Absolut", "Galat Relatif", "Galat Relatif (%)"]

    rows: List[List[str]] = []
    for item in summary_data:
        y_val_str = format_value(item["y_approx"], precision)
        err_abs_str = "-" if item["err_abs"] is None else format_error(item["err_abs"], precision)
        err_rel_str = "-" if item["err_rel"] is None else format_error(item["err_rel"], precision)
        if item["err_rel_pct"] is None:
            err_pct_str = "-"
        else:
            pct_val = item["err_rel_pct"]
            if abs(pct_val) < 1e-3:
                err_pct_str = f"{pct_val:.5f} %"
            else:
                err_pct_str = f"{pct_val:.4f} %"

        rows.append([item["method"], y_val_str, err_abs_str, err_rel_str, err_pct_str])

    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            if len(cell) > col_widths[idx]:
                col_widths[idx] = len(cell)
    col_widths = [w + 2 for w in col_widths]

    sep_line = "+" + "+".join("-" * w for w in col_widths) + "+"
    header_line = "|" + "|".join(f" {h}".ljust(w) for h, w in zip(headers, col_widths)) + "|"

    print(sep_line)
    print(header_line)
    print(sep_line)
    for row in rows:
        line = "|" + "|".join(f" {c}".ljust(w) for c, w in zip(row, col_widths)) + "|"
        print(line)
    print(sep_line)
    print()


def print_analysis(summary_data: List[Dict[str, Any]]) -> None:
    approx_methods = [item for item in summary_data if item["err_abs"] is not None]
    sorted_methods = sorted(approx_methods, key=lambda x: x["err_abs"])

    print("---------------------------- ANALISIS AKURASI METODE ----------------------------")
    print("Urutan metode dari yang paling akurat (galat absolut terkecil ke terbesar):")
    for rank, item in enumerate(sorted_methods, start=1):
        order_info = {
            "Euler": "Orde-1, O(h)",
            "Heun": "Orde-2, O(h^2)",
            "Runge-Kutta 4": "Orde-4, O(h^4)",
        }.get(item["method"], "Metode Numerik")
        print(f" {rank}. {item['method']:<14} | Galat Absolut = {format_error(item['err_abs']):<12} ({order_info})")

    print()
    print("Penjelasan Teoretis:")
    print("Metode Runge-Kutta Orde-4 (RK4) memiliki akurasi tertinggi karena memiliki galat pemotongan")
    print("global berorde O(h^4), disusul oleh Metode Heun dengan orde O(h^2), dan Metode Euler dengan")
    print("orde O(h) yang menghasilkan galat terbesar. Hasil perhitungan konsisten sepenuhnya")
    print("dengan teori konvergensi metode numerik: Galat RK4 << Galat Heun < Galat Euler.")
    print("=" * 80)
    print()


def export_summary_csv(filepath: str, summary_data: List[Dict[str, Any]], target_x: float) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metode", f"y({target_x})_Aproksimasi", "Galat_Absolut", "Galat_Relatif", "Galat_Relatif_Persen"])
        for item in summary_data:
            y_val = item["y_approx"]
            err_abs = "" if item["err_abs"] is None else f"{item['err_abs']:.12e}"
            err_rel = "" if item["err_rel"] is None else f"{item['err_rel']:.12e}"
            err_pct = "" if item["err_rel_pct"] is None else f"{item['err_rel_pct']:.8f}"
            writer.writerow([item["method"], f"{y_val:.12f}", err_abs, err_rel, err_pct])


def export_iteration_csv(
    filepath: str,
    iterations: List[Dict[str, Any]],
    y_exact_func: Callable[[float], float]
) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    has_k1 = "k1" in iterations[0]
    has_k2 = "k2" in iterations[0]
    has_k3 = "k3" in iterations[0]
    has_k4 = "k4" in iterations[0]

    fieldnames = ["i", "x_i", "y_i"]
    if has_k1:
        fieldnames.append("k1")
    if has_k2:
        fieldnames.append("k2")
    if has_k3:
        fieldnames.append("k3")
    if has_k4:
        fieldnames.append("k4")
    fieldnames.extend(["y_eksak", "galat_absolut"])

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for step in iterations:
            x_i = step["x"]
            y_i = step["y"]
            y_ex = y_exact_func(x_i)
            err = absolute_error(y_ex, y_i)

            row = [step["i"], f"{x_i:.12f}", f"{y_i:.12f}"]
            if has_k1:
                row.append("" if step.get("k1") is None else f"{step['k1']:.12f}")
            if has_k2:
                row.append("" if step.get("k2") is None else f"{step['k2']:.12f}")
            if has_k3:
                row.append("" if step.get("k3") is None else f"{step['k3']:.12f}")
            if has_k4:
                row.append("" if step.get("k4") is None else f"{step['k4']:.12f}")
            row.append(f"{y_ex:.12f}")
            row.append(f"{err:.12e}")
            writer.writerow(row)
