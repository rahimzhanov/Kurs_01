import json
from config import PATH_TO_OPERATIONS
from src.utils import read_excel
from src.logger import get_logger

# Инициализация логгера
log = get_logger('services.log')


def search_transactions(search_query: str) -> list:
    """
    Ищет транзакции по заданной строке в описании или категории.

    Args:
        search_query: строка для поиска

    Returns:
        list: список найденных транзакций или пустой список
    """
    try:
        # Читаем данные из Excel
        operations_df = read_excel(PATH_TO_OPERATIONS)

        # Проверяем, что запрос не пустой
        if not search_query or not search_query.strip():
            log.warning("Получен пустой поисковый запрос")
            return []

        # Приводим поисковый запрос к нижнему регистру
        search_lower = search_query.lower().strip()

        # Фильтруем транзакции по поисковому запросу
        mask = (
            operations_df['Описание'].str.lower().str.contains(search_lower, na=False) |
            operations_df['Категория'].str.lower().str.contains(search_lower, na=False)
        )

        found_transactions = operations_df[mask]

        # Если ничего не найдено
        if found_transactions.empty:
            log.info(f"Поиск '{search_query}': транзакций не найдено")
            return []

        # Преобразуем в нужный формат JSON
        result = []
        for _, transaction in found_transactions.iterrows():
            result.append({
                "date": transaction['Дата операции'].strftime("%d.%m.%Y"),
                "amount": float(transaction['Сумма платежа']),
                "category": transaction['Категория'],
                "description": transaction['Описание'],
                "card_number": str(transaction['Номер карты']),
                "status": transaction['Статус']
            })

        log.info(f"Поиск '{search_query}': найдено {len(result)} транзакций")
        return result

    except Exception as e:
        log.error(f"Ошибка при поиске '{search_query}': {str(e)}")
        return []


def search_transactions_json(search_query: str) -> str:
    """
    Ищет транзакции и возвращает результат в формате JSON строки.

    Args:
        search_query: строка для поиска

    Returns:
        str: JSON-строка с результатами поиска
    """
    transactions = search_transactions(search_query)

    # Добавляем информацию о результате поиска
    response = {
        "search_query": search_query,
        "found_count": len(transactions),
        "search_results": transactions
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


# Пример использования
if __name__ == "__main__":
    # Тестируем разные сценарии
    test_queries = ["Лента", "Несуществующее Слово", ""]

    for query in test_queries:
        print(f"\nПоиск: '{query}'")
        result = search_transactions_json(query)
        print(result)
