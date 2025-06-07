# Documentação de Fórmulas - Cálculos de Lacunas

## 1. Conceito de Lacuna (Gap)

A lacuna representa a diferença entre o desempenho atual e uma meta ou referência estabelecida. No contexto deste relatório, as lacunas são calculadas para identificar oportunidades de melhoria em diferentes métricas de performance.

## 2. Fórmulas de Cálculo das Lacunas

### 2.1 LacunaRL (Lacuna de Receita Líquida)

**Descrição**: Diferença entre a receita líquida atual e a mediana esperada

**Fórmula**:

```
LacunaRL = Receita_Liquida_Atual - Mediana_Semana_RL x Resultado Ano Anterior

```

**Interpretação**:

- Valor **negativo**: Performance abaixo da mediana (oportunidade de melhoria)
- Valor **positivo**: Performance acima da mediana (destaque positivo)

### 2.2 LacunaCupom (Lacuna de Quantidade de Cupons)

**Descrição**: Diferença entre a quantidade de cupons emitidos e a mediana esperada

**Fórmula**:

```
LacunaCupom = Qtd_Cupom_Atual - Mediana_Semana_Cupom x Ano Anterior

```

**Interpretação**:

- Valor **negativo**: Menor fluxo de clientes que o esperado
- Valor **positivo**: Fluxo de clientes acima do esperado

### 2.3 LacunaBM (Lacuna de Boleto Médio)

**Descrição**: Diferença entre o boleto médio atual e a mediana esperada

**Fórmula**:

```
LacunaBM = Boleto_Médio_Atual - Mediana_Semana_BM x Ano Anterior

```

**Interpretação**:

- Valor **negativo**: Margem abaixo do esperado (revisar mix ou precificação)
- Valor **positivo**: Margem saudável acima da mediana

### 2.4 LacunaPM (Lacuna de Preço Médio)

**Descrição**: Diferença entre o preço médio atual e a mediana esperada

**Fórmula**:

```
LacunaPM = Preço_Médio_Atual - Mediana_Semana_PM x Ano Anterior

```

**Interpretação**:

- Valor **negativo**: Mix com preço médio inferior ao esperado
- Valor **positivo**: Mix de produtos com bom preço médio

### 2.5 LacunaProd (Lacuna de Produtividade)

**Descrição**: Diferença entre a produtividade atual e a mediana esperada

**Fórmula**:

```
LacunaProd = Produtividade_Atual - Mediana_Semana_Prod x Ano Anterior

```

**Interpretação**:

- Valor **negativo**: Quantidade média de itens por venda abaixo do esperado
- Valor **positivo**: Quantidade média de itens por venda acima do esperado

## 3. Classificação por Grupo Comparável

**Descrição**: Agrupamento de lojas com características similares para comparação justa

**Formato**: `X-Y`

- X: Indica o cluster principal (0-6)
- Y: Indica subgrupo ou característica adicional

## 4. Métricas de Referência (Medianas)

### Por que usar medianas?

As medianas são utilizadas como referência por serem menos sensíveis a outliers que as médias, proporcionando uma comparação mais robusta.

### Cálculo das Medianas Semanais

```
Mediana_Semana_[Métrica] = MEDIANA([Métrica] para todas as lojas do mesmo cluster na mesma semana)

```

## 5. Comparativos Year-over-Year (YoY)

### Fórmula Geral YoY

```
Variacao_YoY_% = ((Valor_Ano_Atual - Valor_Ano_Anterior) / Valor_Ano_Anterior) * 100

```

### Campos YoY identificados:

- receita_liquida_um_aa_com
- qtd_cupom_um_aa_com
- Qtd_item_um_aa_com

## 6. Recomendações de Uso

1. **Priorização**: Focar nas lojas com maior Lacuna de RL negativa
2. **Análise detalhada**: Verificar qual componente da lacuna tem maior impacto
3. **Planos de ação**: Criar ações específicas para cada tipo de lacuna
4. **Monitoramento**: Acompanhar evolução semanal das lacunas

## 7. Observações Importantes

- As fórmulas exatas podem variar ligeiramente dependendo de ajustes sazonais ou estratégicos
- Algumas lojas podem ter metas customizadas ao invés de usar a mediana do cluster
- Períodos promocionais podem requerer ajustes nas fórmulas de cálculo