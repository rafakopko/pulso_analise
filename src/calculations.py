"""
Módulo para cálculos de lacunas e métricas do Projeto Pulso
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)


class LacunaCalculator:
    """Classe para cálculos de lacunas e métricas derivadas"""
    
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.data = data
        self.df_diaria = data.get("pulso_consulta_diaria", pd.DataFrame())
        self.df_cluster = data.get("pulso_consulta_diaria_cluster_a", pd.DataFrame())
    
    def calculate_all_metrics(self) -> Dict[str, Any]:
        """
        Calcula todas as métricas principais do dashboard
        
        Returns:
            Dict: Métricas calculadas
        """
        metrics = {}
        
        if self.df_cluster.empty:
            return metrics
        
        try:
            # KPIs principais
            metrics["lacuna_total_rl"] = self.df_cluster["LacunaRL"].sum()
            metrics["lacuna_total_cupom"] = self.df_cluster["LacunaCupom"].sum()
            metrics["lacuna_total_bm"] = self.df_cluster["LacunaBM"].sum()
            
            # Percentual de captura (assumindo meta de 40%)
            total_lacuna_negativa = self.df_cluster[self.df_cluster["LacunaRL"] < 0]["LacunaRL"].sum()
            metrics["percentual_captura"] = 40.0  # Placeholder - seria calculado baseado em metas
            
            # Contadores
            metrics["total_lojas"] = len(self.df_cluster)
            metrics["lojas_com_lacuna"] = len(self.df_cluster[self.df_cluster["LacunaRL"] < 0])
            metrics["lojas_acima_meta"] = len(self.df_cluster[self.df_cluster["LacunaRL"] > 0])
            
            # Top oportunidades
            metrics["top_oportunidades"] = self.get_top_opportunities(10)
            metrics["top_destaques"] = self.get_top_performers(10)
            
            # Análise por cluster
            metrics["analise_clusters"] = self.analyze_by_cluster()
            
            # Análise por GR
            if "NumeroGR" in self.df_diaria.columns:
                metrics["analise_gr"] = self.analyze_by_gr()
            
            logger.info("Métricas calculadas com sucesso")
            
        except Exception as e:
            logger.error(f"Erro no cálculo de métricas: {str(e)}")
            metrics["error"] = str(e)
        
        return metrics
    
    def get_top_opportunities(self, n: int = 10) -> pd.DataFrame:
        """
        Retorna as maiores oportunidades (lacunas negativas)
        
        Args:
            n: Número de registros a retornar
            
        Returns:
            pd.DataFrame: Top oportunidades
        """
        if self.df_cluster.empty:
            return pd.DataFrame()
        
        # Filtrar apenas lacunas negativas (oportunidades)
        opportunities = self.df_cluster[self.df_cluster["LacunaRL"] < 0].copy()
        
        # Ordenar por maior lacuna (menor valor, pois são negativos)
        opportunities = opportunities.sort_values("LacunaRL").head(n)
        
        # Adicionar colunas calculadas
        opportunities["LacunaRL_Abs"] = abs(opportunities["LacunaRL"])
        opportunities["Rank"] = range(1, len(opportunities) + 1)
        
        return opportunities[["Rank", "NomeLoja", "grupo_comparavel", "LacunaRL", "LacunaRL_Abs", "LacunaCupom", "LacunaBM"]]
    
    def get_top_performers(self, n: int = 10) -> pd.DataFrame:
        """
        Retorna os melhores performers (lacunas positivas)
        
        Args:
            n: Número de registros a retornar
            
        Returns:
            pd.DataFrame: Top performers
        """
        if self.df_cluster.empty:
            return pd.DataFrame()
        
        # Filtrar apenas lacunas positivas (destaques)
        performers = self.df_cluster[self.df_cluster["LacunaRL"] > 0].copy()
        
        # Ordenar por maior lacuna positiva
        performers = performers.sort_values("LacunaRL", ascending=False).head(n)
        
        # Adicionar colunas calculadas
        performers["Rank"] = range(1, len(performers) + 1)
        
        return performers[["Rank", "NomeLoja", "grupo_comparavel", "LacunaRL", "LacunaCupom", "LacunaBM"]]
    
    def analyze_by_cluster(self) -> pd.DataFrame:
        """
        Análise agregada por cluster
        
        Returns:
            pd.DataFrame: Análise por cluster
        """
        if self.df_cluster.empty:
            return pd.DataFrame()
        
        try:
            cluster_analysis = self.df_cluster.groupby("grupo_comparavel").agg({
                "LacunaRL": ["sum", "mean", "count", "std"],
                "LacunaCupom": ["sum", "mean"],
                "LacunaBM": ["sum", "mean"],
                "LacunaPM": ["sum", "mean"],
                "LacunaProd": ["sum", "mean"],
                "NomeLoja": "count"
            }).round(2)
            
            # Flatten column names
            cluster_analysis.columns = [f"{col[1]}_{col[0]}" if col[1] != "" else col[0] for col in cluster_analysis.columns]
            
            # Renomear colunas
            cluster_analysis = cluster_analysis.rename(columns={
                "count_NomeLoja": "Qtd_Lojas",
                "sum_LacunaRL": "LacunaRL_Total",
                "mean_LacunaRL": "LacunaRL_Media",
                "std_LacunaRL": "LacunaRL_Desvio"
            })
              # Calcular métricas adicionais
            cluster_analysis["LacunaRL_Potencial"] = cluster_analysis["LacunaRL_Total"] * -1  # Inverter negativos
            cluster_analysis["LacunaRL_Potencial"] = cluster_analysis["LacunaRL_Potencial"].where(
                cluster_analysis["LacunaRL_Potencial"] > 0, 0
            )
            
            return cluster_analysis.reset_index()
            
        except Exception as e:
            logger.error(f"Erro na análise por cluster: {str(e)}")
            return pd.DataFrame()
    
    def analyze_by_gr(self) -> pd.DataFrame:
        """
        Análise agregada por Gerência Regional (GR)
        
        Returns:
            pd.DataFrame: Análise por GR
        """
        if self.df_cluster.empty:
            return pd.DataFrame()
        
        try:
            # Verificar se NumeroGR existe no df_cluster
            if "NumeroGR" not in self.df_cluster.columns:
                logger.warning("Coluna NumeroGR não encontrada nos dados")
                return pd.DataFrame()
            
            # Usar NumeroGR diretamente do df_cluster
            gr_analysis = self.df_cluster.groupby("NumeroGR").agg({
                "LacunaRL": ["sum", "mean", "count"],
                "LacunaCupom": ["sum", "mean"],
                "LacunaBM": ["sum", "mean"],
                "NomeLoja": "count"
            }).round(2)
            
            # Flatten column names
            gr_analysis.columns = [f"{col[1]}_{col[0]}" if col[1] != "" else col[0] for col in gr_analysis.columns]
            
            # Renomear colunas
            gr_analysis = gr_analysis.rename(columns={
                "count_NomeLoja": "Qtd_Lojas",
                "sum_LacunaRL": "LacunaRL_Total",
                "mean_LacunaRL": "LacunaRL_Media"
            })
            
            return gr_analysis.reset_index()
            
        except Exception as e:
            logger.error(f"Erro na análise por GR: {str(e)}")
            return pd.DataFrame()
    
    def calculate_waterfall_data(self, loja_nome: Optional[str] = None) -> Dict:
        """
        Calcula dados para gráfico waterfall de decomposição de lacunas
        
        Args:
            loja_nome: Nome da loja específica (None para total)
            
        Returns:
            Dict: Dados para gráfico waterfall
        """
        if self.df_cluster.empty:
            return {}
        
        try:
            if loja_nome:
                # Análise de loja específica
                loja_data = self.df_cluster[self.df_cluster["NomeLoja"] == loja_nome]
                if loja_data.empty:
                    return {}
                
                lacuna_rl = loja_data["LacunaRL"].iloc[0]
                lacuna_cupom = loja_data["LacunaCupom"].iloc[0]
                lacuna_bm = loja_data["LacunaBM"].iloc[0]
                lacuna_pm = loja_data["LacunaPM"].iloc[0]
                lacuna_prod = loja_data["LacunaProd"].iloc[0]
                
            else:
                # Análise total
                lacuna_rl = self.df_cluster["LacunaRL"].sum()
                lacuna_cupom = self.df_cluster["LacunaCupom"].sum()
                lacuna_bm = self.df_cluster["LacunaBM"].sum()
                lacuna_pm = self.df_cluster["LacunaPM"].sum()
                lacuna_prod = self.df_cluster["LacunaProd"].sum()
            
            waterfall_data = {
                "categories": ["Base", "Lacuna Cupom", "Lacuna BM", "Lacuna PM", "Lacuna Prod", "Total"],
                "values": [0, lacuna_cupom, lacuna_bm, lacuna_pm, lacuna_prod, lacuna_rl],
                "cumulative": [0, lacuna_cupom, lacuna_cupom + lacuna_bm, 
                              lacuna_cupom + lacuna_bm + lacuna_pm,
                              lacuna_cupom + lacuna_bm + lacuna_pm + lacuna_prod, lacuna_rl]
            }
            
            return waterfall_data
            
        except Exception as e:
            logger.error(f"Erro no cálculo do waterfall: {str(e)}")
            return {}
    
    def get_loja_details(self, loja_nome: str) -> Dict:
        """
        Retorna detalhes completos de uma loja específica
        
        Args:
            loja_nome: Nome da loja
            
        Returns:
            Dict: Detalhes da loja
        """
        details = {}
        
        try:
            # Dados da aba cluster
            if not self.df_cluster.empty:
                loja_cluster = self.df_cluster[self.df_cluster["NomeLoja"] == loja_nome]
                if not loja_cluster.empty:
                    details["cluster_data"] = loja_cluster.iloc[0].to_dict()
            
            # Dados da aba diária
            if not self.df_diaria.empty:
                loja_diaria = self.df_diaria[self.df_diaria["NomeLoja"] == loja_nome]
                if not loja_diaria.empty:
                    details["daily_data"] = loja_diaria.to_dict('records')
            
            # Calcular métricas derivadas
            if "cluster_data" in details:
                cluster_info = details["cluster_data"]
                grupo = cluster_info.get("grupo_comparavel", "")
                
                # Comparativo com cluster
                cluster_peers = self.df_cluster[self.df_cluster["grupo_comparavel"] == grupo]
                if not cluster_peers.empty:
                    details["cluster_comparison"] = {
                        "cluster_size": len(cluster_peers),
                        "cluster_median_rl": cluster_peers["LacunaRL"].median(),
                        "cluster_mean_rl": cluster_peers["LacunaRL"].mean(),
                        "rank_in_cluster": (cluster_peers["LacunaRL"] < cluster_info["LacunaRL"]).sum() + 1
                    }
            
        except Exception as e:
            logger.error(f"Erro ao buscar detalhes da loja {loja_nome}: {str(e)}")
            details["error"] = str(e)
        
        return details
    
    def calculate_trends(self) -> Dict:
        """
        Calcula tendências temporais quando há dados de datavenda
        
        Returns:
            Dict: Análise de tendências
        """
        trends = {}
        
        if self.df_diaria.empty or "datavenda" not in self.df_diaria.columns:
            return trends
        
        try:
            # Agregar por data
            daily_trends = self.df_diaria.groupby("datavenda").agg({
                "receita_liquida": "sum",
                "qtd_cupom": "sum",
                "qtd_item": "sum"
            }).reset_index()
            
            # Calcular variações
            daily_trends["receita_liquida_var"] = daily_trends["receita_liquida"].pct_change() * 100
            daily_trends["qtd_cupom_var"] = daily_trends["qtd_cupom"].pct_change() * 100
            
            trends["daily_data"] = daily_trends
            trends["latest_date"] = daily_trends["datavenda"].max()
            trends["date_range"] = (daily_trends["datavenda"].min(), daily_trends["datavenda"].max())
            
        except Exception as e:
            logger.error(f"Erro no cálculo de tendências: {str(e)}")
            trends["error"] = str(e)
        
        return trends
