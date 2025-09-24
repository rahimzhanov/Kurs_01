import pytest
from unittest.mock import patch, Mock
from src.utils import greeting, get_currencies, get_stocks
from datetime import datetime


class TestUtils:
    """Тесты для utils.py"""

    @patch('src.utils.datetime')
    def test_greeting_morning(self, mock_datetime):
        """Тест приветствия для утра"""
        mock_datetime.now.return_value.hour = 8
        assert greeting() == "Доброе утро"

    @patch('src.utils.datetime')
    def test_greeting_evening(self, mock_datetime):
        """Тест приветствия для вечера"""
        mock_datetime.now.return_value.hour = 20
        assert greeting() == "Добрый вечер"

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

    @patch('src.utils.requests.get')
    def test_get_currencies_error(self, mock_get):
        """Тест ошибки получения курсов"""
        mock_get.side_effect = Exception("API error")
        result = get_currencies(['USD'])
        assert result == "Ошибка получения данных"