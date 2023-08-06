#!/usr/bin/env python3
import os

# Estrutura para configurações do app
config_path = 'config'
conf_path = os.path.join('config', 'conf')
if not os.path.exists(conf_path):
    os.makedirs(conf_path)
    
    filename = 'paths.py'
    data = "import os\n\n\nROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))"
    with open(os.path.join(config_path, filename), 'w') as f:
        f.write(data)