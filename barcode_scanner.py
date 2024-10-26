import cv2
from pyzbar.pyzbar import decode
import websocket
import json

def scan_barcode():
    cap = cv2.VideoCapture(0)
    barcode_processed = False

    ws = websocket.WebSocket()
    ws.connect("ws://localhost:3000")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray_frame)

        if decoded_objects and not barcode_processed:
            obj = decoded_objects[0]
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            barcode_data = obj.data.decode('utf-8')

            # Send the barcode data as a JSON string
            ws.send(json.dumps({"barcode": barcode_data}))

            print(f"Decoded Data: {barcode_data}")
            barcode_processed = True

        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    ws.close()

if __name__ == "__main__":
    try:
        scan_barcode()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
