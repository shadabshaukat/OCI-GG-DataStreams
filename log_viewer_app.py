from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

LOGFILE_PATH = "websocket_messages.log"
MAX_LINES = 500


def tail_log(file_path: str, num_lines: int):
    """Return the last `num_lines` from the log file."""
    if not os.path.isfile(file_path):
        return ["Log file not found."]
    with open(file_path, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        block_size = 1024
        data = b''
        while file_size > 0 and data.count(b'\n') <= num_lines:
            file_size = max(file_size - block_size, 0)
            f.seek(file_size)
            data = f.read() + data
        lines = data.splitlines()[-num_lines:]
        return [line.decode(errors="ignore") for line in lines]


@app.get("/", response_class=HTMLResponse)
async def get_log(request: Request):
    lines = tail_log(LOGFILE_PATH, MAX_LINES)
    lines.reverse()  # Flip to show newest lines first
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Oracle Goldengate Data Streams Log Viewer</title>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{
                background-color: black;
                color: #00FF00;
                font-family: 'Courier New', Courier, monospace;
                padding: 20px;
                white-space: pre-wrap;
                overflow-y: scroll;
                height: 100vh;
            }}
            h1 {{
                color: #00FF00;
            }}
        </style>
    </head>
    <body>
        <h1>☣ Oracle Goldengate Data Streams Log Viewer (Newest First)</h1>
        <div id="log">
            {"<br>".join(lines)}
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
