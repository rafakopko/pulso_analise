"""
Módulo para criação de visualizações e gráficos
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Tuple
import numpy as np

from config import COLOR_PALETTE, NUMBER_FORMATS


class PulsoVisualizations:
    """Classe para criação de visualizações específicas do Projeto Pulso"""
    
    def __init__(self):
        self.colors = COLOR_PALETTE
        self.default_layout = {
            "font": {"family": "Arial, sans-serif", "size": 12},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "margin": {"l": 50, "r": 50, "t": 50, "b": 50}
        }
    
    def create_kpi_cards(self, metrics: Dict) -> None:
        """
        Cria cards de KPIs principais
        
        Args:
            metrics: Métricas calculadas
        """
        if not metrics:
            st.warning("Nenhuma métrica disponível")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            lacuna_total = metrics.get("lacuna_total_rl", 0)
            st.metric(
                label="💰 Lacuna Total RL",
                value=NUMBER_FORMATS["currency"].format(lacuna_total),
                delta=None
            )
        
        with col2:
            percentual_captura = metrics.get("percentual_captura", 0)
            st.metric(
                label="🎯 % Captura",
                value=NUMBER_FORMATS["percentage"].format(percentual_captura),
                delta=None
            )
        
        with col3:
            lojas_lacuna = metrics.get("lojas_com_lacuna", 0)
            total_lojas = metrics.get("total_lojas", 1)
            st.metric(
                label="🏪 Lojas c/ Lacuna",
                value=f"{lojas_lacuna}/{total_lojas}",
                delta=f"{(lojas_lacuna/total_lojas*100):.1f}%" if total_lojas > 0 else "0%"
            )
        
        with col4:
            lacuna_cupom = metrics.get("lacuna_total_cupom", 0)
            st.metric(
                label="🧾 Lacuna Cupom",
                value=NUMBER_FORMATS["integer"].format(lacuna_cupom),
                delta=None
            )
    
    def create_waterfall_chart(self, waterfall_data: Dict, title: str = "Decomposição de Lacunas") -> go.Figure:
        """
        Cria gráfico waterfall para decomposição de lacunas
        
        Args:
            waterfall_data: Dados do waterfall
            title: Título do gráfico
            
        Returns:
            go.Figure: Gráfico waterfall
        """
        if not waterfall_data:
            return go.Figure()
        
        fig = go.Figure(go.Waterfall(
            name="Lacunas",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "total"],
            x=waterfall_data["categories"],
            textposition="outside",
            text=[NUMBER_FORMATS["currency"].format(v) for v in waterfall_data["values"]],
            y=waterfall_data["values"],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": self.colors["success"]}},
            decreasing={"marker": {"color": self.colors["danger"]}},
            totals={"marker": {"color": self.colors["primary"]}}
        ))
        
        fig.update_layout(
            title=title,
            showlegend=False,
            **self.default_layout
        )
        
        return fig
    
    def create_top_opportunities_chart(self, opportunities_df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de barras das principais oportunidades
        
        Args:
            opportunities_df: DataFrame com oportunidades
            
        Returns:
            go.Figure: Gráfico de barras
        """
        if opportunities_df.empty:
            return go.Figure()
        
        # Preparar dados
        x_values = opportunities_df["NomeLoja"]
        y_values = opportunities_df["LacunaRL_Abs"] if "LacunaRL_Abs" in opportunities_df.columns else abs(opportunities_df["LacunaRL"])
        
        fig = px.bar(
            x=y_values,
            y=x_values,
            orientation='h',
            title="🎯 Top 10 Maiores Oportunidades",
            labels={"x": "Lacuna RL (R$)", "y": "Loja"},
            color=y_values,
            color_continuous_scale="Reds"
        )
        
        fig.update_layout(
            **self.default_layout,
            height=400,
            showlegend=False
        )
          # Adicionar valores nas barras
        fig.update_traces(
            texttemplate='R$ %{y:,.0f}',
            textposition='outside'
        )
        
        return fig
    
    def create_cluster_analysis_chart(self, cluster_df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de análise por clusters
        
        Args:
            cluster_df: DataFrame com análise por cluster
            
        Returns:
            go.Figure: Gráfico de dispersão
        """
        if cluster_df.empty:
            return go.Figure()
        
        fig = px.scatter(
            cluster_df,
            x="Qtd_Lojas",
            y="LacunaRL_Total",
            size="LacunaRL_Potencial" if "LacunaRL_Potencial" in cluster_df.columns else "Qtd_Lojas",
            color="grupo_comparavel" if "grupo_comparavel" in cluster_df.columns else None,
            hover_data=["LacunaRL_Media"] if "LacunaRL_Media" in cluster_df.columns else None,
            title="📊 Análise de Clusters - Lacuna vs Quantidade de Lojas"
        )
        
        fig.update_layout(
            **self.default_layout,
            height=500,
            xaxis_title="Quantidade de Lojas",
            yaxis_title="Lacuna Total RL (R$)"
        )
        
        return fig
    
    def create_loja_radar_chart(self, loja_data: Dict, cluster_comparison: Dict) -> go.Figure:
        """
        Cria gráfico radar para comparação da loja com cluster
        
        Args:
            loja_data: Dados da loja
            cluster_comparison: Dados de comparação com cluster
            
        Returns:
            go.Figure: Gráfico radar
        """
        if not loja_data or not cluster_comparison:
            return go.Figure()
        
        # Métricas para o radar
        metrics = ["LacunaRL", "LacunaCupom", "LacunaBM", "LacunaPM", "LacunaProd"]
        loja_values = [loja_data.get(metric, 0) for metric in metrics]
        cluster_values = [cluster_comparison.get(f"cluster_median_{metric.lower()}", 0) for metric in metrics]
        
        # Normalizar valores para melhor visualização
        max_vals = [max(abs(lv), abs(cv)) for lv, cv in zip(loja_values, cluster_values)]
        loja_normalized = [lv/mv if mv != 0 else 0 for lv, mv in zip(loja_values, max_vals)]
        cluster_normalized = [cv/mv if mv != 0 else 0 for cv, mv in zip(cluster_values, max_vals)]
        
        fig = go.Figure()
        
        # Adicionar loja
        fig.add_trace(go.Scatterpolar(
            r=loja_normalized,
            theta=metrics,
            fill='toself',
            name='Loja',
            line_color=self.colors["primary"]
        ))
        
        # Adicionar mediana do cluster
        fig.add_trace(go.Scatterpolar(
            r=cluster_normalized,
            theta=metrics,
            fill='toself',
            name='Mediana Cluster',
            line_color=self.colors["secondary"],
            opacity=0.6
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[-1, 1]
                )),
            showlegend=True,
            title="🎯 Performance vs Cluster",
            **self.default_layout
        )
        
        return fig
    
    def create_trend_chart(self, trend_data: pd.DataFrame, metric: str = "receita_liquida") -> go.Figure:
        """
        Cria gráfico de tendência temporal
        
        Args:
            trend_data: DataFrame com dados temporais
            metric: Métrica a ser plotada
            
        Returns:
            go.Figure: Gráfico de linha
        """
        if trend_data.empty or metric not in trend_data.columns:
            return go.Figure()
        
        fig = px.line(
            trend_data,
            x="datavenda",
            y=metric,
            title=f"📈 Evolução de {metric.replace('_', ' ').title()}",
            markers=True
        )
        
        fig.update_layout(
            **self.default_layout,
            height=400,
            xaxis_title="Data",
            yaxis_title=metric.replace('_', ' ').title()
        )
        
        return fig
    
    def create_gr_comparison_chart(self, gr_df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de comparação entre GRs
        
        Args:
            gr_df: DataFrame com análise por GR
            
        Returns:
            go.Figure: Gráfico de barras
        """
        if gr_df.empty:
            return go.Figure()
        
        fig = px.bar(
            gr_df,
            x="NumeroGR",
            y="LacunaRL_Total",
            title="🏢 Comparativo por Gerência Regional",
            color="LacunaRL_Total",
            color_continuous_scale="RdYlGn_r",
            text="LacunaRL_Total"
        )
        
        fig.update_layout(
            **self.default_layout,
            height=400,
            xaxis_title="Gerência Regional",
            yaxis_title="Lacuna Total RL (R$)"
        )
        
        # Formatar texto nas barras
        fig.update_traces(
            texttemplate=NUMBER_FORMATS["currency"],
            textposition='outside'
        )
        
        return fig
    
    def create_distribution_histogram(self, df: pd.DataFrame, column: str, title: str = None) -> go.Figure:
        """
        Cria histograma de distribuição
        
        Args:
            df: DataFrame com dados
            column: Coluna para histograma
            title: Título do gráfico
            
        Returns:
            go.Figure: Histograma
        """
        if df.empty or column not in df.columns:
            return go.Figure()
        
        fig = px.histogram(
            df,
            x=column,
            nbins=20,
            title=title or f"Distribuição de {column}",
            color_discrete_sequence=[self.colors["primary"]]
        )
        
        # Adicionar linha da média
        mean_val = df[column].mean()
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color=self.colors["danger"],
            annotation_text=f"Média: {mean_val:.2f}"
        )
        
        fig.update_layout(
            **self.default_layout,
            height=400
        )
        
        return fig
    
    def create_correlation_heatmap(self, df: pd.DataFrame, columns: List[str]) -> go.Figure:
        """
        Cria heatmap de correlação
        
        Args:
            df: DataFrame com dados
            columns: Colunas para correlação
            
        Returns:
            go.Figure: Heatmap
        """
        if df.empty:
            return go.Figure()
        
        # Filtrar apenas colunas numéricas existentes
        numeric_cols = [col for col in columns if col in df.columns and df[col].dtype in ['int64', 'float64']]
        
        if len(numeric_cols) < 2:
            return go.Figure()
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="🔗 Matriz de Correlação"
        )
        
        fig.update_layout(
            **self.default_layout,
            height=500
        )
        
        return fig


def format_number(value: float, format_type: str = "currency") -> str:
    """
    Formata números de acordo com o tipo especificado
    
    Args:
        value: Valor a ser formatado
        format_type: Tipo de formatação
        
    Returns:
        str: Valor formatado
    """
    if pd.isna(value):
        return "N/A"
    
    return NUMBER_FORMATS.get(format_type, "{:,.2f}").format(value)


def create_summary_table(df: pd.DataFrame, group_by: str, metrics: List[str]) -> pd.DataFrame:
    """
    Cria tabela resumo agrupada
    
    Args:
        df: DataFrame com dados
        group_by: Coluna para agrupar
        metrics: Métricas a agregar
        
    Returns:
        pd.DataFrame: Tabela resumo
    """
    if df.empty or group_by not in df.columns:
        return pd.DataFrame()
    
    available_metrics = [m for m in metrics if m in df.columns]
    
    if not available_metrics:
        return pd.DataFrame()
    
    summary = df.groupby(group_by)[available_metrics].agg(['sum', 'mean', 'count']).round(2)
    
    return summary
