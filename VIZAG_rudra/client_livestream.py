import asyncio
import websockets
import cv2
import base64

async def send_video(uri):
    cap = cv2.VideoCapture(0)  # Use camera index 0 (default camera)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    async with websockets.connect(uri) as websocket:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame from camera.")
                break

            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode()

            # Send the frame data to the server
            await websocket.send(frame_data)

    cap.release()

if __name__ == "__main__":
    server_uri = "ws://localhost:8000/ws/stream/"  # Replace with your server's URI
    asyncio.get_event_loop().run_until_complete(send_video(server_uri))
