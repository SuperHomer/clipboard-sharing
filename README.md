# Clipboard sharing using sockets

## Description

This project aims to share the clipboard between multiple clients, includes a multi-threaded server and a client application implemented in Python. The server can handle multiple client connections simultaneously and broadcast messages from one client to all others. The client connects to the server, listens for incoming messages, and has a copy event functionality. Both the server and client use environment variables for configuration. The encryption between clients can be enable (see Usage section) and it uses Fernet encryption (see: https://cryptography.io/en/latest/fernet/)

## Installation

Clone the repository to your local machine:
```bash
git clone git@github.com:SuperHomer/clipboard-sharing.git
```

Navigate to the prject directory:
```bash
cd clipboard-sharing
```

Install th required Python packages:
```bash
pip install -r requirements.txt
```

## Usage
Set the necessary environment variables in a .env file:
```
HOST=<your-host>
PORT=<your-port>
KEY=<your-key>
PREFIX_SIZE=<your-prefix-size>
INIT_MESSAGE=<your-initial-message>
ENCRYPTION_ENABLE=<True-or-False>
```

See an example:
```
KEY=<your-key>
HOST="127.0.0.1"
PORT=9090
PREFIX_SIZE=4
INIT_MESSAGE="You are now connected to the server..."
ENCRYPTION_ENABLE=True
```
For key generation checkout the fernet documentation: https://cryptography.io/en/latest/fernet/

Run the server:
```python
python server.py
```

In a new terminal run the client:
```python
python client.py
```
You can run as many clients as you want to share the clipboard with.