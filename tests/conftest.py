from datetime import datetime

import pandas as pd
import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return pd.DataFrame({
        'Дата операции': [datetime(2021, 8, 1), datetime(2021, 8, 2)],
        'Сумма платежа': [-1000, -500],
        'Категория': ['Супермаркеты', 'Кафе'],
        'Описание': ['Лента', 'Starbucks'],
        'Номер карты': ['1234567812345678', '8765432187654321'],
        'Статус': ['OK', 'OK'],
        'Кэшбэк': [10, 5]
    })


@pytest.fixture
def sample_currency_data():
    """Фикстура с тестовыми курсами валют"""
    return {'USD': 75.5, 'EUR': 85.3}