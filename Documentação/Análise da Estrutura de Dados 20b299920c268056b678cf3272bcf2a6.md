# Análise da Estrutura de Dados

<aside>
📹

Fonte: 

[Pulso _ Comitê  04-2025 (1).pptx](Pulso___Comite__04-2025_(1).pptx)

</aside>

## 1. Abas Fonte de Dados

### 1.1 pulso_consulta_diaria

- **Dimensões**: 502 linhas × 102 colunas
- **Origem**: Query customizada do BigQuery (`sandbox-aero.pulso_.pulso_consulta_diaria`)
- **Campos principais**:
    - Identificação: ds_hub, NomeLoja, NumeroGR, GVO, codigo_franquia
    - Classificações: ds_lacuna, ds_i360, ds_demais_alavancas, ds_categoria
    - Temporalidade: datavenda, mes, semana, semana_depara
    - Métricas base: receita_liquida, qtd_cupom, qtd_item
    - Comparativos YoY: receita_liquida_um_aa_com, qtd_cupom_um_aa_com, Qtd_item_um_aa_com
    - Medianas semanais: Mediana_Semana_RL, Mediana_Semana_cupom, Mediana_semana_bm, Mediana_semana_pm, Mediana_semana_prod

### 1.2 pulso_consulta_diaria_cluster_antigo

- **Dimensões**: Similar à anterior mas com 91 colunas
- **Campos exclusivos desta aba**:
    - Cálculos de Lacuna: LacunaRL, LacunaCupom, LacunaBM, LacunaPM, LacunaProd, TTLacuna
    - Classificações adicionais: "Classificação", "Lacuna Positiva/Negativa"

## 2. Abas de Análise e Visualização

### 2.1 Análise Clusters

- **Tipo**: Tabela agregada por loja
- **Estrutura**: NomeLoja | grupo_comparavel | GVO | SUM de LacunaRL
- **Objetivo**: Análise de lacunas de receita líquida agrupadas por loja e cluster

### 2.2 Análise Visão por Praça

- **Tipo**: Tabela agregada por região
- **Estrutura**: grupo_comparavel | divisao | SUM de LacunaRL
- **Objetivo**: Visão regional das lacunas de performance
- **Divisões identificadas**: AJU, BEL, FOR1, FOR2, JPA, REC, THE

### 2.3 Dashboards e Tendências

- **Dashboard -24-25**: Dashboard comparativo 2024-2025
- **Tendência Semanal - 24-25**: Análise de tendências semanais
- **Dashboard -23-24** (oculta): Versão anterior do dashboard
- **Tendência Semanal - 23-24** (oculta): Versão anterior da análise semanal

### 2.4 Abas de Análise Temporal

- **2025**: Dados do ano corrente
- **2024 YTD**: Dados acumulados de 2024
- **2024 YTD | Divisão** (oculta): Detalhamento por divisão
- **2024 FY** (oculta): Ano fiscal completo 2024
- **2023** (oculta): Dados históricos

### 2.5 Análises Específicas

- **GR1**: Análise específica do grupo GR1 (Piloto) e Outras GRs (Grupo controle)
- **Janeiro - Lacuna total**: Análise detalhada de lacunas do mês de janeiro
- **Janeiro - Gráficos**: Visualizações gráficas do mês de janeiro
- **23-25 - Potencial** (oculta): Análise de potencial período 2023-2025
- **23-25 - Potencial Clusters**: Análise de potencial por clusters

## 3. Fluxo de Dados Identificado

1. **Extração**: Dados são extraídos do BigQuery para as duas abas fonte
2. **Transformação**:
    - `pulso_consulta_diaria`: Contém dados brutos e algumas métricas calculadas
    - `pulso_consulta_diaria_cluster_a`: Adiciona cálculos de lacunas e oportunidades
3. **Agregação**: Dados são consumidos pelas outras abas através de:
    - Tabelas dinâmicas (identificadas mas não visíveis no metadata)
    - Fórmulas de agregação (SUMIF, VLOOKUP, etc.)
    - Filtros por período, divisão, cluster

## 4. Métricas Principais Calculadas

### Lacunas (Gaps)

- **LacunaRL**: Gap de Receita Líquida. Diferença entre a receita realizada e o potencial esperado com base em lojas comparáveis.
- **LacunaCupom**: Gap de Cupons. Mede a quantidade de boletos emitidos.
- **LacunaBM**: Gap de BM. Receita ÷ Número de boletos. Mede se o consultor está conseguindo vender mais itens ou itens de maior valor em cada venda.
- **LacunaPM**: Gap de Preço Médio. Receita ÷ Volume de itens. Avalia se o consultor está conseguindo ofertar produtos de ticket mais alto.
- **LacunaProd**: Gap de Produtividade. Volume ÷ Número de boletos. Mede a quantidade média de itens por venda – indica eficiência na composição da cesta.
- **TTLacuna**: Lacuna total = Lacuna de RL (Não utilizado para nenhum cálculo)

### Oportunidades

- **Perfumaria**: Análise de oportunidade e conversão
- **Cross-sell**: Oportunidades de venda cruzada

### Comparativos

- Métricas YoY (Year-over-Year)
- Medianas semanais para benchmarking
- Classificações por performance

## 5. Estrutura Organizacional

- **HUBs**: Agrupamento regional/operacional
- **GRs**: Gerências Regionais (GR1 identificado)
- **GVOs**: Gerente de Vendas e Operações
- **Divisões**: AJU, BEL, FOR1, FOR2, JPA, REC, THE
- **Clusters**: Agrupamentos por características similares (0-0, 1-0, 2-0, 6-0, etc.)

## 6. Abas Ocultas

Várias abas estão marcadas como ocultas (Hidden: 1), indicando:

- Dados históricos mantidos para referência
- Cálculos intermediários
- Versões anteriores de análises

## Próximos passos

1. **Documentar fórmulas**: Criar uma aba de documentação explicando os cálculos de cada lacuna
    
    [Documentação de Fórmulas - Cálculos de Lacunas](Documentac%CC%A7a%CC%83o%20de%20Fo%CC%81rmulas%20-%20Ca%CC%81lculos%20de%20Lacunas%2020b299920c2680a8affdc3b732b954a2.md)
    
2. **Padronizar nomenclatura**: Unificar nomes de campos entre as abas fonte
3. **Criar índice**: Adicionar uma aba índice explicando o propósito de cada aba

[Índice de Abas - Pulso Acompanhamento Gerencial](I%CC%81ndice%20de%20Abas%20-%20Pulso%20Acompanhamento%20Gerencial%2020b299920c268073908be4c4d93fd316.md)

1. **Automatizar atualizações**: Verificar se as queries do BigQuery podem ser automatizadas
2. **Limpar abas obsoletas**: Avaliar necessidade das abas ocultas