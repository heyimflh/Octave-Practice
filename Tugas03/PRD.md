# PRD — Analisis Galat pada Komputasi Numerik dengan Python

**Versi:** 1.0  
**Platform:** Python 3  
**Jenis program:** Console/CLI (`.py`)  
**Basis materi:** Modul praktikum **Galat/Error** Universitas Sebelas Maret, khususnya Tugas pada halaman 13–14. fileciteturn1file0L1317-L1329 fileciteturn1file0L1331-L1338

---

## 1. Ringkasan Produk

Program ini adalah program Python berbasis terminal yang digunakan untuk menyelesaikan seluruh tugas praktikum pada materi **Galat/Error dalam Komputasi Numerik**.

Program wajib mengerjakan tiga studi kasus:

1. Menghitung nilai pendekatan `e^(0.3)` dengan deret Taylor untuk `n = {0, 1, 2, 3, 4}`, kemudian menghitung dan membandingkan galatnya.
2. Menghitung nilai `1/1 + 1/2 + 1/3 + ... + 1/20` dengan tiga metode: perhitungan eksak, setiap pembagian dibulatkan, dan `sum()` tanpa loop eksplisit, kemudian membandingkan galatnya.
3. Menghitung nilai `sin(x)` dengan deret Taylor menggunakan `x = 1` dan `N = {1, 2, 3, 4, 5}`, kemudian menghitung dan membandingkan galatnya.

Tujuan program adalah memberikan hasil numerik, nilai galat, serta analisis perubahan galat ketika jumlah suku/iterasi bertambah. Hal ini sesuai materi bahwa komputasi numerik menghasilkan nilai hampiran dan setiap hasil dapat memiliki error; semakin kecil error, semakin teliti solusi numeriknya. fileciteturn1file0L457-L457 fileciteturn1file0L725-L725

---

## 2. Latar Belakang dan Dasar Materi

Materi praktikum membedakan komputasi analitik dan numerik. Komputasi numerik menggunakan algoritma pendekatan/akproksimasi, menghasilkan nilai perkiraan yang mendekati nilai eksak, dan umumnya melakukan perhitungan berulang sehingga setiap hasil memiliki galat. fileciteturn1file0L457-L457

Materi juga menjelaskan dua sumber utama galat, yaitu:

- **Galat pembulatan (round-off error)**: galat akibat pembulatan angka. fileciteturn1file0L856-L862
- **Galat pemotongan (truncation error)**: galat karena jumlah komputasi/iterasi dibatasi sehingga deret atau proses numerik tidak dihitung sampai tak terhingga. fileciteturn1file0L1093-L1104

Rumus yang dipakai program mengikuti konsep pada modul:

- Galat absolut:
  `error = |nilai_sebenarnya - nilai_hampiran|`
- Galat relatif:
  `error_relatif = |nilai_sebenarnya - nilai_hampiran| / |nilai_sebenarnya|`
- Persentase galat relatif:
  `error_persen = error_relatif × 100%`

Rumus tersebut ditampilkan pada bagian **Rumus Galat** di modul. fileciteturn1file0L726-L726

---

## 3. Tujuan Program

Program harus dapat:

1. Mengimplementasikan deret Taylor dalam Python.
2. Menghasilkan nilai hampiran untuk `e^(0.3)` dan `sin(1)`.
3. Menghitung galat absolut untuk setiap pendekatan.
4. Menghitung galat relatif dan persentase galat sebagai informasi tambahan.
5. Membandingkan perubahan error terhadap jumlah suku `n/N`.
6. Mendemonstrasikan pengaruh pembulatan pada perhitungan `1 + 1/2 + ... + 1/20`.
7. Membandingkan perhitungan biasa/eksak, pembulatan tiap pembagian, dan `sum()`.
8. Menampilkan analisis otomatis yang mudah dipahami mahasiswa.

---

# 4. Ruang Lingkup Fungsional

## 4.1. Tugas 1 — Error `e^(0.3)` dengan Deret Taylor

Tugas pada halaman 13 meminta nilai galat pada perhitungan `e^(0.3)` menggunakan deret Taylor untuk `n = {0,1,2,3,4}`, lalu membandingkan dan menganalisis hasil. Rumus yang diberikan adalah: `e^x = Σ(i=0..n) x^i / i!`. fileciteturn1file0L1317-L1321

### Rumus implementasi

```text
T_n(x) = Σ(i=0..n) x^i / i!
```

Dengan:

```text
x = 0.3
n = 0, 1, 2, 3, 4
```

Nilai acuan/eksak program:

```python
math.exp(0.3)
```

### Output wajib

Untuk setiap `n`, program menampilkan:

- `n`
- Nilai Taylor/hampiran
- Nilai eksak `e^0.3`
- Galat absolut
- Galat relatif
- Persentase galat

### Analisis wajib

Program harus menyimpulkan secara numerik bahwa ketika jumlah suku Taylor bertambah dari `n=0` sampai `n=4`, nilai hampiran semakin dekat ke `e^0.3` dan galat pemotongan semakin kecil.

---

## 4.2. Tugas 2 — Error pada `1 + 1/2 + ... + 1/20`

Tugas pada halaman 13 meminta perhitungan deret:

```text
1/1 + 1/2 + 1/3 + ... + 1/20
```

dan membandingkan tiga metode:

- **a. Perhitungan secara eksak**
- **b. Masing-masing pembagian dibulatkan**
- **c. Tanpa looping menggunakan fungsi `sum()`**

Hal tersebut tercantum langsung pada instruksi tugas. fileciteturn1file0L1325-L1329

### 4.2.1. Metode A — Perhitungan Eksak

Untuk menjaga arti "eksak" secara matematis, program menggunakan `fractions.Fraction` sebagai referensi internal.

Rumus:

```text
H = Σ(i=1..20) 1/i
```

Hasil disimpan sebagai pecahan rasional dan juga ditampilkan dalam bentuk desimal.

### 4.2.2. Metode B — Setiap Pembagian Dibulatkan

Setiap nilai:

```text
1/i
```

dibulatkan terlebih dahulu baru dijumlahkan.

**Catatan sumber:** halaman tugas tidak menentukan berapa jumlah angka di belakang koma. Agar perilaku program tidak ambigu, PRD menetapkan nilai awal **2 angka di belakang koma**, sesuai contoh pembulatan dua desimal yang digunakan pada materi. Nilai tersebut dijadikan konstanta yang mudah diubah.

Contoh konsep:

```text
1/3  -> 0.33
1/4  -> 0.25
1/6  -> 0.17
...
```

Kemudian seluruh nilai hasil pembulatan dijumlahkan.

### 4.2.3. Metode C — `sum()` Tanpa Loop Eksplisit

Program wajib menggunakan fungsi bawaan:

```python
sum(1 / i for i in range(1, 21))
```

Tidak boleh menggunakan `for`/`while` sebagai loop eksplisit untuk perhitungan metode C.

### Output wajib

Program menampilkan:

| Metode | Hasil | Galat Absolut | Galat Relatif | Galat (%) |
|---|---:|---:|---:|---:|
| Eksak | ... | ... | ... | ... |
| Pembagian dibulatkan | ... | ... | ... | ... |
| `sum()` tanpa loop eksplisit | ... | ... | ... | ... |

Nilai pembanding/reference adalah hasil metode A yang direpresentasikan secara desimal dengan presisi tinggi.

### Analisis wajib

Program harus menjelaskan:

- Metode pembulatan tiap pembagian menghasilkan nilai yang berbeda karena setiap suku sudah kehilangan sebagian presisi sebelum dijumlahkan.
- Metode `sum()` menggunakan nilai pecahan floating-point tanpa pembulatan manual pada setiap suku, sehingga hasilnya sangat dekat dengan nilai reference.
- Perbedaan kecil yang masih muncul pada operasi floating-point merupakan bagian dari keterbatasan representasi numerik komputer.

---

# 4.3. Tugas 3 — Error `sin(x)` dengan Deret Taylor

Tugas pada halaman 14 meminta nilai galat untuk perhitungan `sin(x)` menggunakan deret Taylor, dengan `N = {1,2,3,4,5}` dan `x = 1`, lalu membandingkan dan menganalisis hasil. fileciteturn1file0L1331-L1338

Rumus pada modul:

```text
sin(x) = Σ(n=0..N) (-1)^n x^(2n+1) / (2n+1)!
```

### Implementasi

Dengan:

```text
x = 1
N = 1, 2, 3, 4, 5
```

Nilai acuan/eksak program:

```python
math.sin(1)
```

### Output wajib

Untuk setiap `N`, tampilkan:

- `N`
- Nilai Taylor/hampiran
- Nilai eksak `sin(1)`
- Galat absolut
- Galat relatif
- Persentase galat

### Analisis wajib

Program harus menunjukkan bahwa penambahan suku pada deret Taylor menghasilkan pendekatan yang semakin dekat dengan nilai `sin(1)` dan nilai error semakin kecil.

---

# 5. Desain Program

## 5.1. Bentuk Aplikasi

Program berupa **console application** satu file:

```text
main.py
```

Program tidak membutuhkan GUI, database, API, atau koneksi internet.

## 5.2. Library

Gunakan standard library Python saja:

```python
import math
from decimal import Decimal, getcontext
from fractions import Fraction
```

Tidak diperlukan instalasi package eksternal.

---

# 6. Arsitektur Fungsi

Program harus dipisah menjadi fungsi-fungsi kecil agar mudah dibaca dan diuji.

### 6.1. Fungsi galat

```python
def absolute_error(exact, approximation):
    ...
```

Tanggung jawab: menghitung:

```text
|exact - approximation|
```

### 6.2. Fungsi galat relatif

```python
def relative_error(exact, approximation):
    ...
```

Tanggung jawab: menghitung:

```text
|exact - approximation| / |exact|
```

### 6.3. Fungsi persentase galat

```python
def percentage_error(exact, approximation):
    ...
```

Tanggung jawab: mengubah galat relatif menjadi persen.

### 6.4. Faktorial

```python
def factorial(n):
    ...
```

Fungsi menghitung `n!`. Implementasi boleh memanfaatkan `math.factorial()` untuk menjaga kejelasan dan menghindari implementasi yang tidak diperlukan oleh tugas.

### 6.5. Deret Taylor `e^x`

```python
def taylor_exp(x, n):
    ...
```

Rumus:

```text
Σ(i=0..n) x^i/i!
```

### 6.6. Deret Taylor `sin(x)`

```python
def taylor_sin(x, n):
    ...
```

Rumus:

```text
Σ(i=0..n) (-1)^i x^(2i+1)/(2i+1)!
```

### 6.7. Tugas 1

```python
def run_task_1():
    ...
```

Tanggung jawab: menghitung `e^0.3` untuk `n=0..4`, menghitung error, lalu menampilkan tabel dan analisis.

### 6.8. Tugas 2

```python
def run_task_2(round_digits=2):
    ...
```

Tanggung jawab: menjalankan tiga metode perhitungan `1 + 1/2 + ... + 1/20` dan membandingkan error.

### 6.9. Tugas 3

```python
def run_task_3():
    ...
```

Tanggung jawab: menghitung `sin(1)` untuk `N=1..5`, menghitung error, lalu menampilkan tabel dan analisis.

### 6.10. Program utama

```python
def main():
    ...
```

Urutan eksekusi wajib:

```text
1. Header program
2. Tugas 1
3. Tugas 2
4. Tugas 3
5. Ringkasan akhir
```

Program kemudian berhenti secara normal.

---

# 7. Spesifikasi Perhitungan Error

Untuk seluruh tugas, gunakan nilai mutlak agar error tidak bernilai negatif:

```python
error = abs(exact - approximation)
```

Untuk reference nol, program harus menghindari pembagian dengan nol pada error relatif. Pada tiga studi kasus tugas ini reference tidak bernilai nol, tetapi fungsi error relatif tetap harus memiliki pengamanan umum.

Format tampilan yang direkomendasikan:

```text
Nilai Eksak       : 1.3498588076
Nilai Hampiran    : 1.3498375000
Galat Absolut     : 0.0000213076
Galat Relatif     : 0.000015785...
Persentase Galat  : 0.0015785... %
```

Program harus menggunakan angka presisi yang cukup agar error kecil tidak menjadi `0.000000` hanya karena pembulatan tampilan.

---

# 8. Alur Penggunaan

Saat `main.py` dijalankan:

```text
$ python main.py
```

Program langsung menampilkan hasil seluruh tugas.

### Contoh alur layar

```text
============================================================
PRAKTIKUM KOMPUTASI NUMERIK — GALAT / ERROR
============================================================

[TUGAS 1] ERROR e^(0.3) — DERET TAYLOR
...

[TUGAS 2] ERROR 1 + 1/2 + ... + 1/20
...

[TUGAS 3] ERROR sin(1) — DERET TAYLOR
...

============================================================
RINGKASAN ANALISIS
============================================================
...
```

Tidak diperlukan input wajib dari pengguna karena seluruh parameter tugas telah ditentukan pada modul.

---

# 9. Parameter Tetap Program

Parameter wajib tidak boleh berubah dari instruksi praktikum:

```python
EXP_X = 0.3
EXP_N_VALUES = [0, 1, 2, 3, 4]

HARMONIC_START = 1
HARMONIC_END = 20
DEFAULT_ROUND_DIGITS = 2

SIN_X = 1
SIN_N_VALUES = [1, 2, 3, 4, 5]
```

`DEFAULT_ROUND_DIGITS = 2` adalah keputusan implementasi karena halaman tugas tidak menyebutkan jumlah desimal pembulatan. Nilai ini disamakan dengan contoh pembulatan dua desimal pada materi.

---

# 10. Hasil Acuan yang Diharapkan

Angka berikut digunakan sebagai sanity check agar implementasi dapat diverifikasi.

## 10.1. Tugas 1

Untuk `x=0.3`, hasil Taylor secara bertahap adalah:

| n | Hampiran | Galat absolut (≈) |
|---:|---:|---:|
| 0 | 1.0000000000 | 0.3498588076 |
| 1 | 1.3000000000 | 0.0498588076 |
| 2 | 1.3450000000 | 0.0048588076 |
| 3 | 1.3495000000 | 0.0003588076 |
| 4 | 1.3498375000 | 0.0000213076 |

Reference:

```text
exp(0.3) ≈ 1.3498588075760032
```

## 10.2. Tugas 2

Reference matematis:

```text
1 + 1/2 + ... + 1/20
= 55835135/15519504
≈ 3.5977396571436819
```

Dengan pembulatan setiap pembagian ke 2 desimal:

```text
≈ 3.59
```

Dengan:

```python
sum(1 / i for i in range(1, 21))
```

hasil floating-point normal berada sangat dekat dengan:

```text
3.597739657143682
```

## 10.3. Tugas 3

Untuk `x=1`, reference:

```text
sin(1) ≈ 0.8414709848078965
```

Dengan `N=1..5`, hasil Taylor yang diharapkan kira-kira:

| N | Hampiran | Galat absolut (≈) |
|---:|---:|---:|
| 1 | 0.8333333333 | 0.0081376515 |
| 2 | 0.8416666667 | 0.0001956819 |
| 3 | 0.8414682540 | 0.0000027308 |
| 4 | 0.8414710097 | 0.0000000249 |
| 5 | 0.8414709846 | 0.0000000002 |

Nilai ini bukan output yang boleh di-hardcode sebagai jawaban; program harus menghitungnya dari rumus Taylor.

---

# 11. Aturan Analisis Otomatis

Program tidak hanya mencetak angka. Program harus membuat analisis berbasis hasil yang dihitung.

## 11.1. Analisis Tugas 1

Jika error pada `n` terakhir lebih kecil daripada error pada `n` pertama, tampilkan pesan yang menyatakan bahwa penambahan suku Taylor memperkecil error pada pengujian.

## 11.2. Analisis Tugas 2

Program harus membandingkan tiga hasil:

- exact/reference
- pembulatan tiap pembagian
- `sum()` tanpa loop eksplisit

Program harus menyebut metode pembulatan sebagai metode yang kehilangan presisi paling besar pada pengujian default 2 desimal, tanpa memberikan label nilai subjektif seperti "terbaik" atau "terburuk".

## 11.3. Analisis Tugas 3

Program harus menunjukkan perubahan error dari `N=1` hingga `N=5`, serta menyatakan bahwa pada hasil pengujian ini error mengecil ketika jumlah suku bertambah.

---

# 12. Struktur Output Data

Setiap baris hasil perhitungan internal sebaiknya direpresentasikan sebagai dictionary agar mudah dicetak:

```python
{
    "iteration": n,
    "approximation": approximation,
    "exact": exact,
    "absolute_error": absolute_error,
    "relative_error": relative_error,
    "percentage_error": percentage_error,
}
```

Untuk tugas 2 gunakan key `method` sebagai pengganti `iteration`.

---

# 13. Validasi dan Error Handling

Program harus:

1. Menolak nilai `round_digits < 0` jika parameter tersebut dibuat dapat diubah.
2. Menangani kasus `exact == 0` pada fungsi error relatif dengan aman.
3. Menggunakan `abs()` untuk error absolut.
4. Tidak menghasilkan `ZeroDivisionError` untuk parameter valid yang digunakan oleh tugas.
5. Memastikan `n` dan `N` adalah bilangan bulat non-negatif ketika fungsi deret dipanggil.
6. Tidak menggunakan library eksternal.

---

# 14. Non-Functional Requirements

### Readability

Kode harus mudah dipahami mahasiswa Informatika tingkat awal–menengah:

- penamaan variabel jelas;
- fungsi mempunyai satu tanggung jawab;
- komentar hanya digunakan pada bagian yang memang membantu pemahaman;
- tidak menggunakan abstraksi yang tidak diperlukan.

### Reproducibility

Untuk input/parameter yang sama, program harus menghasilkan output numerik yang konsisten.

### Accuracy

Perhitungan error harus menggunakan presisi internal yang cukup tinggi. Pembulatan hanya dilakukan pada metode tugas 2b, bukan pada seluruh hasil program.

### Compatibility

Target minimal:

```text
Python 3.10+
```

---

# 15. Struktur File Project

Versi minimal:

```text
praktikum-galat-error/
└── main.py
```

Opsional untuk pengumpulan yang lebih rapi:

```text
praktikum-galat-error/
├── main.py
├── PRD.md
└── README.md
```

---

# 16. Acceptance Criteria

Program dianggap memenuhi PRD apabila seluruh kondisi berikut terpenuhi:

- [ ] Program dapat dijalankan dengan `python main.py`.
- [ ] Tugas 1 menghitung `e^(0.3)` dengan deret Taylor untuk `n=0,1,2,3,4`.
- [ ] Tugas 1 menampilkan hampiran dan error untuk tiap `n`.
- [ ] Tugas 1 menampilkan analisis perubahan error.
- [ ] Tugas 2 menghitung `1 + 1/2 + ... + 1/20`.
- [ ] Tugas 2 mempunyai metode exact/reference.
- [ ] Tugas 2 membulatkan setiap pembagian pada metode pembulatan.
- [ ] Tugas 2 menggunakan `sum()` dan tidak menggunakan loop eksplisit untuk metode tersebut.
- [ ] Tugas 2 membandingkan hasil ketiga metode.
- [ ] Tugas 2 menampilkan error masing-masing metode terhadap reference.
- [ ] Tugas 3 menghitung `sin(1)` dengan deret Taylor untuk `N=1,2,3,4,5`.
- [ ] Tugas 3 menampilkan hampiran dan error untuk tiap `N`.
- [ ] Tugas 3 menampilkan analisis perubahan error.
- [ ] Rumus yang dipakai sesuai rumus pada modul.
- [ ] Program menggunakan `abs()` untuk galat absolut.
- [ ] Tidak ada dependensi package eksternal.
- [ ] Tidak ada nilai hasil yang di-hardcode sebagai pengganti perhitungan.

---

# 17. Test Case Minimum

## Test Case 1 — Deret `e^x`

```text
Input internal: x=0.3, n=4
Expected approximation: 1.3498375
Expected absolute error: sekitar 0.0000213076
```

## Test Case 2 — Harmonic Sum

```text
Input internal: i=1..20
Expected exact decimal: sekitar 3.5977396571436819
Expected rounded-each-term result with 2 decimals: 3.59
```

## Test Case 3 — Deret `sin(x)`

```text
Input internal: x=1, N=5
Expected approximation: sekitar 0.8414709846480680
Expected absolute error: sekitar 1.5983e-10
```

---

# 18. Traceability terhadap Tugas pada PDF

| Instruksi PDF | Implementasi PRD |
|---|---|
| `e^(0.3)` dengan `n={0,1,2,3,4}` | `run_task_1()` + `taylor_exp()` |
| Bandingkan dan analisis hasil Tugas 1 | tabel hasil + `analyze_exp_results()` |
| `1/1 + ... + 1/20` | `run_task_2()` |
| Perhitungan secara eksak | `Fraction` sebagai reference |
| Masing-masing pembagian dibulatkan | `round_digits=2` pada setiap `1/i` |
| Tanpa looping menggunakan `sum()` | `sum(1 / i for i in range(1, 21))` |
| Bandingkan hasil Tugas 2 | tabel metode + error |
| `sin(x)` dengan deret Taylor | `taylor_sin()` |
| `N={1,2,3,4,5}`, `x=1` | `run_task_3()` |
| Bandingkan dan analisis hasil Tugas 3 | tabel hasil + `analyze_sin_results()` |

---

# 19. Batasan dan Keputusan Implementasi

### 19.1. Jumlah desimal pembulatan Tugas 2b

Instruksi halaman 13 hanya menyebut **"masing-masing pembagian dibulatkan"** dan tidak menetapkan jumlah angka di belakang koma. fileciteturn1file0L1325-L1329

Karena itu:

```text
DEFAULT_ROUND_DIGITS = 2
```

ditetapkan sebagai default implementasi, mengikuti contoh pembulatan dua desimal yang terdapat pada materi. Nilai ini harus dibuat mudah diubah sehingga program dapat mengikuti instruksi dosen apabila angka pembulatan yang diwajibkan ditetapkan kemudian.

### 19.2. Arti "tanpa looping"

Pada metode Tugas 2c, program tidak boleh memakai loop `for` atau `while` secara eksplisit dalam pernyataan perhitungannya. Penggunaan:

```python
sum(1 / i for i in range(1, 21))
```

dinyatakan memenuhi instruksi **menggunakan fungsi `sum()` tanpa looping eksplisit**.

### 19.3. Nilai eksak

Untuk menghindari ketergantungan pada pembulatan floating-point dalam reference Tugas 2, nilai reference disimpan dengan `Fraction`. Untuk `e^0.3` dan `sin(1)`, nilai fungsi `math.exp()` dan `math.sin()` digunakan sebagai nilai acuan numerik berpresisi floating-point Python.

---

# 20. Definition of Done

Project selesai apabila `main.py`:

1. menjalankan ketiga tugas pada halaman 13–14;
2. menggunakan rumus Taylor yang sesuai modul;
3. menghitung galat absolut, relatif, dan persen;
4. menampilkan hasil dalam tabel yang jelas;
5. membandingkan hasil antar nilai `n/N` dan antar metode Tugas 2;
6. menghasilkan analisis otomatis berdasarkan angka yang dihitung;
7. lulus seluruh acceptance criteria dan test case minimum;
8. tidak mengganti perhitungan dengan nilai hardcode.

---

# 21. Kesimpulan PRD

PRD ini mendefinisikan satu program Python console yang secara langsung memetakan seluruh **Tugas 1, Tugas 2, dan Tugas 3** pada halaman 13–14 modul Galat/Error. Fokus program adalah **komputasi numerik, deret Taylor, galat absolut, galat relatif, galat pembulatan, dan galat pemotongan**, bukan fitur aplikasi tambahan yang tidak diperlukan.

Seluruh parameter inti diambil dari tugas pada PDF. Satu-satunya detail yang tidak ditentukan secara eksplisit oleh halaman tugas adalah jumlah desimal pada proses pembulatan Tugas 2b; karena itu PRD menjadikannya parameter dengan default 2 desimal sehingga perilaku program tetap terdokumentasi dan mudah disesuaikan. fileciteturn1file0L1317-L1321 fileciteturn1file0L1325-L1329 fileciteturn1file0L1331-L1338
