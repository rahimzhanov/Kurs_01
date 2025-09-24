import pytest
from unittest.mock import patch, Mock
from src.services import search_transactions
import pandas as pd


class TestServices:
    """Тесты для services.py"""

    @patch('src.services.read_excel')
    def test_search_transactions_found(self, mock_read):
        """Тест успешного поиска транзакций"""
        # Создаем тестовые данные
        test_data = pd.DataFrame({
            'Описание': ['Покупка в Лента', 'Кафе', 'Лента супермаркет'],
            'Категория': ['Супермаркеты', 'Кафе', 'Супермаркеты'],
            'Дата операции': [pd.Timestamp('2021-08-01')] * 3,
            'Сумма платежа': [-100, -200, -300],
            'Номер карты': ['1234'] * 3,
            'Статус': ['OK'] * 3
        })

        mock_read.return_value = test_data

        result = search_transactions('Лента')
        assert len(result) == 2
        # Исправляем проверку - ищем частичное совпадение
        assert all('лента' in t['description'].lower() or 'лента' in t['category'].lower() for t in result)

    @patch('src.services.read_excel')
    def test_search_transactions_empty_query(self, mock_read):
        """Тест пустого запроса"""
        result = search_transactions('')
        assert result == []