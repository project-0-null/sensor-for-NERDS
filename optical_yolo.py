import os
import cv2
import numpy as np
from ultralytics import YOLO


def run_yolo_detector(source=0, model_path="yolov11n.pt", show=True, imgsz=320, flow_interval=3):
    """
    Executa deteccao e rastreamento de pessoas com YOLOv11 e calculo de velocidade
    via Fluxo Optico Denso (Farneback).
    """
    # Se o arquivo de modelo nao estiver no caminho direto, tenta encontrar na mesma pasta do script
    if not os.path.exists(model_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_model = os.path.join(script_dir, model_path)
        if os.path.exists(local_model):
            model_path = local_model

    print(f"[INFO] Carregando modelo YOLO: {model_path}...")
    model = YOLO(model_path)

    print(f"[INFO] Abrindo fonte de video: {source}...")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERRO] Nao foi possivel conectar a camera (indice {source}).")
        return False

    ret, frame1 = cap.read()
    if not ret:
        print("[ERRO] Falha ao capturar primeiro frame da webcam.")
        cap.release()
        return False

    prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    window_name = "Sensor for NERDS - YOLOv11 + Fluxo Optico"
    if show:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_count = 0
    last_movements = {}  # {track_id: (dx, dy, velocidade)}

    print("[INFO] Execucao iniciada com sucesso. Pressione ESC ou 'q' para fechar.")

    while True:
        ret, frame2 = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Rastreamento multiobjeto persistente (ByteTrack/BoT-SORT integrado)
        results = model.track(frame2, persist=True, imgsz=imgsz, verbose=False)
        boxes = []

        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                cls = int(box.cls[0])
                # Classe 0 = person no dataset COCO
                if cls != 0:
                    continue
                if box.id is None:
                    continue

                track_id = int(box.id[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                boxes.append((track_id, x1, y1, x2 - x1, y2 - y1))

        new_movements = {}

        for (track_id, x, y, w, h) in boxes:
            dx, dy, velocidade = 0.0, 0.0, 0.0

            # Desenha retangulo verde ao redor da pessoa
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(frame2.shape[1], x + w + padding)
            y2 = min(frame2.shape[0], y + h + padding)

            is_flow_frame = (frame_count % flow_interval == 0)

            if is_flow_frame:
                roi_prev = prev_gray[y1:y2, x1:x2]
                roi_gray = gray[y1:y2, x1:x2]

                if roi_prev.shape == roi_gray.shape and roi_prev.size > 0:
                    flow = cv2.calcOpticalFlowFarneback(
                        roi_prev, roi_gray,
                        None,
                        0.5, 2, 10, 2, 3, 1.1, 0
                    )

                    mag = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
                    mask = mag > 0.5  # ignora ruido e microvibracoes

                    if np.any(mask):
                        dx_raw = float(np.mean(flow[..., 0][mask]))
                        dy_raw = float(np.mean(flow[..., 1][mask]))
                    else:
                        dx_raw, dy_raw = 0.0, 0.0

                    # Suavizacao e verificacao de inversao com base no movimento anterior
                    if track_id in last_movements:
                        prev_dx, prev_dy, _ = last_movements[track_id]

                        # Produto escalar entre vetor atual e anterior
                        dot = dx_raw * prev_dx + dy_raw * prev_dy
                        if dot < 0:
                            # Inversao brusca de movimento: adota nova direcao sem atrito
                            dx, dy = dx_raw, dy_raw
                        else:
                            # Suavizacao temporal ponderada
                            alpha = 0.6
                            dx = alpha * prev_dx + (1.0 - alpha) * dx_raw
                            dy = alpha * prev_dy + (1.0 - alpha) * dy_raw
                    else:
                        dx, dy = dx_raw, dy_raw

                    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
                    velocidade = np.sqrt(dx**2 + dy**2) * fps

                    if velocidade < 1.0:
                        dx, dy, velocidade = 0.0, 0.0, 0.0
            else:
                # Mantem a ultima estimativa de velocidade nos frames intermediarios
                if track_id in last_movements:
                    dx, dy, velocidade = last_movements[track_id]
                else:
                    dx, dy, velocidade = 0.0, 0.0, 0.0

            new_movements[track_id] = (dx, dy, velocidade)

            # Visualizacao
            cx = x + w // 2
            cy = y + h // 2

            # Vetor de movimento (seta vermelha)
            if velocidade > 1.0:
                cv2.arrowedLine(
                    frame2,
                    (cx, cy),
                    (int(cx + dx * 10), int(cy + dy * 10)),
                    (0, 0, 255),
                    2
                )

            # Legenda de identificacao e velocidade
            label = f"ID #{track_id} | {velocidade:.1f} px/s"
            cv2.putText(
                frame2,
                label,
                (x, max(20, y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        last_movements = new_movements
        prev_gray = gray

        if show:
            cv2.imshow(window_name, frame2)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q'), ord('Q')):
                break

    cap.release()
    if show:
        cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    run_yolo_detector()
