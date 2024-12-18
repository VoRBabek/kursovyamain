import tkinter as tk
from tkinter import filedialog, messagebox
import time
from decimal import Decimal, getcontext
import random  # Импортируем модуль random для генерации случайных чисел

# Устанавливаем точность вычислений
getcontext().prec = 50  # Устанавливаем точность на 50 знаков

class GaussianEliminationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод Гаусса")

        # Элементы интерфейса
        self.txtEquationCount = tk.Entry(root)
        self.txtCoefficients = tk.Text(root, height=10, width=50)
        self.txtResults = tk.Text(root, height=10, width=50)
        btnLoadFromFile = tk.Button(root, text="Загрузить из файла", command=self.load_from_file)
        btnSaveToFile = tk.Button(root, text="Сохранить в файл", command=self.save_to_file)
        btnGenerateRandom = tk.Button(root, text="Сгенерировать случайные коэффициенты", command=self.generate_random_coefficients)
        btnCalculate = tk.Button(root, text="Вычислить", command=self.calculate)
        btnClearResults = tk.Button(root, text="Очистить результаты", command=self.clear_results)

        # Настройка тегов для подсветки ошибок
        self.txtCoefficients.tag_configure("error", background="pink")
        self.txtEquationCount.configure(highlightbackground="red", highlightthickness=0)  # Начальная настройка

        # Размещение элементов на форме
        tk.Label(root, text="Количество уравнений:").pack(fill=tk.X)
        self.txtEquationCount.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(root, text="Коэффициенты:").pack(fill=tk.X)
        self.txtCoefficients.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        btnLoadFromFile.pack(fill=tk.X, padx=5, pady=5)
        btnSaveToFile.pack(fill=tk.X, padx=5, pady=5)
        btnGenerateRandom.pack(fill=tk.X, padx=5, pady=5)  # Добавляем кнопку для генерации случайных коэффициентов
        btnCalculate.pack(fill=tk.X, padx=5, pady=5)
        btnClearResults.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(root, text="Результаты:").pack(fill=tk.X)
        self.txtResults.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Привязка событий для проверки данных в реальном времени
        self.txtCoefficients.bind("<KeyRelease>", self.validate_coefficients)
        self.txtEquationCount.bind("<KeyRelease>", self.validate_equation_count)

    def generate_random_coefficients(self):
        """Генерирует случайные коэффициенты для системы уравнений."""
        try:
            n = int(self.txtEquationCount.get())
            if n <= 0:
                raise ValueError("Количество уравнений должно быть положительным целым числом.")

            self.txtCoefficients.delete(1.0, tk.END)
            for _ in range(n):
                coefficients = [str(random.randint(-10, 10)) for _ in range(n + 1)]  # Генерация случайных чисел от -10 до 10
                self.txtCoefficients.insert(tk.END, " ".join(coefficients) + "\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество уравнений перед генерацией.")

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.txtCoefficients.delete(1.0, tk.END)
                self.txtCoefficients.insert(tk.END, file.read())
            self.validate_coefficients()  # Проверка данных после загрузки

    def save_to_file(self):
        """Сохраняет результаты в файл."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files (*.txt)", "*.txt"),
                                                            ("All files (*.*)", "*.*")])
        if file_path:
            try:
                # Считываем текст из виджета в переменную
                results = self.txtResults.get(1.0, tk.END).strip()
                if not results:
                    raise ValueError("Нет данных для сохранения. Сначала выполните расчет.")

                # Открываем файл и записываем данные
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(results)
                messagebox.showinfo("Успех", f"Результаты успешно сохранены в файл: {file_path}")
            except Exception as ex:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {ex}")

    def highlight_error_line(self, line_number):
        """Подсвечивает строку с ошибкой."""
        self.txtCoefficients.tag_add("error", f"{line_number}.0", f"{line_number}.end")

    def clear_error_highlight(self):
        """Убирает подсветку ошибок."""
        self.txtCoefficients.tag_remove("error", "1.0", tk.END)

    def validate_equation_count(self, event=None):
        """Проверяет корректность поля 'Количество уравнений'."""
        value = self.txtEquationCount.get()
        try:
            n = int(value)  # Пробуем преобразовать в целое число
            if n <= 0:
                raise ValueError  # Если значение <= 0, это ошибка
            self.txtEquationCount.configure(highlightthickness=0)  # Снимаем подсветку
        except ValueError:
            self.txtEquationCount.configure(highlightbackground="red", highlightthickness=2)  # Подсветка ошибки

    def validate_coefficients(self, event=None):
        """Проверяет корректность введенных коэффициентов в реальном времени."""
        self.clear_error_highlight()  # Убираем предыдущие подсветки ошибок

        # Проверяем корректность поля "Количество уравнений"
        try:
            n = int(self.txtEquationCount.get())
            if n <= 0:
                return  # Пропускаем, если некорректное количество уравнений
        except ValueError:
            return

        # Проверяем корректность коэффициентов
        lines = self.txtCoefficients.get(1.0, tk.END).strip().split('\n')

        for i, line in enumerate(lines):
            values = line.strip().split()
            if len(values) != n + 1:
                self.highlight_error_line(i + 1)  # Подсветка, если количество коэффициентов неверное
                continue

            # Проверка, являются ли все элементы числами
            for value in values:
                if not self.is_valid_number(value):
                    self.highlight_error_line(i + 1)  # Подсветка строки с ошибкой
                    break

    def is_valid_number(self, value):
        """Проверяет, является ли строка корректным числом (целым или вещественным)."""
        import decimal
        try:
            Decimal(value)  # Проверяем, можно ли преобразовать в число с помощью Decimal
            return True
        except (ValueError, decimal.InvalidOperation):  # Добавляем обработку InvalidOperation
            return False

    def calculate(self):
        try:
            self.clear_error_highlight()  # Снимаем предыдущую подсветку
            self.txtResults.delete(1.0, tk.END)  # Очищаем результаты перед расчетом
            start_time = time.time()  # Начало измерения времени

            n = int(self.txtEquationCount.get())
            if n <= 0:
                raise ValueError("Введите корректное количество уравнений.")

            lines = self.txtCoefficients.get(1.0, tk.END).strip().split('\n')
            if len(lines) != n:
                raise ValueError("Количество введенных уравнений не соответствует заданному количеству.")

            matrix = []
            for i in range(n):
                input_line = lines[i].strip().split()
                if len(input_line) != n + 1:
                    self.highlight_error_line(i + 1)
                    raise ValueError(f"Уравнение {i + 1} должно содержать {n + 1} коэффициентов.")
                matrix.append([Decimal(x) for x in input_line])  # Используем Decimal для всех коэффициентов

            # Проверка на несовместность системы
            for row in matrix:
                if all(value == 0 for value in row[:-1]) and row[-1] != 0:
                    self.txtResults.insert(tk.END, "Система не имеет решений (несовместна).\n")
                    return

            # Проверка, все ли элементы матрицы равны нулю
            all_zeros = all(all(value == 0 for value in row) for row in matrix)
            if all_zeros:
                self.txtResults.insert(tk.END, "Бесконечное множество решений.\n")
                return

            # Вывод начальной матрицы (с округлением для промежуточных шагов)
            self.txtResults.insert(tk.END, "Начальная матрица:\n")
            for row in matrix:
                self.txtResults.insert(tk.END, ' '.join(f"{val:.3f}" for val in row) + "\n")  # Округляем до 3 знаков
            self.txtResults.insert(tk.END, "\n")

            # Прямой ход метода Гаусса
            for i in range(n):
                if matrix[i][i] == 0:  # Проверка на ноль
                    for j in range(i + 1, n):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            self.txtResults.insert(tk.END,
                                                   f"Поменяли местами строки {i + 1} и {j + 1}, чтобы избежать деления на ноль.\n")
                            break
                    else:
                        raise ValueError(f"В уравнении {i + 1} главный коэффициент равен нулю, решение невозможно.")

                for j in range(i + 1, n):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
                    self.txtResults.insert(tk.END,
                                           f"Из строки {j + 1} вычли строку {i + 1}, умноженную на {factor:.3f}.\n")  # Округляем

                # Вывод промежуточной матрицы (с округлением)
                self.txtResults.insert(tk.END, f"Промежуточная матрица после шага {i + 1}:\n")
                for row in matrix:
                    self.txtResults.insert(tk.END, ' '.join(f"{val:.3f}" for val in row) + "\n")
                self.txtResults.insert(tk.END, "\n")

            # Обратный ход для нахождения решения
            solution = [Decimal(0)] * n
            for i in range(n - 1, -1, -1):
                solution[i] = matrix[i][n] / matrix[i][i]
                for j in range(i - 1, -1, -1):
                    matrix[j][n] -= matrix[j][i] * solution[i]

            # Вывод решения (с высокой точностью)
            self.txtResults.insert(tk.END, "Решение:\n")
            for i in range(n):
                variable = f"x{i + 1}"
                self.txtResults.insert(tk.END, f"{variable} = {solution[i]:.10f}\n")  # Выводим с точностью до 10 знаков

            # Вывод времени выполнения
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.txtResults.insert(tk.END, f"\nВремя выполнения: {elapsed_time:.4f} секунд\n")

        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))

    def clear_results(self):
        self.txtResults.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = GaussianEliminationApp(root)
    root.mainloop()
