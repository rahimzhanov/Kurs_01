import pandas as pd
from logger import get_logger
from  datetime import datetime
from config import PATH_TO_OPERATIONS

log = get_logger('utils.log')

def greeting():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        log.info(f'Функция greeting вернула - Доброе утро')
        return "Доброе утро"
    elif 12 <= hour < 18:
        log.info(f'Функция greeting вернула - Добрый день')
        return 'Добрый день'
    elif 18 <= hour < 24:
        log.info(f'Функция greeting вернула - Добрый вечер')
        return 'Добрый вечер'
    else:  # 0-6 часов
        log.info(f'Функция greeting вернула - Доброй ночи')
        return 'Доброй ночи'

def read_excel(path: str) -> pd.DataFrame:
    """
      Читает Excel файл и преобразует колонку с датами.

    Args:
        path: Путь к Excel файлу

    Returns:
        pd.DataFrame: DataFrame с преобразованными датами
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

    log.info("Отфильтрованные данные от %s до %s: %s rows",
                 first_date, end_date, len(filtered_df))
    print(filtered_df)

def get_cards_info(operations_df: pd.DataFrame) -> pd.DataFrame:
    """
        Возвращает данные суммы платежа и кэшбэк по каждой карте

    :param operations_df: DataFrame полученный из read_excel()

    :return: DataFrame только с данными карты
    """
    operations_df = operations_df[operations_df['Сумма платежа'] < 0]
    cards_info_df = operations_df[['Номер карты', 'Сумма платежа', 'Кэшбэк']].groupby('Номер карты')[['Сумма платежа', 'Кэшбэк']].sum()
    return cards_info_df

if __name__ == "__main__":

    # data_df = read_excel(PATH_TO_OPERATIONS)
    # result = filter_data_by_date(data_df, "2021-08-14 12:12:12")
    # print(get_cards_info(data_df))