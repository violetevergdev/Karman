
def placeholder(filling, elem):
    def on_entry_click(event):
        if elem.get() == filling:
            elem.delete(0, 'end')
            elem.configure(foreground="black")

    def on_focus_out(event):
        if elem.get() == "":
            elem.insert(0, filling)
            elem.configure(foreground="gray")

    elem.insert(0, filling)

    elem.bind("<FocusIn>", on_entry_click)
    elem.bind("<FocusOut>", on_focus_out)