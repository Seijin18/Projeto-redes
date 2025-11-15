#!/bin/bash
# Script para executar simulações NS-3 com PYTHONPATH configurado

export PYTHONPATH=/home/marshibs/ns-3-dev/build/bindings/python:/home/marshibs/ns-3-dev/build/lib:$PYTHONPATH

python3 /home/marshibs/redes/equipe_4_2s2025.py "$@"
