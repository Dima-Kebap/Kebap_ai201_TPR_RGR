from tkinter import messagebox
from fractions import Fraction
import numpy as np
from tkinter import *


# розрахунок пріоритетів та відсотка узгодженості
def calculate_priority(array):
    n = len(array[0])
    array_imp = np.zeros(n)

    for j in range(n):  # сума по рядкам
        array_imp[j] = np.sum(array[:, j])

    array2 = np.zeros((n, n))
    for i in range(n):  # розрахунок значення пріоритету
        for j in range(n):
            array2[i, j] = array[i, j] / array_imp[j]

    array_prior = np.zeros(n)
    for i in range(n):  # розрахунок підсумкового пріоритету для кожної альтернативи для кожного критерію
        array_prior[i] = round(np.sum(array2[i, :]) / n, 5)

    lambda_max = 0  # максимальне власне число матриці
    for j in range(n):
        lambda_max += array_prior[j] * np.sum(array[:, j])

    array_CI = (lambda_max - n) / (n - 1)  # індекс узгодженості
    # знаходимо значення індексу узгодженості для випадкових матриць
    array_RI = (0.0, 0.0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59)[n - 1]

    array_CR = array_CI / array_RI  # Розраховуємо ставлення узгодженості
    array_CR = int(round(array_CR * 100, 0))  # та переводимо його у відсотки

    return array_prior, array_CR  # повертаємо результати


# Розрахунок та показ фінальних результатів
def calculate_result(entry_array, prior_crit, alt_array, crit_array, c_arr):
    n_crit = len(crit_array)
    n_alt = len(alt_array)
    root = Tk()
    window_width = (n_crit + 1) * 125
    root.geometry("{0}x500".format(window_width))  # Встановлюємо розмір вікна
    content_frame = add_scrollbar(root)
    prior_alternat = []

    try:  # розрахунок пріоритетів попарного порівняння
        for value in entry_array:
            cp = calculate_priority(text_to_float(value))
            prior_alternat.append(cp[0])
            c_arr.append(cp[1])
    except ValueError as e:
        messagebox.showinfo("Помилка", "Якесь поле порожнє")
        return

    label = Label(content_frame, text="Результат")
    label.grid(row=0, columnspan=n_crit + 1, pady=10)

    # Створення назв стовпців(назви критерів, та їх ваги)
    for a1 in range(n_crit):
        row_label_text = crit_array[a1]
        entry_text = StringVar(content_frame, value=str(prior_crit[a1]))
        row_label = Label(content_frame, text=row_label_text)
        row_label.grid(row=1, column=a1 + 1, padx=5)
        entry = Entry(content_frame, textvariable=entry_text, state="readonly")
        entry.grid(row=2, column=a1 + 1, padx=5, pady=5)

    entry_text = StringVar(content_frame, value="С (% узгодж) = " + str(c_arr[0]))
    entry = Entry(content_frame, textvariable=entry_text, state="readonly")
    entry.grid(row=1, column=0, padx=5, pady=5)

    row_label_text = "Вага крит."
    row_label = Label(content_frame, text=row_label_text)
    row_label.grid(row=2, column=0, padx=5)

    # Створення назв рядків
    for a1 in range(n_alt):
        row_label_text = alt_array[a1]
        row_label = Label(content_frame, text=row_label_text)
        row_label.grid(row=a1 + 3, column=0, padx=5)
    row_label_text = "С (% узгодж)"
    row_label = Label(content_frame, text=row_label_text)
    row_label.grid(row=n_alt + 3, column=0, padx=5)

    for p in range(n_crit):  # заповнення ячеек пріоритетів по кожному критерію
        for a in range(n_alt):
            entry_var = StringVar(content_frame, value=str(prior_alternat[p][a]))
            entry = Entry(content_frame, textvariable=entry_var, state="readonly")
            entry.grid(row=a + 3, column=p + 1, padx=5, pady=5)
        # проценти узгодженості
        entry_var = StringVar(content_frame, value=str(c_arr[p + 1]))
        entry = Entry(content_frame, textvariable=entry_var, state="readonly")
        entry.grid(row=n_alt + 3, column=p + 1, padx=5, pady=5)

    label = Label(content_frame, text="Підсумкові пріоритети")
    label.grid(row=n_alt + 4, columnspan=n_crit + 1, pady=10)

    result_alternat = np.zeros(n_alt)

    for i in range(n_alt):  # розрахунок підсумкових пріоритетів
        for kr in range(len(prior_crit)):
            result_alternat[i] += prior_alternat[kr][i] * prior_crit[kr]
        result_alternat[i] = round(result_alternat[i], 5)

    for p in range(len(result_alternat)):
        label = Label(content_frame, text=str(alt_array[p]) + " = " + str(result_alternat[p]) + "\n")
        label.grid(row=p + n_alt + 5, columnspan=n_crit + 1)

    result_ind = np.argmax(result_alternat)  # знаходження індексу елемента, з найбільшим значенням пріоритету

    label = Label(content_frame, text="Кращий варіант: " + str(alt_array[result_ind]))  # показ найкращої альтернативи
    label.grid(row=2 * n_alt + 6, columnspan=n_crit + 1, pady=10)
    root.mainloop()


def text_to_float(arr):  # отримання даних з полів, та обчислення значень, які починаються з "1/"
    n = len(arr)
    crit_entry = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            string_fraction = arr[i][j].get()
            if '/' in string_fraction:
                fraction = Fraction(string_fraction)
                crit_entry[i][j] = fraction.numerator / fraction.denominator
            else:
                crit_entry[i][j] = float(arr[i][j].get())
    return crit_entry


# Вікно вводу попарного порівняння альтернатив
def poparne(alt_arr, krit_arr, crit_entry):
    def validate_integer(text):  # перевірка щоб можна було вводити лише числа або "1/", та неможна було ввести нульове значення
        return (text.isdigit() or text == "" or text.startswith("1/")) and not text.startswith("0")

    def copy_entry_value(event, k, row,
                         col):  # додання оберненої величини до симетричного поля відносно головної діагоналі
        if col != row:
            if entry_array[k][row][col].get() != "" and not '1/' in entry_array[k][row][col].get():
                entry_array[k][col][row].set("1/{}".format(entry_array[k][row][col].get()))
            elif entry_array[k][row][col].get().startswith("1/"):
                entry_array[k][col][row].set(entry_array[k][row][col].get()[2:])
            else:
                entry_array[k][col][row].set("")

    c_arr = []  # масив відсотків узгодженості
    try:  # розрахунок пріоритетів порівняння критеріїв
        cp = calculate_priority(text_to_float(crit_entry))
        prior_crit = cp[0]
        c_arr.append(cp[1])
    except ValueError as e:
        messagebox.showinfo("Помилка", "Якесь поле порожнє")
        return

    n_krit = len(krit_arr)
    n_alt = len(alt_arr)
    root = Tk()
    window_width = (n_alt + 1) * 125
    root.geometry("{0}x800".format(window_width))  # Встановлюємо розмір вікна
    content_frame = add_scrollbar(root)
    validation = root.register(validate_integer)
    entry_array = []
    # Створення матриць полів вводу
    for k in range(n_krit):
        entry_array.append([])

        # Створення заголовку для кожної матриці
        label_text = krit_arr[k]
        label = Label(content_frame, text=label_text)
        label.grid(row=k * (n_alt + 2), columnspan=n_alt + 1, pady=10)

        # Створення назв рядків
        for a1 in range(n_alt):
            row_label_text = alt_arr[a1]
            row_label = Label(content_frame, text=row_label_text)
            row_label.grid(row=k * (n_alt + 2) + a1 + 2, column=0, padx=5)

        # Створення назв стовпців
        for a2 in range(n_alt):
            col_label_text = alt_arr[a2]
            col_label = Label(content_frame, text=col_label_text)
            col_label.grid(row=k * (n_alt + 2) + 1, column=a2 + 1, padx=5, pady=5)

        # Створення полів вводу для кожної матриці
        for a1 in range(n_alt):
            entry_array[k].append([])
            for a2 in range(n_alt):
                entry_var = StringVar(content_frame, value="")
                state_var = NORMAL
                if a1 == a2:
                    entry_var = StringVar(content_frame, value="1")
                    state_var = "readonly"
                entry = Entry(content_frame, textvariable=entry_var, state=state_var)
                entry.grid(row=k * (n_alt + 2) + a1 + 2, column=a2 + 1, padx=5, pady=5)

                entry.config(validate="key", validatecommand=(validation, "%P"))
                entry_array[k][a1].append(entry_var)

                entry.bind("<FocusOut>", lambda event, k=k, row=a1, col=a2: copy_entry_value(event, k, row, col))
                entry.bind("<Return>", lambda event, k=k, row=a1, col=a2: copy_entry_value(event, k, row, col))

    # Кнопка, яка проводить фінальні розрахунки
    button = Button(content_frame, text="Розрахувати",
                    command=lambda: calculate_result(entry_array, prior_crit, alt_arr, krit_arr, c_arr))
    button.grid(row=n_krit * (n_alt + 2), columnspan=n_alt + 1, pady=10)

    # Запуск вікна попарного порівняння
    root.mainloop()


# вікно вводу порівнянь критеріїв
def comparison_of_criteria(alt_arr, krit_arr):
    def validate_integer(text):  # перевірка щоб можна було вводити лише числа або "1/", та неможна було ввести нульове значення
        return (text.isdigit() or text == "" or text.startswith("1/")) and not text.startswith("0")

    def copy_entry_value(event, row,
                         col):  # додання оберненої величини до симетричного поля відносно головної діагоналі
        if col != row:
            if entry_array[row][col].get() != "" and not '1/' in entry_array[row][col].get():
                entry_array[col][row].set("1/{}".format(entry_array[row][col].get()))
            elif entry_array[row][col].get().startswith("1/"):
                entry_array[col][row].set(entry_array[row][col].get()[2:])
            else:
                entry_array[col][row].set("")

    n_krit = len(krit_arr)
    root = Tk()
    window_width = (n_krit + 1) * 150
    root.geometry("{0}x300".format(window_width))  # Встановлюємо розмір вікна
    content_frame = add_scrollbar(root)
    validation = root.register(validate_integer)

    entry_array = []
    # заголовок вікна
    label = Label(content_frame, text="Порівняйте критерії за ступенем їх важливості для досягнення мети")
    label.grid(row=0, columnspan=n_krit + 1, pady=10)

    # Створення назв рядків
    for a1 in range(n_krit):
        row_label_text = krit_arr[a1]
        row_label = Label(content_frame, text=row_label_text)
        row_label.grid(row=a1 + 2, column=0, padx=5)

    # Створення назв стовпців
    for a2 in range(n_krit):
        col_label_text = krit_arr[a2]
        col_label = Label(content_frame, text=col_label_text)
        col_label.grid(row=1, column=a2 + 1, padx=5, pady=5)

    # Створення полів вводу
    for a1 in range(n_krit):
        entry_array.append([])
        for a2 in range(n_krit):
            entry_var = StringVar(content_frame, value="")
            state_var = NORMAL
            if a1 == a2:
                entry_var = StringVar(content_frame, value="1")
                state_var = "readonly"
            entry = Entry(content_frame, textvariable=entry_var, state=state_var)
            entry.grid(row=a1 + 2, column=a2 + 1, padx=5, pady=5)
            entry.config(validate="key", validatecommand=(validation, "%P"))
            entry_array[a1].append(entry_var)
            entry.bind("<FocusOut>", lambda event, row=a1, col=a2: copy_entry_value(event, row, col))
            entry.bind("<Return>", lambda event, row=a1, col=a2: copy_entry_value(event, row, col))

    # Кнопка переходу до попарного порівняння альтернатив
    button = Button(content_frame, text="Попарно порівняти критерії",
                    command=lambda: poparne(alt_arr, krit_arr, entry_array))
    button.grid(row=n_krit * (n_krit + 2), columnspan=n_krit + 1, pady=10)

    # Запуск вікна порівнянь критеріїв
    root.mainloop()


# створення скрол барів для вікна
def add_scrollbar(container):
    main_frame = Frame(container)
    main_frame.pack(fill="both", expand=True)

    scrollbarY = Scrollbar(main_frame, orient=VERTICAL)  # для вертикального прокручування
    scrollbarY.pack(side="right", fill="y")
    scrollbarX = Scrollbar(main_frame, orient=HORIZONTAL)  # для горизонтального прокручування
    scrollbarX.pack(side=BOTTOM, fill="x")

    my_canvas = Canvas(main_frame, yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
    my_canvas.pack(side="left", fill="both", expand=True)

    scrollbarY.config(command=my_canvas.yview)
    scrollbarX.config(command=my_canvas.xview)

    content_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_configure(event):
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))

    my_canvas.bind("<Configure>", on_configure)

    return content_frame


# запуск програми
def start():
    # перевірка введених даних(критеріїв та альтернатив)
    def check_data(lb_alt, lb_krit):
        if len(lb_alt) < 3:
            messagebox.showinfo("Помилка", "Список альтернатив має містити хоча б 3 елементи.")
        elif len(lb_krit) < 3:
            messagebox.showinfo("Помилка", "Список критеріїв має містити хоча б 3 елементи.")
        else:
            comparison_of_criteria(lb_alt, lb_krit)

    # додання критерію
    def add_crit(event):
        value = entry_krit.get()  # Отримуємо значення з поля вводу
        if value:  # Перевіряємо, чи введено значення
            listbox_krit.insert("end", value)  # Додаємо значення до списку
            entry_krit.delete(0, "end")  # Очищаємо поле вводу

    # додання альтернативи
    def add_alt(event):
        value = entry_alt.get()  # Отримуємо значення з поля вводу
        if value:  # Перевіряємо, чи введено значення
            listbox_alt.insert("end", value)  # Додаємо значення до списку
            entry_alt.delete(0, "end")  # Очищаємо поле вводу

    root = Tk()
    root.geometry("300x300")  # Встановлюємо розмір вікна
    content_frame = add_scrollbar(root)

    # Додавання вмісту в content_frame
    label_alt = Label(content_frame, text="альтернативи")
    label_alt.grid(row=0, column=0, padx=5, pady=5)

    entry_alt = Entry(content_frame)
    entry_alt.grid(row=1, column=0, padx=5, pady=5)
    entry_alt.bind("<Return>", add_alt)  # Прив'язуємо подію до поля вводу

    listbox_alt = Listbox(content_frame)
    listbox_alt.grid(row=2, column=0, padx=5, pady=5)

    label_krit = Label(content_frame, text="критерії")
    label_krit.grid(row=0, column=1, padx=5, pady=5)

    entry_krit = Entry(content_frame)
    entry_krit.grid(row=1, column=1, padx=5, pady=5)
    entry_krit.bind("<Return>", add_crit)  # Прив'язуємо подію до поля вводу

    listbox_krit = Listbox(content_frame)
    listbox_krit.grid(row=2, column=1, padx=5, pady=5)
    # щоб вручну кожного разу не вводити список альтернатив так критеріїв(розкоментувати ці 3 рядки і закоментувати рядок після них).
    # Після цього можна просто натиснути кнопку "Порівняти критерії"
    #k_a = ["Ціна ", "Рік випуску ", "Марка", "Об’єм двигуна","Пасажиро місткість ","Коробка передач ","Колір"]
    #al_a = ["BMW M5 ", "Audi A5 ", "Mazda RX-8 ","Ford Kuga ","Infiniti QX50 "]
    # button = Button(content_frame, text="Порівняти критерії", command=lambda: check_data(al_a, k_a))
    button = Button(content_frame, text="Порівняти критерії", command=lambda: check_data(listbox_alt.get(0, "end"), listbox_krit.get(0, "end")))

    button.grid(row=3, columnspan=2, padx=5, pady=5)

    root.mainloop()


start()  # запускаємо програму
