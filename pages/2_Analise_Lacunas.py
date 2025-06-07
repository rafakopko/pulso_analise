"""
Página de Análise de Lacunas Detalhada
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.calculations import LacunaCalculator
from src.visualizations import PulsoVisualizations, format_number
from src.utils import SessionManager, filter_dataframe

# Configuração da página
st.set_page_config(
    page_title="Análise de Lacunas - Dashboard Pulso",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Análise de Lacunas")
st.markdown("### Decomposição detalhada das oportunidades comerciais")

# Verificar se há dados
if not SessionManager.is_data_loaded():
    st.warning("⚠️ Nenhum dado carregado. Volte à página inicial para fazer upload do arquivo.")
    if st.button("🏠 Ir para Home"):
        st.switch_page("app.py")
    st.stop()

# Carregar dados
data = SessionManager.get_data()
calculator = LacunaCalculator(data)
metrics = calculator.calculate_all_metrics()

if not metrics or "error" in metrics:
    st.error("❌ Erro no processamento dos dados")
    st.stop()

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

# Filtros disponíveis
df_cluster = data.get("pulso_consulta_diaria_cluster_a", pd.DataFrame())

# Inicializar df_filtrado
df_filtrado = pd.DataFrame()
cluster_selecionado = "Todos"

if not df_cluster.empty:
    # Filtro por cluster
    clusters_disponíveis = ["Todos"] + sorted(df_cluster["grupo_comparavel"].unique().tolist())
    cluster_selecionado = st.sidebar.selectbox(
        "Grupo Comparável:",
        clusters_disponíveis
    )
    
    # Filtro por tipo de lacuna
    tipo_lacuna = st.sidebar.selectbox(
        "Tipo de Análise:",
        ["Todas as Lacunas", "Apenas Oportunidades (Negativas)", "Apenas Destaques (Positivas)"]
    )
    
    # Aplicar filtros
    df_filtrado = df_cluster.copy()
    
    if cluster_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["grupo_comparavel"] == cluster_selecionado]
    
    if tipo_lacuna == "Apenas Oportunidades (Negativas)":
        df_filtrado = df_filtrado[df_filtrado["LacunaRL"] < 0]
    elif tipo_lacuna == "Apenas Destaques (Positivas)":
        df_filtrado = df_filtrado[df_filtrado["LacunaRL"] > 0]
else:
    st.warning("⚠️ Dados de cluster não encontrados no arquivo Excel.")

# Layout principal
viz = PulsoVisualizations()

# Métricas resumo dos dados filtrados
if not df_filtrado.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_lacuna = df_filtrado["LacunaRL"].sum()
        st.metric(
            "💰 Lacuna Total RL",
            format_number(total_lacuna, "currency")
        )
    
    with col2:
        qtd_lojas = len(df_filtrado)
        st.metric(
            "🏪 Quantidade de Lojas",
            f"{qtd_lojas:,}"
        )
    
    with col3:
        lacuna_media = df_filtrado["LacunaRL"].mean()
        st.metric(
            "📊 Lacuna Média",
            format_number(lacuna_media, "currency")
        )
    
    with col4:
        oportunidades = len(df_filtrado[df_filtrado["LacunaRL"] < 0])
        st.metric(
            "🎯 Oportunidades",
            f"{oportunidades:,}"
        )

st.markdown("---")

# Gráfico de decomposição waterfall
st.header("💡 Decomposição de Lacunas")

# Calcular waterfall para dados filtrados
if not df_filtrado.empty:
    # Para dados filtrados, recalcular o waterfall
    lacuna_rl_total = df_filtrado["LacunaRL"].sum()
    lacuna_cupom_total = df_filtrado["LacunaCupom"].sum()
    lacuna_bm_total = df_filtrado["LacunaBM"].sum()
    lacuna_pm_total = df_filtrado["LacunaPM"].sum() if "LacunaPM" in df_filtrado.columns else 0
    lacuna_prod_total = df_filtrado["LacunaProd"].sum() if "LacunaProd" in df_filtrado.columns else 0
    
    waterfall_data_filtrado = {
        "categories": ["Base", "Lacuna Cupom", "Lacuna BM", "Lacuna PM", "Lacuna Prod", "Total"],
        "values": [0, lacuna_cupom_total, lacuna_bm_total, lacuna_pm_total, lacuna_prod_total, lacuna_rl_total]
    }
    
    fig_waterfall = viz.create_waterfall_chart(
        waterfall_data_filtrado, 
        f"Decomposição de Lacunas - {cluster_selecionado if cluster_selecionado != 'Todos' else 'Total'}"
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

# Análise detalhada por lacuna
st.header("📊 Análise Detalhada por Componente")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Receita Líquida", "🧾 Cupom", "💳 Boleto Médio", "💰 Preço Médio", "📦 Produtividade"])

with tab1:
    st.subheader("Distribuição da Lacuna de Receita Líquida")
    
    if not df_filtrado.empty:
        fig_hist_rl = viz.create_distribution_histogram(
            df_filtrado, 
            "LacunaRL", 
            "Distribuição da Lacuna de RL"
        )
        st.plotly_chart(fig_hist_rl, use_container_width=True)
        
        # Top e bottom performers
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🔻 Maiores Lacunas (Oportunidades)**")
            top_lacunas = df_filtrado.nsmallest(10, "LacunaRL")[["NomeLoja", "grupo_comparavel", "LacunaRL"]]
            st.dataframe(top_lacunas, use_container_width=True, hide_index=True)
        
        with col2:
            st.write("**🔺 Melhores Performances**")
            top_performers = df_filtrado.nlargest(10, "LacunaRL")[["NomeLoja", "grupo_comparavel", "LacunaRL"]]
            st.dataframe(top_performers, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Análise da Lacuna de Cupom")
    
    if not df_filtrado.empty and "LacunaCupom" in df_filtrado.columns:
        fig_hist_cupom = viz.create_distribution_histogram(
            df_filtrado, 
            "LacunaCupom", 
            "Distribuição da Lacuna de Cupom"
        )
        st.plotly_chart(fig_hist_cupom, use_container_width=True)
        
        # Correlação entre lacuna de cupom e RL
        col1, col2 = st.columns(2)
        
        with col1:
            correlation = df_filtrado["LacunaRL"].corr(df_filtrado["LacunaCupom"])
            st.metric("🔗 Correlação RL vs Cupom", f"{correlation:.3f}")
        
        with col2:
            impact_cupom = abs(df_filtrado["LacunaCupom"].sum() / df_filtrado["LacunaRL"].sum() * 100) if df_filtrado["LacunaRL"].sum() != 0 else 0
            st.metric("📊 Impacto do Cupom", f"{impact_cupom:.1f}%")

with tab3:
    st.subheader("Análise da Lacuna de Boleto Médio")
    
    if not df_filtrado.empty and "LacunaBM" in df_filtrado.columns:
        fig_hist_bm = viz.create_distribution_histogram(
            df_filtrado, 
            "LacunaBM", 
            "Distribuição da Lacuna de BM"
        )
        st.plotly_chart(fig_hist_bm, use_container_width=True)
        
        # Análise BM vs componentes
        if all(col in df_filtrado.columns for col in ["LacunaPM", "LacunaProd"]):
            st.write("**Decomposição do Boleto Médio:**")
            
            decomp_bm = df_filtrado[["NomeLoja", "LacunaBM", "LacunaPM", "LacunaProd"]].copy()
            decomp_bm["Soma_PM_Prod"] = decomp_bm["LacunaPM"] + decomp_bm["LacunaProd"]
            decomp_bm["Diferenca"] = decomp_bm["LacunaBM"] - decomp_bm["Soma_PM_Prod"]
            
            st.dataframe(decomp_bm.head(10), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Análise da Lacuna de Preço Médio")
    
    if not df_filtrado.empty and "LacunaPM" in df_filtrado.columns:
        fig_hist_pm = viz.create_distribution_histogram(
            df_filtrado, 
            "LacunaPM", 
            "Distribuição da Lacuna de PM"
        )
        st.plotly_chart(fig_hist_pm, use_container_width=True)

with tab5:
    st.subheader("Análise da Lacuna de Produtividade")
    
    if not df_filtrado.empty and "LacunaProd" in df_filtrado.columns:
        fig_hist_prod = viz.create_distribution_histogram(
            df_filtrado, 
            "LacunaProd", 
            "Distribuição da Lacuna de Produtividade"
        )
        st.plotly_chart(fig_hist_prod, use_container_width=True)

# Análise de correlações
st.header("🔗 Matriz de Correlações")

if not df_filtrado.empty:
    lacuna_columns = [col for col in ["LacunaRL", "LacunaCupom", "LacunaBM", "LacunaPM", "LacunaProd"] 
                     if col in df_filtrado.columns]
    
    if len(lacuna_columns) >= 2:
        fig_corr = viz.create_correlation_heatmap(df_filtrado, lacuna_columns)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Dados insuficientes para matriz de correlação")

# Tabela detalhada
st.header("📋 Dados Detalhados")

if not df_filtrado.empty:
    # Preparar colunas para exibição
    display_columns = ["NomeLoja", "grupo_comparavel"]
    for col in ["LacunaRL", "LacunaCupom", "LacunaBM", "LacunaPM", "LacunaProd"]:
        if col in df_filtrado.columns:
            display_columns.append(col)
    
    # Ordenar por LacunaRL
    df_display = df_filtrado[display_columns].sort_values("LacunaRL")
    
    # Mostrar tabela com paginação
    total_rows = len(df_display)
    rows_per_page = 20
    total_pages = (total_rows - 1) // rows_per_page + 1
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        page = st.selectbox(
            "Página:",
            range(1, total_pages + 1),
            format_func=lambda x: f"Página {x} de {total_pages}"
        )
    
    start_idx = (page - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)
    
    st.dataframe(
        df_display.iloc[start_idx:end_idx],
        use_container_width=True,
        hide_index=True
    )
    
    st.info(f"Mostrando registros {start_idx + 1} a {end_idx} de {total_rows} total")

# Botão de navegação
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🏠 Voltar ao Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🏪 Visão por Loja", use_container_width=True):
        st.switch_page("pages/3_Visao_Loja.py")

with col3:
    if st.button("👥 Análise Clusters", use_container_width=True):
        st.switch_page("pages/4_Clusters.py")
