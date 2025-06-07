"""
Módulo de utilitários gerais para a aplicação
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)


def format_currency(value: float, currency: str = "R$") -> str:
    """
    Formata valor numérico como moeda brasileira
    
    Args:
        value: Valor numérico
        currency: Símbolo da moeda (padrão: R$)
        
    Returns:
        str: Valor formatado como moeda
    """
    if pd.isna(value) or value is None:
        return f"{currency} 0,00"
    
    try:
        # Formatação brasileira: separador de milhares (.) e decimais (,)
        formatted = f"{currency} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted
    except (ValueError, TypeError):
        return f"{currency} 0,00"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Formata valor como porcentagem
    
    Args:
        value: Valor numérico (0.15 = 15%)
        decimal_places: Número de casas decimais
        
    Returns:
        str: Valor formatado como porcentagem
    """
    if pd.isna(value) or value is None:
        return "0,00%"
    
    try:
        # Converte para porcentagem e formata com vírgula decimal
        percentage = value * 100
        formatted = f"{percentage:.{decimal_places}f}%".replace(".", ",")
        return formatted
    except (ValueError, TypeError):
        return "0,00%"


def setup_logging():
    """Configura o sistema de logging da aplicação"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('dashboard_pulso.log'),
            logging.StreamHandler()
        ]
    )


def ensure_directories():
    """Garante que todas as pastas necessárias existam"""
    from config import UPLOAD_DIR, PROCESSED_DIR, EXPORTS_DIR
    
    directories = [UPLOAD_DIR, PROCESSED_DIR, EXPORTS_DIR]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Diretório verificado/criado: {directory}")


def save_uploaded_file(uploaded_file, upload_dir: Path) -> Optional[Path]:
    """
    Salva arquivo enviado no diretório de upload
    
    Args:
        uploaded_file: Arquivo do streamlit file_uploader
        upload_dir: Diretório de destino
        
    Returns:
        Optional[Path]: Caminho do arquivo salvo ou None se erro
    """
    try:
        file_path = upload_dir / uploaded_file.name
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        logger.info(f"Arquivo salvo: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo: {str(e)}")
        st.error(f"Erro ao salvar arquivo: {str(e)}")
        return None


def clear_cache():
    """Limpa todos os caches do Streamlit"""
    st.cache_data.clear()
    if 'data' in st.session_state:
        del st.session_state['data']
    if 'metadata' in st.session_state:
        del st.session_state['metadata']
    logger.info("Cache limpo")


def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em bytes para formato legível
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        str: Tamanho formatado
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size_float = float(size_bytes)
    
    while size_float >= 1024 and i < len(size_names) - 1:
        size_float /= 1024.0
        i += 1
    
    return f"{size_float:.1f} {size_names[i]}"


def export_to_excel(data: Dict[str, pd.DataFrame], filename: str, export_dir: Path) -> Optional[Path]:
    """
    Exporta dados para arquivo Excel
    
    Args:
        data: Dicionário com DataFrames
        filename: Nome do arquivo (sem extensão)
        export_dir: Diretório de destino
        
    Returns:
        Optional[Path]: Caminho do arquivo exportado
    """
    try:
        file_path = export_dir / f"{filename}.xlsx"
        
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for sheet_name, df in data.items():
                # Limitar nome da aba a 31 caracteres (limite do Excel)
                safe_sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
        
        logger.info(f"Arquivo Excel exportado: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Erro ao exportar Excel: {str(e)}")
        st.error(f"Erro ao exportar Excel: {str(e)}")
        return None


def validate_data_consistency(data: Dict[str, pd.DataFrame]) -> Dict[str, List[str]]:
    """
    Valida consistência entre os DataFrames
    
    Args:
        data: Dicionário com DataFrames
        
    Returns:
        Dict[str, List[str]]: Dicionário com issues encontrados
    """
    issues = {"warnings": [], "errors": []}
    
    try:
        df_diaria = data.get("pulso_consulta_diaria")
        df_cluster = data.get("pulso_consulta_diaria_cluster_antigo")
        
        if df_diaria is not None and df_cluster is not None:
            # Verificar se as lojas são consistentes
            lojas_diaria = set(df_diaria["NomeLoja"].unique()) if "NomeLoja" in df_diaria.columns else set()
            lojas_cluster = set(df_cluster["NomeLoja"].unique()) if "NomeLoja" in df_cluster.columns else set()
            
            lojas_missing_cluster = lojas_diaria - lojas_cluster
            lojas_missing_diaria = lojas_cluster - lojas_diaria
            
            if lojas_missing_cluster:
                issues["warnings"].append(f"Lojas na aba diária mas não na cluster: {len(lojas_missing_cluster)}")
            
            if lojas_missing_diaria:
                issues["warnings"].append(f"Lojas na aba cluster mas não na diária: {len(lojas_missing_diaria)}")
            
            # Verificar valores nulos em campos críticos
            critical_fields = ["LacunaRL", "LacunaCupom", "LacunaBM"]
            for field in critical_fields:
                if field in df_cluster.columns:
                    null_count = df_cluster[field].isnull().sum()
                    if null_count > 0:
                        issues["warnings"].append(f"Valores nulos em {field}: {null_count} registros")
        
    except Exception as e:
        issues["errors"].append(f"Erro na validação: {str(e)}")
    
    return issues


def create_summary_stats(df: pd.DataFrame, numeric_columns: List[str]) -> pd.DataFrame:
    """
    Cria estatísticas resumo para colunas numéricas
    
    Args:
        df: DataFrame com dados
        numeric_columns: Lista de colunas numéricas
        
    Returns:
        pd.DataFrame: Estatísticas resumo
    """
    if df.empty:
        return pd.DataFrame()
    
    # Filtrar apenas colunas que existem no DataFrame
    existing_columns = [col for col in numeric_columns if col in df.columns]
    
    if not existing_columns:
        return pd.DataFrame()
    
    stats = df[existing_columns].describe().round(2)
    
    # Adicionar estatísticas extras
    stats.loc['missing'] = df[existing_columns].isnull().sum()
    stats.loc['missing_pct'] = (df[existing_columns].isnull().sum() / len(df) * 100).round(2)
    
    return stats


def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Aplica filtros a um DataFrame
    
    Args:
        df: DataFrame a ser filtrado
        filters: Dicionário com filtros {coluna: valor}
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if column in filtered_df.columns and value is not None:
            if isinstance(value, list):
                # Filtro múltiplo
                filtered_df = filtered_df[filtered_df[column].isin(value)]
            elif isinstance(value, tuple) and len(value) == 2:
                # Filtro de range
                min_val, max_val = value
                filtered_df = filtered_df[
                    (filtered_df[column] >= min_val) & 
                    (filtered_df[column] <= max_val)
                ]
            else:
                # Filtro simples
                filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df


def create_download_link(file_path: Path, link_text: str = "Download") -> str:
    """
    Cria link de download para arquivo
    
    Args:
        file_path: Caminho do arquivo
        link_text: Texto do link
        
    Returns:
        str: HTML do link de download
    """
    try:
        with open(file_path, "rb") as f:
            bytes_data = f.read()
        
        import base64
        b64 = base64.b64encode(bytes_data).decode()
        
        href = f'''
        <a href="data:application/octet-stream;base64,{b64}" 
           download="{file_path.name}" 
           style="text-decoration: none; 
                  background-color: #0066cc; 
                  color: white; 
                  padding: 0.5em 1em; 
                  border-radius: 0.3em;">
            {link_text}
        </a>
        '''
        
        return href
        
    except Exception as e:
        logger.error(f"Erro ao criar link de download: {str(e)}")
        return f"Erro: {str(e)}"


def show_data_info(data: Dict[str, pd.DataFrame], use_expanders: bool = True):
    """
    Mostra informações resumidas dos dados carregados
    
    Args:
        data: Dicionário com DataFrames
        use_expanders: Se deve usar expanders (False quando já está dentro de um expander)
    """
    if not data:
        st.info("Nenhum dado carregado")
        return
    
    if use_expanders:
        st.subheader("📋 Resumo dos Dados Carregados")
    
    for sheet_name, df in data.items():
        if use_expanders:
            with st.expander(f"📊 {sheet_name} ({len(df)} registros)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Dimensões:**", f"{df.shape[0]} linhas × {df.shape[1]} colunas")
                    st.write("**Memória:**", format_file_size(df.memory_usage(deep=True).sum()))
                
                with col2:
                    if len(df) > 0:
                        st.write("**Período:**")
                        if 'datavenda' in df.columns:
                            min_date = df['datavenda'].min()
                            max_date = df['datavenda'].max()
                            st.write(f"De {min_date} até {max_date}")
                        else:
                            st.write("Data não disponível")
                
                # Mostrar primeiras linhas
                if st.checkbox(f"Mostrar dados de {sheet_name}", key=f"show_{sheet_name}"):
                    st.dataframe(df.head(10))
        else:
            # Versão sem expanders para uso dentro de outros expanders
            st.write(f"### 📊 {sheet_name} ({len(df)} registros)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dimensões:**", f"{df.shape[0]} linhas × {df.shape[1]} colunas")
                st.write("**Memória:**", format_file_size(df.memory_usage(deep=True).sum()))
            
            with col2:
                if len(df) > 0:
                    st.write("**Período:**")
                    if 'datavenda' in df.columns:
                        min_date = df['datavenda'].min()
                        max_date = df['datavenda'].max()
                        st.write(f"De {min_date} até {max_date}")
                    else:
                        st.write("Data não disponível")
            
            # Mostrar primeiras linhas
            if st.checkbox(f"Mostrar dados de {sheet_name}", key=f"show_{sheet_name}"):
                st.dataframe(df.head(10))
            
            st.markdown("---")


def initialize_session_state():
    """Inicializa variáveis do session state"""
    if 'data_loaded' not in st.session_state:
        st.session_state['data_loaded'] = False
    
    if 'current_file' not in st.session_state:
        st.session_state['current_file'] = None
    
    if 'last_update' not in st.session_state:
        st.session_state['last_update'] = None
    
    if 'filters' not in st.session_state:
        st.session_state['filters'] = {}


class SessionManager:
    """Gerenciador de sessão para persistir dados"""
    
    @staticmethod
    def save_data(data: Dict[str, pd.DataFrame], metadata: Dict):
        """Salva dados na sessão"""
        st.session_state['data'] = data
        st.session_state['metadata'] = metadata
        st.session_state['data_loaded'] = True
        st.session_state['last_update'] = pd.Timestamp.now()
    
    @staticmethod
    def get_data() -> Dict[str, pd.DataFrame]:
        """Recupera dados da sessão"""
        return st.session_state.get('data', {})
    
    @staticmethod
    def get_metadata() -> Dict:
        """Recupera metadados da sessão"""
        return st.session_state.get('metadata', {})
    
    @staticmethod
    def is_data_loaded() -> bool:
        """Verifica se há dados carregados"""
        return st.session_state.get('data_loaded', False)
    
    @staticmethod
    def clear_session():
        """Limpa dados da sessão"""
        keys_to_clear = ['data', 'metadata', 'data_loaded', 'current_file', 'last_update']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
