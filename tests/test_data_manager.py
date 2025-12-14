"""
Tests for data_manager.py
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_manager import DataManager


class TestDataManager:
    """Tests for DataManager class."""
    
    def test_depot_creation(self, temp_data_dir):
        """Test depot creation and retrieval."""
        dm = DataManager(data_dir=temp_data_dir)
        
        dm.add_depot("DVI2", "Vienna Depot 2")
        dm.add_depot("MUC1", "Munich Depot 1")
        
        depots = dm.get_depots()
        assert "DVI2" in depots
        assert "MUC1" in depots
        assert len(depots) == 2
    
    def test_upload_training_data(self, temp_data_dir, sample_training_data):
        """Test uploading training data format."""
        dm = DataManager(data_dir=temp_data_dir)
        dm.add_depot("DVI2")
        
        result = dm.upload_data("DVI2", sample_training_data, "Test Week")
        
        assert result['records_uploaded'] == 100
        assert result['new_records'] == 100
        assert result['duplicates_skipped'] == 0
    
    def test_upload_weekly_data_normalization(self, temp_data_dir, sample_weekly_data):
        """Test that weekly data is normalized correctly."""
        dm = DataManager(data_dir=temp_data_dir)
        dm.add_depot("DVI2")
        
        result = dm.upload_data("DVI2", sample_weekly_data, "Week 48")
        
        # Retrieve and check normalization
        df = dm.get_depot_data("DVI2")
        
        # Check that concession_type was created from binary columns
        assert 'concession_type' in df.columns
        
        # Check that address_id was created from zip_code + pid
        assert 'address_id' in df.columns
        assert df['address_id'].notna().any()
        
        # Check pattern columns were extracted
        assert 'geo_anomaly' in df.columns or 'high_value' in df.columns
    
    def test_deduplication(self, temp_data_dir, sample_training_data):
        """Test that duplicate rows are skipped."""
        dm = DataManager(data_dir=temp_data_dir)
        dm.add_depot("DVI2")
        
        # Upload once
        dm.upload_data("DVI2", sample_training_data)
        
        # Upload again (should skip all as duplicates)
        result = dm.upload_data("DVI2", sample_training_data)
        
        assert result['new_records'] == 0
        assert result['duplicates_skipped'] == 100
    
    def test_get_depot_summary(self, temp_data_dir, sample_training_data):
        """Test depot summary generation."""
        dm = DataManager(data_dir=temp_data_dir)
        dm.add_depot("DVI2", "Vienna Depot 2")
        dm.upload_data("DVI2", sample_training_data)
        
        summary = dm.get_depot_summary("DVI2")
        
        assert summary['depot_id'] == 'DVI2'
        assert summary['name'] == 'Vienna Depot 2'
        assert summary['total_records'] == 100
        assert 'concession_rate' in summary


class TestWidFormatNormalization:
    """Tests specifically for wide-format data normalization."""
    
    def test_concession_type_from_binary(self, temp_data_dir):
        """Test concession_type is correctly derived from binary columns."""
        dm = DataManager(data_dir=temp_data_dir)
        dm.add_depot("TEST")
        
        df = pd.DataFrame({
            'transporter_id': ['DRV01', 'DRV02', 'DRV03'],
            'tracking_id': ['T1', 'T2', 'T3'],
            'delivery_date_time': pd.date_range('2024-12-01', periods=3, freq='1h'),
            'Delivered to Neighbour': [1, 0, 0],
            'Delivered to Mailslot': [0, 1, 0],
            'Delivered to Household Member / Customer': [0, 0, 0],
        })
        
        dm.upload_data("TEST", df)
        result = dm.get_depot_data("TEST")
        
        assert result.loc[0, 'concession_type'] == 'neighbor'
        assert result.loc[1, 'concession_type'] == 'mailbox'
        assert pd.isna(result.loc[2, 'concession_type']) or result.loc[2, 'concession_type'] is None
    
    def test_address_id_fallback(self, temp_data_dir):
        """Test address_id is created from zip_code + pid when missing."""
        dm = DataManager(data_dir=temp_data_dir)
        dm.add_depot("TEST")
        
        df = pd.DataFrame({
            'transporter_id': ['DRV01'],
            'tracking_id': ['T1'],
            'delivery_date_time': ['2024-12-01'],
            'zip_code': ['1010'],
            'PID': ['P0001'],
        })
        
        dm.upload_data("TEST", df)
        result = dm.get_depot_data("TEST")
        
        assert 'address_id' in result.columns
        assert result.loc[0, 'address_id'] == '1010_P0001'
