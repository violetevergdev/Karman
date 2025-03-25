import ctypes
import json
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from dotenv import load_dotenv

from modules.gui_components.create_vib_wind import create_vib_wind
from modules.vib.start_vib import start_vib


def gui():
    def start():
        selected_vib = selected_items_list.get()
        vib_path = next(key for key, val in get_vibs().items() if val == selected_vib)
        err = start_vib(vib_path, server_val.get())
        if err:
            showerror('Ошибка', f'Ошибка {err}')
            return
        showinfo("Готово", "Выборка завершена")

    def upd_func():
        new_values = [val for val in get_vibs().values()]
        selected_items_list.configure(values=new_values)
        selected_items_list.set('')

    def create_vib():
        new_vib_window = tk.Toplevel()
        new_vib_window.geometry('380x300')
        new_vib_window.title('Новая выборка')
        x = (new_vib_window.winfo_screenwidth() - new_vib_window.winfo_reqwidth()) / 2
        y = (new_vib_window.winfo_screenheight() - new_vib_window.winfo_reqheight()) / 2
        new_vib_window.wm_geometry("+%d+%d" % (x, y))
        new_vib_window['bg'] = '#996666'
        new_vib_window.resizable(False, False)
        new_vib_window.attributes('-topmost', True)
        create_vib_wind(new_vib_window, upd_func, icon_path)
        new_vib_window.iconbitmap(icon_path)
        new_vib_window.protocol("WM_DELETE_WINDOW", lambda: new_vib_window.destroy())
        new_vib_window.mainloop()

    load_dotenv()
    root = tk.Tk()
    root.geometry('390x245')
    root.title(f'Karman v{(os.getenv("APP_VERS"))}')
    root.resizable(False, False)
    root.attributes('-topmost', True)
    root['bg'] = '#996666'

    main_label = tk.Label(root, text='KaRMaN', font=('Fixedsys', 18), bg=root['bg'], fg='#333')
    main_label.place(x=10, y=0)

    main_frame = tk.Frame(root, bg=root['bg'])
    main_frame.place(x=0, y=35, width=250, height=215)

    new_vib_btn = tk.Button(main_frame, text='Создать выборку', font=('Fixedsys', 12), bg='#999', command=create_vib)
    new_vib_btn.place(relx=0.235, rely=0.11)

    select_frame = tk.LabelFrame(main_frame, text='Выбери че хош', fg='#333', bg=root['bg'], font=('Fixedsys', 12))
    select_frame.place(relx=0.05, rely=0.33, relwidth=0.9, relheight=0.35)

    def get_vibs():
        dir_path = 'C:\\soft_for_py_exe\\karman\\config\\vib'
        dir_lst = os.listdir(dir_path)
        name_dicts = dict()
        for el in dir_lst:
            with open(os.path.join(dir_path, el), 'r', encoding='UTF-8') as f:
                vib_json = json.load(f)
                name_dicts[os.path.join(dir_path, el)] = vib_json['Наименование']

        return name_dicts

    selected_items_list = ttk.Combobox(select_frame, values=[val for val in get_vibs().values()], state='readonly', font=('Fixedsys', 13))
    selected_items_list.place(relx=0.05, rely=0.06, relwidth=0.9, relheight=0.6)

    start_btn = tk.Button(main_frame, text='Запустить', font=('Fixedsys', 12), bg='#999', command=start)
    start_btn.place(relx=0.05, rely=0.75, relwidth=0.9)

    #================

    config_frame = tk.LabelFrame(root, bg='#996867')
    config_frame.place(x=250, y=-5, width=145, height=255)

    serv_label = tk.Label(config_frame, text='Сервер:', font=('Fixedsys', 12), bg=config_frame['bg'])
    serv_label.place(relx=0.26, y=15)

    server_val = tk.StringVar(value='209')
    servers = ['209', '210', '206', '179', '183', '184', '129-MO МСП', '139-M МСП', '114-тест', '138-МСП тест']
    y_val = 45
    y_block_val = y_val

    for i, serv in enumerate(servers):
        el = tk.Radiobutton(config_frame, variable=server_val, text=serv, value=serv, font=('Fixedsys', 12), bg=config_frame['bg'], activebackground=config_frame['bg'])
        if len(serv) > 3:
            y_val += 25
            el.place(x=10, y=y_val)
        else:
            if i in (0,1,2):
                el.place(x=10, y=y_block_val)
                y_block_val +=20
            else:
                el.place(x=70, y=y_val)
                y_val += 20
        if i == 0:
            el.select()

    if os.getenv('ENV_FOR_DYNACONF') == 'prod':
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
        icon_path = os.path.join('./', 'icon.ico')

    root.iconbitmap(icon_path)
    root.mainloop()

