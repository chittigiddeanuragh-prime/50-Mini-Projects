import cv2
from ultralytics import YOLO


MODEL_PATH = "best.pt"
CAMERA_INDEX = 0
CONFIDENCE = 0.50


model = YOLO(MODEL_PATH)

camera = cv2.VideoCapture(CAMERA_INDEX)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()


print("Weapon Detection System Started")
print("Press Q to quit.")


while True:

    success, frame = camera.read()

    if not success:
        print("Error: Could not read camera frame.")
        break

    results = model(
        frame,
        conf=CONFIDENCE,
        verbose=False
    )

    detected_weapon = False

    for result in results:

        boxes = result.boxes

        for box in boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            confidence = float(
                box.conf[0]
            )

            class_id = int(
                box.cls[0]
            )

            class_name = model.names[class_id]

            detected_weapon = True

            label = (
                f"{class_name.upper()} "
                f"{confidence * 100:.1f}%"
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            cv2.rectangle(
                frame,
                (x1, y1 - 35),
                (x2, y1),
                (0, 0, 255),
                -1
            )

            cv2.putText(
                frame,
                label,
                (x1 + 5, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

    if detected_weapon:

        cv2.putText(
            frame,
            "WARNING: OBJECT DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )

    else:

        cv2.putText(
            frame,
            "STATUS: NO DETECTION",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Computer Vision Weapon Detection",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()