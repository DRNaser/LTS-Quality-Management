"""
Pytest configuration and fixtures for LTS Quality Management tests.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def sample_training_data():
    """Sample data mimicking training data format (long format with address_id)."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        'week': np.random.randint(11, 33, n),
        'tracking_id': [f'TRK{i:06d}' for i in range(n)],
        'creation_datet_ime': pd.date_range(end='2024-12-01', periods=n, freq='1h'),
        'address_id': [f'ADDR_{np.random.randint(1, 20):04d}' for _ in range(n)],
        'gross_concession_usd': np.random.uniform(0, 10, n),
        'delivery_date_time': pd.date_range(end='2024-12-01', periods=n, freq='1h'),
        'driver_id': np.random.choice(['DRV01', 'DRV02', 'DRV03'], n),
        'lt_attempt_shipment_reason': np.random.choice([None, 'neighbor', 'mailbox'], n, p=[0.8, 0.1, 0.1]),
    })


@pytest.fixture
def sample_weekly_data():
    """Sample data mimicking weekly data format (wide format with binary columns)."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        'year': [2024] * n,
        'week': [48] * n,
        'station': ['DVI2'] * n,
        'transporter_id': np.random.choice(['DRV01', 'DRV02', 'DRV03'], n),
        'tracking_id': [f'TRK{i:06d}' for i in range(n)],
        'delivery_date_time': pd.date_range(end='2024-12-03', periods=n, freq='30min'),
        'zip_code': np.random.choice(['1010', '1020', '1030'], n),
        'PID': [f'P{i:04d}' for i in range(n)],
        'Concession Cost': np.random.uniform(0, 15, n),
        'Delivered to Neighbour': np.random.choice([0, 1], n, p=[0.9, 0.1]),
        'Delivered to Household Member / Customer': np.random.choice([0, 1], n, p=[0.85, 0.15]),
        'Delivered to Mailslot': np.random.choice([0, 1], n, p=[0.95, 0.05]),
        'Geo Distance > 25m': np.random.choice([0, 1], n, p=[0.92, 0.08]),
        'High Value Item': np.random.choice([0, 1], n, p=[0.97, 0.03]),
        'contact': np.random.choice([True, False], n, p=[0.8, 0.2]),
    })


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for data storage tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
