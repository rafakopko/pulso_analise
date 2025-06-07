"""
Módulo para carregamento e processamento de dados Excel
"""

import pandas as pd
import streamlit as st
from pathlib import Path
import openpyxl
from typing import Dict, List, Optional, Tuple
import logging

from config import REQUIRED_COLUMNS, EXCEL_CONFIG, MESSAGES

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Classe para carregamento e validação de dados do Excel"""
    
    def __init__(self):
        self.data: Dict[str, pd.DataFrame] = {}
        self.metadata: Dict = {}
    
    def validate_file(self, file) -> Tuple[bool, str]:
        """
        Valida se o arquivo Excel está no formato correto
        
        Args:
            file: Arquivo enviado via streamlit file_uploader
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem)
        """
        try:
            # Verificar tamanho do arquivo
            if file.size > EXCEL_CONFIG["max_file_size"] * 1024 * 1024:
                return False, f"Arquivo muito grande. Máximo: {EXCEL_CONFIG['max_file_size']}MB"
            
            # Verificar extensão
            file_extension = Path(file.name).suffix.lower()
            if file_extension not in [f".{ext}" for ext in EXCEL_CONFIG["file_types"]]:
                return False, f"Tipo de arquivo inválido. Use: {', '.join(EXCEL_CONFIG['file_types'])}"
            
            # Verificar se é um arquivo Excel válido
            try:
                workbook = openpyxl.load_workbook(file, read_only=True)
                sheet_names = workbook.sheetnames
                workbook.close()
            except Exception as e:
                return False, f"Arquivo Excel corrompido: {str(e)}"
            
            # Verificar abas obrigatórias
            missing_sheets = []
            for required_sheet in EXCEL_CONFIG["required_sheets"]:
                if required_sheet not in sheet_names:
                    missing_sheets.append(required_sheet)
            
            if missing_sheets:
                return False, f"Abas não encontradas: {', '.join(missing_sheets)}"
            
            return True, "Arquivo válido"
            
        except Exception as e:
            logger.error(f"Erro na validação do arquivo: {str(e)}")
            return False, f"Erro na validação: {str(e)}"
    
    def load_excel_data(self, file) -> Dict[str, pd.DataFrame]:
        """
        Carrega dados das abas principais do Excel
        
        Args:
            file: Arquivo Excel enviado
            
        Returns:
            Dict[str, pd.DataFrame]: Dicionário com DataFrames das abas
        """
        try:
            # Validar arquivo
            is_valid, message = self.validate_file(file)
            if not is_valid:
                st.error(f"❌ {message}")
                return {}
            
            # Carregar abas principais
            data = {}
            
            with st.spinner("🔄 Carregando dados..."):
                # Aba principal - dados diários
                try:
                    df_diaria = pd.read_excel(
                        file, 
                        sheet_name="pulso_consulta_diaria",
                        engine='openpyxl'
                    )
                    data["pulso_consulta_diaria"] = df_diaria
                    logger.info(f"Carregada aba pulso_consulta_diaria: {df_diaria.shape}")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao carregar aba 'pulso_consulta_diaria': {str(e)}")
                    return {}
                
                # Aba com cálculos de lacunas
                try:
                    df_cluster = pd.read_excel(
                        file,
                        sheet_name="pulso_consulta_diaria_cluster_antigo", 
                        engine='openpyxl'
                    )
                    data["pulso_consulta_diaria_cluster_antigo"] = df_cluster
                    logger.info(f"Carregada aba cluster: {df_cluster.shape}")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao carregar aba 'pulso_consulta_diaria_cluster_antigo': {str(e)}")
                    return {}
            
            # Validar colunas obrigatórias
            validation_success = True
            for sheet_name, df in data.items():
                missing_cols = self._validate_columns(df, sheet_name)
                if missing_cols:
                    st.warning(f"⚠️ Colunas não encontradas em '{sheet_name}': {', '.join(missing_cols)}")
                    validation_success = False
            
            if not validation_success:
                st.warning("⚠️ Algumas colunas obrigatórias não foram encontradas. A aplicação pode não funcionar corretamente.")
            
            # Processar dados básicos
            data = self._preprocess_data(data)
            
            # Salvar metadados
            self.metadata = {
                "file_name": file.name,
                "file_size": file.size,
                "upload_time": pd.Timestamp.now(),
                "total_records": sum(len(df) for df in data.values()),
                "sheets_loaded": list(data.keys())
            }
            
            self.data = data
            st.success(MESSAGES["upload_success"])
            
            return data
            
        except Exception as e:
            logger.error(f"Erro no carregamento dos dados: {str(e)}")
            st.error(f"❌ Erro no carregamento: {str(e)}")
            return {}
    
    def _validate_columns(self, df: pd.DataFrame, sheet_name: str) -> List[str]:
        """
        Valida se as colunas obrigatórias existem no DataFrame
        
        Args:
            df: DataFrame a ser validado
            sheet_name: Nome da aba/sheet
            
        Returns:
            List[str]: Lista de colunas faltantes
        """
        if sheet_name not in REQUIRED_COLUMNS:
            return []
        
        required_cols = REQUIRED_COLUMNS[sheet_name]
        existing_cols = df.columns.tolist()
        missing_cols = [col for col in required_cols if col not in existing_cols]
        
        return missing_cols
    
    def _preprocess_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Pré-processa os dados carregados
        
        Args:
            data: Dicionário com DataFrames
            
        Returns:
            Dict[str, pd.DataFrame]: Dados processados
        """
        processed_data = {}
        
        for sheet_name, df in data.items():
            df_processed = df.copy()
            
            # Conversões comuns
            if 'datavenda' in df_processed.columns:
                df_processed['datavenda'] = pd.to_datetime(df_processed['datavenda'], errors='coerce')
            
            # Limpar nomes de colunas
            df_processed.columns = df_processed.columns.str.strip()
            
            # Substituir valores nulos em colunas numéricas por 0
            numeric_cols = df_processed.select_dtypes(include=['number']).columns
            df_processed[numeric_cols] = df_processed[numeric_cols].fillna(0)
            
            # Substituir valores nulos em colunas de texto por string vazia
            text_cols = df_processed.select_dtypes(include=['object']).columns
            df_processed[text_cols] = df_processed[text_cols].fillna('')
            
            processed_data[sheet_name] = df_processed
            
            logger.info(f"Pré-processamento de '{sheet_name}' concluído: {df_processed.shape}")
        
        return processed_data
    
    def get_data_summary(self) -> Dict:
        """
        Retorna resumo dos dados carregados
        
        Returns:
            Dict: Resumo dos dados
        """
        if not self.data:
            return {}
        
        summary = {
            "metadata": self.metadata,
            "sheets": {}
        }
        
        for sheet_name, df in self.data.items():
            summary["sheets"][sheet_name] = {
                "rows": len(df),
                "columns": len(df.columns),
                "columns_list": df.columns.tolist(),
                "memory_usage": df.memory_usage(deep=True).sum()
            }
        
        return summary


def load_sample_data() -> Dict[str, pd.DataFrame]:
    """
    Carrega dados de exemplo para demonstração
    
    Returns:
        Dict[str, pd.DataFrame]: Dados de exemplo
    """
    # Criar dados fictícios para demonstração
    sample_data = {
        "pulso_consulta_diaria": pd.DataFrame({
            "NomeLoja": [f"Loja {i:03d}" for i in range(1, 21)],
            "codigo_franquia": range(1, 21),
            "NumeroGR": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4],
            "datavenda": pd.date_range("2025-01-01", periods=20, freq="D"),
            "receita_liquida": [10000 + i * 1000 for i in range(20)],
            "qtd_cupom": [100 + i * 10 for i in range(20)],
            "qtd_item": [200 + i * 20 for i in range(20)],
            "Mediana_Semana_RL": [15000] * 20,
            "Mediana_Semana_cupom": [150] * 20
        }),
        "pulso_consulta_diaria_cluster_antigo": pd.DataFrame({
            "NomeLoja": [f"Loja {i:03d}" for i in range(1, 21)],
            "grupo_comparavel": ["1-0", "1-0", "2-0", "2-0", "3-0"] * 4,
            "LacunaRL": [-5000, -3000, -1000, 2000, 4000] * 4,
            "LacunaCupom": [-50, -30, -10, 20, 40] * 4,
            "LacunaBM": [-100, -60, -20, 40, 80] * 4,
            "LacunaPM": [-10, -6, -2, 4, 8] * 4,
            "LacunaProd": [-5, -3, -1, 2, 4] * 4
        })
    }
    
    return sample_data
