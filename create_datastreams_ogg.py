import asyncio
import requests
import websockets
import json
import ssl
import pathlib
import urllib.parse

async def client():
    # Define connection parameters
    username = "oggadmin"
    raw_password = "abcdABCD1234##"
    password = urllib.parse.quote(raw_password)  # Encode special characters
    host = "ogg-t1"
    port = 9102

    # Construct URL for POST request
    post_url = f"https://{username}:{password}@{host}:{port}/services/v2/stream/DS"

    # Create the streaming resource
    payload = {"source": {"trail": "aa"}}
    response = requests.post(post_url, json=payload, verify='/tmp/ogg-t1.pem')
    if response.status_code != 200:
        print(f"Failed to create stream: {response.status_code} - {response.text}")
        return

    # Prepare SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    pem_path = pathlib.Path("/tmp/ogg-t1.pem")  # Replace with actual PEM path
    ssl_context.load_verify_locations(pem_path)
    ssl_context.load_cert_chain(pem_path)

    # Construct WebSocket URL
    ws_url = f"wss://{username}:{password}@{host}:{port}/services/v2/stream/DS?begin=earliest"

    # Establish websocket connection and receive data
    async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
        while True:
            try:
                resp = await websocket.recv()
                records = json.loads(resp)
                for rec in records:
                    print(rec)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
                break
            except Exception as e:
                print(f"Error: {e}")

# Run the client
asyncio.get_event_loop().run_until_complete(client())
