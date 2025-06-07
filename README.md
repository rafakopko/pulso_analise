# 🎯 Dashboard Pulso - Guia de Instalação e Uso

## 📋 Sobre o Sistema

O **Dashboard Pulso** é um sistema de análise de lacunas comerciais que automatiza o relatório gerencial do Projeto Pulso, permitindo identificar oportunidades de vendas através de comparação entre lojas similares.

## 🚀 Instalação Automática (Recomendado)

### Para usuários Windows:

1. **Clique duas vezes** no arquivo `instalar_e_executar.bat`
2. O sistema fará tudo automaticamente:
   - Verificará se Python está instalado
   - Instalará as dependências necessárias
   - Iniciará o dashboard no navegador
3. Acesse: http://localhost:8504

### Para usuários avançados (Windows):

1. **Clique com botão direito** no arquivo `instalar_e_executar.ps1`
2. Selecione **"Executar com PowerShell"**
3. Se aparecer erro de política de execução, execute:
   ```
   PowerShell -ExecutionPolicy Bypass -File instalar_e_executar.ps1
   ```

### Para usuários Linux/Mac:

1. Abra o terminal na pasta do projeto
2. Execute:
   ```bash
   chmod +x instalar_e_executar.sh
   ./instalar_e_executar.sh
   ```

## 🔧 Instalação Manual (Caso a automática falhe)

### Pré-requisitos:
- Python 3.9 ou superior
- Conexão com internet

### Passos:

1. **Instalar Python** (se não tiver):
   - Acesse: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação

2. **Abrir terminal/prompt** na pasta do projeto

3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar aplicação**:
   ```bash
   streamlit run app.py --server.port 8504
   ```

5. **Acessar no navegador**: http://localhost:8504

## 📊 Como Usar

### 1. Carregamento de Dados
- Clique em "Fazer upload" e selecione o arquivo Excel
- Ou use "Dados de Exemplo" para teste

### 2. Navegação
- **Home**: Visão geral e KPIs principais
- **Análise de Lacunas**: Decomposição detalhada
- **Visão por Loja**: Análise específica por loja
- **Análise Clusters**: Comparação entre grupos
- **Exportar Dados**: Geração de relatórios

### 3. Arquivo Excel Esperado
O sistema espera um arquivo com as abas:
- `pulso_consulta_diaria_cluster_antigo`
- `pulso_consulta_diaria`

## 🎯 Funcionalidades Principais

### KPIs Calculados:
- **Lacuna RL**: Diferença na Receita Líquida vs mediana do cluster
- **Lacuna Cupom**: Gap na quantidade de vendas
- **Lacuna BM**: Diferença no Boleto Médio
- **Lacuna PM**: Gap no Preço Médio
- **Lacuna Prod**: Diferença na Produtividade

### Visualizações:
- Gráficos de waterfall (decomposição)
- Distribuições e histogramas
- Matriz de correlações
- Rankings de oportunidades
- Análise por clusters

## ⚠️ Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python: https://www.python.org/downloads/
- Certifique-se de marcar "Add to PATH"
- Reinicie o computador após instalação

### Erro: "Falha na instalação de dependências"
- Verifique conexão com internet
- Execute como administrador
- Tente: `pip install --upgrade pip`

### Página não carrega
- Verifique se apareceu: "Local URL: http://localhost:8504"
- Tente acessar manualmente no navegador
- Verifique se porta 8504 não está em uso

### Erro no upload de arquivo
- Verifique se o arquivo é .xlsx
- Confirme se tem as abas necessárias
- Tente com arquivo menor

## 📞 Estrutura do Projeto

```
pulso_analise/
├── app.py                    # Página principal
├── instalar_e_executar.bat   # Instalador Windows
├── instalar_e_executar.ps1   # Instalador PowerShell  
├── instalar_e_executar.sh    # Instalador Linux/Mac
├── requirements.txt          # Dependências
├── config.py                # Configurações
├── pages/                   # Páginas do dashboard
│   ├── 2_Analise_Lacunas.py
│   ├── 3_Visao_Loja.py  
│   ├── 4_Clusters.py
│   └── 5_Exportar.py
├── src/                     # Código principal
│   ├── calculations.py      # Cálculos de lacunas
│   ├── data_loader.py       # Carregamento de dados
│   ├── visualizations.py    # Gráficos
│   └── utils.py            # Utilitários
└── data/                   # Dados e exports
    ├── upload/
    ├── processed/
    └── exports/
```

## 🛡️ Segurança e Privacidade

- Todos os dados ficam localmente no seu computador
- Nenhuma informação é enviada para servidores externos
- Para parar o sistema: feche a janela do terminal/prompt

## 📋 Requisitos do Sistema

- **SO**: Windows 7+, macOS 10.12+, Ubuntu 16.04+
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espaço**: 500MB livres
- **Internet**: Apenas para instalação inicial

---

**Desenvolvido para automação do relatório gerencial do Projeto Pulso** 🎯
