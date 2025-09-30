import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from config import PATH_TO_OPERATIONS
from src.logger import get_logger

load_dotenv()

log = get_logger('utils.log')


def greeting():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        log.info('Функция greeting вернула - Доброе утро')
        return "Доброе утро"
    elif 12 <= hour < 18:
        log.info('Функция greeting вернула - Добрый день')
        return 'Добрый день'
    elif 18 <= hour < 24:
        log.info('Функция greeting вернула - Добрый вечер')
        return 'Добрый вечер'
    else:  # 0-6 часов
        log.info('Функция greeting вернула - Доброй ночи')
        return 'Доброй ночи'


def read_excel(path: str) -> pd.DataFrame:
    """
      Читает Excel файл и преобразует колонку с датами.

    Args:
        path: Путь к Excel файлу

    Returns:
        DataFrame: DataFrame с преобразованными датами
    """
    df = pd.read_excel(path)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    return df


def filter_data_by_date(operations_df: pd.DataFrame, date_end: str) -> pd.DataFrame:
    """Фильтрует данные с начала месяца до указанной даты."""
    end_date = pd.to_datetime(date_end)
    first_date = end_date.replace(day=1, hour=0, minute=0, second=0)

    filtered_df = operations_df[
        (operations_df["Дата операции"] >= first_date) &
        (operations_df["Дата операции"] <= end_date)
    ]

    log.info("Отфильтрованные данные от %s до %s: %s rows", first_date, end_date, len(filtered_df))

    return filtered_df


def get_cards_info(operations_df: pd.DataFrame) -> pd.DataFrame:
    """
        Возвращает данные суммы платежа и кэшбэк по каждой карте

    Args:
        operations_df: DataFrame полученный из read_excel()

    Returns:
        DataFrame только с данными карты
    """
    operations_df = operations_df[(operations_df['Сумма платежа'] < 0) & (operations_df['Статус'] == 'OK')]
    cards_info_df = (
        operations_df[['Номер карты', 'Сумма платежа', 'Кэшбэк']]
        .groupby('Номер карты')[['Сумма платежа', 'Кэшбэк']]
        .sum()
    )
    return cards_info_df


def top_five_operations(operations_df: pd.DataFrame) -> pd.DataFrame:
    """
    Топ-5 транзакций по сумме платежа

    Args:
        operations_df : принимает DataFrame с данными операций

    Returns:
        DataFrame: возвращает DataFrame с 5 транзакциями с максимальными суммами платежа
                     с колонками: Дата операции, Сумма платежа, Категория, Описание
    """
    # Фильтруем только нужные колонки
    filtered_df = operations_df[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]

    # Находим топ-5 по сумме платежа
    result_df = filtered_df.nlargest(5, 'Сумма платежа')

    return result_df


def get_currencies(currency_codes: list) -> dict:
    """
    Получает курсы валют к рублю.

    Args:
        currency_codes: список кодов валют

    Returns:
        dict: Словарь {код_валюты: курс} или сообщение об ошибке
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        result = {}
        for code in currency_codes:
            result[code] = data['Valute'][code]['Value']
        log.info('get_currencies: курс валют получен')
        return result

    except:
        log.warning('get_currencies: Ошибка получения данных')
        return "Ошибка получения данных"


def get_stocks(stocks: list) -> dict:
    """
    Получает стоимость акций из списка.

    Args:
        stocks: список акций

    Returns:
        dict: Словарь {код_акции: стоимость} или сообщение об ошибке
    """
    api_key = os.getenv('API_KEY')

    try:
        result = {}
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            result[stock] = float(data["Global Quote"]["05. price"])

        log.info('get_stocks: стоимость акций получена')
        return result

    except:
        log.warning('get_stocks: Ошибка получения данных')
        return "Ошибка получения данных"
