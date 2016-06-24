#!/bin/bash
gunicorn server:app --bind=0.0.0.0:8000 --reload --workers 1 --timeout 120 --log-level=debug 
