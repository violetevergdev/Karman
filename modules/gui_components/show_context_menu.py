from tkinter import Menu


def copy_entry_contents(entry):
    entry.clipboard_clear()
    entry.clipboard_append(entry.get())


def paste_data(event):
    clipboard_data = event.clipboard_get()
    event.delete(0, 'end')
    event.insert(0, clipboard_data)
    event.configure(foreground="black")


def show_context_menu(root, event, entry):
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Копировать", command=lambda: copy_entry_contents(entry))
    context_menu.add_command(label="Вставить", command=lambda: paste_data(entry))
    context_menu.tk.call("tk_popup", context_menu, event.x_root, event.y_root)
