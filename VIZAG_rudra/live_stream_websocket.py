import asyncio
import websockets
import cv2
import base64

async def video_stream(websocket, path):
    cap = cv2.VideoCapture(0)  # Capture video from the first camera

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Compress the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            # Convert to base64 and send through the WebSocket
            await websocket.send(base64.b64encode(buffer).decode())
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed with error.")
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally.")
    finally:
        cap.release()

async def main():
    # Replace with the server's IP and desired port
    async with websockets.serve(video_stream, "192.168.29.66", 8765):
        await asyncio.Future()  # Run indefinitely

if __name__ == "__main__":
    asyncio.run(main())
