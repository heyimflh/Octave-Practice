function pengenalan_octave2_lengkap_fixed()
% ========================================================================
% PENGENALAN MATLAB/OCTAVE 2 - SOURCE CODE LENGKAP DAN ROBUST
% Berdasarkan contoh syntax pada PDF Pengenalan MATLAB/Octave 2.
%
% PENTING:
% - File ini sengaja dibuat sebagai FUNCTION FILE agar function lokal di
%   bagian bawah dapat dipanggil dengan aman pada GNU Octave.
% - Nama file harus sama dengan nama function utama:
%       pengenalan_octave2_lengkap_fixed.m
% - Jalankan dari Command Window dengan:
%       pengenalan_octave2_lengkap_fixed
% - USE_INPUT = false agar program berjalan langsung tanpa menunggu input.
%   Ubah menjadi true untuk mencoba input() seperti pada PDF.
% ========================================================================

clear;
clc;
close all;

fprintf('============================================================\n');
fprintf('      PENGENALAN MATLAB/OCTAVE 2 - DEMONSTRASI LENGKAP\n');
fprintf('============================================================\n\n');


%% ========================================================================
% 1. LOOPING - FOR LOOP
% ========================================================================

fprintf('\n============================================================\n');
fprintf('1. LOOPING - FOR LOOP\n');
fprintf('============================================================\n');

fprintf('\n-- For loop kondisi 1 --\n');
for i = 1:4
    p = i^2;
    fprintf('i = %d, p = %d\n', i, p);
end

fprintf('\n-- For loop kondisi 2 --\n');
for j = 1:0.5:4
    q = j/2;
    fprintf('j = %.1f, q = %.4f\n', j, q);
end


%% ========================================================================
% 2. LOOPING - WHILE, CONTINUE, BREAK
% ========================================================================

fprintf('\n============================================================\n');
fprintf('2. WHILE LOOP, CONTINUE, DAN BREAK\n');
fprintf('============================================================\n');

fprintf('\n-- While loop --\n');
p = 1;
while p <= 5
    q = p^2 + p;
    fprintf('p = %d, q = %d\n', p, q);
    p = p + 1;
end

fprintf('\n-- Continue --\n');
for i = 1:4
    if i == 3
        continue;
    end
    p = i^2;
    fprintf('i = %d, p = %d\n', i, p);
end

fprintf('\n-- Break --\n');
for i = 1:4
    if i == 3
        break;
    end
    p = i^2;
    fprintf('i = %d, p = %d\n', i, p);
end


%% ========================================================================
% 3. DIFFERENSIAL
% ========================================================================

fprintf('\n============================================================\n');
fprintf('3. DIFFERENSIAL\n');
fprintf('============================================================\n');

% Pada PDF digunakan syms, input, sym, dan diff.
% USE_INPUT=false dipakai agar file dapat dijalankan langsung.
USE_INPUT = true;

symbolic_ok = false;
try
    pkg load symbolic;
    syms x;
    symbolic_ok = true;
catch err
    fprintf('\n[INFO] Package symbolic tidak tersedia.\n');
    fprintf('[INFO] Contoh diff/int dilewati tanpa menghentikan program.\n');
    fprintf('[INFO] Pesan package: %s\n', err.message);
end

if symbolic_ok
    if USE_INPUT
        f = input('Masukkan bentuk persamaan f(x) = ');
    else
        % Persamaan contoh dari PDF, dibuat otomatis agar tidak meminta input.
        f = 'x^2 + 5*x + 7';
        fprintf('Input otomatis: %s\n', f);
    end

    try
        f_asli = sym(f);
        f_turunan = diff(f_asli, x);

        fprintf('\nf_asli =\n');
        disp(f_asli);
        fprintf('f_turunan =\n');
        disp(f_turunan);
    catch err
        fprintf('[INFO] Contoh diferensial tidak dijalankan.\n');
        fprintf('[INFO] Pesan: %s\n', err.message);
    end
end


%% ========================================================================
% 4. INTEGRAL
% ========================================================================

fprintf('\n============================================================\n');
fprintf('4. INTEGRAL\n');
fprintf('============================================================\n');

if symbolic_ok
    if USE_INPUT
        f = input('Masukkan bentuk persamaan f(x) = ');
    else
        % Persamaan contoh dari PDF, dibuat otomatis agar tidak meminta input.
        f = 'sin(3*x) - 2*x^3';
        fprintf('Input otomatis: %s\n', f);
    end

    try
        f_asli = sym(f);
        f_integral = int(f_asli, x);

        fprintf('\nf_asli =\n');
        disp(f_asli);
        fprintf('f_integral =\n');
        disp(f_integral);
    catch err
        fprintf('[INFO] Contoh integral tidak dijalankan.\n');
        fprintf('[INFO] Pesan: %s\n', err.message);
    end
end


%% ========================================================================
% 5. FUNCTION
% ========================================================================

fprintf('\n============================================================\n');
fprintf('5. FUNCTION\n');
fprintf('============================================================\n');

fprintf('\n-- Function dasar --\n');
func('Yujin');

fprintf('\n-- Function utama + function lokal --\n');
funcDenganCall('Yujin');

fprintf('\n-- Function dengan 1 nilai return --\n');
a = doubleit(5);
fprintf('a = %g\n', a);

fprintf('\n-- Function dengan beberapa nilai return --\n');
[x_multi, y_multi] = multi(3, 4);
fprintf('x_multi = %g\n', x_multi);
fprintf('y_multi = %g\n', y_multi);

fprintf('\n-- Function dengan return --\n');
funcDenganReturn('Jungwon');

b = doubleitWithReturn(4);
fprintf('b = %g\n', b);


%% ========================================================================
% 6. ANONYMOUS FUNCTION
% ========================================================================

fprintf('\n============================================================\n');
fprintf('6. ANONYMOUS FUNCTION\n');
fprintf('============================================================\n');

squared = @(x) x.^2;
fprintf('\nsquared = @(x) x.^2\n');
fprintf('squared(3) = %g\n', squared(3));
fprintf('squared(1:3) = ');
disp(squared(1:3));

addition = @(x,y) x+y;
fprintf('addition(5,7) = %g\n', addition(5,7));


%% ========================================================================
% 7. GRAFIK GARIS 2D - CONTOH 1
% ========================================================================

fprintf('\n============================================================\n');
fprintf('7. GRAFIK GARIS 2D - CONTOH 1\n');
fprintf('============================================================\n');

x = 1:25:100;
y = x.^3 + 2*x.^2 - 40*x;

fprintf('x =\n');
disp(x);
fprintf('y =\n');
disp(y);

try
    figure('Name', 'Grafik 2D - Contoh 1');
    plot(x, y);
    grid on;
    xlabel('Sumbu X');
    ylabel('Sumbu Y');
    title('Grafik Garis 2D - y = x^3 + 2x^2 - 40x');
catch err
    fprintf('[INFO] Grafik 2D contoh 1 tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% 8. GRAFIK GARIS 2D - CONTOH 2
% ========================================================================

fprintf('\n============================================================\n');
fprintf('8. GRAFIK GARIS 2D - CONTOH 2\n');
fprintf('============================================================\n');

x = 0:1:100;
y = x.^3 + 2*x.^2 - 40*x;

fprintf('x =\n');
disp(x);
fprintf('y =\n');
disp(y);

try
    figure('Name', 'Grafik 2D - Contoh 2');
    plot(x, y);
    grid on;
    xlabel('Sumbu X');
    ylabel('Sumbu Y');
    title('Grafik Garis 2D - x = 0:1:100');
catch err
    fprintf('[INFO] Grafik 2D contoh 2 tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% 9. GRAFIK GARIS 2D - LINSPACE
% ========================================================================

fprintf('\n============================================================\n');
fprintf('9. GRAFIK 2D - LINSPACE\n');
fprintf('============================================================\n');

x = linspace(0,20);
y = exp(-x/4).*sin(x);

try
    figure('Name', 'Grafik 2D - Linspace');
    plot(x, y);
    xlabel('Sumbu X');
    ylabel('Sumbu Y');
    title('Grafik persamaan f(x)=exp(-x/4).*sin(x)');
    grid on;
catch err
    fprintf('[INFO] Grafik 2D linspace tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% 10. GRAFIK GARIS 2D - DUA KURVA
% ========================================================================

fprintf('\n============================================================\n');
fprintf('10. GRAFIK 2D - DUA KURVA DALAM SATU PLOT\n');
fprintf('============================================================\n');

x = 0:0.01:2*pi;
y = -10*sin(2*x) - 8*cos(3*x);
z = 8*sin(6*x).*-6.*cos(10*x);

try
    figure('Name', 'Grafik 2D - Dua Kurva');
    plot(x, y, x, z);
    grid on;
    xlabel('Sumbu X');
    ylabel('Nilai');
    title('Grafik 2D - Dua Kurva');
catch err
    fprintf('[INFO] Grafik 2D dua kurva tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% 11. GRAFIK GARIS 3D - LINE PLOT
% ========================================================================

fprintf('\n============================================================\n');
fprintf('11. GRAFIK GARIS 3D - LINE PLOT\n');
fprintf('============================================================\n');

t = 0:0.1:6*pi;
x = sqrt(t).*sin(2*t);
y = sqrt(t).*cos(2*t);
z = 0.5*t;

try
    figure('Name', 'Grafik 3D - Line Plot');
    plot3(x, y, z, 'k', 'linewidth', 1);
    grid on;
    xlabel('x');
    ylabel('y');
    zlabel('z');
    title('Grafik Garis 3D: LINE PLOT');
catch err
    fprintf('[INFO] Grafik 3D line plot tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% 12. GRAFIK GARIS 3D - MESH PLOT
% ========================================================================

fprintf('\n============================================================\n');
fprintf('12. GRAFIK 3D - MESH PLOT\n');
fprintf('============================================================\n');

x = -7.3:0.5:7.5;
y = x;
[X, Y] = meshgrid(x, y);
R = sqrt(X.^2 + Y.^2);

% Contoh PDF: Z = sin(R)./R
% R tidak memiliki titik 0 untuk rentang ini, tetapi pengecekan ini
% dipertahankan agar formula tetap aman bila rentang diubah.
R_safe = R;
R_safe(R_safe == 0) = eps;
Z = sin(R_safe)./R_safe;

try
    figure('Name', 'Grafik 3D - Mesh Plot');
    mesh(X, Y, Z);
    grid on;
    xlabel('x');
    ylabel('y');
    zlabel('z');
    title('Grafik Garis 3D: MESH PLOT');
catch err
    fprintf('[INFO] Grafik 3D mesh plot tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% 13. MESHGRID - MEMAHAMI MATRIKS X DAN Y
% ========================================================================

fprintf('\n============================================================\n');
fprintf('13. MESHGRID - MEMAHAMI MATRIKS X DAN Y\n');
fprintf('============================================================\n');

x = [1, 2, 3];
y = [10, 20];
[X, Y] = meshgrid(x, y);

fprintf('\nVector x =\n');
disp(x);
fprintf('Vector y =\n');
disp(y);
fprintf('Matriks X =\n');
disp(X);
fprintf('Matriks Y =\n');
disp(Y);

fprintf('Contoh koordinat berdasarkan posisi yang sama:\n');
fprintf('X(1,1), Y(1,1) -> (%g, %g)\n', X(1,1), Y(1,1));
fprintf('X(1,2), Y(1,2) -> (%g, %g)\n', X(1,2), Y(1,2));
fprintf('X(2,1), Y(2,1) -> (%g, %g)\n', X(2,1), Y(2,1));


%% ========================================================================
% 14. GRAFIK GARIS 3D - CONTOUR PLOT
% ========================================================================

fprintf('\n============================================================\n');
fprintf('14. GRAFIK 3D - CONTOUR PLOT\n');
fprintf('============================================================\n');

x = -3:0.25:3;
y = -3:0.25:3;
[X, Y] = meshgrid(x, y);
Z = 1.8.^(-1.5*sqrt(X.^2 + Y.^2)).*cos(0.5*Y).*sin(X);

try
    figure('Name', 'Grafik 3D - Contour Plot');
    contour3(X, Y, Z, 15);
    grid on;
    xlabel('x');
    ylabel('y');
    zlabel('z');
    title('Grafik Garis 3D: CONTOUR PLOT');
catch err
    fprintf('[INFO] Grafik contour3 tidak dapat ditampilkan.\n');
    fprintf('[INFO] Pesan graphics: %s\n', err.message);
end


%% ========================================================================
% SELESAI
% ========================================================================

fprintf('\n============================================================\n');
fprintf('SEMUA DEMONSTRASI SELESAI DIJALANKAN.\n');
fprintf('============================================================\n');

end


% ========================================================================
% LOCAL FUNCTIONS
% Function lokal diletakkan setelah function utama.
% Karena file ini adalah function file, semua function di bawah dapat
% dipanggil oleh function utama tanpa error "undefined".
% ========================================================================

function func(param)
    fprintf('Nama saya %s!\n', param);
end


function funcDenganCall(param)
    fprintf('Nama saya %s!\n', param);
    callname(param);
end


function callname(param)
    fprintf('Kata "%s" diawali dengan huruf %c.\n', param, param(1));
end


function result = doubleit(param)
    result = 2*param;
end


function [mult2, mult3] = multi(param1, param2)
    mult2 = param1*2;
    mult3 = param2*3;
end


function funcDenganReturn(param)
    fprintf('Nama saya %s!\n', param);
    return;
end


function result = doubleitWithReturn(param)
    result = 0;
    return;
end
