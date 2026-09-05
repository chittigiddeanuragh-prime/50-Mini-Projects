import tkinter as tk


def convert():
    try:
        value = float(value_entry.get())
        category = category_var.get()
        from_unit = from_var.get()
        to_unit = to_var.get()

        if category == "Length":
            units = {
                "Meter": 1,
                "Kilometer": 1000,
                "Centimeter": 0.01,
                "Millimeter": 0.001,
                "Mile": 1609.344,
                "Yard": 0.9144,
                "Foot": 0.3048,
                "Inch": 0.0254
            }
            result = value * units[from_unit] / units[to_unit]

        elif category == "Weight":
            units = {
                "Kilogram": 1,
                "Gram": 0.001,
                "Milligram": 0.000001,
                "Pound": 0.45359237,
                "Ounce": 0.0283495231
            }
            result = value * units[from_unit] / units[to_unit]

        elif category == "Temperature":
            if from_unit == to_unit:
                result = value
            elif from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (value * 9 / 5) + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (value - 32) * 5 / 9
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                result = value + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                result = value - 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                result = (value - 32) * 5 / 9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                result = (value - 273.15) * 9 / 5 + 32

        elif category == "Area":
            units = {
                "Square Meter": 1,
                "Square Kilometer": 1000000,
                "Square Foot": 0.092903,
                "Square Yard": 0.836127,
                "Acre": 4046.8564224,
                "Hectare": 10000
            }
            result = value * units[from_unit] / units[to_unit]

        elif category == "Time":
            units = {
                "Second": 1,
                "Minute": 60,
                "Hour": 3600,
                "Day": 86400,
                "Week": 604800
            }
            result = value * units[from_unit] / units[to_unit]

        result_label.config(
            text=f"{value:g} {from_unit} = {result:.6g} {to_unit}",
            fg="#FFE600"
        )

        status_label.config(
            text="Conversion completed!",
            fg="#00C853"
        )

    except (ValueError, KeyError):
        result_label.config(
            text="Please enter a valid value",
            fg="#FF3333"
        )

        status_label.config(
            text="Enter a valid number and units",
            fg="#FF3333"
        )


def clear():
    value_entry.delete(0, tk.END)
    result_label.config(
        text="Result will appear here",
        fg="#FFFFFF"
    )
    status_label.config(
        text="Ready",
        fg="#FFFFFF"
    )


def update_units(*args):
    category = category_var.get()

    if category == "Length":
        units = [
            "Meter",
            "Kilometer",
            "Centimeter",
            "Millimeter",
            "Mile",
            "Yard",
            "Foot",
            "Inch"
        ]

    elif category == "Weight":
        units = [
            "Kilogram",
            "Gram",
            "Milligram",
            "Pound",
            "Ounce"
        ]

    elif category == "Temperature":
        units = [
            "Celsius",
            "Fahrenheit",
            "Kelvin"
        ]

    elif category == "Area":
        units = [
            "Square Meter",
            "Square Kilometer",
            "Square Foot",
            "Square Yard",
            "Acre",
            "Hectare"
        ]

    else:
        units = [
            "Second",
            "Minute",
            "Hour",
            "Day",
            "Week"
        ]

    from_menu["menu"].delete(0, "end")
    to_menu["menu"].delete(0, "end")

    for unit in units:
        from_menu["menu"].add_command(
            label=unit,
            command=lambda value=unit: from_var.set(value)
        )

        to_menu["menu"].add_command(
            label=unit,
            command=lambda value=unit: to_var.set(value)
        )

    from_var.set(units[0])
    to_var.set(units[1])


root = tk.Tk()
root.title("My Unit Converter")
root.geometry("900x800")
root.minsize(700, 650)
root.resizable(True, True)
root.configure(bg="#101820")


title = tk.Label(
    root,
    text="Unit Converter",
    font=("Arial", 34, "bold"),
    bg="#101820",
    fg="#FF3333"
)
title.pack(pady=(35, 5))


subtitle = tk.Label(
    root,
    text="Convert values quickly and easily",
    font=("Arial", 13),
    bg="#101820",
    fg="#FFE600"
)
subtitle.pack(pady=(0, 25))


main_frame = tk.Frame(
    root,
    bg="#182A3A",
    bd=2,
    relief="solid",
    highlightbackground="#0066FF",
    highlightthickness=2
)

main_frame.pack(
    padx=50,
    pady=10,
    fill="both",
    expand=True
)


category_label = tk.Label(
    main_frame,
    text="Choose Category",
    font=("Arial", 14, "bold"),
    bg="#182A3A",
    fg="#FFFFFF"
)
category_label.pack(pady=(35, 10))


category_var = tk.StringVar()
category_var.set("Length")


category_menu = tk.OptionMenu(
    main_frame,
    category_var,
    "Length",
    "Weight",
    "Temperature",
    "Area",
    "Time"
)

category_menu.config(
    font=("Arial", 13, "bold"),
    bg="#FF3333",
    fg="#FFFFFF",
    activebackground="#FF5555",
    activeforeground="#FFFFFF",
    relief="flat",
    width=18
)

category_menu["menu"].config(
    bg="#FFFFFF",
    fg="#101820",
    activebackground="#FFE600",
    activeforeground="#101820"
)

category_menu.pack(
    ipady=8
)


value_label = tk.Label(
    main_frame,
    text="Enter Value",
    font=("Arial", 14, "bold"),
    bg="#182A3A",
    fg="#FFFFFF"
)
value_label.pack(pady=(30, 10))


value_entry = tk.Entry(
    main_frame,
    font=("Arial", 17),
    justify="center",
    bg="#0B1117",
    fg="#FFFFFF",
    insertbackground="#FFE600",
    relief="solid",
    bd=1,
    width=25
)

value_entry.pack(
    ipady=10
)


units_frame = tk.Frame(
    main_frame,
    bg="#182A3A"
)

units_frame.pack(
    pady=30,
    fill="x",
    padx=60
)


from_label = tk.Label(
    units_frame,
    text="From",
    font=("Arial", 13, "bold"),
    bg="#182A3A",
    fg="#0066FF"
)

from_label.grid(
    row=0,
    column=0,
    pady=8
)


to_label = tk.Label(
    units_frame,
    text="To",
    font=("Arial", 13, "bold"),
    bg="#182A3A",
    fg="#FF3333"
)

to_label.grid(
    row=0,
    column=2,
    pady=8
)


from_var = tk.StringVar()
to_var = tk.StringVar()


from_menu = tk.OptionMenu(
    units_frame,
    from_var,
    ""
)

from_menu.config(
    font=("Arial", 12),
    bg="#0066FF",
    fg="#FFFFFF",
    activebackground="#3385FF",
    activeforeground="#FFFFFF",
    relief="flat",
    width=18
)

from_menu["menu"].config(
    bg="#FFFFFF",
    fg="#101820",
    activebackground="#FFE600",
    activeforeground="#101820"
)

from_menu.grid(
    row=1,
    column=0,
    padx=20,
    ipady=8
)


arrow_label = tk.Label(
    units_frame,
    text="→",
    font=("Arial", 25, "bold"),
    bg="#182A3A",
    fg="#FFE600"
)

arrow_label.grid(
    row=1,
    column=1,
    padx=10
)


to_menu = tk.OptionMenu(
    units_frame,
    to_var,
    ""
)

to_menu.config(
    font=("Arial", 12),
    bg="#FF3333",
    fg="#FFFFFF",
    activebackground="#FF5555",
    activeforeground="#FFFFFF",
    relief="flat",
    width=18
)

to_menu["menu"].config(
    bg="#FFFFFF",
    fg="#101820",
    activebackground="#FFE600",
    activeforeground="#101820"
)

to_menu.grid(
    row=1,
    column=2,
    padx=20,
    ipady=8
)


button_frame = tk.Frame(
    main_frame,
    bg="#182A3A"
)

button_frame.pack(pady=15)


convert_button = tk.Button(
    button_frame,
    text="Convert",
    font=("Arial", 13, "bold"),
    bg="#FFE600",
    fg="#101820",
    activebackground="#FFF27A",
    activeforeground="#101820",
    relief="flat",
    cursor="hand2",
    command=convert
)

convert_button.grid(
    row=0,
    column=0,
    padx=10,
    ipadx=35,
    ipady=10
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 13, "bold"),
    bg="#0066FF",
    fg="#FFFFFF",
    activebackground="#3385FF",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear
)

clear_button.grid(
    row=0,
    column=1,
    padx=10,
    ipadx=35,
    ipady=10
)


result_label = tk.Label(
    main_frame,
    text="Result will appear here",
    font=("Arial", 19, "bold"),
    bg="#182A3A",
    fg="#FFFFFF",
    wraplength=700
)

result_label.pack(
    pady=(30, 10)
)


status_label = tk.Label(
    main_frame,
    text="Ready",
    font=("Arial", 11),
    bg="#182A3A",
    fg="#FFFFFF"
)

status_label.pack(
    pady=10
)


info_label = tk.Label(
    main_frame,
    text="Length  •  Weight  •  Temperature  •  Area  •  Time",
    font=("Arial", 10),
    bg="#182A3A",
    fg="#8FA8C2"
)

info_label.pack(
    pady=(20, 30)
)


category_var.trace_add(
    "write",
    update_units
)

update_units()

root.mainloop()