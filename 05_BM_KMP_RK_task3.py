import timeit
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_text(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

text1 = read_text("article1.txt")
text2 = read_text("article2.txt")

# ---------- Boyer–Moore ----------
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return -1

    # таблиця "поганого символу"
    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i

    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return s
        else:
            shift = j - bad_char.get(text[s + j], -1)
            s += max(1, shift)

    return -1

# ---------- KMP ----------
def kmp_prefix_table(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return -1

    lps = kmp_prefix_table(pattern)

    i = 0
    j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1

# ---------- Rabin–Karp ----------
def rabin_karp(text, pattern, d=256, q=101):
    m = len(pattern)
    n = len(text)

    if m == 0 or n < m:
        return -1

    h = pow(d, m - 1) % q
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t:
            if text[s:s + m] == pattern:
                return s

        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0:
                t += q

    return -1

# ---------- ТЕСТОВІ ПІДРЯДКИ ----------
existing_pattern = "алгоритм пошуку підрядка"     
fake_pattern = "qwertyqwerty123"  

# ---------- ФУНКЦІЯ ВИМІРЮВАННЯ ЧАСУ ----------
def measure_time(func, text, pattern, repeat=5):
    timer = timeit.Timer(lambda: func(text, pattern))
    return min(timer.repeat(repeat=repeat, number=10))

# ---------- ЗАПУСК ТЕСТІВ ----------
def run_tests(text, text_name):
    print(f"\n===== Результати для {text_name} =====")

    for pattern_name, pattern in [("Існуючий", existing_pattern),
                                  ("Вигаданий", fake_pattern)]:

        print(f"\nПідрядок: {pattern_name}")

        t_bm = measure_time(boyer_moore, text, pattern)
        t_kmp = measure_time(kmp_search, text, pattern)
        t_rk = measure_time(rabin_karp, text, pattern)

        print(f"Boyer–Moore: {t_bm:.6f} s")
        print(f"KMP:         {t_kmp:.6f} s")
        print(f"Rabin–Karp:  {t_rk:.6f} s")

# ---------- ГОЛОВНИЙ ЗАПУСК ----------
run_tests(text1, "Стаття 1")
run_tests(text2, "Стаття 2")
