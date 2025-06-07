"""
Página de Visão por Loja Individual
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.calculations import LacunaCalculator
from src.visualizations import PulsoVisualizations, format_number
from src.utils import SessionManager

# Configuração da página
st.set_page_config(
    page_title="Visão por Loja - Dashboard Pulso",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Visão por Loja")
st.markdown("### Análise detalhada de performance individual")

# Verificar se há dados
if not SessionManager.is_data_loaded():
    st.warning("⚠️ Nenhum dado carregado. Volte à página inicial para fazer upload do arquivo.")
    if st.button("🏠 Ir para Home"):
        st.switch_page("app.py")
    st.stop()

# Carregar dados
data = SessionManager.get_data()
calculator = LacunaCalculator(data)
viz = PulsoVisualizations()  # Inicializar viz aqui
df_cluster = data.get("pulso_consulta_diaria_cluster_antigo", pd.DataFrame())

if df_cluster.empty:
    st.error("❌ Dados de cluster não encontrados")
    st.stop()

# Sidebar - Seleção de loja
st.sidebar.header("🔍 Seleção de Loja")

# Lista de lojas
lojas_disponiveis = sorted(df_cluster["NomeLoja"].unique().tolist())
loja_selecionada = st.sidebar.selectbox(
    "Selecione uma loja:",
    lojas_disponiveis,
    help="Escolha a loja para análise detalhada"
)

# Busca de loja
busca_loja = st.sidebar.text_input(
    "🔍 Buscar loja:",
    placeholder="Digite parte do nome..."
)

if busca_loja:
    lojas_filtradas = [loja for loja in lojas_disponiveis if busca_loja.lower() in loja.lower()]
    if lojas_filtradas:
        loja_selecionada = st.sidebar.selectbox(
            "Resultados da busca:",
            lojas_filtradas
        )
    else:
        st.sidebar.warning("Nenhuma loja encontrada")

# Obter detalhes da loja
loja_details = calculator.get_loja_details(loja_selecionada)

if not loja_details or "cluster_data" not in loja_details:
    st.error(f"❌ Dados não encontrados para a loja: {loja_selecionada}")
    st.stop()

loja_data = loja_details["cluster_data"]

# Header da loja
st.header(f"📊 {loja_selecionada}")

# Informações básicas
col1, col2, col3 = st.columns(3)

with col1:
    cluster = loja_data.get("grupo_comparavel", "N/A")
    st.info(f"**Cluster:** {cluster}")

with col2:
    if "cluster_comparison" in loja_details:
        cluster_size = loja_details["cluster_comparison"]["cluster_size"]
        rank = loja_details["cluster_comparison"]["rank_in_cluster"]
        st.info(f"**Ranking no Cluster:** {rank}º de {cluster_size}")

with col3:
    # Status baseado na lacuna
    lacuna_rl = loja_data.get("LacunaRL", 0)
    if lacuna_rl < 0:
        status = "🎯 Oportunidade"
        status_color = "error"
    elif lacuna_rl > 0:
        status = "⭐ Destaque"
        status_color = "success"
    else:
        status = "➖ Neutro"
        status_color = "info"
    
    st.info(f"**Status:** {status}")

st.markdown("---")

# KPIs da loja
st.subheader("💡 Métricas de Lacunas")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    lacuna_rl = loja_data.get("LacunaRL", 0)
    delta_rl = "📈" if lacuna_rl > 0 else "📉" if lacuna_rl < 0 else "➖"
    st.metric(
        "💰 Lacuna RL",
        format_number(lacuna_rl, "currency"),
        delta=f"{delta_rl} {abs(lacuna_rl):,.0f}"
    )

with col2:
    lacuna_cupom = loja_data.get("LacunaCupom", 0)
    st.metric(
        "🧾 Lacuna Cupom",
        f"{lacuna_cupom:,.0f}",
        delta=f"{'📈' if lacuna_cupom > 0 else '📉' if lacuna_cupom < 0 else '➖'} {abs(lacuna_cupom):,.0f}"
    )

with col3:
    lacuna_bm = loja_data.get("LacunaBM", 0)
    st.metric(
        "💳 Lacuna BM",
        format_number(lacuna_bm, "currency"),
        delta=f"{'📈' if lacuna_bm > 0 else '📉' if lacuna_bm < 0 else '➖'} {abs(lacuna_bm):,.0f}"
    )

with col4:
    lacuna_pm = loja_data.get("LacunaPM", 0)
    st.metric(
        "💰 Lacuna PM",
        format_number(lacuna_pm, "currency"),
        delta=f"{'📈' if lacuna_pm > 0 else '📉' if lacuna_pm < 0 else '➖'} {abs(lacuna_pm):,.0f}"
    )

with col5:
    lacuna_prod = loja_data.get("LacunaProd", 0)
    st.metric(
        "📦 Lacuna Prod",
        f"{lacuna_prod:,.2f}",
        delta=f"{'📈' if lacuna_prod > 0 else '📉' if lacuna_prod < 0 else '➖'} {abs(lacuna_prod):,.2f}"
    )

st.markdown("---")

# Layout principal
col1, col2 = st.columns(2)

with col1:
    # Gráfico waterfall da loja
    st.subheader("💡 Decomposição de Lacunas")
    waterfall_data = calculator.calculate_waterfall_data(loja_selecionada)
    if waterfall_data:
        fig_waterfall = viz.create_waterfall_chart(
            waterfall_data, 
            f"Decomposição - {loja_selecionada}"
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
    else:
        st.info("Dados insuficientes para decomposição")

with col2:
    # Comparação com cluster
    st.subheader("📊 Comparação com Cluster")
    
    if "cluster_comparison" in loja_details:
        cluster_comp = loja_details["cluster_comparison"]
        
        # Métricas comparativas
        st.write("**Vs. Mediana do Cluster:**")
        
        cluster_median = cluster_comp.get("cluster_median_rl", 0)
        diferenca = lacuna_rl - cluster_median
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.metric(
                "Mediana Cluster",
                format_number(cluster_median, "currency")
            )
        
        with col_comp2:
            st.metric(
                "Diferença",
                format_number(diferenca, "currency"),
                delta=f"{'Acima' if diferenca > 0 else 'Abaixo'} da mediana"
            )
        
        # Gráfico radar (se dados suficientes)
        try:
            # Criar dados fictícios para o radar baseados nos dados reais
            radar_data = {
                "LacunaRL": lacuna_rl,
                "LacunaCupom": lacuna_cupom,
                "LacunaBM": lacuna_bm,
                "LacunaPM": lacuna_pm,
                "LacunaProd": lacuna_prod
            }
            
            radar_cluster = {
                "cluster_median_lacunarl": cluster_median,
                "cluster_median_lacunacupom": 0,  # Placeholder
                "cluster_median_lacunabm": 0,     # Placeholder
                "cluster_median_lacunapm": 0,     # Placeholder
                "cluster_median_lacunaprod": 0    # Placeholder
            }
            
            fig_radar = viz.create_loja_radar_chart(radar_data, radar_cluster)
            if fig_radar.data:  # Verificar se o gráfico tem dados
                st.plotly_chart(fig_radar, use_container_width=True)
        except Exception as e:
            st.info("Gráfico radar não disponível")

# Análise do cluster
st.subheader("👥 Análise do Cluster")

cluster_lojas = df_cluster[df_cluster["grupo_comparavel"] == cluster].copy()

if not cluster_lojas.empty:
    # Estatísticas do cluster
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🏪 Lojas no Cluster",
            f"{len(cluster_lojas):,}"
        )
    
    with col2:
        cluster_mean = cluster_lojas["LacunaRL"].mean()
        st.metric(
            "📊 Lacuna Média",
            format_number(cluster_mean, "currency")
        )
    
    with col3:
        cluster_std = cluster_lojas["LacunaRL"].std()
        st.metric(
            "📈 Desvio Padrão",
            format_number(cluster_std, "currency")
        )
    
    # Ranking no cluster
    st.write("**🏆 Ranking no Cluster:**")
    
    cluster_ranking = cluster_lojas.sort_values("LacunaRL", ascending=False).reset_index(drop=True)
    cluster_ranking["Posição"] = range(1, len(cluster_ranking) + 1)
    
    # Destacar a loja selecionada
    loja_position = cluster_ranking[cluster_ranking["NomeLoja"] == loja_selecionada].index
    
    if not loja_position.empty:
        loja_idx = loja_position[0]
        
        # Mostrar contexto (3 acima e 3 abaixo)
        start_idx = max(0, loja_idx - 3)
        end_idx = min(len(cluster_ranking), loja_idx + 4)
        
        ranking_context = cluster_ranking.iloc[start_idx:end_idx]
        
        # Criar um DataFrame estilizado
        def highlight_selected(row):
            return ['background-color: #ffffcc' if row.name == loja_idx else '' for _ in row]
        
        st.dataframe(
            ranking_context[["Posição", "NomeLoja", "LacunaRL"]],
            use_container_width=True,
            hide_index=True
        )
        
        posicao_atual = loja_idx + 1
        total_lojas = len(cluster_ranking)
        percentil = (total_lojas - posicao_atual) / total_lojas * 100
        
        st.info(f"📍 **{loja_selecionada}** está na posição **{posicao_atual}** de **{total_lojas}** lojas (percentil {percentil:.1f})")

# Dados históricos (se disponível)
if "daily_data" in loja_details and loja_details["daily_data"]:
    st.subheader("📈 Evolução Temporal")
    
    daily_data = pd.DataFrame(loja_details["daily_data"])
    
    if "datavenda" in daily_data.columns:
        # Preparar dados para gráfico de tendência
        daily_data["datavenda"] = pd.to_datetime(daily_data["datavenda"])
        daily_data = daily_data.sort_values("datavenda")
        
        # Selecionar métrica para visualização
        metricas_disponiveis = [col for col in ["receita_liquida", "qtd_cupom", "qtd_item"] 
                               if col in daily_data.columns]
        
        if metricas_disponiveis:
            metrica_selecionada = st.selectbox(
                "Selecione a métrica:",
                metricas_disponiveis,
                format_func=lambda x: x.replace("_", " ").title()
            )
            
            fig_trend = viz.create_trend_chart(daily_data, metrica_selecionada)
            st.plotly_chart(fig_trend, use_container_width=True)

# Recomendações baseadas na análise
st.subheader("💡 Insights e Recomendações")

insights = []

# Análise da lacuna principal
if lacuna_rl < -10000:  # Lacuna significativa
    insights.append("🎯 **Oportunidade Alta**: Lacuna de RL significativa identificada")
    
    if abs(lacuna_cupom) > abs(lacuna_bm):
        insights.append("🧾 **Foco em Cupom**: A lacuna é principalmente devido ao número de vendas")
        insights.append("📢 **Ação Sugerida**: Trabalhar estratégias de atração e conversão de clientes")
    else:
        insights.append("💳 **Foco em Boleto Médio**: A lacuna é principalmente devido ao valor por venda")
        insights.append("🎁 **Ação Sugerida**: Trabalhar cross-sell, up-sell e mix de produtos")

elif lacuna_rl > 10000:  # Performance acima da média
    insights.append("⭐ **Destaque Positivo**: Performance acima da mediana do cluster")
    insights.append("🏆 **Benchmark**: Esta loja pode ser referência para outras do cluster")

else:  # Performance próxima da média
    insights.append("➖ **Performance Equilibrada**: Próxima da mediana do cluster")
    insights.append("🔍 **Análise Fina**: Verificar oportunidades pontuais de melhoria")

# Mostrar insights
for insight in insights:
    st.write(insight)

if not insights:
    st.info("💭 Análise de insights em desenvolvimento...")

# Navegação
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🏠 Voltar ao Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🎯 Análise de Lacunas", use_container_width=True):
        st.switch_page("pages/2_Analise_Lacunas.py")

with col3:
    if st.button("👥 Análise Clusters", use_container_width=True):
        st.switch_page("pages/4_Clusters.py")
