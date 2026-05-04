import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода
        ttk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        add_button = ttk.Button(self.root, text="Добавить расход", command=self.add_expense)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица расходов
        columns = ("Сумма", "Категория", "Дата")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.filter_category = ttk.Entry(self.root)
        self.filter_category.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=5, column=2, padx=5, pady=5, sticky='e')
        self.filter_date = ttk.Entry(self.root)
        self.filter_date.grid(row=5, column=3, padx=5, pady=5)

        # Кнопки фильтрации и сброса
        filter_button = ttk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        filter_button.grid(row=6, column=0, padx=5, pady=10)

        reset_button = ttk.Button(self.root, text="Сбросить фильтр", command=self.load_data)
        reset_button.grid(row=6, column=1, padx=5, pady=10)

        # Общая сумма
        self.total_label = ttk.Label(self.root, text="Общая сумма: 0")
        self.total_label.grid(row=7, column=0, padx=5, pady=10, sticky='w')

    def add_expense(self):
        amount_str = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date_str = self.date_entry.get().strip()

        # Валидация суммы
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число для суммы.")
            return

        # Валидация даты
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна иметь формат ГГГГ-ММ-ДД.")
            return

        # Добавление в таблицу и список
        self.tree.insert('', 'end', values=(amount, category, date_str))
        self.data.append({"Сумма": amount, "Категория": category, "Дата": date_str})
        self.save_data()
        self.update_total()

        # Очистка полей
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def load_data(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Загрузка данных
        try:
            with open('expenses.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

        # Отображение
        for expense in self.data:
            self.tree.insert('', 'end', values=(expense["Сумма"], expense["Категория"], expense["Дата"]))
        self.apply_filter()  # для применения фильтров при загрузке
        self.update_total()

    def save_data(self):
        with open('expenses.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def apply_filter(self):
        category_filter = self.filter_category.get().lower().strip()
        date_filter = self.filter_date.get().strip()

        filtered = self.data

        if category_filter:
            filtered = [e for e in filtered if category_filter in e["Категория"].lower()]

        if date_filter:
            try:
                datetime.strptime(date_filter, '%Y-%m-%d')
                filtered = [e for e in filtered if e["Дата"] == date_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Дата фильтра должна иметь формат ГГГГ-ММ-ДД.")
                return

        # Обновление таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        for expense in filtered:
            self.tree.insert('', 'end', values=(expense["Сумма"], expense["Категория"], expense["Дата"]))
        self.update_total(filtered)

    def update_total(self, data=None):
        # Подсчёт суммы
        if data is None:
            data = self.data
        total = sum(e["Сумма"] for e in data)
        self.total_label.config(text=f"Общая сумма: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()