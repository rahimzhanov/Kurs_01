import pandas as pd
from datetime import datetime
from logger import get_logger
from utils import read_excel
from config import PATH_TO_OPERATIONS

# Загружаем данные
df = read_excel(PATH_TO_OPERATIONS)

log = get_logger('reports.log')


def spending_by_weekday(transactions: pd.DataFrame, date: str = None) -> pd.DataFrame:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями
        date: опциональная дата в формате YYYY-MM-DD HH:MM:SS

    Returns:
        pd.DataFrame: средние траты по дням недели
    """
    try:
        # 1. Берем текущую дату или переданную
        if date:
            end_date = pd.to_datetime(date)
        else:
            end_date = pd.to_datetime(datetime.now())

        # 2. Вычисляем дату 3 месяца назад
        start_date = end_date - pd.DateOffset(months=3)

        # 3. Берем только траты за этот период
        # Траты - это отрицательные суммы
        mask = (transactions['Дата операции'] >= start_date) & \
               (transactions['Дата операции'] <= end_date) & \
               (transactions['Сумма платежа'] < 0)

        last_3_months = transactions[mask].copy()

        # 4. Добавляем столбец с днем недели
        last_3_months['День недели'] = last_3_months['Дата операции'].dt.dayofweek

        # 5. Делаем положительные суммы для удобства
        last_3_months['Траты'] = last_3_months['Сумма платежа'].abs()

        # 6. Группируем по дню недели и считаем среднее
        result = last_3_months.groupby('День недели')['Траты'].mean().round(2).reset_index()

        # 7. Переименовываем дни недели
        days = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда',
                3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}

        result['День недели'] = result['День недели'].map(days)
        result = result.rename(columns={'Траты': 'Средние траты'})

        log.info(f"Рассчитаны траты за 3 месяца")
        return result

    except Exception as e:
        log.error(f"Ошибка: {e}")
        return pd.DataFrame()



def spending_by_weekday_json(transactions: pd.DataFrame, date: str = None) -> str:
    """
    Возвращает средние траты по дням недели в формате JSON.

    Args:
        transactions: DataFrame с транзакциями
        date: опциональная дата в формате YYYY-MM-DD HH:MM:SS

    Returns:
        str: JSON-строка с результатами
    """
    result_df = spending_by_weekday(transactions, date)

    if result_df.empty:
        return '{"error": "Нет данных"}'


    return result_df.to_json(force_ascii=False, orient='records')


# Пример использования
if __name__ == "__main__":


    # Простой тест
    result = spending_by_weekday(df, "2021-08-14 12:12:12")
    print("Средние траты по дням недели:")
    print(result)