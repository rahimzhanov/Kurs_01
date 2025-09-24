import json
from src.utils import read_excel, greeting, get_cards_info, top_five_operations, get_currencies, get_stocks, \
    filter_data_by_date
from config import PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS
from src.logger import get_logger

log = get_logger('views.log')


def load_user_settings():
    """Загружает настройки пользователя из user_settings.json"""
    try:
        with open(PATH_TO_USER_SETTINGS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Возвращаем настройки по умолчанию, если файл не найден
        return {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }


def generate_response(input_datetime: str) -> dict:
    """
    Главная функция, принимающая дату и возвращающая JSON-ответ

    Args:
        input_datetime: строка с датой в формате YYYY-MM-DD HH:MM:SS

    Returns:
        dict: JSON-ответ со всеми требуемыми данными
    """
    # Загружаем настройки пользователя
    settings = load_user_settings()

    # Читаем данные из Excel
    operations_df = read_excel(PATH_TO_OPERATIONS)

    # Фильтруем данные по дате (с начала месяца до указанной даты)
    filtered_df = filter_data_by_date(operations_df, input_datetime)

    # Формируем ответ
    response = {
        "greeting": greeting(),
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": []
    }

    # Данные по картам
    cards_info = get_cards_info(filtered_df)
    for card_number, row in cards_info.iterrows():
        response["cards"].append({
            "last_digits": str(card_number)[-4:],  # Последние 4 цифры карты
            "total_spent": abs(float(row['Сумма платежа'])),  # Сумма расходов (положительное число)
            "cashback": float(row['Кэшбэк'])  # Кешбэк
        })

    # Топ-5 транзакций
    top_transactions = top_five_operations(filtered_df)
    for _, transaction in top_transactions.iterrows():
        response["top_transactions"].append({
            "date": transaction['Дата операции'].strftime("%d.%m.%Y"),
            "amount": float(transaction['Сумма платежа']),
            "category": transaction['Категория'],
            "description": transaction['Описание']
        })

    # Курсы валют
    currencies = get_currencies(settings['user_currencies'])
    if isinstance(currencies, dict):  # Проверяем, что получили данные, а не ошибку
        for currency, rate in currencies.items():
            response["currency_rates"].append({
                "currency": currency,
                "rate": float(rate)
            })

    # Стоимость акций
    stocks = get_stocks(settings['user_stocks'])
    if isinstance(stocks, dict):  # Проверяем, что получили данные, а не ошибку
        for stock, price in stocks.items():
            response["stock_prices"].append({
                "stock": stock,
                "price": float(price)
            })

    log.info(f"Ответ сформирован: {len(response['cards'])} карт, "
             f"{len(response['top_transactions'])} транзакций, "
             f"{len(response['currency_rates'])} валют, "
             f"{len(response['stock_prices'])} акций")
    return response


# Пример использования
if __name__ == "__main__":
    # Тестируем функцию
    result = generate_response("2021-08-14 12:12:12")
    print(json.dumps(result, ensure_ascii=False, indent=2))
