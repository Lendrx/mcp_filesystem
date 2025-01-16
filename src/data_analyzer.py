import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataAnalyzer:
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path) if data_path else None
        self.data = None
        logger.info(f"DataAnalyzer initialisiert mit Pfad: {data_path}")
    
    def load_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        path = Path(file_path) if file_path else self.data_path
        if not path:
            raise ValueError("Kein Dateipfad angegeben!")
            
        logger.info(f"Lade Daten von: {path}")
        try:
            self.data = pd.read_csv(path)
            return self.data
        except Exception as e:
            logger.error(f"Fehler beim Laden der Daten: {e}")
            raise
    
    def get_basic_stats(self, columns: Optional[List[str]] = None) -> Dict:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        if columns:
            numeric_data = self.data[columns].select_dtypes(include=[np.number])
        else:
            numeric_data = self.data.select_dtypes(include=[np.number])
            
        stats = {
            col: {
                'mean': numeric_data[col].mean(),
                'median': numeric_data[col].median(),
                'std': numeric_data[col].std(),
                'min': numeric_data[col].min(),
                'max': numeric_data[col].max()
            }
            for col in numeric_data.columns
        }
        
        return stats
    
    def find_outliers(self, column: str, threshold: float = 2.0) -> Dict:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        data = self.data[column]
        z_scores = np.abs((data - data.mean()) / data.std())
        outliers = data[z_scores > threshold]
        
        return {
            'outliers': outliers.tolist(),
            'indices': outliers.index.tolist(),
            'count': len(outliers)
        }
    
    def generate_summary(self) -> Dict:
        if self.data is None:
            raise ValueError("Keine Daten geladen!")
            
        return {
            'shape': self.data.shape,
            'columns': self.data.columns.tolist(),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'numeric_columns': self.data.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': self.data.select_dtypes(include=['object']).columns.tolist()
        }

# Beispielverwendung
if __name__ == "__main__":
    # Beispieldaten erstellen
    example_data = pd.DataFrame({
        'A': np.random.normal(0, 1, 100),
        'B': np.random.normal(5, 2, 100),
        'C': ['cat', 'dog'] * 50
    })
    
    # Beispieldaten speichern
    data_path = Path('../data/example_data.csv')
    data_path.parent.mkdir(parents=True, exist_ok=True)
    example_data.to_csv(data_path, index=False)
    
    # Analyzer testen
    analyzer = DataAnalyzer(str(data_path))
    
    try:
        # Daten laden
        analyzer.load_data()
        
        # Statistiken berechnen
        stats = analyzer.get_basic_stats()
        print("\nGrundlegende Statistiken:")
        print(stats)
        
        # Ausreißer finden
        outliers = analyzer.find_outliers('A')
        print("\nGefundene Ausreißer in Spalte A:")
        print(outliers)
        
        # Zusammenfassung generieren
        summary = analyzer.generate_summary()
        print("\nDatensatz-Zusammenfassung:")
        print(summary)
        
    except Exception as e:
        logger.error(f"Fehler bei der Analyse: {e}")
