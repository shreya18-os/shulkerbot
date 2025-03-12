#!/bin/bash
apt-get update
apt-get install -y libffi-dev libnacl-dev python3-pip
pip install --no-cache-dir --force-reinstall discord.py pynacl ffmpeg
