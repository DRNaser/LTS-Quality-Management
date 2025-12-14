"""
Customer Abuse Detection Module
Detects patterns of potential customer abuse - addresses/customers repeatedly triggering concessions.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict

import sys
sys.path.append('..')
from config import column_config


@dataclass
class AbusePattern:
    """Container for detected abuse patterns"""
    pattern_id: str
    address_id: Optional[str]
    pattern_type: str              # "repeat_concession", "high_frequency", "multi_driver", "time_pattern"
    severity: str                  # "critical", "high", "medium", "low"
    confidence: float              # 0-1 confidence score
    description: str
    concession_count: int
    unique_incidents: int
    drivers_involved: List[str]
    date_range: Tuple[datetime, datetime]
    details: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class AddressProfile:
    """Profile of an address/customer location"""
    address_id: str
    total_deliveries: int
    total_concessions: int
    concession_rate: float
    unique_drivers: int
    concession_types: Dict[str, int]
    first_seen: datetime
    last_seen: datetime
    is_suspicious: bool
    abuse_score: float             # 0-100 abuse likelihood
    patterns: List[str]


class CustomerAbuseDetector:
    """
    Detects potential customer abuse patterns in delivery data.
    
    Abuse Indicators:
    1. Same address with repeated concessions across multiple drivers
    2. Unusually high concession rate at specific addresses
    3. Concentrated concession times (suggesting planned absence)
    4. Pattern of specific concession types (e.g., always "not home")
    5. Tracking IDs from same address with high concession frequency
    
    Note: address_id may not always be available due to privacy.
    When missing, uses tracking_id patterns and postal_code as fallback.
    """
    
    def __init__(self):
        self.column_config = column_config
        
        # Thresholds for abuse detection
        self.min_deliveries_for_analysis = 3
        self.high_concession_threshold = 0.30      # 30%+ concession rate
        self.critical_concession_threshold = 0.50  # 50%+ concession rate
        self.multi_driver_threshold = 2            # Same address, 2+ drivers with concessions
        self.repeat_window_days = 30               # Look for repeats within 30 days
    
    def analyze(self, 
                df: pd.DataFrame,
                include_address_analysis: bool = True) -> Dict[str, Any]:
        """
        Run full abuse detection analysis.
        
        Args:
            df: Delivery data with tracking_id, address_id (optional), concession_type
            include_address_analysis: Whether to analyze address patterns
            
        Returns:
            Dictionary with abuse patterns, suspicious addresses, and summary
        """
        df = self._prepare_data(df)
        
        results = {
            "patterns": [],
            "suspicious_addresses": [],
            "address_profiles": {},
            "summary": {},
            "has_address_data": 'address_id' in df.columns and df['address_id'].notna().any()
        }
        
        # Analyze by address if available
        if include_address_analysis and results["has_address_data"]:
            address_results = self._analyze_addresses(df)
            results["patterns"].extend(address_results["patterns"])
            results["suspicious_addresses"] = address_results["suspicious"]
            results["address_profiles"] = address_results["profiles"]
        
        # Analyze by tracking ID patterns (always available)
        tracking_results = self._analyze_tracking_patterns(df)
        results["patterns"].extend(tracking_results["patterns"])
        
        # Analyze time patterns for potential abuse
        time_results = self._analyze_time_patterns(df)
        results["patterns"].extend(time_results)
        
        # Generate summary
        results["summary"] = self._generate_summary(results, df)
        
        # Sort patterns by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        results["patterns"].sort(key=lambda x: (severity_order.get(x.severity, 4), -x.confidence))
        
        return results
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for analysis"""
        df = df.copy()
        
        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Ensure required columns
        if 'tracking_id' not in df.columns:
            df['tracking_id'] = range(len(df))  # Fallback
        
        # Parse dates
        if 'delivery_date_time' in df.columns:
            df['delivery_date_time'] = pd.to_datetime(df['delivery_date_time'], errors='coerce')
            df['date'] = df['delivery_date_time'].dt.date
            df['hour'] = df['delivery_date_time'].dt.hour
            df['dayofweek'] = df['delivery_date_time'].dt.dayofweek
        
        # Flag concessions
        if 'concession_type' in df.columns:
            df['is_concession'] = df['concession_type'].notna() & (df['concession_type'] != '')
        else:
            df['is_concession'] = False
        
        return df
    
    def _analyze_addresses(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze concession patterns by address"""
        results = {
            "patterns": [],
            "suspicious": [],
            "profiles": {}
        }
        
        # Filter to rows with address_id
        addr_df = df[df['address_id'].notna()].copy()
        
        if len(addr_df) == 0:
            return results
        
        # Group by address
        address_groups = addr_df.groupby('address_id')
        
        for address_id, group in address_groups:
            if len(group) < self.min_deliveries_for_analysis:
                continue
            
            # Calculate metrics
            total = len(group)
            concessions = group['is_concession'].sum()
            rate = concessions / total
            unique_drivers = group['transporter_id'].nunique()
            
            # Build profile
            concession_types = {}
            if 'concession_type' in group.columns:
                concession_types = group[group['is_concession']]['concession_type'].value_counts().to_dict()
            
            profile = AddressProfile(
                address_id=str(address_id),
                total_deliveries=total,
                total_concessions=int(concessions),
                concession_rate=rate,
                unique_drivers=unique_drivers,
                concession_types=concession_types,
                first_seen=group['delivery_date_time'].min(),
                last_seen=group['delivery_date_time'].max(),
                is_suspicious=rate >= self.high_concession_threshold,
                abuse_score=self._calculate_abuse_score(rate, concessions, unique_drivers, concession_types),
                patterns=[]
            )
            
            results["profiles"][str(address_id)] = profile
            
            # Detect patterns
            patterns_found = []
            
            # Pattern 1: High concession rate
            if rate >= self.critical_concession_threshold and concessions >= 3:
                pattern = AbusePattern(
                    pattern_id=f"HIGH_RATE_{address_id}",
                    address_id=str(address_id),
                    pattern_type="high_frequency",
                    severity="critical" if rate >= 0.70 else "high",
                    confidence=min(rate, 1.0),
                    description=f"Adresse mit {rate*100:.0f}% Concession-Rate ({concessions}/{total} Lieferungen)",
                    concession_count=int(concessions),
                    unique_incidents=int(concessions),
                    drivers_involved=group[group['is_concession']]['transporter_id'].unique().tolist(),
                    date_range=(group['delivery_date_time'].min(), group['delivery_date_time'].max()),
                    details={
                        "concession_rate": rate,
                        "concession_types": concession_types,
                        "total_deliveries": total
                    },
                    recommendations=[
                        "Adresse für manuelle Überprüfung markieren",
                        "Kundenhistorie prüfen",
                        "Bei nächster Zustellung Foto-Dokumentation anfordern"
                    ]
                )
                results["patterns"].append(pattern)
                patterns_found.append("high_frequency")
            
            # Pattern 2: Multi-driver concessions (same address, different drivers = suspicious)
            if unique_drivers >= self.multi_driver_threshold and concessions >= 3:
                drivers_with_concessions = group[group['is_concession']]['transporter_id'].unique()
                if len(drivers_with_concessions) >= 2:
                    pattern = AbusePattern(
                        pattern_id=f"MULTI_DRIVER_{address_id}",
                        address_id=str(address_id),
                        pattern_type="multi_driver",
                        severity="high" if len(drivers_with_concessions) >= 3 else "medium",
                        confidence=min(len(drivers_with_concessions) / 5, 1.0),
                        description=f"Concessions bei {len(drivers_with_concessions)} verschiedenen Fahrern an gleicher Adresse",
                        concession_count=int(concessions),
                        unique_incidents=len(drivers_with_concessions),
                        drivers_involved=list(drivers_with_concessions),
                        date_range=(group['delivery_date_time'].min(), group['delivery_date_time'].max()),
                        details={
                            "drivers_with_concessions": list(drivers_with_concessions),
                            "all_drivers": group['transporter_id'].unique().tolist()
                        },
                        recommendations=[
                            "Kunden-Missbrauch möglich - mehrere Fahrer betroffen",
                            "Zustellzeit mit Kunden abstimmen",
                            "Alternative Zustellorte vorschlagen"
                        ]
                    )
                    results["patterns"].append(pattern)
                    patterns_found.append("multi_driver")
            
            # Pattern 3: Repeat concessions in short window
            concession_rows = group[group['is_concession']].sort_values('delivery_date_time')
            if len(concession_rows) >= 3:
                dates = concession_rows['delivery_date_time'].dt.date.tolist()
                if len(set(dates)) < len(dates):  # Same-day repeats
                    pattern = AbusePattern(
                        pattern_id=f"REPEAT_{address_id}",
                        address_id=str(address_id),
                        pattern_type="repeat_concession",
                        severity="high",
                        confidence=0.8,
                        description=f"Wiederholte Concessions am gleichen Tag an dieser Adresse",
                        concession_count=int(concessions),
                        unique_incidents=len(set(dates)),
                        drivers_involved=concession_rows['transporter_id'].unique().tolist(),
                        date_range=(concession_rows['delivery_date_time'].min(), 
                                   concession_rows['delivery_date_time'].max()),
                        details={"dates_with_concessions": [str(d) for d in set(dates)]},
                        recommendations=[
                            "Möglicher systematischer Kundenmissbrauch",
                            "Lieferung nur mit Unterschrift",
                            "Zeitfenster-Zustellung erwägen"
                        ]
                    )
                    results["patterns"].append(pattern)
                    patterns_found.append("repeat_concession")
            
            profile.patterns = patterns_found
            
            # Add to suspicious list if any pattern found
            if profile.is_suspicious or patterns_found:
                results["suspicious"].append(profile)
        
        # Sort suspicious by abuse score
        results["suspicious"].sort(key=lambda x: x.abuse_score, reverse=True)
        
        return results
    
    def _analyze_tracking_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze patterns using tracking IDs (when address not available)"""
        results = {"patterns": []}
        
        # Look for patterns in tracking ID prefixes (often contain address/route info)
        if 'tracking_id' not in df.columns:
            return results
        
        # Extract tracking prefix (first 8-10 chars often contain location info)
        df['tracking_prefix'] = df['tracking_id'].astype(str).str[:10]
        
        prefix_groups = df.groupby('tracking_prefix')
        
        for prefix, group in prefix_groups:
            if len(group) < 5:  # Need enough samples
                continue
            
            concessions = group['is_concession'].sum()
            rate = concessions / len(group)
            
            if rate >= self.high_concession_threshold and concessions >= 3:
                pattern = AbusePattern(
                    pattern_id=f"TRACKING_{prefix}",
                    address_id=None,
                    pattern_type="tracking_pattern",
                    severity="medium",
                    confidence=min(rate * 0.8, 0.9),  # Lower confidence without address
                    description=f"Tracking-Muster {prefix}... zeigt {rate*100:.0f}% Concession-Rate",
                    concession_count=int(concessions),
                    unique_incidents=int(concessions),
                    drivers_involved=group[group['is_concession']]['transporter_id'].unique().tolist(),
                    date_range=(group['delivery_date_time'].min(), group['delivery_date_time'].max()),
                    details={
                        "tracking_prefix": prefix,
                        "total_deliveries": len(group),
                        "concession_rate": rate
                    },
                    recommendations=[
                        "Tracking-Muster auf gemeinsame Adresse prüfen",
                        "Route analysieren"
                    ]
                )
                results["patterns"].append(pattern)
        
        return results
    
    def _analyze_time_patterns(self, df: pd.DataFrame) -> List[AbusePattern]:
        """Detect suspiciously consistent time patterns (planned absences)"""
        patterns = []
        
        if 'hour' not in df.columns or 'address_id' not in df.columns:
            return patterns
        
        addr_df = df[df['address_id'].notna() & df['is_concession']]
        
        if len(addr_df) < 10:
            return patterns
        
        # Group by address and analyze hour patterns
        for address_id, group in addr_df.groupby('address_id'):
            if len(group) < 3:
                continue
            
            # Check if concessions always happen at same hour
            hours = group['hour'].value_counts()
            if len(hours) > 0:
                most_common_hour = hours.index[0]
                most_common_count = hours.values[0]
                concentration = most_common_count / len(group)
                
                if concentration >= 0.7 and len(group) >= 3:  # 70%+ at same hour
                    pattern = AbusePattern(
                        pattern_id=f"TIME_{address_id}",
                        address_id=str(address_id),
                        pattern_type="time_pattern",
                        severity="medium",
                        confidence=concentration,
                        description=f"{concentration*100:.0f}% der Concessions an dieser Adresse um {most_common_hour}:00 Uhr",
                        concession_count=len(group),
                        unique_incidents=len(group),
                        drivers_involved=group['transporter_id'].unique().tolist(),
                        date_range=(group['delivery_date_time'].min(), group['delivery_date_time'].max()),
                        details={
                            "peak_hour": most_common_hour,
                            "concentration": concentration,
                            "hour_distribution": hours.to_dict()
                        },
                        recommendations=[
                            f"Kunde scheint um {most_common_hour}:00 Uhr regelmäßig abwesend",
                            "Alternative Zustellzeit vorschlagen",
                            "Paketshop/Locker als Alternative anbieten"
                        ]
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _calculate_abuse_score(self, 
                                rate: float, 
                                concessions: int,
                                unique_drivers: int,
                                concession_types: Dict) -> float:
        """Calculate abuse likelihood score (0-100)"""
        score = 0
        
        # High concession rate (max 40 points)
        score += min(rate * 80, 40)
        
        # Multiple concessions (max 20 points)
        score += min(concessions * 4, 20)
        
        # Multiple drivers affected (max 20 points) - strong indicator
        score += min((unique_drivers - 1) * 10, 20)
        
        # Consistent concession type (max 20 points) - suggests pattern
        if concession_types:
            total_type_concessions = sum(concession_types.values())
            max_type_count = max(concession_types.values())
            type_concentration = max_type_count / total_type_concessions if total_type_concessions > 0 else 0
            if type_concentration >= 0.8:  # 80%+ same type
                score += 20
            elif type_concentration >= 0.6:
                score += 10
        
        return min(score, 100)
    
    def _generate_summary(self, results: Dict, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate analysis summary"""
        patterns = results["patterns"]
        
        return {
            "total_patterns_detected": len(patterns),
            "critical_patterns": len([p for p in patterns if p.severity == "critical"]),
            "high_patterns": len([p for p in patterns if p.severity == "high"]),
            "suspicious_addresses": len(results["suspicious_addresses"]),
            "has_address_data": results["has_address_data"],
            "total_records_analyzed": len(df),
            "total_concessions": df['is_concession'].sum() if 'is_concession' in df.columns else 0,
            "addresses_with_patterns": len(set(p.address_id for p in patterns if p.address_id)),
        }
    
    def get_top_suspicious_addresses(self, 
                                      results: Dict, 
                                      top_n: int = 10) -> List[AddressProfile]:
        """Get top N most suspicious addresses"""
        suspicious = results.get("suspicious_addresses", [])
        return suspicious[:top_n]
    
    def get_patterns_for_address(self, 
                                  results: Dict, 
                                  address_id: str) -> List[AbusePattern]:
        """Get all patterns for a specific address"""
        return [p for p in results.get("patterns", []) if p.address_id == address_id]


# =============================================================================
# STREAMLIT UI COMPONENT
# =============================================================================

def render_abuse_detection_tab(df: pd.DataFrame):
    """Render the customer abuse detection tab in Streamlit"""
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    
    st.header("🚨 Kunden-Missbrauchserkennung")
    st.markdown("*Erkennung von verdächtigen Mustern - Kunden die wiederholt ungerechtfertigte Concessions auslösen*")
    
    # Check for required columns
    has_address = 'address_id' in df.columns and df['address_id'].notna().any()
    has_tracking = 'tracking_id' in df.columns
    
    # Show data availability
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Address-ID verfügbar", "✅ Ja" if has_address else "❌ Nein")
    with col2:
        st.metric("Tracking-ID verfügbar", "✅ Ja" if has_tracking else "❌ Nein")
    
    if not has_address:
        st.warning("""
        ⚠️ **Address-ID nicht verfügbar** - Eingeschränkte Analyse möglich.
        
        Für vollständige Kunden-Missbrauchserkennung wird die `address_id` Spalte benötigt.
        Die Analyse wird mit Tracking-ID Mustern fortgesetzt.
        """)
    
    st.divider()
    
    # Run analysis
    detector = CustomerAbuseDetector()
    
    with st.spinner("Analysiere Muster..."):
        results = detector.analyze(df)
    
    # Summary metrics
    summary = results["summary"]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🚨 Kritische Muster", summary["critical_patterns"])
    col2.metric("⚠️ Hohe Priorität", summary["high_patterns"])
    col3.metric("📍 Verdächtige Adressen", summary["suspicious_addresses"])
    col4.metric("📊 Muster gesamt", summary["total_patterns_detected"])
    
    st.divider()
    
    # Patterns list
    if results["patterns"]:
        st.subheader("🔍 Erkannte Muster")
        
        for pattern in results["patterns"][:20]:  # Top 20
            severity_icon = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }
            
            with st.expander(
                f"{severity_icon.get(pattern.severity, '⚪')} {pattern.description}", 
                expanded=pattern.severity in ["critical", "high"]
            ):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Typ:** {pattern.pattern_type}")
                    st.markdown(f"**Konfidenz:** {pattern.confidence*100:.0f}%")
                    if pattern.address_id:
                        st.markdown(f"**Adress-ID:** `{pattern.address_id}`")
                
                with col2:
                    st.markdown(f"**Concessions:** {pattern.concession_count}")
                    st.markdown(f"**Fahrer betroffen:** {len(pattern.drivers_involved)}")
                
                with col3:
                    st.markdown("**Empfehlungen:**")
                    for rec in pattern.recommendations:
                        st.markdown(f"• {rec}")
        
        # Export patterns
        if st.button("📥 Muster exportieren"):
            patterns_data = [{
                "Adress-ID": p.address_id or "N/A",
                "Typ": p.pattern_type,
                "Schwere": p.severity,
                "Beschreibung": p.description,
                "Concessions": p.concession_count,
                "Fahrer": ", ".join(p.drivers_involved[:5]),
                "Konfidenz": f"{p.confidence*100:.0f}%"
            } for p in results["patterns"]]
            
            patterns_df = pd.DataFrame(patterns_data)
            csv = patterns_df.to_csv(index=False)
            st.download_button(
                "📥 Als CSV herunterladen",
                csv,
                f"abuse_patterns_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
    else:
        st.success("✅ Keine verdächtigen Muster erkannt!")
    
    # Suspicious addresses table
    if results["suspicious_addresses"]:
        st.divider()
        st.subheader("📍 Verdächtige Adressen (Top 15)")
        
        addr_data = [{
            "Adress-ID": a.address_id,
            "Lieferungen": a.total_deliveries,
            "Concessions": a.total_concessions,
            "Rate": f"{a.concession_rate*100:.1f}%",
            "Fahrer": a.unique_drivers,
            "Abuse-Score": f"{a.abuse_score:.0f}/100",
            "Muster": ", ".join(a.patterns) if a.patterns else "-"
        } for a in results["suspicious_addresses"][:15]]
        
        addr_df = pd.DataFrame(addr_data)
        
        # Highlight critical rows
        def highlight_abuse(row):
            if float(row['Abuse-Score'].split('/')[0]) >= 70:
                return ['background-color: #FFCDD2'] * len(row)
            elif float(row['Abuse-Score'].split('/')[0]) >= 50:
                return ['background-color: #FFF9C4'] * len(row)
            return [''] * len(row)
        
        styled = addr_df.style.apply(highlight_abuse, axis=1)
        st.dataframe(styled, use_container_width=True, hide_index=True)
    
    # Analysis explanation
    with st.expander("ℹ️ Wie funktioniert die Erkennung?"):
        st.markdown("""
        **Erkannte Muster:**
        
        1. **Hohe Concession-Rate** (`high_frequency`)
           - Adressen mit >30% Concession-Rate
           - Kritisch bei >50%
        
        2. **Multi-Fahrer-Muster** (`multi_driver`)
           - Gleiche Adresse, verschiedene Fahrer haben Concessions
           - Starker Indikator für Kundenproblem, nicht Fahrerproblem
        
        3. **Wiederholungs-Muster** (`repeat_concession`)
           - Mehrere Concessions am gleichen Tag
           - Deutet auf systematisches Verhalten hin
        
        4. **Zeit-Muster** (`time_pattern`)
           - Concessions immer zur gleichen Uhrzeit
           - Kunde wahrscheinlich planmäßig abwesend
        
        5. **Tracking-Muster** (`tracking_pattern`)
           - Verwendet wenn Address-ID nicht verfügbar
           - Analysiert gemeinsame Tracking-ID Präfixe
        
        **Abuse-Score (0-100):**
        - Kombiniert Rate, Häufigkeit, Anzahl Fahrer und Konsistenz
        - >70 = Kritisch, >50 = Hoch, >30 = Medium
        """)


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    np.random.seed(42)
    
    # Create test data with some abuse patterns
    n_records = 1000
    
    # Normal addresses
    addresses = [f"ADDR_{i:04d}" for i in range(100)]
    
    # Create abuse addresses (high concession rate)
    abuse_addresses = ["ABUSE_001", "ABUSE_002", "ABUSE_003"]
    
    data = []
    
    # Normal deliveries
    for i in range(n_records - 50):
        addr = np.random.choice(addresses)
        data.append({
            'tracking_id': f'TRK{i:06d}',
            'address_id': addr,
            'transporter_id': np.random.choice(['DRV01', 'DRV02', 'DRV03', 'DRV04', 'DRV05']),
            'delivery_date_time': datetime.now() - timedelta(days=np.random.randint(0, 60)),
            'concession_type': np.random.choice([None]*95 + ['neighbor', 'safe_location'], 1)[0]
        })
    
    # Abuse pattern deliveries
    for i in range(50):
        addr = np.random.choice(abuse_addresses)
        data.append({
            'tracking_id': f'ABUSE_TRK{i:04d}',
            'address_id': addr,
            'transporter_id': np.random.choice(['DRV01', 'DRV02', 'DRV03', 'DRV04', 'DRV05']),
            'delivery_date_time': datetime.now() - timedelta(days=np.random.randint(0, 30)),
            'concession_type': np.random.choice(['neighbor', 'safe_location', None], 1, p=[0.4, 0.4, 0.2])[0]
        })
    
    df = pd.DataFrame(data)
    
    # Run analysis
    detector = CustomerAbuseDetector()
    results = detector.analyze(df)
    
    print("=" * 60)
    print("Customer Abuse Detection Test")
    print("=" * 60)
    print(f"\nSummary: {results['summary']}")
    print(f"\nPatterns found: {len(results['patterns'])}")
    
    for p in results['patterns'][:5]:
        print(f"\n  [{p.severity.upper()}] {p.description}")
        print(f"    Address: {p.address_id}, Concessions: {p.concession_count}")
