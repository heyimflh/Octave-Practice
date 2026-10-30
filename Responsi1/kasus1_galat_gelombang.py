import math

import matplotlib.pyplot as plt
import numpy as np

LAMBDA = 12
V = 36
X = 10
H0 = 5
BATAS_N = (23, 24, 25)
TOLERANSI = 1.0

t = np.linspace(0, 5, 501)
arg = t * V / LAMBDA


def cos_pendekatan(z, n):
    hasil = np.zeros_like(z, dtype=float)
    for k in range(n + 1):
        hasil += (-1) ** k * z ** (2 * k) / math.factorial(2 * k)
    return hasil


def exp_pendekatan(z, n):
    hasil = 0.0
    for k in range(n + 1):
        hasil += z ** k / math.factorial(k)
    return hasil


def h_eksak():
    return H0 * (np.cos(arg) + np.exp(X))


def h_pendekatan(n):
    return H0 * (cos_pendekatan(arg, n) + exp_pendekatan(X, n))


h_ex = h_eksak()
hasil = {n: h_pendekatan(n) for n in BATAS_N}

print("Parameter: lambda = %d, v = %d, x = %d, h0 = %d" % (LAMBDA, V, X, H0))
print("Rentang t : 0 <= t <= 5 (%d titik)" % len(t))
print("Rerata |h eksak| = %.6f" % np.mean(np.abs(h_ex)))
print()

header = "%-6s %-20s %-20s %-18s %-10s" % (
    "n", "Rerata galat mutlak", "Galat mutlak maks", "Rerata galat rel (%)", "Layak?"
)
print(header)
print("-" * len(header))

ringkasan = []
for n in BATAS_N:
    galat_mutlak = np.abs(h_ex - hasil[n])
    galat_relatif = galat_mutlak / np.abs(h_ex) * 100
    rerata_mutlak = np.mean(galat_mutlak)
    rerata_relatif = np.mean(galat_relatif)
    layak = rerata_relatif < TOLERANSI
    ringkasan.append((n, rerata_mutlak, rerata_relatif, layak))
    print("%-6d %-20.8f %-20.8f %-18.8f %-10s" % (
        n, rerata_mutlak, np.max(galat_mutlak), rerata_relatif,
        "Ya" if layak else "Tidak"
    ))

print()
print("Kesimpulan (toleransi error %.1f%%):" % TOLERANSI)
for n, rm, rr, layak in ringkasan:
    status = "layak" if layak else "tidak layak"
    print("- n = %d : rerata galat relatif %.6f%% -> %s digunakan" % (n, rr, status))

terbaik = min(ringkasan, key=lambda s: s[1])
print()
print("Galat terkecil dihasilkan oleh n = %d." % terbaik[0])
if all(s[3] for s in ringkasan):
    print("Ketiga pendekatan memenuhi toleransi, jadi saran matematikawan layak dipakai.")
elif any(s[3] for s in ringkasan):
    print("Sebagian pendekatan memenuhi toleransi, gunakan n yang lolos saja.")
else:
    print("Tidak ada pendekatan yang memenuhi toleransi, saran matematikawan belum layak.")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))

ax1.plot(t, h_ex, "k-", linewidth=3, label="Eksak")
gaya = {23: ("r--", 2.0), 24: ("g-.", 1.6), 25: ("b:", 1.4)}
for n in BATAS_N:
    ax1.plot(t, hasil[n], gaya[n][0], linewidth=gaya[n][1], label="Pendekatan n = %d" % n)
ax1.set_title("Perbandingan Gelombang Air Laut: Eksak vs Pendekatan Deret")
ax1.set_xlabel("t")
ax1.set_ylabel("h(t)")
ax1.grid(True)
ax1.legend()

for n in BATAS_N:
    galat = np.abs(h_ex - hasil[n])
    galat = np.where(galat == 0, np.finfo(float).tiny, galat)
    ax2.semilogy(t, galat, label="n = %d" % n)
ax2.set_title("Galat Mutlak terhadap Hasil Eksak")
ax2.set_xlabel("t")
ax2.set_ylabel("|h eksak - h pendekatan|")
ax2.grid(True, which="both")
ax2.legend()

plt.tight_layout()
plt.savefig("grafik_kasus1.png", dpi=150)
plt.show()
