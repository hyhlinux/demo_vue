# !/usr/bin/env python
import sys
import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../')
from src.views import app
from src.config import CONFIG

current_directory = os.path.dirname(os.path.abspath(__name__))
app.static('/statics', os.path.join(current_directory, 'statics'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
