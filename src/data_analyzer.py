import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ECommerceAnalyzer:
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path) if data_path else None
        self.data = None
        logger.info(f"ECommerceAnalyzer initialisiert mit Pfad: {data_path}")
    
    def load_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        path = Path(file_path) if file_path else self.data_path
        if not path:
            raise ValueError("Kein Dateipfad angegeben!")
            
        logger.info(f"Lade Daten von: {path}")
        try:
            self.data = pd.read_csv(path)
            # Konvertiere date zu datetime
            self.data['date'] = pd.to_datetime(self.data['date'])
            return self.data
        except Exception as e:
            logger.error(f"Fehler beim Laden der Daten: {e}")
            raise
            
    def get_sales_summary(self, group_by: str = 'product_category') -> pd.DataFrame:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        summary = self.data.groupby(group_by).agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'rating': 'mean',
            'return_status': lambda x: (x == 'Yes').mean()
        }).round(2)
        
        summary.columns = ['Verkaufte Einheiten', 'Gesamtumsatz', 
                         'Durchschnittliche Bewertung', 'Rückgabequote']
        return summary
        
    def analyze_daily_sales(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        daily_stats = self.data.groupby('date').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'rating': 'mean'
        }).round(2)
        
        daily_stats.columns = ['Tagesumsatz', 'Verkaufte Einheiten', 
                             'Durchschnittliche Bewertung']
        return daily_stats
        
    def analyze_customer_countries(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        country_stats = self.data.groupby('customer_country').agg({
            'customer_id': 'count',
            'total_amount': 'sum',
            'rating': 'mean'
        }).round(2)
        
        country_stats.columns = ['Anzahl Kunden', 'Gesamtumsatz', 
                               'Durchschnittliche Bewertung']
        return country_stats
        
    def analyze_payment_methods(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        payment_stats = self.data.groupby('payment_method').agg({
            'total_amount': ['sum', 'mean', 'count']
        }).round(2)
        
        payment_stats.columns = ['Gesamtumsatz', 'Durchschnittlicher Betrag', 
                               'Anzahl Transaktionen']
        return payment_stats
        
    def analyze_delivery_impact(self) -> Dict:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        correlation = self.data['delivery_time_days'].corr(self.data['rating'])
        
        delivery_impact = {
            'korrelation_lieferzeit_bewertung': round(correlation, 3),
            'durchschnittliche_bewertung_pro_lieferzeit': 
                self.data.groupby('delivery_time_days')['rating'].mean().to_dict()
        }
        
        return delivery_impact

    def get_top_products(self, metric: str = 'quantity', top_n: int = 5) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        if metric not in ['quantity', 'total_amount']:
            raise ValueError("Metrik muss 'quantity' oder 'total_amount' sein!")
            
        top_products = self.data.groupby(['product_id', 'product_category']).agg({
            metric: 'sum',
            'rating': 'mean'
        }).round(2)
        
        top_products = top_products.sort_values(metric, ascending=False).head(top_n)
        return top_products

# Beispielverwendung
if __name__ == "__main__":
    # Korrekten Pfad zur Datei erstellen
    import os
    
    # Pfad relativ zum Skript-Verzeichnis erstellen
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'ecommerce_sales.csv')
    
    # Analyzer initialisieren
    analyzer = ECommerceAnalyzer(data_path)
    
    try:
        # Daten laden
        analyzer.load_data()
        
        # Verschiedene Analysen durchführen
        print("\nVerkaufszusammenfassung nach Kategorien:")
        print(analyzer.get_sales_summary())
        
        print("\nTop 5 Produkte nach Verkaufsmenge:")
        print(analyzer.get_top_products())
        
        print("\nAnalyse der Zahlungsmethoden:")
        print(analyzer.analyze_payment_methods())
        
        print("\nLänderbasierte Statistiken:")
        print(analyzer.analyze_customer_countries())
        
        print("\nEinfluss der Lieferzeit:")
        print(analyzer.analyze_delivery_impact())
        
    except Exception as e:
        logger.error(f"Fehler bei der Analyse: {e}")
