import flet as ft

TITLE = "ماشین حساب امیرعباس عبادی"

BUTTONS = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]


def main(page: ft.Page):
    page.title = TITLE
    page.bgcolor = "#121212"
    page.padding = 16
    page.theme_mode = "dark"

    title = ft.Text(
        TITLE,
        size=22,
        weight="bold",
        color="#FFFFFF",
        text_align="center",
    )
    expr_text = ft.Text("", size=20, color="#9E9E9E", text_align="right")
    result_text = ft.Text("0", size=48, weight="bold", color="#FFFFFF", text_align="right")

    state = {"expr": ""}

    def refresh():
        expr_text.value = state["expr"]
        page.update()

    def calculate():
        raw = state["expr"]
        if not raw:
            return
        e = raw.replace("×", "*").replace("÷", "/")
        e = e.replace("%", "/100")
        try:
            if not all(c in "0123456789+-*/.() " for c in e):
                raise ValueError
            val = eval(e, {"__builtins__": {}}, {})
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            result_text.value = str(round(val, 10) if isinstance(val, float) else val)
            state["expr"] = result_text.value
        except Exception:
            result_text.value = "خطا"
            state["expr"] = ""
        expr_text.value = raw
        page.update()

    def on_click(e):
        key = e.control.data
        if key == "C":
            state["expr"] = ""
            result_text.value = "0"
        elif key == "⌫":
            state["expr"] = state["expr"][:-1]
        elif key == "=":
            calculate()
            return
        else:
            state["expr"] += key
        refresh()

    def make_button(label, expand=1):
        if label in "÷×-+=":
            bg = "#FF9800"
        elif label in ("C", "⌫", "%"):
            bg = "#616161"
        else:
            bg = "#2C2C2C"
        return ft.Container(
            content=ft.Text(label, size=26, color="#FFFFFF"),
            alignment=ft.Alignment(0, 0) if hasattr(ft, "Alignment") else None,
            bgcolor=bg,
            border_radius=16,
            height=72,
            expand=expand,
            data=label,
            on_click=on_click,
            ink=True,
        )

    rows = []
    for row in BUTTONS:
        cells = []
        for label in row:
            cells.append(make_button(label, expand=2 if (label == "0") else 1))
        rows.append(ft.Row(cells, spacing=10))

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    title,
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Column(
                            [expr_text, result_text],
                            horizontal_alignment="end",
                            spacing=4,
                        ),
                        padding=16,
                        bgcolor="#1E1E1E",
                        border_radius=16,
                        alignment=ft.Alignment(1, 0) if hasattr(ft, "Alignment") else None,
                    ),
                    ft.Container(height=10),
                    *rows,
                ],
                spacing=10,
            )
        )
    )


if hasattr(ft, "run"):
    ft.run(main)
else:
    ft.app(target=main)
