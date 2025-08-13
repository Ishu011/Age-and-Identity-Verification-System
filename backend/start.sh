#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT --workers=4 --timeout=300 app:app
