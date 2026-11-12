from abc import ABC, abstractmethod
import pandas as pd

class MarketDataProvider(ABC):
    """Interfaz abstracta para fuentes de datos del mercado."""

    @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        """Extrae y retorna los datos en forma de DataFrame."""
        pass