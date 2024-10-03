import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import pandas as pd
import calendar


class PriceChartGenerator:
    def __init__(self, price_history):
        # Преобразуем историю в DataFrame для удобной обработки
        self.history = pd.DataFrame(price_history)

        # Преобразуем столбец с датами в datetime
        self.history["timestamp"] = pd.to_datetime(self.history["timestamp"])

    def generate_year_chart(self):
        # Группируем по месяцам и высчитываем среднюю цену
        self.history["month"] = self.history["timestamp"].dt.to_period(
            "M"
        )  # Сгруппировано по месяцам
        monthly_avg = self.history.groupby("month")["price"].mean()

        # Построение графика
        fig, ax = plt.subplots(figsize=(10, 5))
        monthly_avg.plot(ax=ax, marker="o", color="b")

        ax.set_title("Изменение цен за последний год")
        ax.set_xlabel("Месяцы")
        ax.set_ylabel("Средняя цена")
        ax.grid(True)

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        return buf

    import calendar
    from datetime import datetime
    import matplotlib.pyplot as plt
    from io import BytesIO
    import pandas as pd

    def generate_month_chart(self):
        # Преобразуем строковый таймстемп в формат datetime
        self.history["timestamp"] = pd.to_datetime(self.history["timestamp"])

        # Берем данные только за последний месяц текущего года
        current_date = datetime.now()
        monthly_data = self.history[
            (self.history["timestamp"].dt.month == current_date.month)
            & (self.history["timestamp"].dt.year == current_date.year)
        ]

        # Построение графика
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            monthly_data["timestamp"].dt.day,
            monthly_data["price"],
            marker="o",
            color="b",
        )

        ax.set_title("Изменение цен за текущий месяц")
        ax.set_xlabel("Дни месяца")
        ax.set_ylabel("Цена")
        ax.grid(True)

        # Установка меток оси X
        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
        ax.set_xticks(
            range(1, days_in_month + 1)
        )  # Устанавливаем тики для каждого дня в месяце

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        return buf
