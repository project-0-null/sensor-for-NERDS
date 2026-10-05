import argparse
import sys
import cv2
from optical_yolo import run_yolo_detector
from optical_classic import run_classic_detector


def check_webcam(index=0):
    """Verifica se a webcam no indice especificado pode ser acessada."""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return False
    ret, _ = cap.read()
    cap.release()
    return ret


def find_available_camera():
    """Tenta detectar uma webcam valida (indices 0 ou 1)."""
    for idx in [0, 1]:
        if check_webcam(idx):
            return idx
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Sensor for NERDS - Deteccao de Pessoas e Fluxo Optico em Tempo Real"
    )
    parser.add_argument(
        "--mode",
        choices=["yolo", "classic"],
        default="yolo",
        help="Modo de deteccao: 'yolo' (YOLOv11 Deep Learning, padrao) ou 'classic' (HOG + SVM)",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Fonte de video: '0' ou '1' para webcam, ou caminho de arquivo de video (ex: video.mp4)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov11n.pt",
        help="Modelo YOLO para deteccao (padrao: yolov11n.pt)",
    )

    args = parser.parse_args()

    # Determina a fonte de video
    if args.source.isdigit():
        source_idx = int(args.source)
        # Se for webcam 0 padrao, valida se ela esta aberta ou se precisa tentar a 1
        if source_idx == 0 and not check_webcam(0):
            print("[AVISO] Câmera no índice 0 não respondeu. Testando índice 1...")
            if check_webcam(1):
                print("[INFO] Câmera encontrada no índice 1!")
                source = 1
            else:
                print("\n" + "=" * 60)
                print("[ALERTA] Não foi possível acessar a webcam (tentadas portas 0 e 1).")
                print("Possíveis causas:")
                print("  1. A webcam não está conectada.")
                print("  2. Outro programa (Teams, Zoom, Discord, etc.) está usando a câmera.")
                print("  3. Permissões de câmera desativadas no sistema operacional.")
                print("=" * 60 + "\n")
                input("Pressione Enter para sair...")
                sys.exit(1)
        else:
            source = source_idx
    else:
        source = args.source

    print("\n" + "=" * 60)
    print("           SENSOR FOR NERDS - SISTEMA INICIADO")
    print(f" Modo: {args.mode.upper()}")
    print(f" Fonte: {source}")
    print("=" * 60 + "\n")

    if args.mode == "yolo":
        success = run_yolo_detector(source=source, model_path=args.model)
    else:
        success = run_classic_detector(source=source)

    if not success:
        print("[ERRO] A execução do detector foi interrompida com falha.")
        sys.exit(1)


if __name__ == "__main__":
    main()
