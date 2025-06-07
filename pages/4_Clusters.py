import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from src.data_loader import DataLoader
    from src.calculations import LacunaCalculator
    from src.visualizations import PulsoVisualizations
    from src.utils import SessionManager, format_currency, format_percentage
    import config
    APP_CONFIG = config
except ImportError as e:
    st.error(f"Erro de importação: {e}")
    st.stop()

st.set_page_config(
    page_title="Análise de Clusters - Projeto Pulso",
    page_icon="👥",
    layout="wide"
)

def perform_clustering(df, n_clusters=None, features=None):
    """
    Realiza análise de clustering nas lojas
    """
    if features is None:
        features = ['RL', 'BM', 'PM', 'Cupom', 'Prod']
    
    # Preparar dados para clustering
    cluster_data = df[features].copy()
    cluster_data = cluster_data.fillna(cluster_data.mean())
    
    # Normalizar dados
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)
    
    # Determinar número ideal de clusters se não especificado
    if n_clusters is None:
        n_clusters = determine_optimal_clusters(scaled_data)
    
    # Aplicar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    # Adicionar clusters ao dataframe
    df_clustered = df.copy()
    df_clustered['Cluster'] = clusters
    df_clustered['Cluster_Label'] = [f'Cluster {i+1}' for i in clusters]
    
    # Calcular centróides
    centroids = pd.DataFrame(
        scaler.inverse_transform(kmeans.cluster_centers_),
        columns=features
    )
    centroids['Cluster'] = range(n_clusters)
    centroids['Cluster_Label'] = [f'Cluster {i+1}' for i in range(n_clusters)]
    
    return df_clustered, centroids, features, scaler

def determine_optimal_clusters(data, max_clusters=8):
    """
    Determina o número ideal de clusters usando método do cotovelo
    """
    inertias = []
    K_range = range(2, min(max_clusters + 1, len(data)))
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
      # Método do cotovelo simplificado
    if len(inertias) >= 3:
        # Calcular diferenças de segunda ordem
        diffs = np.diff(inertias)
        second_diffs = np.diff(diffs)
        
        # Encontrar o ponto de maior curvatura
        if len(second_diffs) > 0:
            optimal_k = int(np.argmax(second_diffs)) + 3  # +3 porque começamos do 2 e perdemos 2 índices
        else:
            optimal_k = 3
    else:
        optimal_k = 3
    
    return int(min(optimal_k, max_clusters))

def create_cluster_visualization(df_clustered, centroids, features):
    """
    Cria visualizações de clustering
    """
    # 1. Scatter plot 2D (PCA)
    pca = PCA(n_components=2)
    scaled_data = StandardScaler().fit_transform(df_clustered[features].fillna(df_clustered[features].mean()))
    pca_data = pca.fit_transform(scaled_data)
    
    fig_pca = px.scatter(
        x=pca_data[:, 0], 
        y=pca_data[:, 1],
        color=df_clustered['Cluster_Label'],
        hover_data={'Loja': df_clustered['Loja']},
        title="Distribuição dos Clusters (PCA 2D)",
        labels={'x': f'PC1 ({pca.explained_variance_ratio_[0]:.1%} da variância)',
                'y': f'PC2 ({pca.explained_variance_ratio_[1]:.1%} da variância)'}
    )
    fig_pca.update_layout(height=500)
    
    # 2. Radar chart dos centróides
    fig_radar = go.Figure()
    
    for _, centroid in centroids.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[centroid[feature] for feature in features],
            theta=features,
            fill='toself',
            name=centroid['Cluster_Label'],
            opacity=0.7
        ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, None])
        ),
        title="Perfil dos Clusters - Centróides",
        height=500
    )
    
    # 3. Boxplot por feature
    fig_box = make_subplots(
        rows=2, cols=3,
        subplot_titles=features,
        vertical_spacing=0.12
    )
    
    positions = [(1,1), (1,2), (1,3), (2,1), (2,2)]
    
    for i, feature in enumerate(features):
        if i < len(positions):
            row, col = positions[i]
            
            for cluster_label in df_clustered['Cluster_Label'].unique():
                cluster_data = df_clustered[df_clustered['Cluster_Label'] == cluster_label]
                
                fig_box.add_trace(
                    go.Box(
                        y=cluster_data[feature],
                        name=cluster_label,
                        showlegend=(i == 0)
                    ),
                    row=row, col=col
                )
    
    fig_box.update_layout(
        title="Distribuição das Métricas por Cluster",
        height=600
    )
    
    return fig_pca, fig_radar, fig_box

def analyze_cluster_characteristics(df_clustered, centroids):
    """
    Analisa características de cada cluster
    """
    cluster_stats = []
    
    for cluster_id in sorted(df_clustered['Cluster'].unique()):
        cluster_data = df_clustered[df_clustered['Cluster'] == cluster_id]
        
        stats = {
            'Cluster': f'Cluster {cluster_id + 1}',
            'Qtd_Lojas': len(cluster_data),
            'RL_Medio': cluster_data['RL'].mean(),
            'BM_Medio': cluster_data['BM'].mean(),
            'PM_Medio': cluster_data['PM'].mean(),
            'Cupom_Medio': cluster_data['Cupom'].mean(),
            'Prod_Medio': cluster_data['Prod'].mean(),
            'Lojas': ', '.join(cluster_data['Loja'].tolist()[:5]) + ('...' if len(cluster_data) > 5 else '')
        }
        
        cluster_stats.append(stats)
    
    return pd.DataFrame(cluster_stats)

def main():
    st.title("👥 Análise de Clusters")
    st.markdown("Análise de agrupamento de lojas com características similares")
    
    # Verificar se há dados carregados
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("⚠️ Nenhum dado carregado. Por favor, carregue os dados na página inicial.")
        if st.button("🏠 Voltar para página inicial"):
            st.switch_page("app.py")
        return
    
    df = st.session_state.data.copy()
    
    # Sidebar com controles
    st.sidebar.header("Configurações do Clustering")
    
    # Seleção de features
    available_features = ['RL', 'BM', 'PM', 'Cupom', 'Prod']
    selected_features = st.sidebar.multiselect(
        "Selecione as métricas para clustering:",
        available_features,
        default=available_features
    )
    
    if len(selected_features) < 2:
        st.error("Selecione pelo menos 2 métricas para análise de clustering.")
        return
    
    # Número de clusters
    auto_clusters = st.sidebar.checkbox("Determinar automaticamente o número de clusters", value=True)
    
    if not auto_clusters:
        n_clusters = st.sidebar.slider("Número de clusters:", 2, 8, 4)
    else:
        n_clusters = None
    
    # Botão para executar clustering
    if st.sidebar.button("🔄 Executar Análise de Clusters", type="primary"):
        with st.spinner("Executando análise de clustering..."):
            try:
                # Realizar clustering
                df_clustered, centroids, features_used, scaler = perform_clustering(
                    df, n_clusters, selected_features
                )
                
                # Salvar resultados na sessão
                st.session_state.df_clustered = df_clustered
                st.session_state.centroids = centroids
                st.session_state.features_used = features_used
                
                st.success(f"✅ Clustering executado com sucesso! {len(centroids)} clusters identificados.")
                
            except Exception as e:
                st.error(f"Erro ao executar clustering: {str(e)}")
                return
    
    # Verificar se há resultados de clustering
    if 'df_clustered' not in st.session_state:
        st.info("👆 Configure os parâmetros na barra lateral e execute a análise de clusters.")
        return
    
    df_clustered = st.session_state.df_clustered
    centroids = st.session_state.centroids
    features_used = st.session_state.features_used
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Visualizações dos Clusters")
        
        # Tabs para diferentes visualizações
        tab1, tab2, tab3 = st.tabs(["🎯 Distribuição 2D", "📡 Perfil dos Clusters", "📈 Distribuições"])
        
        with tab1:
            fig_pca, fig_radar, fig_box = create_cluster_visualization(df_clustered, centroids, features_used)
            st.plotly_chart(fig_pca, use_container_width=True)
        
        with tab2:
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with tab3:
            st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        st.subheader("📋 Resumo dos Clusters")
        
        cluster_stats = analyze_cluster_characteristics(df_clustered, centroids)
        
        for _, cluster in cluster_stats.iterrows():
            with st.container():
                st.markdown(f"**{cluster['Cluster']}**")
                st.metric("Lojas", cluster['Qtd_Lojas'])
                st.metric("RL Médio", format_currency(cluster['RL_Medio']))
                st.metric("BM Médio", format_currency(cluster['BM_Medio']))
                
                with st.expander("Ver lojas"):
                    st.text(cluster['Lojas'])
                
                st.markdown("---")
    
    # Tabela detalhada
    st.subheader("📊 Dados Detalhados por Cluster")
    
    # Filtro por cluster
    selected_cluster = st.selectbox(
        "Selecione um cluster para análise detalhada:",
        ['Todos'] + sorted(df_clustered['Cluster_Label'].unique())
    )
    
    if selected_cluster == 'Todos':
        display_df = df_clustered
    else:
        display_df = df_clustered[df_clustered['Cluster_Label'] == selected_cluster]
    
    # Configurar colunas para exibição
    display_columns = ['Loja', 'Cluster_Label'] + features_used
    
    # Formatar dados para exibição
    display_data = display_df[display_columns].copy()
    
    for col in features_used:
        if col in ['RL', 'BM', 'PM']:
            display_data[col] = display_data[col].apply(lambda x: format_currency(x) if pd.notna(x) else '-')
        else:
            display_data[col] = display_data[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else '-')
    
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Estatísticas do cluster selecionado
    if selected_cluster != 'Todos':
        st.subheader(f"📈 Estatísticas - {selected_cluster}")
        
        cluster_data = df_clustered[df_clustered['Cluster_Label'] == selected_cluster]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "RL Médio",
                format_currency(cluster_data['RL'].mean()),
                f"σ: {format_currency(cluster_data['RL'].std())}"
            )
        
        with col2:
            st.metric(
                "BM Médio",
                format_currency(cluster_data['BM'].mean()),
                f"σ: {format_currency(cluster_data['BM'].std())}"
            )
        
        with col3:
            st.metric(
                "PM Médio",
                format_currency(cluster_data['PM'].mean()),
                f"σ: {format_currency(cluster_data['PM'].std())}"
            )
        
        with col4:
            st.metric(
                "Cupom Médio",
                f"{cluster_data['Cupom'].mean():,.0f}",
                f"σ: {cluster_data['Cupom'].std():,.0f}"
            )
        
        with col5:
            st.metric(
                "Prod Médio",
                f"{cluster_data['Prod'].mean():,.1f}",
                f"σ: {cluster_data['Prod'].std():,.1f}"
            )

if __name__ == "__main__":
    main()
