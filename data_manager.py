"""
Data Management Module
Handles multi-depot data storage, weekly uploads, and data persistence.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import os
import hashlib


class DataManager:
    """
    Manages delivery data across multiple depots with persistent storage.
    
    Features:
    - Multi-depot data organization
    - Incremental data uploads (append new data weekly)
    - Data deduplication
    - Historical data retention
    - Export/backup functionality
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create depot directories
        self.depots_dir = self.data_dir / "depots"
        self.depots_dir.mkdir(exist_ok=True)
        
        # Metadata file
        self.metadata_file = self.data_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load or initialize metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            "depots": {},
            "last_updated": None,
            "total_records": 0
        }
    
    def _save_metadata(self):
        """Save metadata to disk"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)
    
    def get_depots(self) -> List[str]:
        """Get list of all registered depots"""
        return list(self.metadata.get("depots", {}).keys())
    
    def add_depot(self, depot_id: str, depot_name: str = None):
        """Register a new depot"""
        if depot_id not in self.metadata["depots"]:
            depot_dir = self.depots_dir / depot_id
            depot_dir.mkdir(exist_ok=True)
            
            self.metadata["depots"][depot_id] = {
                "name": depot_name or depot_id,
                "created": datetime.now().isoformat(),
                "record_count": 0,
                "date_range": {"start": None, "end": None},
                "uploads": []
            }
            self._save_metadata()
    
    def upload_data(self, 
                    depot_id: str, 
                    df: pd.DataFrame,
                    upload_label: str = None) -> Dict[str, Any]:
        """
        Upload data for a depot (appends to existing data).
        
        Args:
            depot_id: Depot identifier
            df: DataFrame with delivery data
            upload_label: Optional label for this upload (e.g., "Week 50 2024")
            
        Returns:
            Upload summary with stats
        """
        # Ensure depot exists
        if depot_id not in self.metadata["depots"]:
            self.add_depot(depot_id)
        
        depot_dir = self.depots_dir / depot_id
        
        # Standardize column names
        df = self._standardize_columns(df)
        
        # Add metadata columns
        df['_depot_id'] = depot_id
        df['_upload_date'] = datetime.now().isoformat()
        df['_upload_label'] = upload_label or f"Upload {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Create unique row ID for deduplication
        df['_row_hash'] = df.apply(self._create_row_hash, axis=1)
        
        # Load existing data
        existing_df = self.get_depot_data(depot_id)
        
        # Deduplicate
        if not existing_df.empty and '_row_hash' in existing_df.columns:
            existing_hashes = set(existing_df['_row_hash'])
            new_records = df[~df['_row_hash'].isin(existing_hashes)]
            duplicates = len(df) - len(new_records)
        else:
            new_records = df
            duplicates = 0
        
        # Combine data
        if existing_df.empty:
            combined = new_records
        else:
            combined = pd.concat([existing_df, new_records], ignore_index=True)
        
        # Save to parquet (efficient storage)
        data_file = depot_dir / "deliveries.parquet"
        combined.to_parquet(data_file, index=False)
        
        # Update metadata
        self.metadata["depots"][depot_id]["record_count"] = len(combined)
        
        if 'delivery_date_time' in combined.columns:
            dates = pd.to_datetime(combined['delivery_date_time'], errors='coerce')
            self.metadata["depots"][depot_id]["date_range"] = {
                "start": dates.min().isoformat() if pd.notna(dates.min()) else None,
                "end": dates.max().isoformat() if pd.notna(dates.max()) else None
            }
        
        upload_info = {
            "date": datetime.now().isoformat(),
            "label": upload_label,
            "records_uploaded": len(df),
            "new_records": len(new_records),
            "duplicates_skipped": duplicates
        }
        self.metadata["depots"][depot_id]["uploads"].append(upload_info)
        self.metadata["total_records"] = sum(
            d.get("record_count", 0) for d in self.metadata["depots"].values()
        )
        self._save_metadata()
        
        return upload_info
    
    def get_depot_data(self, depot_id: str) -> pd.DataFrame:
        """Get all data for a specific depot"""
        data_file = self.depots_dir / depot_id / "deliveries.parquet"
        
        if data_file.exists():
            return pd.read_parquet(data_file)
        return pd.DataFrame()
    
    def get_all_data(self, depots: List[str] = None) -> pd.DataFrame:
        """
        Get combined data from multiple depots.
        
        Args:
            depots: List of depot IDs (None = all depots)
        """
        if depots is None:
            depots = self.get_depots()
        
        dfs = []
        for depot_id in depots:
            df = self.get_depot_data(depot_id)
            if not df.empty:
                dfs.append(df)
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()
    
    def get_depot_summary(self, depot_id: str) -> Dict[str, Any]:
        """Get summary statistics for a depot"""
        if depot_id not in self.metadata["depots"]:
            return {}
        
        depot_meta = self.metadata["depots"][depot_id]
        df = self.get_depot_data(depot_id)
        
        summary = {
            "depot_id": depot_id,
            "name": depot_meta.get("name", depot_id),
            "total_records": depot_meta.get("record_count", 0),
            "date_range": depot_meta.get("date_range", {}),
            "upload_count": len(depot_meta.get("uploads", [])),
            "last_upload": depot_meta.get("uploads", [{}])[-1] if depot_meta.get("uploads") else None,
        }
        
        if not df.empty:
            summary["transporter_count"] = df['transporter_id'].nunique() if 'transporter_id' in df.columns else 0
            summary["concession_rate"] = (
                df['concession_type'].notna().sum() / len(df) * 100
            ) if 'concession_type' in df.columns else 0
        
        return summary
    
    def delete_depot_data(self, depot_id: str, confirm: bool = False):
        """Delete all data for a depot"""
        if not confirm:
            raise ValueError("Must set confirm=True to delete data")
        
        if depot_id in self.metadata["depots"]:
            depot_dir = self.depots_dir / depot_id
            data_file = depot_dir / "deliveries.parquet"
            if data_file.exists():
                data_file.unlink()
            
            del self.metadata["depots"][depot_id]
            self._save_metadata()
    
    def export_depot(self, depot_id: str, format: str = "csv") -> bytes:
        """Export depot data to specified format"""
        df = self.get_depot_data(depot_id)
        
        if format == "csv":
            return df.to_csv(index=False).encode()
        elif format == "xlsx":
            import io
            output = io.BytesIO()
            df.to_excel(output, index=False)
            return output.getvalue()
        elif format == "parquet":
            import io
            output = io.BytesIO()
            df.to_parquet(output, index=False)
            return output.getvalue()
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names"""
        df = df.copy()
        
        # Lowercase column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Common column mappings
        mappings = {
            # Transporter/Driver identification (internal: transporter_id)
            'driver': 'transporter_id',
            'driver_id': 'transporter_id',
            'driverid': 'transporter_id',
            'driver_name': 'transporter_id',
            'fahrer': 'transporter_id',
            'fahrer_id': 'transporter_id',
            'transporter': 'transporter_id',
            
            # Tracking/Package identification
            'tracking': 'tracking_id',
            'trackingid': 'tracking_id',
            'tracking_number': 'tracking_id',
            'package_id': 'tracking_id',
            'shipment_id': 'tracking_id',
            'sendungsnummer': 'tracking_id',
            
            # Address identification (for customer abuse detection)
            'address': 'address_id',
            'addressid': 'address_id',
            'address_hash': 'address_id',
            'customer_id': 'address_id',
            'recipient_id': 'address_id',
            'empfänger_id': 'address_id',
            'adresse_id': 'address_id',
            
            # Date/time
            'date': 'delivery_date_time',
            'datetime': 'delivery_date_time',
            'delivery_date': 'delivery_date_time',
            'dnr_date': 'delivery_date_time',
            'zustelldatum': 'delivery_date_time',
            'lieferdatum': 'delivery_date_time',
            
            # Concession info
            'concession': 'concession_type',
            'type': 'concession_type',
            'dnr_type': 'concession_type',
            'concession_reason': 'concession_type',
            'grund': 'concession_type',
            
            # Cost
            'cost': 'concession_cost',
            'kosten': 'concession_cost',
            
            # Contact
            'contact': 'contact_made',
            'kontakt': 'contact_made',
        }
        
        for old, new in mappings.items():
            if old in df.columns and new not in df.columns:
                df = df.rename(columns={old: new})
        
        # Parse dates
        if 'delivery_date_time' in df.columns:
            df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
        
        return df
    
    def _normalize_weekly_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize wide-format weekly data (e.g., dvi2 week 48.xlsx) to standard format.
        
        Wide-format has binary columns like 'Delivered to Neighbour' instead of 'concession_type'.
        This method:
        1. Maps binary concession columns to a single 'concession_type' column.
        2. Creates a fallback 'address_id' from 'zip_code' + 'pid' if missing.
        3. Extracts additional pattern-recognition features.
        """
        df = df.copy()
        
        # Lowercase columns for matching
        df.columns = df.columns.str.lower().str.strip()
        
        # Define wide-format concession columns -> concession_type values
        concession_col_map = {
            'delivered to neighbour': 'neighbor',
            'delivered to household member / customer': 'household_member',
            'delivered to mailslot': 'mailbox',
            'delivered to receptionist': 'receptionist',
            'delivery preferences not followed': 'prefs_not_followed',
            'unattended delivery & no photo on delivery': 'unattended_no_photo',
            'mailbox eligible, delivered elsewhere': 'mailbox_eligible_elsewhere',
        }
        
        # Check if this is wide-format data (has binary concession columns)
        matched_cols = [c for c in concession_col_map.keys() if c in df.columns]
        
        if matched_cols and 'concession_type' not in df.columns:
            # This is wide-format data - need to normalize
            
            # Determine concession_type from binary columns (first match wins, priority order)
            def determine_concession_type(row):
                for col, ctype in concession_col_map.items():
                    if col in row.index and row.get(col) in [1, '1', True, 'Yes', 'yes', 'TRUE']:
                        return ctype
                return None
            
            df['concession_type'] = df.apply(determine_concession_type, axis=1)
            
            # Map 'concession cost' column
            if 'concession cost' in df.columns:
                df['concession_cost'] = pd.to_numeric(df['concession cost'], errors='coerce')
        
        # Handle missing address_id - create fallback from zip_code + pid
        if 'address_id' not in df.columns or df['address_id'].isna().all():
            if 'zip_code' in df.columns and 'pid' in df.columns:
                df['address_id'] = df['zip_code'].astype(str) + '_' + df['pid'].astype(str)
            elif 'zip_code' in df.columns:
                df['address_id'] = df['zip_code'].astype(str)
            # else: leave address_id missing, abuse detection will fallback to tracking_id
        
        # Extract additional pattern-recognition features from wide-format
        pattern_cols = {
            'geo distance > 25m': 'geo_anomaly',
            'simultaneous group stops': 'group_stop',
            'multiple concessions reasons': 'multi_concession',
            'no photo on delivery': 'no_photo',
            'photo on delivery': 'has_photo',
            'high value item': 'high_value',
            'signature on delivery': 'has_signature',
            'delivered using otp': 'otp_delivery',
            'successful contact opportunity': 'contact_success',
            'unsuccessful contact opportunity': 'contact_fail',
        }
        
        for old_col, new_col in pattern_cols.items():
            if old_col in df.columns and new_col not in df.columns:
                df[new_col] = df[old_col].apply(
                    lambda x: True if x in [1, '1', True, 'Yes', 'yes', 'TRUE'] else False
                )
        
        return df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names"""
        df = df.copy()
        
        # First, normalize wide-format weekly data if detected
        df = self._normalize_weekly_data(df)
        
        # Lowercase column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Common column mappings
        mappings = {
            # Transporter/Driver identification (internal: transporter_id)
            'driver': 'transporter_id',
            'driver_id': 'transporter_id',
            'driverid': 'transporter_id',
            'driver_name': 'transporter_id',
            'fahrer': 'transporter_id',
            'fahrer_id': 'transporter_id',
            'transporter': 'transporter_id',
            
            # Tracking/Package identification
            'tracking': 'tracking_id',
            'trackingid': 'tracking_id',
            'tracking_number': 'tracking_id',
            'package_id': 'tracking_id',
            'shipment_id': 'tracking_id',
            'sendungsnummer': 'tracking_id',
            
            # Address identification (for customer abuse detection)
            'address': 'address_id',
            'addressid': 'address_id',
            'address_hash': 'address_id',
            'customer_id': 'address_id',
            'recipient_id': 'address_id',
            'empfänger_id': 'address_id',
            'adresse_id': 'address_id',
            
            # Date/time
            'date': 'delivery_date_time',
            'datetime': 'delivery_date_time',
            'delivery_date': 'delivery_date_time',
            'dnr_date': 'delivery_date_time',
            'zustelldatum': 'delivery_date_time',
            'lieferdatum': 'delivery_date_time',
            
            # Concession info
            'concession': 'concession_type',
            'type': 'concession_type',
            'dnr_type': 'concession_type',
            'concession_reason': 'concession_type',
            'grund': 'concession_type',
            'shipment_reason': 'concession_type',  # Added for weekly data
            
            # Cost
            'cost': 'concession_cost',
            'kosten': 'concession_cost',
            
            # Contact
            'contact': 'contact_made',
            'kontakt': 'contact_made',
        }
        
        for old, new in mappings.items():
            if old in df.columns and new not in df.columns:
                df = df.rename(columns={old: new})
        
        # Parse dates
        if 'delivery_date_time' in df.columns:
            df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
        
        return df
    
    def _create_row_hash(self, row) -> str:
        """Create unique hash for a row (for deduplication)"""
        # Use key columns for uniqueness
        key_cols = ['transporter_id', 'delivery_date_time', 'tracking_id']
        available_cols = [c for c in key_cols if c in row.index and pd.notna(row.get(c))]
        
        if not available_cols:
            # Use all columns if no key columns
            values = str(row.values)
        else:
            values = str([row.get(c) for c in available_cols])
        
        return hashlib.md5(values.encode()).hexdigest()


# =============================================================================
# STREAMLIT UI COMPONENTS FOR DATA MANAGEMENT
# =============================================================================

def render_data_management_sidebar(data_manager: DataManager):
    """Render sidebar components for data management - Redesigned for better UX"""
    import streamlit as st
    
    st.sidebar.markdown("### 🏭 Depots")
    
    # Show existing depots
    depots = data_manager.get_depots()
    
    if depots:
        # Always visible depot list with stats
        for depot_id in depots:
            summary = data_manager.get_depot_summary(depot_id)
            depot_name = summary.get('name', depot_id)
            records = summary.get('total_records', 0)
            rate = summary.get('concession_rate', 0)
            
            # Depot card - always visible
            st.sidebar.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                border-left: 4px solid #0D47A1;
                border-radius: 8px;
                padding: 0.75rem;
                margin-bottom: 0.5rem;
            ">
                <div style="font-weight: 600; color: #0D47A1; font-size: 0.95rem;">
                    📦 {depot_name}
                </div>
                <div style="font-size: 0.8rem; color: #4A5568; margin-top: 0.25rem;">
                    <span style="margin-right: 1rem;">📊 {records:,} Datensätze</span>
                    <span>📈 {rate:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.sidebar.divider()
        
        # Depot Management Section (Edit/Delete)
        st.sidebar.markdown("**⚙️ Depot verwalten**")
        
        # Select depot to manage
        manage_depot = st.sidebar.selectbox(
            "Depot auswählen",
            options=depots,
            format_func=lambda x: f"{x} - {data_manager.metadata['depots'][x].get('name', x)}",
            key="manage_depot_select",
            label_visibility="collapsed"
        )
        
        if manage_depot:
            col1, col2 = st.sidebar.columns(2)
            
            # Edit/Rename
            with col1:
                if st.button("✏️ Umbenennen", key=f"edit_{manage_depot}", use_container_width=True):
                    st.session_state[f'editing_{manage_depot}'] = True
            
            # Delete
            with col2:
                if st.button("🗑️ Löschen", key=f"delete_{manage_depot}", use_container_width=True):
                    st.session_state[f'deleting_{manage_depot}'] = True
            
            # Edit form
            if st.session_state.get(f'editing_{manage_depot}', False):
                new_name = st.sidebar.text_input(
                    "Neuer Name",
                    value=data_manager.metadata['depots'][manage_depot].get('name', manage_depot),
                    key=f"new_name_{manage_depot}"
                )
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    if st.button("💾 Speichern", key=f"save_{manage_depot}"):
                        data_manager.metadata['depots'][manage_depot]['name'] = new_name
                        data_manager._save_metadata()
                        st.session_state[f'editing_{manage_depot}'] = False
                        st.rerun()
                with col2:
                    if st.button("❌ Abbrechen", key=f"cancel_edit_{manage_depot}"):
                        st.session_state[f'editing_{manage_depot}'] = False
                        st.rerun()
            
            # Delete confirmation
            if st.session_state.get(f'deleting_{manage_depot}', False):
                st.sidebar.warning(f"⚠️ Depot '{manage_depot}' wirklich löschen?")
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    if st.button("✅ Ja, löschen", key=f"confirm_delete_{manage_depot}"):
                        data_manager.delete_depot_data(manage_depot, confirm=True)
                        st.session_state[f'deleting_{manage_depot}'] = False
                        st.rerun()
                with col2:
                    if st.button("❌ Nein", key=f"cancel_delete_{manage_depot}"):
                        st.session_state[f'deleting_{manage_depot}'] = False
                        st.rerun()
    else:
        st.sidebar.info("📭 Keine Depots vorhanden")
    
    st.sidebar.divider()
    
    # Add new depot - Compact form
    st.sidebar.markdown("**➕ Neues Depot**")
    
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        new_depot_id = st.text_input("ID", placeholder="z.B. DVI2", key="new_depot_id", label_visibility="collapsed")
    with col2:
        new_depot_name = st.text_input("Name", placeholder="z.B. Wien 2", key="new_depot_name", label_visibility="collapsed")
    
    if st.sidebar.button("➕ Depot erstellen", use_container_width=True):
        if new_depot_id:
            data_manager.add_depot(new_depot_id.strip().upper(), new_depot_name or None)
            st.sidebar.success(f"✅ {new_depot_id} erstellt!")
            st.rerun()
        else:
            st.sidebar.warning("Bitte ID eingeben")
    
    return depots


def render_data_upload_tab(data_manager: DataManager):
    """Render the data upload tab"""
    import streamlit as st
    
    st.header("📤 Data Upload")
    st.markdown("*Upload raw delivery data for your depots. New data is appended automatically.*")
    
    depots = data_manager.get_depots()
    
    if not depots:
        st.warning("⚠️ No depots registered. Add a depot in the sidebar first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Select depot
        selected_depot = st.selectbox(
            "Select Depot",
            options=depots,
            format_func=lambda x: f"{x} - {data_manager.metadata['depots'][x].get('name', x)}"
        )
        
        # Upload label
        upload_label = st.text_input(
            "Upload Label (optional)",
            placeholder=f"e.g., Week {datetime.now().isocalendar()[1]} 2024"
        )
    
    with col2:
        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your raw delivery/concession data"
        )
    
    if uploaded_file is not None:
        # Preview data
        st.subheader("📋 Data Preview")
        
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.write(f"**Rows:** {len(df):,} | **Columns:** {len(df.columns)}")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column mapping check
            st.subheader("🔍 Column Detection")
            
            expected_cols = ['transporter_id', 'delivery_date_time', 'concession_type', 'tracking_id']
            df_cols_lower = [c.lower().strip() for c in df.columns]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Expected Columns:**")
                for col in expected_cols:
                    if col in df_cols_lower or any(col in c for c in df_cols_lower):
                        st.markdown(f"✅ {col}")
                    else:
                        st.markdown(f"⚠️ {col} (may be mapped automatically)")
            
            with col2:
                st.markdown("**Your Columns:**")
                st.write(", ".join(df.columns[:10]))
                if len(df.columns) > 10:
                    st.write(f"... and {len(df.columns) - 10} more")
            
            # Upload button
            st.divider()
            
            if st.button("📤 Upload Data to Depot", type="primary"):
                with st.spinner("Uploading and processing data..."):
                    # Reset file pointer
                    uploaded_file.seek(0)
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    result = data_manager.upload_data(
                        depot_id=selected_depot,
                        df=df,
                        upload_label=upload_label or None
                    )
                
                st.success(f"""
                ✅ **Upload Complete!**
                - Records uploaded: {result['records_uploaded']:,}
                - New records added: {result['new_records']:,}
                - Duplicates skipped: {result['duplicates_skipped']:,}
                """)
                
                st.balloons()
                
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    # Upload history
    st.divider()
    st.subheader("📜 Upload History")
    
    all_uploads = []
    for depot_id in depots:
        depot_meta = data_manager.metadata["depots"].get(depot_id, {})
        for upload in depot_meta.get("uploads", []):
            all_uploads.append({
                "Depot": depot_id,
                "Date": upload.get("date", "")[:16],
                "Label": upload.get("label", ""),
                "Records": upload.get("records_uploaded", 0),
                "New": upload.get("new_records", 0)
            })
    
    if all_uploads:
        uploads_df = pd.DataFrame(all_uploads)
        uploads_df = uploads_df.sort_values("Date", ascending=False)
        st.dataframe(uploads_df, use_container_width=True, hide_index=True)
    else:
        st.info("No uploads yet. Upload data above to get started.")


def render_depot_comparison(data_manager: DataManager, features_df: pd.DataFrame):
    """Render depot comparison view"""
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    
    st.subheader("🏭 Depot Comparison")
    
    depots = data_manager.get_depots()
    
    if len(depots) < 2:
        st.info("Add at least 2 depots to see comparisons.")
        return
    
    # Get combined data
    all_data = data_manager.get_all_data()
    
    if all_data.empty:
        st.warning("No data uploaded yet.")
        return
    
    # Summary by depot
    depot_stats = all_data.groupby('_depot_id').agg({
        'driver_id': 'nunique',
        'concession_type': lambda x: x.notna().sum(),
        '_depot_id': 'count'
    }).reset_index()
    depot_stats.columns = ['Depot', 'Drivers', 'Concessions', 'Total Deliveries']
    depot_stats['Concession Rate'] = (depot_stats['Concessions'] / depot_stats['Total Deliveries'] * 100).round(2)
    
    # Display metrics
    cols = st.columns(len(depots))
    for i, depot_id in enumerate(depots):
        stats = depot_stats[depot_stats['Depot'] == depot_id]
        if not stats.empty:
            with cols[i]:
                st.metric(
                    f"📦 {depot_id}",
                    f"{stats['Concession Rate'].values[0]:.1f}%",
                    help=f"Deliveries: {stats['Total Deliveries'].values[0]:,}"
                )
                st.caption(f"{stats['Drivers'].values[0]} drivers | {stats['Total Deliveries'].values[0]:,} deliveries")
    
    # Comparison chart
    fig = px.bar(
        depot_stats,
        x='Depot',
        y='Concession Rate',
        color='Depot',
        title="Concession Rate by Depot",
        text='Concession Rate'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend comparison
    st.subheader("📈 Weekly Trends by Depot")
    
    all_data['week'] = pd.to_datetime(all_data['delivery_date_time']).dt.isocalendar().week
    all_data['year'] = pd.to_datetime(all_data['delivery_date_time']).dt.year
    all_data['year_week'] = all_data['year'].astype(str) + '-W' + all_data['week'].astype(str).str.zfill(2)
    
    weekly = all_data.groupby(['_depot_id', 'year_week']).agg({
        'concession_type': lambda x: x.notna().sum(),
        'driver_id': 'count'
    }).reset_index()
    weekly.columns = ['Depot', 'Week', 'Concessions', 'Deliveries']
    weekly['Rate'] = weekly['Concessions'] / weekly['Deliveries'] * 100
    
    fig = px.line(
        weekly,
        x='Week',
        y='Rate',
        color='Depot',
        markers=True,
        title="Weekly Concession Rate Trend"
    )
    fig.update_layout(xaxis_title="Week", yaxis_title="Concession Rate (%)")
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    # Test the data manager
    dm = DataManager(data_dir="test_data")
    
    # Add depots
    dm.add_depot("DVI2", "Vienna Depot 2")
    dm.add_depot("MUC1", "Munich Depot 1")
    dm.add_depot("FRA3", "Frankfurt Depot 3")
    
    print("Depots:", dm.get_depots())
    
    # Create sample data
    np.random.seed(42)
    sample = pd.DataFrame({
        'transporter_id': np.random.choice(['DRV001', 'DRV002', 'DRV003'], 100),
        'delivery_date_time': pd.date_range(end='2024-12-13', periods=100, freq='1h'),
        'tracking_id': [f'TRK{i}' for i in range(100)],
        'concession_type': np.random.choice([None, 'neighbor', 'safe_location'], 100, p=[0.9, 0.05, 0.05])
    })
    
    # Upload data
    result = dm.upload_data("DVI2", sample, "Test Week 50")
    print("Upload result:", result)
    
    # Get summary
    print("Depot summary:", dm.get_depot_summary("DVI2"))
