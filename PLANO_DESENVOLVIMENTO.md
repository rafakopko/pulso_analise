# Plano de Desenvolvimento - Dashboard Pulso
*Criado em: 07/06/2025*

## 📋 Resumo Executivo

### Contexto do Projeto
O **Projeto Pulso** é um sistema de gestão comercial baseado em análise de lacunas de vendas entre lojas similares. Com potencial comprovado de **R$ 119 milhões de captura até 2028** e resultados de piloto demonstrando **61-65% de uplift**, a automação deste relatório é estratégica para a expansão do projeto.

### Objetivo da Aplicação
Automatizar a geração do relatório gerencial atualmente feito em Excel, centralizando análises de lacunas em um dashboard interativo que facilite a tomada de decisão e escale o acesso para equipes regionais.

## 🎯 Escopo do MVP

### Funcionalidades Core
1. **Upload e processamento** do arquivo Excel base
2. **Cálculo automático** de lacunas (RL, Cupom, BM, PM, Prod)
3. **Dashboard executivo** com KPIs principais
4. **Análise por clusters** e comparativos
5. **Visão por loja** com detalhamentos
6. **Exportação** de relatórios em Excel/PDF

### Usuários-Alvo MVP
- **Diretoria**: Visão estratégica e KPIs
- **Gerentes Regionais**: Performance por região
- **Analistas**: Deep dives e análises detalhadas

## 🏗️ Arquitetura Técnica

### Stack Tecnológica
```
Frontend: Streamlit 1.30.0
Backend: Python 3.9+
Dados: Pandas 2.0.3, OpenPyXL 3.1.2
Visualização: Plotly 5.18.0
Deploy Local: Localhost:8501
Deploy Cloud (Futuro): Streamlit Cloud/AWS
```

### Estrutura de Pastas
```
pulso_analise/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências Python
├── config.py             # Configurações globais
├── README.md             # Documentação do usuário
│
├── data/                 # Dados e uploads
│   ├── upload/          # Arquivos Excel enviados
│   ├── processed/       # Dados processados
│   └── exports/         # Relatórios exportados
│
├── src/                 # Código fonte
│   ├── __init__.py
│   ├── data_loader.py   # Carregamento Excel
│   ├── calculations.py  # Cálculos de lacunas
│   ├── visualizations.py # Gráficos e charts
│   └── utils.py         # Funções auxiliares
│
├── pages/               # Páginas Streamlit
│   ├── 1_📊_Home.py
│   ├── 2_🎯_Analise_Lacunas.py
│   ├── 3_🏪_Visao_Loja.py
│   ├── 4_👥_Clusters.py
│   └── 5_📈_Exportar.py
│
└── docs/               # Documentação original
    └── [arquivos existentes]
```

## 📊 Módulos do Dashboard

### 1. 🏠 Home - Centro de Comando
**KPIs Principais:**
- Lacuna Total de RL (R$ milhões)
- % de Captura vs Meta
- Top 10 Maiores Oportunidades
- Evolução Semanal vs Ano Anterior
- Performance por GR

**Visualizações:**
- Cards com métricas principais
- Gráfico de evolução temporal
- Mapa de calor regional
- Ranking de lojas

### 2. 🎯 Análise de Lacunas
**Decomposição de Lacunas:**
- RL → Cupom + Boleto Médio
- BM → Preço Médio + Produtividade
- Análise por Cluster
- Comparativo temporal

**Visualizações:**
- Gráfico waterfall de decomposição
- Matriz de oportunidades
- Box plot por cluster
- Tabela detalhada de lacunas

### 3. 🏪 Visão por Loja
**Análise Individual:**
- Ficha completa da loja
- Performance vs mediana do cluster
- Histórico de 13 semanas
- Radar comparativo

**Visualizações:**
- Seletor de loja
- Gráficos de evolução
- Comparativo com cluster
- Métricas de performance

### 4. 👥 Análise de Clusters
**Inteligência Comparativa:**
- Composição dos clusters
- Rankings internos
- Dispersão de performance
- Best practices

**Visualizações:**
- Lista de clusters
- Box plots comparativos
- Identificação de outliers
- Benchmarking

### 5. 📈 Exportar Relatórios
**Geração de Relatórios:**
- Export para Excel formatado
- Relatórios personalizados
- Agendamento (futuro)
- Histórico de exports

## 🔄 Fluxo de Dados

### 1. Entrada
```
Excel Upload → Validação → Cache Session State
```

### 2. Processamento
```
Dados Brutos → Cálculos de Lacunas → Agregações → Visualizações
```

### 3. Saída
```
Dashboard Interativo + Relatórios Excel/PDF
```

## 📈 Cronograma de Desenvolvimento

### Fase 1: Fundação (Semana 1-2)
- [x] Análise da documentação
- [ ] Setup do ambiente Python
- [ ] Estrutura base do projeto
- [ ] Carregamento do Excel base
- [ ] Página Home básica

### Fase 2: Core MVP (Semana 3-4)
- [ ] Cálculos de lacunas
- [ ] Visualizações principais
- [ ] Páginas de análise
- [ ] Sistema de filtros
- [ ] Validação com dados reais

### Fase 3: Refinamento (Semana 5-6)
- [ ] UX/UI melhorada
- [ ] Performance otimizada
- [ ] Exportação de relatórios
- [ ] Testes e correções
- [ ] Documentação final

### Fase 4: Deploy e Treinamento (Semana 7)
- [ ] Deploy local testado
- [ ] Manual do usuário
- [ ] Treinamento da equipe
- [ ] Coleta de feedback
- [ ] Preparação para cloud

## 🎯 Métricas de Sucesso

### Indicadores Técnicos
- [ ] Tempo de carregamento < 10 segundos
- [ ] Processamento de arquivo Excel < 30 segundos
- [ ] Interface responsiva e intuitiva
- [ ] Zero falhas na carga de dados

### Indicadores de Negócio
- [ ] Redução de 90% no tempo de geração do relatório
- [ ] Aumento de 50% na frequência de análises
- [ ] Facilitar acesso para 100% das GRs
- [ ] Base sólida para expansion cloud

## 🚀 Roadmap Futuro

### Fase Cloud (3-6 meses)
- [ ] Migração para Streamlit Cloud/AWS
- [ ] Conexão direta com BigQuery
- [ ] Atualizações automáticas
- [ ] Controle de acesso por usuário

### Fase Analytics (6-12 meses)
- [ ] Machine Learning para previsões
- [ ] Detecção de anomalias
- [ ] Recomendações automáticas
- [ ] Sistema de alertas

### Fase Colaboração (12+ meses)
- [ ] Gestão de planos de ação
- [ ] Comentários e anotações
- [ ] Workflow de aprovações
- [ ] Integração com email/WhatsApp

## 📋 Critérios de Aceite

### Funcionalidades Obrigatórias
- [x] Upload de arquivo Excel funcional
- [ ] Cálculo correto de todas as lacunas
- [ ] Dashboard com todas as 5 páginas
- [ ] Filtros funcionais (GR, período, cluster)
- [ ] Exportação para Excel
- [ ] Performance adequada

### Qualidade de Código
- [ ] Código documentado e comentado
- [ ] Tratamento de erros
- [ ] Validação de dados
- [ ] Testes básicos
- [ ] README completo

## 🔗 Referências Técnicas

### Documentação Base
- [Estrutura Técnica MVP](docs/Estrutura_Tecnica_MVP.md)
- [Dashboard Ideal](docs/Dashboard_Ideal.md)
- [Documentação de Fórmulas](docs/Documentacao_Formulas.md)
- [Análise da Estrutura de Dados](docs/Analise_Estrutura_Dados.md)

### Dados de Entrada
- Arquivo: `Base/Pulso _ Acompanhamento Gerencial .xlsx`
- Abas principais: `pulso_consulta_diaria`, `pulso_consulta_diaria_cluster_antigo`
- Campos críticos: NomeLoja, LacunaRL, LacunaCupom, LacunaBM, LacunaPM, LacunaProd

---

**Responsável:** Desenvolvimento automatizado
**Status:** Em desenvolvimento  
**Última atualização:** 07/06/2025
