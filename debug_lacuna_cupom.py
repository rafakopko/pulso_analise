"""
Script para debugar os valores de LacunaCupom
"""
import pandas as pd
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data_loader import DataLoader

# Carregar dados
loader = DataLoader()
base_path = Path(__file__).parent / "Base" / "Pulso _ Acompanhamento Gerencial .xlsx"

if base_path.exists():
    print(f"Carregando arquivo: {base_path}")
    data = loader.load_excel_data(base_path)
    
    if data and "pulso_consulta_diaria_cluster_a" in data:
        df_cluster = data["pulso_consulta_diaria_cluster_a"]
        
        print(f"\nShape do DataFrame: {df_cluster.shape}")
        print(f"\nColunas disponíveis: {list(df_cluster.columns)}")
        
        if "LacunaCupom" in df_cluster.columns:
            print(f"\nEstatísticas da LacunaCupom:")
            print(df_cluster["LacunaCupom"].describe())
            
            print(f"\nValores únicos de LacunaCupom (primeiros 10):")
            unique_values = df_cluster["LacunaCupom"].unique()
            print(unique_values[:10])
            
            print(f"\nContagem de valores zeros:")
            zeros = (df_cluster["LacunaCupom"] == 0).sum()
            total = len(df_cluster)
            print(f"Zeros: {zeros}/{total} ({zeros/total*100:.1f}%)")
            
            print(f"\nContagem de valores não-zeros:")
            non_zeros = (df_cluster["LacunaCupom"] != 0).sum()
            print(f"Não-zeros: {non_zeros}/{total} ({non_zeros/total*100:.1f}%)")
            
            # Mostrar alguns exemplos de dados
            print(f"\nPrimeiras 10 linhas com NomeLoja e LacunaCupom:")
            print(df_cluster[["NomeLoja", "LacunaCupom"]].head(10))
            
            # Verificar lojas com LacunaCupom não-zero
            non_zero_cupom = df_cluster[df_cluster["LacunaCupom"] != 0]
            if not non_zero_cupom.empty:
                print(f"\nLojas com LacunaCupom não-zero (primeiras 5):")
                print(non_zero_cupom[["NomeLoja", "LacunaCupom"]].head())
        else:
            print("❌ Coluna LacunaCupom não encontrada!")
    else:
        print("❌ Dados cluster não encontrados!")
else:
    print(f"❌ Arquivo não encontrado: {base_path}")
