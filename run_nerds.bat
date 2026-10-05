@echo off
setlocal enabledelayedexpansion
title Sensor for NERDS - Inicializador
cd /d "%~dp0"

echo ========================================================
echo             SENSOR FOR NERDS - INICIALIZADOR
echo ========================================================

:: 1. Verifica instalacao do Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Python nao foi encontrado no sistema!
    echo.
    echo Por favor, instale o Python 3.10 ou superior atraves do site oficial:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante a instalacao, marque a opcao:
    echo   "[X] Add Python to PATH" ou "[X] Adicionar Python ao PATH"
    echo.
    pause
    exit /b 1
)

:: 2. Cria o ambiente virtual NERDS se nao existir
if not exist "NERDS\Scripts\activate.bat" (
    echo [INFO] Criando ambiente virtual isolado (NERDS)...
    python -m venv NERDS
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao criar o ambiente virtual NERDS.
        echo Verifique se possui permissoes no diretorio.
        pause
        exit /b 1
    )
)

:: 3. Ativa o ambiente virtual
call NERDS\Scripts\activate.bat

:: 4. Instala dependencias na primeira execucao
if not exist "NERDS\.installed" (
    echo.
    echo ========================================================
    echo  Configuracao Inicial: Baixando dependencias necessarias
    echo  (Isso so acontece na primeira vez!)
    echo ========================================================
    echo.

    python -m pip install --upgrade pip

    :: Detecta presenca de GPU NVIDIA via nvidia-smi
    where nvidia-smi >nul 2>nul
    if %errorlevel% equ 0 (
        echo [INFO] GPU NVIDIA detectada! Instalando PyTorch com aceleracao CUDA...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    ) else (
        echo [INFO] Nenhuma GPU dedicada detectada. Instalando versao leve para CPU...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    )

    echo [INFO] Instalando bibliotecas necessarias (OpenCV, Ultralytics, NumPy)...
    pip install -r requirements.txt

    if %errorlevel% equ 0 (
        type nul > "NERDS\.installed"
        echo.
        echo [SUCESSO] Instalacao finalizada com sucesso!
        echo.
    ) else (
        echo.
        echo [ERRO] Ocorreu uma falha ao instalar as dependencias.
        pause
        exit /b 1
    )
)

:: 5. Executa a aplicacao
echo [INFO] Iniciando o Sensor for NERDS...
python main.py %*

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Aplicacao finalizada com codigo de saida %errorlevel%.
    pause
)
