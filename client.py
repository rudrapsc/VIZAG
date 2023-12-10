import asyncio
import websockets
import cv2
import base64

async def send_video(uri):
    cap = cv2.VideoCapture(0)
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                encoded_string = base64.b64encode(buffer).decode()
                await websocket.send(encoded_string)
    finally:
        cap.release()

# Replace with the Django server's IP address and port
uri = "ws://192.168.29.66:8000/ws/stream/"
asyncio.get_event_loop().run_until_complete(send_video(uri))