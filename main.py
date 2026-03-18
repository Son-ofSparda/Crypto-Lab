import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import random
from typing import Tuple, List, Dict
import sympy


class CryptoLab:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoLab - Математическая криптография")
        self.root.geometry("1400x800")

        # Инициализация переменных ДО создания интерфейса
        self.current_cipher = "caesar"  # Значение по умолчанию
        self.dh_state = {"p": 23, "g": 5, "a": None, "b": None}

        # Настройка стилей для минималистичного дизайна
        self.setup_styles()

        # Основной контейнер
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Заголовок
        self.create_header()

        # Основная рабочая область
        self.create_workspace()

        # Панель логов
        self.create_log_panel()

    def setup_styles(self):
        """Настройка минималистичных, но элегантных стилей"""
        style = ttk.Style()
        style.theme_use('clam')

        # Цветовая схема
        self.bg_color = "#f5f5f7"
        self.accent_color = "#0071e3"
        self.text_color = "#1d1d1f"
        self.secondary_color = "#86868b"

        # Настройка стилей
        style.configure("Title.TLabel",
                        font=("Helvetica", 24, "bold"),
                        foreground=self.text_color,
                        background=self.bg_color)

        style.configure("Subtitle.TLabel",
                        font=("Helvetica", 12),
                        foreground=self.secondary_color,
                        background=self.bg_color)

        style.configure("Accent.TButton",
                        font=("Helvetica", 10),
                        background=self.accent_color,
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none")

        style.map("Accent.TButton",
                  background=[('active', '#0051b3')])

        style.configure("Log.TLabel",
                        font=("Menlo", 10),
                        background="white",
                        foreground=self.text_color)

        self.root.configure(bg=self.bg_color)

    def create_header(self):
        """Создание заголовка приложения"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(header_frame,
                                text="CryptoLab",
                                style="Title.TLabel")
        title_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(header_frame,
                                   text="Визуализатор математических шифров",
                                   style="Subtitle.TLabel")
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))

    def create_workspace(self):
        """Создание основной рабочей области"""
        workspace = ttk.Frame(self.main_container)
        workspace.pack(fill=tk.BOTH, expand=True)

        # Левая панель - выбор алгоритма
        self.create_algorithm_panel(workspace)

        # Центральная панель - ввод/вывод
        self.create_io_panel(workspace)

        # Правая панель - математические параметры
        self.create_math_panel(workspace)

    def create_algorithm_panel(self, parent):
        """Панель выбора алгоритма"""
        panel = ttk.LabelFrame(parent, text="Алгоритмы", padding=10)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Исторические шифры
        hist_label = ttk.Label(panel, text="Исторические шифры",
                               font=("Helvetica", 10, "bold"))
        hist_label.pack(anchor=tk.W, pady=(0, 5))

        self.caesar_btn = ttk.Button(panel, text="Шифр Цезаря",
                                     command=lambda: self.switch_cipher("caesar"))
        self.caesar_btn.pack(fill=tk.X, pady=2)

        self.vigenere_btn = ttk.Button(panel, text="Шифр Виженера",
                                       command=lambda: self.switch_cipher("vigenere"))
        self.vigenere_btn.pack(fill=tk.X, pady=2)

        # Современные алгоритмы
        modern_label = ttk.Label(panel, text="Современные алгоритмы",
                                 font=("Helvetica", 10, "bold"))
        modern_label.pack(anchor=tk.W, pady=(15, 5))

        self.rsa_btn = ttk.Button(panel, text="RSA",
                                  command=lambda: self.switch_cipher("rsa"))
        self.rsa_btn.pack(fill=tk.X, pady=2)

        self.dh_btn = ttk.Button(panel, text="Диффи-Хеллман",
                                 command=lambda: self.switch_cipher("diffie_hellman"))
        self.dh_btn.pack(fill=tk.X, pady=2)

        # Хеширование
        hash_label = ttk.Label(panel, text="Хеширование",
                               font=("Helvetica", 10, "bold"))
        hash_label.pack(anchor=tk.W, pady=(15, 5))

        self.xor_btn = ttk.Button(panel, text="XOR-хеш",
                                  command=lambda: self.switch_cipher("xor_hash"))
        self.xor_btn.pack(fill=tk.X, pady=2)

    def create_io_panel(self, parent):
        """Панель ввода/вывода текста"""
        panel = ttk.Frame(parent)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Ввод текста
        input_frame = ttk.LabelFrame(panel, text="Входной текст", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.input_text = scrolledtext.ScrolledText(input_frame,
                                                    wrap=tk.WORD,
                                                    font=("Helvetica", 11),
                                                    height=8,
                                                    relief=tk.FLAT,
                                                    borderwidth=1)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления
        control_frame = ttk.Frame(panel)
        control_frame.pack(fill=tk.X, pady=5)

        self.encrypt_btn = ttk.Button(control_frame,
                                      text="Зашифровать →",
                                      style="Accent.TButton",
                                      command=self.encrypt)
        self.encrypt_btn.pack(side=tk.LEFT, padx=5)

        self.decrypt_btn = ttk.Button(control_frame,
                                      text="← Расшифровать",
                                      style="Accent.TButton",
                                      command=self.decrypt)
        self.decrypt_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(control_frame,
                                    text="Очистить",
                                    command=self.clear_all)
        self.clear_btn.pack(side=tk.RIGHT, padx=5)

        # Вывод текста
        output_frame = ttk.LabelFrame(panel, text="Результат", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                     wrap=tk.WORD,
                                                     font=("Helvetica", 11),
                                                     height=8,
                                                     relief=tk.FLAT,
                                                     borderwidth=1)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def create_math_panel(self, parent):
        """Панель математических параметров"""
        self.math_panel = ttk.LabelFrame(parent, text="Математические параметры", padding=10)
        self.math_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        # Здесь будут динамически обновляемые параметры
        self.update_math_panel()

    def create_log_panel(self):
        """Панель логов с пошаговыми вычислениями"""
        log_frame = ttk.LabelFrame(self.main_container, text="Пошаговые вычисления", padding=10)
        log_frame.pack(fill=tk.X, pady=(20, 0))

        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  wrap=tk.WORD,
                                                  font=("Menlo", 10),
                                                  height=8,
                                                  relief=tk.FLAT,
                                                  borderwidth=1,
                                                  bg="white")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def update_math_panel(self):
        """Обновление панели математических параметров в зависимости от выбранного алгоритма"""
        # Очистка панели
        for widget in self.math_panel.winfo_children():
            widget.destroy()

        if self.current_cipher == "caesar":
            self.create_caesar_params()
        elif self.current_cipher == "vigenere":
            self.create_vigenere_params()
        elif self.current_cipher == "rsa":
            self.create_rsa_params()
        elif self.current_cipher == "diffie_hellman":
            self.create_diffie_hellman_params()
        elif self.current_cipher == "xor_hash":
            self.create_xor_params()

    def create_caesar_params(self):
        """Параметры для шифра Цезаря"""
        ttk.Label(self.math_panel, text="Сдвиг (k):").pack(anchor=tk.W)

        self.caesar_shift = tk.IntVar(value=3)
        shift_slider = ttk.Scale(self.math_panel,
                                 from_=1, to=25,
                                 variable=self.caesar_shift,
                                 orient=tk.HORIZONTAL,
                                 command=lambda x: self.update_caesar_label())
        shift_slider.pack(fill=tk.X, pady=5)

        self.shift_label = ttk.Label(self.math_panel,
                                     text=f"Текущий сдвиг: {self.caesar_shift.get()}")
        self.shift_label.pack()

        # Таблица соответствия
        ttk.Label(self.math_panel, text="\nПример соответствия:").pack()
        self.create_caesar_table()

    def create_caesar_table(self):
        """Создание таблицы соответствия для шифра Цезаря"""
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        shift = self.caesar_shift.get()

        table_text = f"А → {alphabet[shift % 33]}\n"
        table_text += f"Б → {alphabet[(1 + shift) % 33]}\n"
        table_text += f"В → {alphabet[(2 + shift) % 33]}"

        ttk.Label(self.math_panel, text=table_text,
                  font=("Menlo", 10)).pack()

    def update_caesar_label(self):
        """Обновление метки с текущим сдвигом"""
        self.shift_label.config(text=f"Текущий сдвиг: {self.caesar_shift.get()}")
        self.create_caesar_table()

    def create_vigenere_params(self):
        """Параметры для шифра Виженера"""
        ttk.Label(self.math_panel, text="Ключевое слово:").pack(anchor=tk.W)

        self.vigenere_key = tk.StringVar(value="КЛЮЧ")
        key_entry = ttk.Entry(self.math_panel,
                              textvariable=self.vigenere_key,
                              font=("Helvetica", 11))
        key_entry.pack(fill=tk.X, pady=5)

        ttk.Label(self.math_panel,
                  text="\nПринцип: Ci = (Pi + Ki) mod 26",
                  font=("Menlo", 9)).pack()

    def create_rsa_params(self):
        """Параметры для RSA"""
        # Простые числа p и q
        ttk.Label(self.math_panel, text="Простое число p:").pack(anchor=tk.W)
        self.rsa_p = tk.IntVar(value=17)
        p_spin = ttk.Spinbox(self.math_panel,
                             from_=2, to=100,
                             textvariable=self.rsa_p,
                             command=self.update_rsa_keys)
        p_spin.pack(fill=tk.X, pady=2)

        ttk.Label(self.math_panel, text="Простое число q:").pack(anchor=tk.W)
        self.rsa_q = tk.IntVar(value=19)
        q_spin = ttk.Spinbox(self.math_panel,
                             from_=2, to=100,
                             textvariable=self.rsa_q,
                             command=self.update_rsa_keys)
        q_spin.pack(fill=tk.X, pady=2)

        # Вычисленные значения
        self.rsa_n_label = ttk.Label(self.math_panel,
                                     text="n = p × q = 323")
        self.rsa_n_label.pack(anchor=tk.W, pady=5)

        self.rsa_phi_label = ttk.Label(self.math_panel,
                                       text="φ(n) = (p-1)(q-1) = 288")
        self.rsa_phi_label.pack(anchor=tk.W)

        # Кнопка для показа закрытого ключа
        self.show_private_btn = ttk.Button(self.math_panel,
                                           text="Показать закрытый ключ (d)",
                                           command=self.show_private_key)
        self.show_private_btn.pack(fill=tk.X, pady=10)

        self.private_key_label = ttk.Label(self.math_panel, text="")
        self.private_key_label.pack()

    def update_rsa_keys(self):
        """Обновление вычислений RSA"""
        p = self.rsa_p.get()
        q = self.rsa_q.get()

        n = p * q
        phi = (p - 1) * (q - 1)

        self.rsa_n_label.config(text=f"n = p × q = {n}")
        self.rsa_phi_label.config(text=f"φ(n) = (p-1)(q-1) = {phi}")

    def show_private_key(self):
        """Вычисление и отображение закрытого ключа RSA"""
        p = self.rsa_p.get()
        q = self.rsa_q.get()
        e = 65537  # Стандартная открытая экспонента

        phi = (p - 1) * (q - 1)

        try:
            d = sympy.mod_inverse(e, phi)
            self.private_key_label.config(
                text=f"d = {d}\n\nПроверка: ({e} × {d}) mod {phi} = 1")

            self.log(f"🔐 RSA: Вычислен закрытый ключ d = {d}")
            self.log(f"   Уравнение: {e} × d ≡ 1 mod {phi}")
        except:
            self.private_key_label.config(text="Ошибка: e и φ(n) не взаимно просты")

    def create_diffie_hellman_params(self):
        """Параметры для протокола Диффи-Хеллмана"""
        # Общие параметры
        ttk.Label(self.math_panel, text="Общие параметры:").pack(anchor=tk.W)

        ttk.Label(self.math_panel, text="Простое число p:").pack(anchor=tk.W)
        self.dh_p = tk.IntVar(value=23)
        p_spin = ttk.Spinbox(self.math_panel,
                             from_=2, to=100,
                             textvariable=self.dh_p,
                             command=self.update_dh_params)
        p_spin.pack(fill=tk.X, pady=2)

        ttk.Label(self.math_panel, text="Основание g:").pack(anchor=tk.W)
        self.dh_g = tk.IntVar(value=5)
        g_spin = ttk.Spinbox(self.math_panel,
                             from_=2, to=20,
                             textvariable=self.dh_g,
                             command=self.update_dh_params)
        g_spin.pack(fill=tk.X, pady=2)

        # Алиса
        ttk.Label(self.math_panel, text="\n👤 Алиса:").pack()
        self.dh_a = tk.IntVar(value=6)
        ttk.Label(self.math_panel, text="Секрет a:").pack()
        ttk.Spinbox(self.math_panel,
                    from_=2, to=20,
                    textvariable=self.dh_a,
                    command=self.update_dh_params).pack(fill=tk.X, pady=2)

        # Боб
        ttk.Label(self.math_panel, text="👤 Боб:").pack()
        self.dh_b = tk.IntVar(value=15)
        ttk.Label(self.math_panel, text="Секрет b:").pack()
        ttk.Spinbox(self.math_panel,
                    from_=2, to=20,
                    textvariable=self.dh_b,
                    command=self.update_dh_params).pack(fill=tk.X, pady=2)

        # Результат
        self.dh_result_label = ttk.Label(self.math_panel,
                                         text="\nОбщий секрет: вычисляется...")
        self.dh_result_label.pack(pady=10)

        self.update_dh_params()

    def update_dh_params(self):
        """Обновление вычислений Диффи-Хеллмана"""
        p = self.dh_p.get()
        g = self.dh_g.get()
        a = self.dh_a.get()
        b = self.dh_b.get()

        # Вычисление открытых ключей
        A = pow(g, a, p)
        B = pow(g, b, p)

        # Вычисление общего секрета
        secret_alice = pow(B, a, p)
        secret_bob = pow(A, b, p)

        if secret_alice == secret_bob:
            self.dh_result_label.config(
                text=f"✅ Общий секрет: {secret_alice}\n\n"
                     f"A = {g}^{a} mod {p} = {A}\n"
                     f"B = {g}^{b} mod {p} = {B}\n"
                     f"Secret = {B}^{a} mod {p} = {secret_alice}")

            self.log(f"🔑 DH: Алиса → A = {A}")
            self.log(f"   Боб → B = {B}")
            self.log(f"   Общий секрет: {secret_alice}")

    def create_xor_params(self):
        """Параметры для XOR-хеширования"""
        ttk.Label(self.math_panel,
                  text="XOR-хеш — простая\nкриптографическая хеш-функция",
                  justify=tk.LEFT).pack()

        ttk.Label(self.math_panel,
                  text="\nПринцип:\n• Разбиваем на 8-битные блоки\n• XOR всех блоков",
                  font=("Menlo", 9)).pack()

    def switch_cipher(self, cipher_name):
        """Переключение между шифрами"""
        self.current_cipher = cipher_name
        self.update_math_panel()
        self.clear_all()
        self.log(f"🔄 Переключено на {self.get_cipher_name(cipher_name)}")

    def get_cipher_name(self, cipher):
        """Получение читаемого названия шифра"""
        names = {
            "caesar": "шифр Цезаря",
            "vigenere": "шифр Виженера",
            "rsa": "RSA",
            "diffie_hellman": "Диффи-Хеллман",
            "xor_hash": "XOR-хеш"
        }
        return names.get(cipher, cipher)

    def encrypt(self):
        """Шифрование в зависимости от выбранного алгоритма"""
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для шифрования")
            return

        self.log(f"\n📝 Начало шифрования ({self.get_cipher_name(self.current_cipher)})")

        result = ""
        if self.current_cipher == "caesar":
            result = self.caesar_encrypt(text)
        elif self.current_cipher == "vigenere":
            result = self.vigenere_encrypt(text)
        elif self.current_cipher == "rsa":
            result = self.rsa_encrypt(text)
        elif self.current_cipher == "xor_hash":
            result = self.xor_hash(text)
        elif self.current_cipher == "diffie_hellman":
            messagebox.showinfo("Инфо",
                                "Протокол Диффи-Хеллман используется для генерации ключа, а не шифрования текста")
            return

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        self.log("✅ Шифрование завершено")

    def decrypt(self):
        """Расшифрование"""
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для расшифрования")
            return

        if self.current_cipher == "xor_hash":
            messagebox.showinfo("Инфо", "Хеш-функции необратимы - расшифрование невозможно")
            return

        self.log(f"\n📝 Начало расшифрования ({self.get_cipher_name(self.current_cipher)})")

        result = ""
        if self.current_cipher == "caesar":
            result = self.caesar_decrypt(text)
        elif self.current_cipher == "vigenere":
            result = self.vigenere_decrypt(text)
        elif self.current_cipher == "rsa":
            result = self.rsa_decrypt(text)
        else:
            messagebox.showinfo("Инфо", "Расшифрование для данного алгоритма не реализовано")
            return

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        self.log("✅ Расшифрование завершено")

    def caesar_encrypt(self, text):
        """Шифрование Цезаря"""
        shift = self.caesar_shift.get()
        result = []
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        for char in text.upper():
            if char in alphabet:
                idx = alphabet.index(char)
                new_idx = (idx + shift) % 33
                new_char = alphabet[new_idx]
                result.append(new_char)
                self.log(f"   '{char}' ({idx}) + {shift} = {new_idx} → '{new_char}'")
            else:
                result.append(char)

        return "".join(result)

    def caesar_decrypt(self, text):
        """Расшифрование Цезаря"""
        shift = self.caesar_shift.get()
        result = []
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        for char in text.upper():
            if char in alphabet:
                idx = alphabet.index(char)
                new_idx = (idx - shift) % 33
                new_char = alphabet[new_idx]
                result.append(new_char)
                self.log(f"   '{char}' ({idx}) - {shift} = {new_idx} → '{new_char}'")
            else:
                result.append(char)

        return "".join(result)

    def vigenere_encrypt(self, text):
        """Шифрование Виженера"""
        key = self.vigenere_key.get().upper()
        if not key:
            key = "КЛЮЧ"

        result = []
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        key_indices = [alphabet.index(k) for k in key if k in alphabet]

        if not key_indices:
            return text

        key_len = len(key_indices)
        key_pos = 0

        for char in text.upper():
            if char in alphabet:
                char_idx = alphabet.index(char)
                key_idx = key_indices[key_pos % key_len]
                new_idx = (char_idx + key_idx) % 33
                new_char = alphabet[new_idx]
                result.append(new_char)
                self.log(
                    f"   '{char}' ({char_idx}) + ключ '{key[key_pos % key_len]}' ({key_idx}) = {new_idx} → '{new_char}'")
                key_pos += 1
            else:
                result.append(char)

        return "".join(result)

    def vigenere_decrypt(self, text):
        """Расшифрование Виженера"""
        key = self.vigenere_key.get().upper()
        if not key:
            key = "КЛЮЧ"

        result = []
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        key_indices = [alphabet.index(k) for k in key if k in alphabet]

        if not key_indices:
            return text

        key_len = len(key_indices)
        key_pos = 0

        for char in text.upper():
            if char in alphabet:
                char_idx = alphabet.index(char)
                key_idx = key_indices[key_pos % key_len]
                new_idx = (char_idx - key_idx) % 33
                new_char = alphabet[new_idx]
                result.append(new_char)
                self.log(
                    f"   '{char}' ({char_idx}) - ключ '{key[key_pos % key_len]}' ({key_idx}) = {new_idx} → '{new_char}'")
                key_pos += 1
            else:
                result.append(char)

        return "".join(result)

    def rsa_encrypt(self, text):
        """RSA шифрование"""
        p = self.rsa_p.get()
        q = self.rsa_q.get()
        n = p * q
        e = 65537

        # Преобразуем текст в числа (упрощенно)
        result = []
        for char in text:
            m = ord(char)
            if m < n:  # Упрощение: каждый символ шифруется отдельно
                c = pow(m, e, n)
                result.append(str(c))
                self.log(f"   '{char}' → {m}^{e} mod {n} = {c}")
            else:
                result.append(char)

        return " ".join(result)

    def rsa_decrypt(self, text):
        """RSA расшифрование"""
        p = self.rsa_p.get()
        q = self.rsa_q.get()
        n = p * q
        e = 65537
        phi = (p - 1) * (q - 1)

        try:
            d = sympy.mod_inverse(e, phi)
        except:
            return "Ошибка: невозможно вычислить закрытый ключ"

        result = []
        for token in text.split():
            try:
                c = int(token)
                m = pow(c, d, n)
                char = chr(m)
                result.append(char)
                self.log(f"   {c}^{d} mod {n} = {m} → '{char}'")
            except:
                result.append(token)

        return "".join(result)

    def xor_hash(self, text):
        """XOR-хеширование"""
        # Преобразуем текст в байты
        data = text.encode('utf-8')
        hash_value = 0

        self.log(f"   Вычисление XOR для {len(data)} байт:")

        for i, byte in enumerate(data):
            old_hash = hash_value
            hash_value ^= byte
            self.log(f"   Байт {i}: {byte:02x} XOR {old_hash:02x} = {hash_value:02x}")

        hex_hash = f"{hash_value:02x}"
        self.log(f"   Итоговый хеш: {hex_hash}")

        return f"XOR-хеш: {hex_hash}"

    def log(self, message):
        """Добавление сообщения в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def clear_all(self):
        """Очистка всех полей"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.log_text.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = CryptoLab(root)

    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    # Проверка наличия sympy
    try:
        import sympy
    except ImportError:
        print("Установите sympy: pip install sympy")
        exit(1)

    main()