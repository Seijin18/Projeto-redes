#!/bin/bash
# Script wrapper que ativa o ambiente virtual Python e executa o simulador NS-3

source /home/marshibs/ns3_env/bin/activate

# Adicionar NS-3 ao PYTHONPATH se instalado
# export PYTHONPATH=/path/to/ns3/install/lib/python/site-packages:$PYTHONPATH

# Executar o script Python com os argumentos passados
python3 /home/marshibs/redes/equipe_4_2s2025.py "$@"
