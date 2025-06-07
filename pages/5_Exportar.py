import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from src.utils import format_currency, format_percentage
    import config
    APP_CONFIG = config
except ImportError as e:
    st.error(f"Erro de importação: {e}")
    st.stop()

st.set_page_config(
    page_title="Exportar Relatórios - Projeto Pulso",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("📈 Visualizar Dados")
    st.markdown("Visualize os dados carregados e use a função de impressão do navegador para exportar como PDF")
    
    # Verificar se há dados carregados
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("⚠️ Nenhum dado carregado. Por favor, carregue os dados na página inicial.")
        if st.button("🏠 Voltar para página inicial"):
            st.switch_page("app.py")
        return
    
    df = st.session_state.data
    
    # Obter dados de outras análises se disponíveis
    gaps_df = st.session_state.get('gaps_data', None)
    clusters_df = st.session_state.get('df_clustered', None)
    
    # Obter DataFrame principal para visualização
    if isinstance(df, dict):
        # Pegar o primeiro DataFrame disponível ou o mais relevante
        if "pulso_consulta_diaria" in df:
            main_df = df["pulso_consulta_diaria"]
        elif "pulso_consulta_diaria_cluster_antigo" in df:
            main_df = df["pulso_consulta_diaria_cluster_antigo"]
        else:
            main_df = list(df.values())[0]  # Primeiro DataFrame disponível
    else:
        main_df = df
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Resumo dos Dados Disponíveis")
        
        # Cards informativos
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Total de Lojas", len(main_df))
        
        with col_b:
            st.metric("Análise de Gaps", "Disponível" if gaps_df is not None else "Não realizada")
        
        with col_c:
            st.metric("Clustering", "Disponível" if clusters_df is not None else "Não realizado")
        
        # Prévia dos dados
        st.subheader("👀 Prévia dos Dados")
        tab1, tab2, tab3 = st.tabs(["📋 Dados Principais", "🎯 Gaps", "👥 Clusters"])
        
        with tab1:
            st.dataframe(main_df.head(10), use_container_width=True)
        
        with tab2:
            if gaps_df is not None:
                st.dataframe(gaps_df.head(10), use_container_width=True)
            else:
                st.info("Análise de gaps não foi realizada. Vá para a página 'Análise de Lacunas' para gerar.")
        
        with tab3:
            if clusters_df is not None:
                cluster_summary = clusters_df.groupby('Cluster_Label').size().reset_index(name='Qtd_Lojas')
                st.dataframe(cluster_summary, use_container_width=True)
            else:
                st.info("Análise de clusters não foi realizada. Vá para a página 'Clusters' para gerar.")
    
    with col2:
        st.subheader("📝 Exportação")
        
        st.markdown("""
        **Como exportar:**
        1. Use Ctrl+P (ou Cmd+P no Mac)
        2. Selecione "Salvar como PDF"
        3. Ajuste as configurações conforme necessário
        4. Clique em "Salvar"
        """)
        
        st.info("💡 Dica: Para melhor resultado, use 'Paisagem' como orientação da página")
    
    # Seção de estatísticas detalhadas
    st.markdown("---")
    st.subheader("📈 Estatísticas Detalhadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Métricas Principais")
        
        stats_data = []
        for metric in ['RL', 'BM', 'PM', 'Cupom', 'Prod']:
            if metric in main_df.columns:
                stats_data.append({
                    'Métrica': metric,
                    'Média': main_df[metric].mean(),
                    'Mediana': main_df[metric].median(),
                    'Desvio': main_df[metric].std(),
                    'Mín': main_df[metric].min(),
                    'Máx': main_df[metric].max()
                })
        
        if stats_data:
            stats_df = pd.DataFrame(stats_data)
            
            # Formatar valores monetários
            for col in ['Média', 'Mediana', 'Desvio', 'Mín', 'Máx']:
                stats_df[f'{col}_Formatted'] = stats_df.apply(
                    lambda row: format_currency(row[col]) if row['Métrica'] in ['RL', 'BM', 'PM'] 
                    else f"{row[col]:,.2f}", axis=1
                )
            
            display_stats = stats_df[['Métrica', 'Média_Formatted', 'Mediana_Formatted', 'Desvio_Formatted']].copy()
            display_stats.columns = ['Métrica', 'Média', 'Mediana', 'Desvio Padrão']
            
            st.dataframe(display_stats, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Top 5 Lojas por RL")
        
        if 'RL' in main_df.columns:
            top_lojas = main_df.nlargest(5, 'RL')[['Loja', 'RL']].copy()
            if 'BM' in main_df.columns:
                top_lojas = main_df.nlargest(5, 'RL')[['Loja', 'RL', 'BM']].copy()
            if 'Cupom' in main_df.columns:
                top_lojas = main_df.nlargest(5, 'RL')[['Loja', 'RL', 'BM', 'Cupom']].copy()
            
            # Formatar valores
            top_lojas['RL'] = top_lojas['RL'].apply(format_currency)
            if 'BM' in top_lojas.columns:
                top_lojas['BM'] = top_lojas['BM'].apply(format_currency)
            if 'Cupom' in top_lojas.columns:
                top_lojas['Cupom'] = top_lojas['Cupom'].apply(lambda x: f"{x:,.0f}")
            
            st.dataframe(top_lojas, use_container_width=True, hide_index=True)
        else:
            st.info("Dados de RL não disponíveis")
    
    # Informações adicionais
    st.markdown("---")
    st.markdown("#### ℹ️ Informações dos Dados")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown(f"""
        **Resumo dos Dados:**
        - **Total de Lojas:** {len(main_df)}
        - **Colunas Disponíveis:** {len(main_df.columns)}
        - **Data de Processamento:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """)
    
    with info_col2:
        st.markdown("""
        **Análises Realizadas:**
        - ✅ Dados Carregados
        - {} Análise de Gaps
        - {} Clustering de Lojas
        """.format(
            "✅" if gaps_df is not None else "❌",
            "✅" if clusters_df is not None else "❌"
        ))

if __name__ == "__main__":
    main()
