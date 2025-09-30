from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.views import generate_response, load_user_settings


class TestViews:
    """Тесты для views.py"""

    def test_load_user_settings_success(self):
        """Тест загрузки настроек пользователя"""
        with patch('builtins.open', Mock(return_value=Mock(
                __enter__=Mock(return_value=Mock(
                    read=Mock(return_value='{"user_currencies": ["USD"]}')
                )),
                __exit__=Mock()
        ))):
            result = load_user_settings()
            assert result['user_currencies'] == ['USD']

    def test_load_user_settings_default(self):
        """Тест настроек по умолчанию при отсутствии файла"""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = load_user_settings()
            assert 'user_currencies' in result
            assert 'user_stocks' in result

    @patch('src.views.read_excel')
    @patch('src.views.filter_data_by_date')
    @patch('src.views.get_cards_info')
    @patch('src.views.get_currencies')
    @patch('src.views.get_stocks')
    def test_generate_response_basic(self, mock_stocks, mock_currencies,
                                     mock_cards, mock_filter, mock_read):
        """Базовый тест генерации ответа"""
        # Создаем реальный DataFrame вместо Mock
        test_df = pd.DataFrame({
            'Дата операции': [pd.Timestamp('2021-08-01'), pd.Timestamp('2021-08-02')],
            'Сумма платежа': [-1000, -500],
            'Категория': ['Супермаркет', 'Кафе'],
            'Описание': ['Покупка', 'Обед'],
            'Номер карты': ['1234', '5678'],
            'Статус': ['OK', 'OK'],
            'Кэшбэк': [10, 5]
        })

        mock_read.return_value = test_df
        mock_filter.return_value = test_df

        mock_cards.return_value = pd.DataFrame({
            'Сумма платежа': [-1000, -500],
            'Кэшбэк': [10, 5]
        }, index=['1234567812345678', '8765432187654321'])

        mock_currencies.return_value = {'USD': 75.5}
        mock_stocks.return_value = {'AAPL': 150.0}

        result = generate_response("2021-08-14 12:12:12")

        assert 'greeting' in result
        assert len(result['cards']) == 2
        assert len(result['currency_rates']) == 1