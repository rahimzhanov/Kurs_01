# tests/test_utils.py

from unittest.mock import Mock, patch

import pytest

from src.utils import get_currencies, get_stocks, greeting


class TestUtils:
    """Тесты для utils.py"""

    @pytest.mark.parametrize("hour,expected", [
        (6, "Доброе утро"),
        (8, "Доброе утро"),
        (12, "Добрый день"),
        (15, "Добрый день"),
        (18, "Добрый вечер"),
        (21, "Добрый вечер"),
        (0, "Доброй ночи"),
        (5, "Доброй ночи"),
    ])
    @patch('src.utils.datetime')
    def test_greeting_parametrized(self, mock_datetime, hour, expected):
        """Параметризованный тест приветствия"""
        mock_datetime.now.return_value.hour = hour
        assert greeting() == expected

    @patch('src.utils.requests.get')
    def test_get_currencies_success(self, mock_get):
        """Тест получения курсов валют"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'Valute': {'USD': {'Value': 75.5}, 'EUR': {'Value': 85.3}}
        }
        mock_get.return_value = mock_response

        result = get_currencies(['USD', 'EUR'])
        assert result == {'USD': 75.5, 'EUR': 85.3}

    @pytest.mark.parametrize("api_side_effect,expected", [
        (Exception("Network error"), "Ошибка получения данных"),
        (Mock(json=Mock(side_effect=ValueError)), "Ошибка получения данных"),
    ])
    @patch('src.utils.requests.get')
    def test_get_currencies_error_cases(self, mock_get, api_side_effect, expected):
        """Параметризованный тест ошибок"""
        mock_get.side_effect = api_side_effect
        result = get_currencies(['USD'])
        assert result == expected

# import pytest
# from unittest.mock import patch, Mock
# from src.utils import greeting, get_currencies, get_stocks
# from datetime import datetime
#
#
# class TestUtils:
#     """Тесты для utils.py"""
#
#     @patch('src.utils.datetime')
#     def test_greeting_morning(self, mock_datetime):
#         """Тест приветствия для утра"""
#         mock_datetime.now.return_value.hour = 8
#         assert greeting() == "Доброе утро"
#
#     @patch('src.utils.datetime')
#     def test_greeting_evening(self, mock_datetime):
#         """Тест приветствия для вечера"""
#         mock_datetime.now.return_value.hour = 20
#         assert greeting() == "Добрый вечер"
#
#     @patch('src.utils.requests.get')
#     def test_get_currencies_success(self, mock_get):
#         """Тест получения курсов валют"""
#         mock_response = Mock()
#         mock_response.json.return_value = {
#             'Valute': {'USD': {'Value': 75.5}, 'EUR': {'Value': 85.3}}
#         }
#         mock_get.return_value = mock_response
#
#         result = get_currencies(['USD', 'EUR'])
#         assert result == {'USD': 75.5, 'EUR': 85.3}
#
#     @patch('src.utils.requests.get')
#     def test_get_currencies_error(self, mock_get):
#         """Тест ошибки получения курсов"""
#         mock_get.side_effect = Exception("API error")
#         result = get_currencies(['USD'])
#         assert result == "Ошибка получения данных"