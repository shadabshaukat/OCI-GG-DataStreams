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
