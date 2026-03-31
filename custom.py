import asyncio
import websockets
import json
import pyautogui

async def main():
    async with websockets.serve(handle_droidpad, "0.0.0.0", 8765):
        print(f"WebSocket server running on ws://0.0.0.0:8765")
        print("Press Ctrl+C to stop the server")
        await asyncio.Future()

async def handle_droidpad(websocket):
    print("Device Linked!")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                state = data.get("state")
                btn_id = data.get("id")
                print(f"Received: {btn_id}")
                pyautogui.write(btn_id)
            except websockets.exceptions.ConnectionClosed:
              print("Device disconnected")
    except Exception as e:
        print(f"Error in connection: {e}")
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
