
import asyncio
# import websockets
# import base64
# import numpy as np
from .views import receive_video
# async def receive_video():
#     uri = "ws://192.168.1.26:8765"  # Replace with the server's IP and port
#     async with websockets.connect(uri) as websocket:
#         while True:
#             try:
#                 # Receive base64-encoded image data from the WebSocket server
#                 data = await websocket.recv()
                
#                 # Decode base64 and convert to NumPy array
#                 buffer = base64.b64decode(data)
#                 image = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), 1)

#                 # Display the received frame
#                 cv2.imshow("Video Stream", image)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break

#             except websockets.exceptions.ConnectionClosedError:
#                 print("Connection closed with error.")
#                 break
#             except websockets.exceptions.ConnectionClosedOK:
#                 print("Connection closed normally.")
#                 break
receive_video()
if __name__ == "__main__":
    asyncio.run(main())