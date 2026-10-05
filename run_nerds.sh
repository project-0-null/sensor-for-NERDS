#!/usr/bin/env bash
set -e

# Garante execucao no diretorio do proprio script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "          SENSOR FOR NERDS - INICIALIZADOR (LINUX)"
echo "========================================================"

# 1. Verifica instalacao do Python 3
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERRO] python3 não foi encontrado no sistema."
    echo "Por favor instale o Python 3 e o modulo venv:"
    echo "  sudo apt update && sudo apt install -y python3 python3-venv python3-pip"
    echo ""
    exit 1
fi

# 2. Cria ambiente virtual NERDS se nao existir
if [ ! -d "NERDS" ] || [ ! -f "NERDS/bin/activate" ]; then
    echo "[INFO] Criando ambiente virtual isolado (NERDS)..."
    python3 -m venv NERDS
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar ambiente virtual."
        echo "Tente rodar: sudo apt install python3-venv"
        exit 1
    fi
fi

# 3. Ativa o ambiente virtual
source NERDS/bin/activate

# 4. Instala dependencias na primeira execucao
if [ ! -f "NERDS/.installed" ]; then
    echo ""
    echo "========================================================"
    echo "  Configuração Inicial: Baixando dependências necessárias"
    echo "  (Isso só acontece na primeira vez!)"
    echo "========================================================"
    echo ""

    pip install --upgrade pip

    # Verifica presenca de GPU NVIDIA
    if command -v nvidia-smi &> /dev/null; then
        echo "[INFO] GPU NVIDIA detectada! Instalando PyTorch com aceleração CUDA..."
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    else
        echo "[INFO] Nenhuma GPU dedicada detectada. Instalando versão leve para CPU..."
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    fi

    echo "[INFO] Instalando bibliotecas do projeto (OpenCV, Ultralytics, NumPy)..."
    pip install -r requirements.txt

    touch "NERDS/.installed"
    echo ""
    echo "[SUCESSO] Instalação concluída com sucesso!"
    echo ""
fi

# 5. Executa a aplicacao
echo "[INFO] Iniciando o Sensor for NERDS..."
python3 main.py "$@"
