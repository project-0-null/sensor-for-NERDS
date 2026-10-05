import cv2
import numpy as np


def run_classic_detector(source=0, show=True):
    """Executa deteccao de pessoas usando HOG + SVM e Fluxo Optico Farneback."""
    print("[INFO] Iniciando detector classico (HOG + SVM)...")
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERRO] Nao foi possivel abrir a fonte de video: {source}")
        return False

    ret, frame1 = cap.read()
    if not ret:
        print("[ERRO] Falha ao ler primeiro frame da camera.")
        cap.release()
        return False

    prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    window_name = "Sensor for NERDS - Classico (HOG+Farneback)"
    if show:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    print("[INFO] Pressione ESC ou 'q' para sair.")
    while True:
        ret, frame2 = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        boxes, _ = hog.detectMultiScale(frame2, winStride=(8, 8))

        for (x, y, w, h) in boxes:
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(frame2.shape[1], x + w + padding)
            y2 = min(frame2.shape[0], y + h + padding)

            roi_prev = prev_gray[y1:y2, x1:x2]
            roi_gray = gray[y1:y2, x1:x2]

            if roi_prev.shape != roi_gray.shape or roi_prev.size == 0:
                continue

            flow = cv2.calcOpticalFlowFarneback(
                roi_prev, roi_gray,
                None,
                0.5, 2, 10, 2, 3, 1.1, 0
            )

            mag = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
            mask = mag > 0.5

            if np.any(mask):
                dx = float(np.mean(flow[..., 0][mask]))
                dy = float(np.mean(flow[..., 1][mask]))
            else:
                dx, dy = 0.0, 0.0

            velocidade = np.sqrt(dx**2 + dy**2) * fps

            centro_x = x + w // 2
            centro_y = y + h // 2

            # Desenha vetor de movimento
            cv2.arrowedLine(
                frame2,
                (centro_x, centro_y),
                (int(centro_x + dx * 10), int(centro_y + dy * 10)),
                (0, 0, 255),
                2
            )

            # Informacoes de velocidade
            cv2.putText(
                frame2,
                f"v: {velocidade:.2f} px/s",
                (x, max(20, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        if show:
            cv2.imshow(window_name, frame2)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q'), ord('Q')):
                break

        prev_gray = gray

    cap.release()
    if show:
        cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    run_classic_detector()
