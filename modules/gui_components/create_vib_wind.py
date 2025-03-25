import os.path
import re
import tkinter as tk
from tkinter.messagebox import showwarning, askyesno

from modules.gui_components.show_context_menu import show_context_menu
from modules.gui_components.specific_vib_wind import specific_vib_wind




def create_vib_wind(root, upd, icon_path):
    def valid_input(P):
        if not P:
            return True
        return bool(re.match(r"^[a-zA-Z0-9;~_-]$", P[-1]))

    def next_step():
        def valid_and_extr_data():
            datas = [name_of_vib_label, name_of_vib, name_of_file_label, name_of_file, database_label, database, table_label, table, fields_label, fields]
            data_extr = dict()
            try:
                for key, value in enumerate(datas):
                    if key % 2 == 0:
                        if datas[key+1].get() in ('', ' ', None):
                            showwarning('Ошибка валидации', 'Заполните все поля')
                            return
                            # return {'Наименование': 'test-name', 'Имя файла': 'test', "Выборки": {'База данных': ['PF', 'VPL'], 'Таблица': ['PF~MAN','VPL~PO'], 'Поля': ['MAN~DPW', 'MAN~RA', 'PO~NPERS', 'MAN~RE@M', 'MAN~RE@MO']}}
                        else:
                            if value['text'] in ('База данных', 'Таблица', 'Поля'):
                                vib_dict = data_extr.setdefault("Выборки", dict())
                                vib_dict[value['text']] = datas[key+1].get().strip().split(';')
                            else:
                                if value['text'] == "Имя файла":
                                    ex = os.path.isfile(f"C:\\soft_for_py_exe\\karman\\config\\vib\\{datas[key+1].get().strip()}.json")
                                    if ex:
                                        showwarning('Ошибка', 'Файл с таким названием уже существует')
                                        return

                                data_extr[value['text']] = datas[key + 1].get().strip()
                return data_extr

            except Exception as e:
                return e

        if is_valid := valid_and_extr_data():
            is_ok = askyesno('Подтверждение', f'Проверьте правильность данных: {is_valid}')
            if is_ok:
                root.destroy()
                specific_wind = tk.Toplevel()
                specific_wind.geometry('810x135')
                specific_wind.title('Уточнения выборки')
                x = (specific_wind.winfo_screenwidth() - specific_wind.winfo_reqwidth()) / 2
                y = (specific_wind.winfo_screenheight() - specific_wind.winfo_reqheight()) / 2
                specific_wind.wm_geometry("+%d+%d" % (x, y))
                specific_wind['bg'] = '#996666'
                specific_wind.resizable(False, False)
                specific_wind.attributes('-topmost', True)
                specific_vib_wind(specific_wind, is_valid, upd)
                specific_wind.iconbitmap(icon_path)
                specific_wind.protocol("WM_DELETE_WINDOW", lambda: specific_wind.destroy())
                specific_wind.mainloop()
            else:
                return False

    def how_to_use():
        how_wind = tk.Toplevel()
        how_wind.title('Правила заполнения')
        how_wind.configure(bg='#996666')
        how_wind.geometry('600x450')
        how_wind.resizable(width=False, height=False)
        how_wind.attributes('-topmost', True)
        x = (how_wind.winfo_screenwidth() - how_wind.winfo_reqwidth()) / 2
        y = (how_wind.winfo_screenheight() - how_wind.winfo_reqheight()) / 2
        how_wind.wm_geometry("+%d+%d" % (x, y))

        txt = tk.Text(how_wind, wrap="word", bg='#996666', font=('Courier', 14))
        txt.pack()
        txt.insert("1.0", "1. Все данные разделяются точкой с запятой ';', например, если вам нужно указать две БД, вы пишите 'PF;MAN'\n\n2. Таблица: ожидает сл. формата данных 'PF~MAN', если нужно несколько таблиц, то указываем так же через ';' - 'PF~MAN;VPL~PO', т.е. через знак 'тильда' указывается база данных, в которой располагается эта таблица и наименование самой таблицы (MAN, PO, POPAY и тп)\n\n3. Поля: формат ввода идентичный как и в поле Таблица, однако через знак '~' указывается таблица, в которой располагается поле и наименование этого поля (NPERS, RA и тп)\n\n4. Будьте внимательны, очередность указания баз данных, таблиц и полей имеют важность, если вам нужно взять PF и VPL, то указываться это должно в той последовательности, в которой находится в НВП, т.е. PF в списке указано раньше VPL, значит PF мы указываем первым, и через ';' указываем VPL\n\n5. Если в выборке будет необходимость указать разные уточнения для какого то поля в разрезе с сервером, на котором будет производиться выборка (Москва и Область), то данное поле нужно указать сл. образом: 'MAN~RE@M;MAN~RE@MO' *английская раскладка")
        txt['state'] = 'disabled'

        how_wind.protocol("WM_DELETE_WINDOW", lambda: how_wind.destroy())
        how_wind.mainloop()

    main_menu = tk.Menu()
    main_menu.add_cascade(label="Как заполнять?", command=how_to_use)

    root.config(menu=main_menu)

    main_frame = tk.LabelFrame(root, text='Основные значения', bg=root['bg'], font=('Courier', 12))
    main_frame.place(relx=0.02, rely=0.01, relheight=0.72, relwidth=0.95)

    name_of_vib_label = tk.Label(main_frame, text='Наименование', bg=root['bg'], font=('Courier', 13))
    name_of_vib_label.place(relx=0.01, rely=0.019)

    name_of_vib = tk.Entry(main_frame, font=('Courier', 13))
    name_of_vib.place(relx=0.4, rely=0.019)
    name_of_vib.bind("<Button-3>", lambda event, entry=name_of_vib: show_context_menu(main_frame, event, entry))

    name_of_file_label = tk.Label(main_frame, text='Имя файла', bg=root['bg'], font=('Courier', 13))
    name_of_file_label.place(relx=0.01, rely=0.22)

    name_of_file = tk.Entry(main_frame, font=('Courier', 13), validate='key', validatecommand=(root.register(valid_input), '%P'))
    name_of_file.place(relx=0.4, rely=0.22)
    name_of_file.bind("<Button-3>", lambda event, entry=name_of_file: show_context_menu(main_frame, event, entry))

    database_label = tk.Label(main_frame, text='База данных', bg=root['bg'], font=('Courier', 13))
    database_label.place(relx=0.01, rely=0.41)

    database = tk.Entry(main_frame, font=('Courier', 13), validate='key', validatecommand=(root.register(valid_input), '%P'))
    database.place(relx=0.4, rely=0.41)
    database.bind("<Button-3>", lambda event, entry=database: show_context_menu(main_frame, event, entry))

    table_label = tk.Label(main_frame, text='Таблица', bg=root['bg'], font=('Courier', 13))
    table_label.place(relx=0.01, rely=0.6)

    table = tk.Entry(main_frame, font=('Courier', 13), validate='key', validatecommand=(root.register(valid_input), '%P'))
    table.place(relx=0.4, rely=0.6)
    table.bind("<Button-3>", lambda event, entry=table: show_context_menu(main_frame, event, entry))

    fields_label = tk.Label(main_frame, text='Поля', bg=root['bg'], font=('Courier', 13))
    fields_label.place(relx=0.01, rely=0.79)

    fields = tk.Entry(main_frame, font=('Courier', 13), validate='key', validatecommand=(root.register(valid_input), '%P'))
    fields.place(relx=0.4, rely=0.79)
    fields.bind("<Button-3>", lambda event, entry=fields: show_context_menu(main_frame, event, entry))

    next_btn = tk.Button(root, text='Далее', bg='#999', font=('Courier', 13), command=next_step)
    next_btn.place(relx=0.2, rely=0.8, relwidth=0.6)
