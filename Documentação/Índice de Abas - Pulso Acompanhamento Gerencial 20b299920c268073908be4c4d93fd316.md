# Índice de Abas - Pulso Acompanhamento Gerencial

# 📊 Visão Geral do Arquivo

Este arquivo consolida dados de performance de lojas para análise gerencial, com foco em identificação de lacunas (gaps) e oportunidades de melhoria. Os dados são atualizados diariamente via BigQuery.

**Última atualização dos dados**: 07/06/2025 03:50 AM

---

## 🗂️ Estrutura das Abas

### 1️⃣ **Premissas e Sumário**

- **Status**: ✅ Visível
- **Propósito**: Documentação das premissas utilizadas nas análises e sumário executivo dos principais indicadores
- **Conteúdo**:
    - Definições de métricas
    - Critérios de agrupamento
    - Resumo de performance geral
- **Frequência de atualização**: Mensal

### 2️⃣ **Dashboard -24-25**

- **Status**: ✅ Visível
- **Propósito**: Painel principal de acompanhamento comparativo entre 2024 e 2025
- **Conteúdo**:
    - KPIs principais
    - Gráficos de evolução
    - Comparativos YoY
- **Usuários**: Diretoria e Gerência Regional
- **Frequência de atualização**: Diária

### 3️⃣ **Tendência Semanal - 24-25**

- **Status**: ✅ Visível
- **Propósito**: Análise de tendências semanais para identificação de padrões
- **Conteúdo**:
    - Evolução semanal de vendas
    - Sazonalidade
    - Projeções de curto prazo
- **Frequência de atualização**: Semanal

### 4️⃣ **GR1**

- **Status**: ✅ Visível
- **Propósito**: Análise específica do Grupo Regional 1
- **Conteúdo**:
    - Performance detalhada das lojas do GR1
    - Rankings internos
    - Planos de ação específicos
- **Usuários**: Gestor do GR1 e equipe

### 5️⃣ **2025**

- **Status**: ✅ Visível
- **Propósito**: Consolidado de dados do ano corrente (2025)
- **Conteúdo**:
    - Dados acumulados YTD
    - Performance mensal
    - Acompanhamento de metas
- **Frequência de atualização**: Diária

### 6️⃣ **2024 YTD**

- **Status**: ✅ Visível
- **Propósito**: Dados acumulados de 2024 para comparação
- **Conteúdo**:
    - Base histórica para comparativos
    - Performance final por período
- **Frequência de atualização**: Congelado (histórico)

### 7️⃣ **2024 YTD | Divisão**

- **Status**: 🔒 Oculta
- **Propósito**: Detalhamento de 2024 por divisão geográfica
- **Conteúdo**: Dados segmentados por AJU, BEL, FOR1, FOR2, JPA, REC, THE
- **Motivo oculta**: Dados intermediários para cálculos

### 8️⃣ **pulso_consulta_diaria**

- **Status**: ✅ Visível | 🔴 ABA FONTE
- **Propósito**: Base de dados principal importada do BigQuery
- **Conteúdo**:
    - 502 registros × 102 campos
    - Dados brutos de vendas diárias
    - Métricas base e comparativos
- **Query origem**: `sandbox-aero.pulso_.pulso_consulta_diaria`
- **⚠️ ATENÇÃO**: Não editar manualmente - dados são sobrescritos na atualização

### 9️⃣ **Análise Clusters**

- **Status**: ✅ Visível
- **Propósito**: Comparativo de performance entre clusters de lojas similares
- **Conteúdo**:
    - Agrupamento por características
    - Benchmarking entre lojas
    - Identificação de best practices
- **Fonte de dados**: pulso_consulta_diaria_cluster_a

### 🔟 **Análise Visão por Praça**

- **Status**: ✅ Visível
- **Propósito**: Visão agregada por região/praça
- **Conteúdo**:
    - Performance por divisão geográfica
    - Comparativos regionais
    - Identificação de oportunidades locais
- **Divisões**: AJU, BEL, FOR1, FOR2, JPA, REC, THE

### 1️⃣1️⃣ **Tabela dinâmica 17**

- **Status**: 🔒 Oculta
- **Propósito**: Tabela dinâmica auxiliar para cálculos
- **Motivo oculta**: Processamento intermediário

### 1️⃣2️⃣ **23-25 - Potencial**

- **Status**: 🔒 Oculta
- **Propósito**: Análise de potencial de crescimento 2023-2025
- **Conteúdo**: Projeções e cenários
- **Motivo oculta**: Análise estratégica em revisão

### 1️⃣3️⃣ **23-25 - Potencial Clusters**

- **Status**: ✅ Visível
- **Propósito**: Potencial de crescimento segmentado por clusters
- **Conteúdo**:
    - Gaps de performance por cluster
    - Oportunidades priorizadas
    - Metas de captura

### 1️⃣4️⃣ **Dashboard -23-24**

- **Status**: 🔒 Oculta
- **Propósito**: Dashboard do período anterior (arquivo)
- **Motivo oculta**: Substituído pelo Dashboard 24-25

### 1️⃣5️⃣ **Tendência Semanal - 23-24**

- **Status**: 🔒 Oculta
- **Propósito**: Análise semanal do período anterior (arquivo)
- **Motivo oculta**: Substituído pela versão 24-25

### 1️⃣6️⃣ **2025 YTD | Divisão**

- **Status**: 🔒 Oculta
- **Propósito**: Detalhamento 2025 por divisão
- **Conteúdo**: Dados para alimentar análises agregadas
- **Motivo oculta**: Dados intermediários

### 1️⃣7️⃣ **Qtde de Lojas**

- **Status**: 🔒 Oculta
- **Propósito**: Cadastro e contagem de lojas ativas
- **Conteúdo**: Base para cálculos de médias e expansão
- **Motivo oculta**: Dados de apoio

### 1️⃣8️⃣ **2024 FY**

- **Status**: 🔒 Oculta
- **Propósito**: Dados do ano fiscal completo 2024
- **Motivo oculta**: Histórico de referência

### 1️⃣9️⃣ **2023**

- **Status**: 🔒 Oculta
- **Propósito**: Dados históricos de 2023
- **Motivo oculta**: Base histórica para análises de tendência

### 2️⃣0️⃣ **Janeiro - Lacuna total**

- **Status**: 🔒 Oculta
- **Propósito**: Análise detalhada de lacunas do mês de Janeiro
- **Conteúdo**: Deep dive mensal
- **Motivo oculta**: Análise específica do período

### 2️⃣1️⃣ **Janeiro - Gráficos**

- **Status**: ✅ Visível
- **Propósito**: Visualizações gráficas da performance de Janeiro
- **Conteúdo**:
    - Gráficos de evolução diária
    - Comparativos com meta
    - Análise de tendências

### 2️⃣2️⃣ **pulso_consulta_diaria_cluster_a**

- **Status**: ✅ Visível | 🔴 ABA FONTE
- **Propósito**: Base de dados enriquecida com cálculos de lacunas
- **Conteúdo**:
    - Dados base + cálculos de gaps
    - 91 campos incluindo lacunas e oportunidades
    - Classificações de performance
- **⚠️ ATENÇÃO**: Alimentada a partir de pulso_consulta_diaria

---

## 📋 Legendas

- ✅ **Visível**: Aba disponível para consulta
- 🔒 **Oculta**: Aba oculta (dados auxiliares ou históricos)
- 🔴 **ABA FONTE**: Dados origem - não editar manualmente

## 🔄 Fluxo de Atualização

1. **BigQuery** → `pulso_consulta_diaria` (dados brutos)
2. `pulso_consulta_diaria` → `pulso_consulta_diaria_cluster_antigo` (cálculos)
3. Abas de análise consomem dados das abas fonte via fórmulas e tabelas dinâmicas

## 👥 Contatos

- **Dúvidas sobre dados**: [Equipe BI]
- **Solicitação de acessos**: [Gestor do Projeto]
- **Suporte técnico**: [TI]

## 📅 Calendário de Atualizações

- **Diário**: Dados fonte (3:50 AM)
- **Semanal**: Tendências e análises semanais (Segunda-feira)
- **Mensal**: Revisão de premissas e metas (1º dia útil)