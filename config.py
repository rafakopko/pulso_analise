"""
Configurações globais da aplicação Dashboard Pulso
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "upload"
PROCESSED_DIR = DATA_DIR / "processed"
EXPORTS_DIR = DATA_DIR / "exports"
DOCS_DIR = BASE_DIR / "Documentação"

# Configurações do Streamlit
PAGE_CONFIG = {
    "page_title": "Dashboard Pulso - Análise de Lacunas",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        "Get Help": None,
        "Report a bug": None,
        "About": "Dashboard Pulso v1.0 - Análise de Lacunas Comerciais"
    }
}

# Configurações de dados
EXCEL_CONFIG = {
    "file_types": ["xlsx", "xls"],
    "max_file_size": 50,  # MB
    "required_sheets": [
        "pulso_consulta_diaria",
        "pulso_consulta_diaria_cluster_antigo"
    ]
}

# Campos obrigatórios no Excel
REQUIRED_COLUMNS = {
    "pulso_consulta_diaria": [
        "NomeLoja", "codigo_franquia", "NumeroGR", "datavenda",
        "receita_liquida", "qtd_cupom", "qtd_item",
        "Mediana_Semana_RL", "Mediana_Semana_cupom"
    ],
    "pulso_consulta_diaria_cluster_antigo": [
        "NomeLoja", "grupo_comparavel", "LacunaRL", "LacunaCupom",
        "LacunaBM", "LacunaPM", "LacunaProd"
    ]
}

# Mapeamento de cores para visualizações
COLOR_PALETTE = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e", 
    "success": "#2ca02c",
    "warning": "#ff7f0e",
    "danger": "#d62728",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Configurações de cache
CACHE_CONFIG = {
    "ttl": 3600,  # 1 hora
    "max_entries": 10
}

# Mensagens padrão
MESSAGES = {
    "upload_success": "✅ Arquivo carregado com sucesso!",
    "upload_error": "❌ Erro ao carregar arquivo. Verifique o formato.",
    "processing": "🔄 Processando dados...",
    "no_data": "📁 Nenhum dado encontrado. Faça upload do arquivo Excel.",
    "invalid_format": "⚠️ Formato de arquivo inválido.",
    "missing_sheets": "⚠️ Abas obrigatórias não encontradas no arquivo."
}

# Formatação de números
NUMBER_FORMATS = {
    "currency": "R$ {:,.0f}",
    "percentage": "{:.1f}%",
    "integer": "{:,.0f}",
    "decimal": "{:,.2f}"
}
