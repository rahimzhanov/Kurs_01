"""
Основной модуль запуска приложения.
"""

from datetime import datetime

from config import PATH_TO_OPERATIONS
from src.reports import spending_by_weekday_json
from src.services import search_transactions_json
from src.utils import read_excel
from src.views import generate_response


def main():
    # Чтение данных
    df = read_excel(PATH_TO_OPERATIONS)

    # Текущая дата и время
    current_datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fixed_date = "2021-08-14 12:12:12"

    print("=== Генерация полного ответа ===")
    result = generate_response(fixed_date)
    print(result)

    print("\n=== Поиск транзакций (например, 'Лента') ===")
    search_result = search_transactions_json("Лента")
    print(search_result)

    print("\n=== Средние траты по дням недели ===")
    weekday_spending = spending_by_weekday_json(spending_by_weekday(df, fixed_date))
    print(weekday_spending)


if __name__ == "__main__":
    main()