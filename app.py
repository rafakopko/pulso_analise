"""
Dashboard Pulso - Aplicação Principal
Análise de Lacunas Comerciais para Varejo

Desenvolvido para automatizar o relatório gerencial do Projeto Pulso
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from config import PAGE_CONFIG, MESSAGES, UPLOAD_DIR
from src.data_loader import DataLoader, load_sample_data, check_default_base_exists, load_default_base_if_exists
from src.calculations import LacunaCalculator
from src.visualizations import PulsoVisualizations
from src.utils import (
    setup_logging, ensure_directories, initialize_session_state,
    SessionManager, show_data_info, clear_cache
)

# Configuração da página
st.set_page_config(**PAGE_CONFIG)

# Setup inicial
setup_logging()
ensure_directories()
initialize_session_state()

# Carregamento automático da base padrão se não houver dados carregados
if not SessionManager.is_data_loaded() and check_default_base_exists():
    with st.spinner("🔄 Carregando base padrão..."):
        default_data = load_default_base_if_exists()
        if default_data:
            loader = DataLoader()
            # Usar os metadados criados na função load_default_base
            SessionManager.save_data(default_data, loader.metadata)
            st.success("✅ Base padrão carregada automaticamente!")
            st.rerun()

# Sidebar
st.sidebar.title("🎯 Dashboard Pulso")
st.sidebar.markdown("---")

# Header principal
st.title("📊 Dashboard Pulso")
st.markdown("### Análise de Lacunas Comerciais - Projeto Pulso")
st.markdown("---")

# Seção de upload de arquivos
st.header("📁 Carregamento de Dados")

# Verificar se há dados carregados para mostrar informações
if SessionManager.is_data_loaded():
    metadata = SessionManager.get_metadata()
    source = metadata.get('source', 'upload')
    if source == 'base_padrao':
        st.info("📊 **Base padrão carregada.** Você pode fazer upload de uma nova base para atualizar os dados.")
    else:
        st.info("📊 **Dados carregados.** Você pode fazer upload de uma nova base para atualizar os dados.")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Faça upload do arquivo Excel para atualizar a base (Pulso _ Acompanhamento Gerencial.xlsx)",
        type=['xlsx', 'xls'],
        help="Selecione o arquivo Excel com os dados do Pulso"
    )

with col2:
    if check_default_base_exists() and st.button("🔄 Recarregar Base Padrão", help="Recarregar a base padrão"):
        with st.spinner("Recarregando base padrão..."):
            default_data = load_default_base_if_exists()
            if default_data:
                loader = DataLoader()
                SessionManager.save_data(default_data, loader.metadata)
                st.success("✅ Base padrão recarregada!")
                st.rerun()

# Processar upload
if uploaded_file is not None:
    loader = DataLoader()
    
    # Verificar se é um arquivo novo
    current_file = SessionManager.get_metadata().get("file_name")
    if current_file != uploaded_file.name:
        with st.spinner("🔄 Processando arquivo..."):
            data = loader.load_excel_data(uploaded_file)
            
            if data:
                # Salvar na sessão
                SessionManager.save_data(data, loader.metadata)
                st.success(MESSAGES["upload_success"])
                st.rerun()

# Verificar se há dados carregados
if SessionManager.is_data_loaded():
    data = SessionManager.get_data()
    metadata = SessionManager.get_metadata()
    
    # Informações do arquivo carregado
    st.sidebar.success("✅ Dados Carregados")
    st.sidebar.info(f"📄 **Arquivo:** {metadata.get('file_name', 'N/A')}")
    st.sidebar.info(f"📅 **Carregado:** {metadata.get('upload_time', 'N/A')}")
    
    if st.sidebar.button("🗑️ Limpar Dados"):
        SessionManager.clear_session()
        clear_cache()
        st.rerun()
    
    # Calcular métricas
    calculator = LacunaCalculator(data)
    metrics = calculator.calculate_all_metrics()
    
    if metrics and "error" not in metrics:
        # Criar visualizações
        viz = PulsoVisualizations()
        
        # KPIs principais
        st.header("📊 Indicadores Principais")
        viz.create_kpi_cards(metrics)
        
        st.markdown("---")
        
        # Layout principal com colunas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Maiores Oportunidades")
            top_opp = metrics.get("top_oportunidades", pd.DataFrame())
            if not top_opp.empty:
                fig_opp = viz.create_top_opportunities_chart(top_opp)
                st.plotly_chart(fig_opp, use_container_width=True)
                
                # Tabela das oportunidades
                st.write("**Detalhamento:**")
                display_cols = ["Rank", "NomeLoja", "grupo_comparavel", "LacunaRL"]
                if all(col in top_opp.columns for col in display_cols):
                    st.dataframe(
                        top_opp[display_cols].head(5),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.info("Nenhuma oportunidade encontrada")
        
        with col2:
            st.subheader("📈 Análise por Clusters")
            cluster_analysis = metrics.get("analise_clusters", pd.DataFrame())
            if not cluster_analysis.empty:
                fig_cluster = viz.create_cluster_analysis_chart(cluster_analysis)
                st.plotly_chart(fig_cluster, use_container_width=True)
                
                # Tabela dos clusters
                st.write("**Resumo por Cluster:**")
                display_cols = ["grupo_comparavel", "Qtd_Lojas", "LacunaRL_Total"]
                if all(col in cluster_analysis.columns for col in display_cols):
                    st.dataframe(
                        cluster_analysis[display_cols].head(5),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.info("Dados de cluster não disponíveis")
        
        # Decomposição de lacunas
        st.header("💡 Decomposição de Lacunas")
        waterfall_data = calculator.calculate_waterfall_data()
        if waterfall_data:
            fig_waterfall = viz.create_waterfall_chart(waterfall_data, "Decomposição Total de Lacunas")
            st.plotly_chart(fig_waterfall, use_container_width=True)
        else:
            st.info("Dados insuficientes para decomposição")
        
        # Análise por GR (se disponível)
        gr_analysis = metrics.get("analise_gr")
        if gr_analysis is not None and not gr_analysis.empty:
            st.header("🏢 Performance por Gerência Regional")
            fig_gr = viz.create_gr_comparison_chart(gr_analysis)
            st.plotly_chart(fig_gr, use_container_width=True)
          # Seção de dados detalhados (expansível)
        with st.expander("📋 Dados Detalhados"):
            show_data_info(data, use_expanders=False)
          # Navegação para outras páginas
        st.markdown("---")
        st.subheader("🔗 Análises Detalhadas")
        
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
        
        with nav_col1:
            if st.button("🎯 Análise de Lacunas", use_container_width=True):
                st.switch_page("pages/2_Analise_Lacunas.py")
        
        with nav_col2:
            if st.button("🏪 Visão por Loja", use_container_width=True):
                st.switch_page("pages/3_Visao_Loja.py")
        
        with nav_col3:
            if st.button("👥 Análise Clusters", use_container_width=True):
                st.switch_page("pages/4_Clusters.py")
        
        with nav_col4:
            if st.button("📈 Exportar Dados", use_container_width=True):
                st.switch_page("pages/5_Exportar.py")
    
    else:
        st.error("❌ Erro no processamento dos dados")
        if "error" in metrics:
            st.error(f"Detalhes: {metrics['error']}")

else:
    # Página inicial - sem dados
    st.info(MESSAGES["no_data"])
    
    # Instruções
    st.markdown("""
    ### 📖 Como usar este dashboard:
    
    1. **Upload de Dados**: Faça upload do arquivo Excel "Pulso _ Acompanhamento Gerencial .xlsx"
    2. **Análise Automática**: O sistema processará os dados e calculará automaticamente as lacunas
    3. **Navegação**: Use as páginas específicas para análises detalhadas
    4. **Exportação**: Gere relatórios personalizados na aba de exportação
    
    ### 🎯 Sobre o Projeto Pulso:
    
    O Projeto Pulso é um sistema inovador de gestão comercial que identifica lacunas de vendas 
    através de comparação inteligente entre lojas similares (clusters).
    
    **Principais Métricas:**
    - **Lacuna de RL**: Diferença na Receita Líquida vs. mediana do cluster
    - **Lacuna de Cupom**: Gap na quantidade de vendas
    - **Lacuna de BM**: Diferença no Boleto Médio
    - **Lacuna de PM**: Gap no Preço Médio
    - **Lacuna de Prod**: Diferença na Produtividade
    
    ### 📊 Dados de Exemplo:
    
    Clique em "Usar Dados de Exemplo" para explorar o dashboard com dados fictícios.
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Dashboard Pulso v1.0 | Análise de Lacunas Comerciais<br>
        Desenvolvido para automação do relatório gerencial
    </div>
    """, 
    unsafe_allow_html=True
)
