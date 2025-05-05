# OCI-GG-DataStreams

## Clone Repo
```
git clone https://github.com/shadabshaukat/OCI-GG-DataStreams.git

cd OCI-GG-DataStreams/
```

## Install Python Packages
```
## For Python3.7 onwards
sudo pip3 install fastapi websockets uvicorn

## For Python3.6 and below
sudo pip3 install "uvicorn<0.18.0"
```

## Create Data Stream and WebSockets Secure Client
In a TMUX Session
```
sudo yum install -y tmux
tmux

python3 create_datastreams.py
python3 websockets_client.py
```

## Launch Log Viewer App
In Seperate TMUX session
```
tmux
/usr/local/bin/uvicorn log_viewer_app:app --host 0.0.0.0 --port 8000 --reload
```

## Open Browser
http://localhost:8000/

<img width="1242" alt="Screenshot 2025-05-06 at 00 03 34 1" src="https://github.com/user-attachments/assets/861fbc47-31d2-49e4-9765-e302ed862662" />

