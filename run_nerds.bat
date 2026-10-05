@echo off
setlocal enabledelayedexpansion
title Sensor for NERDS - Inicializador
cd /d "%~dp0"

echo ========================================================
echo             SENSOR FOR NERDS - INICIALIZADOR
echo ========================================================
echo.

REM 1. Verifica se o Python esta instalado e funcionando
set "PY_CMD="

python -c "import sys" >nul 2>nul
if !errorlevel! equ 0 (
    set "PY_CMD=python"
) else (
    py -c "import sys" >nul 2>nul
    if !errorlevel! equ 0 (
        set "PY_CMD=py"
    )
)

if "%PY_CMD%"=="" (
    echo [ERRO] Python nao encontrado ou configurado incorretamente!
    echo.
    echo Para resolver:
    echo 1. Baixe o instalador no site oficial: https://www.python.org/downloads/
    echo 2. Execute o instalador e marque OBRIGATORIAMENTE a caixa:
    echo    "[X] Add Python to PATH" ou "[X] Adicionar Python ao PATH"
    echo 3. Finalize a instalacao e tente abrir este arquivo novamente.
    echo.
    goto :pause_and_exit
)

REM 2. Cria o ambiente virtual isolado (NERDS) se ainda nao existir
if not exist "NERDS\Scripts\activate.bat" (
    echo [INFO] Criando ambiente virtual isolado (NERDS)...
    %PY_CMD% -m venv NERDS
    if not exist "NERDS\Scripts\activate.bat" (
        echo.
        echo [ERRO] Falha ao criar a pasta NERDS.
        echo Verifique se ha permissoes de escrita nesta pasta.
        goto :pause_and_exit
    )
)

REM 3. Ativa o ambiente virtual
call NERDS\Scripts\activate.bat

REM 4. Instala dependencias na primeira execucao
if not exist "NERDS\.installed" (
    echo.
    echo ========================================================
    echo  Configuracao Inicial: Baixando dependencias necessarias
    echo  (Isso so acontece na primeira vez!)
    echo ========================================================
    echo.

    python -m pip install --upgrade pip

    REM Detecta presenca de GPU NVIDIA via nvidia-smi
    where nvidia-smi >nul 2>nul
    if !errorlevel! equ 0 (
        echo [INFO] GPU NVIDIA detectada! Instalando PyTorch com aceleracao CUDA...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    ) else (
        echo [INFO] Nenhuma GPU dedicada detectada. Instalando versao leve para CPU...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    )

    echo [INFO] Instalando bibliotecas necessarias (OpenCV, Ultralytics, NumPy)...
    pip install -r requirements.txt

    if !errorlevel! neq 0 (
        echo.
        echo [ERRO] Ocorreu uma falha ao baixar/instalar os pacotes.
        goto :pause_and_exit
    )

    type nul > "NERDS\.installed"
    echo.
    echo [SUCESSO] Instalacao finalizada com sucesso!
    echo.
)

REM 5. Executa a aplicacao principal
echo [INFO] Iniciando o Sensor for NERDS...
python main.py %*

if !errorlevel! neq 0 (
    echo.
    echo [AVISO] Aplicacao finalizada com codigo de retorno !errorlevel!.
)

:pause_and_exit
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
