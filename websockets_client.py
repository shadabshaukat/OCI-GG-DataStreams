import asyncio
import websockets
import json
import logging
import ssl
import base64

# === CONFIGURATION ===
username = "oggadmin"
password = "abcdABCD1234##"
host = "ogg-t1"
port = 9102
stream_name = "DS"
begin_position = "now"  # Options: "earliest" or "now". Ref : https://docs.oracle.com/en-us/iaas/goldengate/doc/add-data-streams.html
ca_cert_path = "/tmp/ogg-t1.pem"  # Path to your custom certificate

# === URI CONSTRUCTION ===
uri = f"wss://{host}:{port}/services/v2/stream/{stream_name}?begin={begin_position}"

# === SSL CONTEXT SETUP ===
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(cafile=ca_cert_path)

# === Logging Setup ===
logfile = "websocket_messages.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')

# === Base64-Encoded Auth Header ===
auth_str = f"{username}:{password}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Authorization": f"Basic {auth_b64}"
}

async def consume_messages():
    try:
        async with websockets.connect(
            uri,
            ssl=ssl_context,
            extra_headers=headers
        ) as websocket:

            logging.info("✅ Connected to WebSocket server")

            while True:
                try:
                    message = await websocket.recv()
                    try:
                        data = json.loads(message)
                        if data:
                            logging.info(f"📨 Message received: {data}")
                            print(json.dumps(data, indent=2))
                        else:
                            logging.warning("⚠️ Received empty payload: []")
                    except json.JSONDecodeError:
                        logging.warning(f"⚠️ Received non-JSON message: {message}")
                except websockets.exceptions.ConnectionClosed as e:
                    logging.error(f"WebSocket connection closed: {e}")
                    break
    except Exception as e:
        logging.error(f"❌ Error connecting to WebSocket: {e}")
        print(f"❌ Error: {e}")

# === Entry Point ===
if __name__ == "__main__":
    print(f"Connecting to: {uri}")
    try:
        asyncio.run(consume_messages())  # For Python 3.7+
    except AttributeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(consume_messages())
