import os
import sys

# Set the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# pylint: disable=wrong-import-position
from .app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)