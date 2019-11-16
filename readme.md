# UniQueue Backend
### Berkeley CS160 FA19 Project

## Usage Instructions

First install the required packages:

```sh
pip3 install -r requirements.txt
```

Then start the web server

```sh
gunicorn app:app
```

Or, for debugging purposes:

```sh
python3 app.py
```