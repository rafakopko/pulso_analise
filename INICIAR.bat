@echo off
chcp 65001 > nul
title Dashboard Pulso - INICIAR
color 0A

echo.
echo ================================
echo    🎯 DASHBOARD PULSO v1.0
echo ================================
echo.
echo ⚡ INICIANDO SISTEMA...

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python não encontrado!
    echo.
    echo 🤖 Instalando Python automaticamente...
    echo    Por favor aguarde, isso pode levar alguns minutos.
    echo.
    
    :: Baixar Python usando PowerShell
    echo 📥 Baixando Python 3.11...
    powershell -command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe' -UseBasicParsing } catch { Write-Host 'Erro no download'; exit 1 }}"
    
    if not exist "python_installer.exe" (
        echo ❌ ERRO: Falha no download do Python!
        echo.
        echo 📖 Instalação manual necessária:
        echo 1. Acesse: https://www.python.org/downloads/
        echo 2. Baixe Python 3.11 ou superior
        echo 3. ⚠️  MARQUE "Add Python to PATH"
        echo.
        start https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo ⚙️  Instalando Python (pode demorar alguns minutos)...
    echo    IMPORTANTE: Não feche esta janela!
    
    :: Instalar Python silenciosamente
    python_installer.exe /quiet PrependPath=1 Include_test=0 InstallAllUsers=0
    
    :: Aguardar instalação
    timeout /t 10 /nobreak > nul
    
    :: Limpar arquivo temporário
    del python_installer.exe
    
    :: Verificar se foi instalado
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ ERRO: Python não foi instalado corretamente!
        echo    Tente reiniciar o computador e executar novamente.
        pause
        exit /b 1
    )
    
    echo ✅ Python instalado com sucesso!
)

:: Instalar dependências se necessário
echo ⏳ Verificando dependências...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependências...
    python -m pip install --quiet streamlit pandas plotly openpyxl xlsxwriter
)

:: Iniciar aplicação
echo ✅ Iniciando Dashboard Pulso...
echo.
echo 🌐 Abrindo no navegador: http://localhost:8504
echo ⏹️  Para parar: feche esta janela
echo.

start http://localhost:8504
streamlit run app.py --server.port 8504 --server.headless true

pause
