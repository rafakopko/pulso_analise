"""
Projeto Pulso - Páginas do Dashboard
====================================

Este módulo contém todas as páginas do dashboard Streamlit do Projeto Pulso.

Páginas disponíveis:
- Home (app.py): Dashboard principal com KPIs
- 2_Analise_Lacunas.py: Análise detalhada de lacunas
- 3_Visao_Loja.py: Visão individual por loja
- 4_Clusters.py: Análise de clustering de lojas
- 5_Exportar.py: Exportação de relatórios

Estrutura conforme o Plano de Desenvolvimento MVP.
"""

__version__ = "1.0.0"
__author__ = "Projeto Pulso Team"

# Informações das páginas para navegação
PAGES_INFO = {
    "home": {
        "title": "🏠 Home - Centro de Comando",
        "description": "KPIs principais e visão geral",
        "file": "app.py"
    },    "gaps": {
        "title": "🎯 Análise de Lacunas", 
        "description": "Decomposição detalhada de lacunas",
        "file": "2_Analise_Lacunas.py"
    },
    "store": {
        "title": "🏪 Visão por Loja",
        "description": "Análise individual de lojas", 
        "file": "3_Visao_Loja.py"
    },
    "clusters": {
        "title": "👥 Análise de Clusters",
        "description": "Inteligência comparativa por clusters",
        "file": "4_Clusters.py"
    },
    "export": {
        "title": "📈 Exportar Relatórios",
        "description": "Geração de relatórios personalizados",
        "file": "5_Exportar.py"
    }
}
