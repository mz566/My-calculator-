from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from threading import Thread
from urllib.request import urlopen
import json


# =========================
# BUTTON
# =========================

class CalcButton(Button):

    def __init__(self, button_color=(0.14, 0.14, 0.17, 1), **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.button_color = button_color

        with self.canvas.before:
            self.bg_color = Color(*self.button_color)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        self.bind(on_press=self.start_glow)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def start_glow(self, *args):
        self.bg_color.rgb = (0.35, 0.75, 1.0)
        Clock.schedule_once(self.stop_glow, 0.15)

    def stop_glow(self, *args):
        self.bg_color.rgb = self.button_color


# =========================
# CALCULATOR
# =========================

class Calculator(App):

    def build(self):

        Window.clearcolor = (0.03, 0.03, 0.04, 1)

        self.root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # Title
        title = Label(
            text="MY CALCULATOR",
            font_size=dp(22),
            size_hint_y=0.07
        )

        self.root.add_widget(title)

        # Display
        self.display = Label(
            text="0",
            font_size=dp(48),
            halign="right",
            valign="middle",
            padding=(dp(15), 0),
            size_hint_y=0.20
        )

        with self.display.canvas.before:
            Color(0.08, 0.08, 0.10, 1)
            self.display_bg = RoundedRectangle(
                pos=self.display.pos,
                size=self.display.size,
                radius=[dp(20)]
            )

        self.display.bind(
            pos=self.update_display,
            size=self.update_display
        )

        self.root.add_widget(self.display)

        # Mode buttons
        modes = BoxLayout(
            spacing=dp(8),
            size_hint_y=0.08
        )

        calc_mode = Button(
            text="CALCULATOR",
            font_size=dp(16)
        )

        currency_mode = Button(
            text="CURRENCY",
            font_size=dp(16)
        )

        calc_mode.bind(
            on_press=lambda x: self.show_calculator()
        )

        currency_mode.bind(
            on_press=lambda x: self.show_currency()
        )

        modes.add_widget(calc_mode)
        modes.add_widget(currency_mode)

        self.root.add_widget(modes)

        # Main content
        self.main_area = BoxLayout(
            orientation="vertical"
        )

        self.root.add_widget(self.main_area)

        self.show_calculator()

        return self.root

    def update_display(self, *args):
        self.display_bg.pos = self.display.pos
        self.display_bg.size = self.display.size

    # =========================
    # CALCULATOR MODE
    # =========================

    def show_calculator(self):

        self.main_area.clear_widgets()

        buttons = [
            "C", "⌫", "÷", "×",
            "7", "8", "9", "−",
            "4", "5", "6", "+",
            "1", "2", "3", "=",
            "0", ".", "(", ")"
        ]

        keyboard = GridLayout(
            cols=4,
            spacing=dp(8)
        )

        for value in buttons:

            if value in ["÷", "×", "−", "+"]:
                color = (0.12, 0.28, 0.65, 1)

            elif value == "=":
                color = (0.08, 0.60, 0.30, 1)

            elif value == "C":
                color = (0.65, 0.12, 0.12, 1)

            else:
                color = (0.14, 0.14, 0.17, 1)

            button = CalcButton(
                text=value,
                font_size=dp(29),
                color=(1, 1, 1, 1),
                button_color=color
            )

            button.bind(
                on_press=lambda btn:
                self.calculate(btn.text)
            )

            keyboard.add_widget(button)

        self.main_area.add_widget(keyboard)

    # =========================
    # CALCULATOR LOGIC
    # =========================

    def calculate(self, value):

        if value == "C":
            self.display.text = "0"

        elif value == "⌫":

            if len(self.display.text) > 1:
                self.display.text = self.display.text[:-1]
            else:
                self.display.text = "0"

        elif value == "=":

            try:

                expression = self.display.text
                expression = expression.replace("×", "*")
                expression = expression.replace("÷", "/")
                expression = expression.replace("−", "-")

                answer = eval(
                    expression,
                    {"__builtins__": None},
                    {}
                )

                self.display.text = str(answer)

            except:
                self.display.text = "Error"

        else:

            if self.display.text == "0":
                self.display.text = value
            else:
                self.display.text += value

    # =========================
    # CURRENCY MODE
    # =========================

    def show_currency(self):

        self.main_area.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(5)
        )

        # Amount
        layout.add_widget(
            Label(
                text="Amount",
                font_size=dp(18),
                size_hint_y=0.10
            )
        )

        self.amount_input = TextInput(
            text="1",
            input_filter="float",
            multiline=False,
            halign="center",
            font_size=dp(30),
            size_hint_y=0.18
        )

        layout.add_widget(self.amount_input)

        # FROM
        layout.add_widget(
            Label(
                text="FROM",
                font_size=dp(16),
                size_hint_y=0.08
            )
        )

        self.from_currency = Spinner(
            text="NGN",
            values=(
                "NGN",
                "USD",
                "GBP",
                "EUR",
                "CAD",
                "AUD",
                "GHS",
                "ZAR",
                "KES"
            ),
            font_size=dp(21),
            size_hint_y=0.14
        )

        layout.add_widget(self.from_currency)

        # TO
        layout.add_widget(
            Label(
                text="TO",
                font_size=dp(16),
                size_hint_y=0.08
            )
        )

        self.to_currency = Spinner(
            text="USD",
            values=(
                "NGN",
                "USD",
                "GBP",
                "EUR",
                "CAD",
                "AUD",
                "GHS",
                "ZAR",
                "KES"
            ),
            font_size=dp(21),
            size_hint_y=0.14
        )

        layout.add_widget(self.to_currency)

        # Convert
        convert = CalcButton(
            text="CONVERT  💱",
            font_size=dp(22),
            color=(1, 1, 1, 1),
            button_color=(0.08, 0.45, 0.70, 1),
            size_hint_y=0.15
        )

        convert.bind(
            on_press=lambda x:
            self.convert_currency()
        )

        layout.add_widget(convert)

        # Result
        self.currency_result = Label(
            text="Enter an amount and press CONVERT",
            font_size=dp(22),
            halign="center",
            size_hint_y=0.18
        )

        layout.add_widget(self.currency_result)

        self.main_area.add_widget(layout)

    # =========================
    # CURRENCY CONVERSION
    # =========================

    def convert_currency(self):

        try:

            amount = float(
                self.amount_input.text
            )

        except:

            self.currency_result.text = (
                "Enter a valid amount"
            )
            return

        from_currency = self.from_currency.text
        to_currency = self.to_currency.text

        self.currency_result.text = (
            "Getting live exchange rate..."
        )

        Thread(
            target=self.get_exchange_rate,
            args=(
                amount,
                from_currency,
                to_currency
            ),
            daemon=True
        ).start()

    def get_exchange_rate(
        self,
        amount,
        from_currency,
        to_currency
    ):

        try:

            url = (
                "https://open.er-api.com/v6/latest/"
                + from_currency
            )

            response = urlopen(
                url,
                timeout=15
            )

            data = json.loads(
                response.read().decode()
            )

            if data.get("result") != "success":
                raise Exception("Rate unavailable")

            rate = data["rates"][to_currency]

            result = amount * rate

            Clock.schedule_once(
                lambda dt:
                self.show_result(
                    amount,
                    from_currency,
                    result,
                    to_currency,
                    rate
                )
            )

        except Exception:

            Clock.schedule_once(
                lambda dt:
                self.show_error()
            )

    def show_result(
        self,
        amount,
        from_currency,
        result,
        to_currency,
        rate
    ):

        self.currency_result.text = (
            f"{amount:,.2f} {from_currency}\n"
            f"= {result:,.2f} {to_currency}\n\n"
            f"Rate: 1 {from_currency} = "
            f"{rate:.4f} {to_currency}"
        )

    def show_error(self):

        self.currency_result.text = (
            "Could not get exchange rate.\n"
            "Check your internet connection."
        )


Calculator().run()