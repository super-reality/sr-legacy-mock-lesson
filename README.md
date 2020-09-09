# FunnyLesson

## Setup

It's recommended that you set up [virtual environments](https://docs.python.org/3/library/venv.html) first.

```shell script
pip install -r requirements.txt
```

**Known issue:** `opencv-python` may cause antivirus false flags, due to its nature of requesting sensitive features.

## Running

```shell script
python server.py
```

## Building

```shell script
pyinstaller server.py --onefile
```

**Known issue:** Same as above; whitelist `build/` and `dist/` directories in your antivirus.
