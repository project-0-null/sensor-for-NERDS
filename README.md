# Sensor for NERDS 🚀

Sistema inteligente de **detecção de pessoas, rastreamento multiobjeto e cálculo de velocidade/direção de movimento em tempo real** usando Webcam, YOLOv11 e Fluxo Óptico Denso (Farneback).

Projetado para rodar em **qualquer computador** (Windows, Linux ou macOS), com ou sem placa de vídeo dedicada (GPU NVIDIA ou CPU).

---

## ⚡ Como Rodar em 1 Clique

Não precisa configurar ambiente virtual manualmente! O projeto conta com scripts automáticos que:
1. Verificam se o Python está instalado.
2. Criam automaticamente o ambiente virtual isolado chamado **`NERDS`**.
3. Detectam se você possui GPU NVIDIA (CUDA) ou apenas CPU, instalando a versão mais eficiente do PyTorch automaticamente.
4. Instalam todas as dependências na primeira execução.
5. Abrem a webcam e iniciam a detecção imediatamente!

### 🪟 No Windows
Basta dar **duplo clique** no arquivo:
```
run_nerds.bat
```
*(Caso prefira abrir via Prompt de Comando / PowerShell: `.\run_nerds.bat`)*

> **Nota:** Se você ainda não tem o Python instalado, baixe em [python.org](https://www.python.org/downloads/) e lembre-se de marcar a caixinha **"Add Python to PATH"**.

---

### 🐧 No Linux / macOS
Abra o terminal na pasta do projeto e execute:
```bash
./run_nerds.sh
```
*(Caso necessário, dê permissão de execução com `chmod +x run_nerds.sh`)*

---

## 🎮 Controles Durante a Execução

- **Sair da Aplicação:** Pressione a tecla `ESC` ou `q` com a janela de vídeo selecionada.

---

## 🛠️ Opções Avançadas (Linha de Comando)

Você também pode passar argumentos para o inicializador:

```bash
# Executar com um arquivo de vídeo gravado em vez de webcam:
python main.py --source meu_video.mp4

# Utilizar o detector clássico leve (HOG + SVM):
python main.py --mode classic

# Utilizar outro índice de webcam (ex: webcam externa):
python main.py --source 1
```

---

## 📂 Estrutura do Projeto

```
sensor-for-NERDS/
├── run_nerds.bat       # Inicializador automático para Windows
├── run_nerds.sh        # Inicializador automático para Linux/macOS
├── main.py             # Ponto de entrada com seleção inteligente de câmera
├── optical_yolo.py     # Motor YOLOv11 + Tracking + Fluxo Óptico
├── optical_classic.py  # Motor clássico (HOG + Farneback)
├── yolov11n.pt         # Pesos pré-treinados do modelo YOLOv11 Nano
├── requirements.txt    # Lista de dependências (OpenCV, Ultralytics, NumPy)
└── README.md           # Este manual
```

---

## 👥 Repositório & Colaboração

Repositório Oficial: [https://github.com/project-0-null/sensor-for-NERDS.git](https://github.com/project-0-null/sensor-for-NERDS.git)

Para clonar em um novo computador:
```bash
git clone https://github.com/project-0-null/sensor-for-NERDS.git
cd sensor-for-NERDS
# E execute run_nerds.bat (Windows) ou ./run_nerds.sh (Linux)
```
