from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import spending_by_weekday


class TestReports:
    """Тесты для reports.py"""

    def test_spending_by_weekday_basic(self):
        """Базовый тест трат по дням недели"""
        # Создаем тестовые данные за 3 месяца
        test_data = pd.DataFrame({
            'Дата операции': pd.date_range('2021-05-01', periods=10, freq='D'),
            'Сумма платежа': [-100, -200, -300, -400, -500] * 2,
            'Статус': ['OK'] * 10
        })

        result = spending_by_weekday(test_data, "2021-06-14 12:12:12")

        assert not result.empty
        assert 'День недели' in result.columns
        assert 'Средние траты' in result.columns