import functools
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

from config import PATH_TO_OPERATIONS
from src.logger import get_logger
from src.utils import read_excel

# Загружаем данные
df = read_excel(PATH_TO_OPERATIONS)

log = get_logger('reports.log')


def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результата функции-отчёта в JSON-файл.

    Args:
        filename: имя файла. Если не указано — генерируется автоматически.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Выполняем функцию
            result = func(*args, **kwargs)

            # Определяем имя файла
            if filename:
                file_path = Path(filename)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = Path(f"report_{timestamp}.json")

            # Сохраняем результат
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                log.info(f"Отчет сохранён: {file_path}")
            except Exception as e:
                log.error(f"Ошибка при сохранении отчета '{file_path}': {e}")

            return result

        return wrapper
    return decorator


@save_report
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
                3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресеньe'}

        result['День недели'] = result['День недели'].map(days)
        result = result.rename(columns={'Траты': 'Средние траты'})

        log.info("Рассчитаны траты за 3 месяца")
        return result

    except Exception as e:
        log.error(f"Ошибка: {e}")
        return pd.DataFrame()


def spending_by_weekday_json(result_df: pd.DataFrame) -> str:
    """
    Преобразует DataFrame с тратами по дням недели в формат JSON.

    Args:
        result_df: DataFrame с результатами работы spending_by_weekday()

    Returns:
        str: JSON-строка с результатами
    """
    if result_df.empty:
        log.error('Нет данных для преобразования в JSON')
        return '{"error": "Нет данных"}'

    log.info('Данные успешно преобразованы в JSON')
    return result_df.to_json(force_ascii=False, orient='records')
