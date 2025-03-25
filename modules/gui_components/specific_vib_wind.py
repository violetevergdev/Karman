import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning, askyesno
from modules.gui_components.placeholder import placeholder
from modules.gui_components.show_context_menu import show_context_menu


def get_options():
    with open("C:\\soft_for_py_exe\\karman\\config\\common.json", encoding="utf8") as f:
        options = json.load(f)["OPTIONS_DICT"]
        return [val for val in options]


def specific_vib_wind(root, datas: dict, upd):
    def get_all_data():
        data_dict = {}
        ind = 0
        for i, widget in enumerate(scrollable_frame.winfo_children()):
            if isinstance(widget, tk.Label):
                label_text = widget.cget("text")
                combobox = scrollable_frame.winfo_children()[i + 1]
                entry_from = scrollable_frame.winfo_children()[i + 2]
                entry_to = scrollable_frame.winfo_children()[i + 3]

                if isinstance(combobox, ttk.Combobox) and isinstance(entry_from, tk.Entry) and isinstance(entry_to,
                                                                                                          tk.Entry):
                    tmp_opt = combobox.get()
                    tmp_ot = entry_from.get()
                    tmp_do = entry_to.get()


                    if tmp_opt == "все данные":
                        ind += 1
                        continue
                    elif tmp_opt == "от-до (заполнять оба поля)":
                        if tmp_ot == "Значение (от *опц)":
                            showwarning("Ошибка", "Заполните значение от")
                            return False
                        elif tmp_do == "*Значение до":
                            showwarning("Ошибка", "Заполните значение до")
                            return False
                        else:
                            data_dict[label_text] = {
                                "select": "form1:table1:" + str(ind) + ":menu1",
                                "option": tmp_opt,
                                "set_ot": "form1:table1:" + str(ind) + ":text7",
                                "set_keys_ot": (tmp_ot if tmp_ot != "Значение (от *опц)" else ""),
                                "set_do": "form1:table1:" + str(ind) + ":text9",
                                "set_keys_do": (tmp_do if tmp_do != "*Значение до" else ""),
                            }
                    elif "@" in str(label_text):
                            if str(label_text).endswith("@M"):
                                label_text = label_text.replace("@M", "")
                                if label_text in data_dict:
                                    data_dict[label_text].update({
                                        "set_keys_M": (tmp_ot if tmp_ot != "Значение (от *опц)" else ""),
                                    })
                                else:
                                    data_dict[label_text] = {
                                        "select": "form1:table1:" + str(ind) + ":menu1",
                                        "option": tmp_opt,
                                        "set": "form1:table1:" + str(ind) + ":text7",
                                        "set_keys_M": (tmp_ot if tmp_ot != "Значение (от *опц)" else ""),
                                    }
                            elif str(label_text).endswith("@MO"):
                                label_text = label_text.replace("@MO", "")
                                if label_text in data_dict:
                                    data_dict[label_text].update({
                                        "set_keys_MO": (tmp_ot if tmp_ot != "Значение (от *опц)" else ""),
                                    })
                                else:
                                    data_dict[label_text] = {
                                        "select": "form1:table1:" + str(ind) + ":menu1",
                                        "option": tmp_opt,
                                        "set": "form1:table1:" + str(ind) + ":text7",
                                        "set_keys_MO": (tmp_ot if tmp_ot != "Значение (от *опц)" else ""),
                                    }
                    else:
                        data_dict[label_text] = {
                            "select": "form1:table1:" + str(ind) + ":menu1",
                            "option": tmp_opt,
                            "set": "form1:table1:" + str(ind) + ":text7",
                            "set_keys": ("" if tmp_ot == "Значение (от *опц)" else tmp_ot),
                        }
                    ind += 1

        return data_dict

    def save_vib():
        specific_data = get_all_data()

        if specific_data or specific_data == {}:
            datas["Уточнения"] = specific_data
            tmp_fields = datas["Выборки"]["Поля"]
            new_fields = []

            for el in tmp_fields:
                if el.endswith("@M"):
                    el = el.replace("@M", "")
                    if el in new_fields:
                        continue
                    else:
                        new_fields.append(el)
                elif el.endswith("@MO"):
                    el = el.replace("@MO", "")
                    if el in new_fields:
                        continue
                    else:
                        new_fields.append(el)
                else:
                    if el in new_fields:
                        continue
                    else:
                        new_fields.append(el)

            datas["Выборки"]["Поля"] = new_fields

            if askyesno('Подтверждение', 'Вы подтверждаете правильность данных?'):
                filename = datas["Имя файла"] + '.json'
                out_path = os.path.join("C:\\soft_for_py_exe\\karman\\config\\vib", filename)
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(datas, f, ensure_ascii=False, indent=4)

                root.destroy()
                upd()
                os.startfile(out_path)


    max_height = 315
    y_size = 4
    el_count = 0

    main_frame = tk.LabelFrame(root, text="Внесение уточнений", bg=root["bg"], font=("Courier", 13))
    main_frame.place(relx=0.02, rely=0.01, relheight=0.7, relwidth=0.95)

    canvas = tk.Canvas(main_frame, bg=root["bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=root["bg"])

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    wind = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=810)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(x=0.5, relwidth=0.999, relheight=1)

    opt = get_options()

    for el in datas["Выборки"]["Поля"]:
        name_of_vib_label = tk.Label(scrollable_frame, text=el, bg=root["bg"], font=("Courier", 12))
        name_of_vib_label.place(x=4, y=y_size)

        type_soecif = ttk.Combobox(scrollable_frame, font=("Courier", 12), values=opt, state="readonly")
        type_soecif.place(x=110, y=y_size)
        type_soecif.current(0)

        specif_ot_entry = tk.Entry(scrollable_frame, font=("Courier", 12), foreground="gray")
        specif_ot_entry.place(x=340, y=y_size, height=25, width=200)
        placeholder("Значение (от *опц)", specif_ot_entry)
        specif_ot_entry.bind("<Button-3>", lambda event, entry=specif_ot_entry: show_context_menu(main_frame, event, entry))

        specif_do_entry = tk.Entry(scrollable_frame, font=("Courier", 12), foreground="gray")
        specif_do_entry.place(x=547, y=y_size, height=25, width=200)
        placeholder("*Значение до", specif_do_entry)
        specif_do_entry.bind("<Button-3>", lambda event, entry=specif_do_entry: show_context_menu(main_frame, event, entry))

        y_size += 35
        el_count += 1

        root.update_idletasks()
        current_width = root.winfo_width()
        current_height = root.winfo_height()
        new_height = current_height + 30
        if new_height < max_height:
            root.geometry(f"{current_width}x{new_height}")

        if el_count > 5:
            scrollbar.place(x=750, relheight=1)
            canvas.configure(scrollregion=canvas.bbox("all"))

            def on_mousewheel(event):
                canvas.yview_scroll(-1 * (event.delta // 120), "units")

            root.bind_all("<MouseWheel>", on_mousewheel)

    canvas.itemconfig(wind, height=y_size)
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    save_btn = tk.Button(root, text="Сохранить", bg="#999", font=("Courier", 13), command=save_vib)
    save_btn.place(relx=0.2, rely=0.8, relwidth=0.6)


