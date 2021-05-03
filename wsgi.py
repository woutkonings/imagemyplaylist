s# -*- coding: utf-8 -*-

"""Application entry point."""
from flaskr import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)