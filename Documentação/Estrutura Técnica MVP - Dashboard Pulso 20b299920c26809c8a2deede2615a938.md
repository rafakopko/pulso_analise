# Estrutura Técnica MVP - Dashboard Pulso

## 1. Stack Mínima Essencial

### 1.1 Dependências Core

```
streamlit==1.30.0
pandas==2.0.3
plotly==5.18.0
openpyxl==3.1.2  # Leitura de Excel

```

### 1.2 Dependências Adicionais (MVP)

```
numpy==1.24.3
xlsxwriter==3.1.9  # Export Excel formatado
python-dotenv==1.0.0  # Variáveis de ambiente

```

## 2. Estrutura Simplificada do Projeto

```
dashboard-pulso-mvp/
│
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── .env                   # Configurações locais
│
├── data/
│   └── upload/           # Pasta para upload do Excel
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py    # Carregamento e processamento do Excel
│   ├── calculations.py   # Cálculos de lacunas
│   └── charts.py         # Gráficos padronizados
│
└── pages/
    ├── __init__.py
    ├── 1_📊_Home.py
    ├── 2_🎯_Analise_Lacunas.py
    ├── 3_🏪_Visao_Loja.py
    └── 4_👥_Clusters.py

```

## 3. Funcionalidades MVP

### 3.1 Upload e Processamento do Excel

**app.py - Página Principal**

- Upload do arquivo Excel atualizado
- Validação básica do formato
- Cache dos dados na sessão
- Indicador de última atualização

### 3.2 Análises Essenciais

**Home (Visão Executiva)**

- KPIs principais: Lacuna Total, % Captura, Lojas com maior Gap
- KPIs principais: Lacuna Total, % Captura por GR e Praça
- Gráfico de evolução temporal
- Top 10 maiores oportunidades
- Resumo por região/divisão

**Análise de Lacunas**

- Decomposição: RL → Cupom + BM → PM + PROD
- Visualização waterfall
- Comparativo período anterior
- Export para Excel

**Visão por Loja**

- Seletor de loja com busca
- Métricas vs mediana do cluster
- Evolução últimas semanas
- Radar de performance

**Análise de Clusters**

- Lista de clusters e composição
- Box plot comparativo
- Ranking interno
- Identificação de outliers

## 4. Implementação Básica

### 4.1 Estrutura do app.py

```python
import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data
from utils.calculations import calculate_gaps

# Configuração da página
st.set_page_config(
    page_title="Dashboard Pulso",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Dashboard Pulso - MVP")

# Upload do arquivo
uploaded_file = st.file_uploader(
    "Faça upload do arquivo Excel atualizado",
    type=['xlsx']
)

if uploaded_file:
    # Carregar dados
    data = load_excel_data(uploaded_file)

    # Salvar no session state
    st.session_state['data'] = data
    st.session_state['last_update'] = pd.Timestamp.now()

    st.success("Dados carregados com sucesso!")

```

### 4.2 Processamento de Dados

**utils/data_loader.py**

- Leitura das abas principais
- Validação de colunas esperadas
- Tratamento de valores nulos
- Criação de dataframes processados

**utils/calculations.py**

- Cálculo de lacunas por loja
- Agregações por região/cluster
- Métricas derivadas
- Comparativos temporais

### 4.3 Visualizações

**utils/charts.py**

- Funções para gráficos padrão
- Configurações visuais consistentes
- Interatividade básica
- Export como imagem

## 5. Fluxo de Trabalho

```
1. Usuário faz upload do Excel
   ↓
2. Sistema valida e processa dados
   ↓
3. Dados ficam em memória (session state)
   ↓
4. Navegação entre páginas mantém dados
   ↓
5. Análises e visualizações sob demanda
   ↓
6. Export de resultados

```

## 6. Nice to Have (Futuro)

### 6.1 Fase 2 - Melhorias

- [ ]  Conexão direta com BigQuery
- [ ]  Cache persistente local
- [ ]  Histórico de uploads
- [ ]  Comparação entre versões
- [ ]  Mais tipos de visualização

### 6.2 Fase 3 - Analytics

- [ ]  Modelos preditivos básicos
- [ ]  Detecção de anomalias
- [ ]  Sistema de alertas
- [ ]  Recomendações automáticas

### 6.3 Fase 4 - Colaboração

- [ ]  Comentários em análises
- [ ]  Compartilhamento de views
- [ ]  Gestão de planos de ação
- [ ]  Integração com email

## 7. Setup Rápido

```bash
# 1. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar aplicação
streamlit run app.py

# 4. Abrir no navegador
# http://localhost:8501

```

## 8. Estrutura de Dados Esperada

### 8.1 Abas Necessárias no Excel

- `pulso_consulta_diaria`: Dados principais
- `pulso_consulta_diaria_cluster_antigo`: Dados com cálculos

### 8.2 Colunas Essenciais

**Identificação**

- NomeLoja, codigo_franquia, NumeroGR
- ds_hub, divisao, grupo_comparavel

**Métricas**

- receita_liquida, qtd_cupom
- Mediana_Semana_RL, Mediana_Semana_cupom
- LacunaRL, LacunaCupom, LacunaBM, etc.

**Temporais**

- datavenda, mes, semana

## 9. Dicas de Performance

- Usar `@st.cache_data` para dados processados
- Filtrar dados antes de visualizar
- Limitar número de pontos em gráficos
- Paginar tabelas grandes
- Pré-calcular agregações comuns

## 10. Próximos Passos

### Imediato (MVP)

1. Implementar estrutura básica
2. Criar páginas essenciais
3. Adicionar cálculos principais
4. Testar com dados reais

### Curto Prazo

1. Melhorar UX/UI
2. Adicionar mais filtros
3. Otimizar performance
4. Documentar uso

### Médio Prazo

1. Automatizar atualizações
2. Adicionar analytics
3. Expandir visualizações
4. Integrar com outras fontes