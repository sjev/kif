#!/bin/bash
echo export PATH=$PATH:/home/$USER/.local/bin >> ~/.bashrc
source ~/.bashrc

echo "Running container init, use this script to install libraries etc."
pip install -e .
