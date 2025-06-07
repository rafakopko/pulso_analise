"""
Projeto Pulso - Módulo Principal
================================

Este módulo contém todas as funcionalidades core do sistema de análise de lacunas
do Projeto Pulso, incluindo carregamento de dados, cálculos e visualizações.

Módulos disponíveis:
- data_loader: Carregamento e validação de dados Excel
- calculations: Cálculos de lacunas e métricas
- visualizations: Gráficos e dashboards
- utils: Funções auxiliares e utilitários
"""

from .data_loader import DataLoader
from .calculations import LacunaCalculator
from .visualizations import PulsoVisualizations
from .utils import (
    SessionManager,
    format_currency,
    format_percentage,
    export_to_excel
)

__version__ = "1.0.0"
__author__ = "Projeto Pulso Team"

# Exportar classes principais para facilitar importação
__all__ = [
    'DataLoader',
    'LacunaCalculator', 
    'PulsoVisualizations',
    'SessionManager',
    'format_currency',
    'format_percentage',
    'export_to_excel'
]
