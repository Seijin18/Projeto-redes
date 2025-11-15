#!/bin/bash

# Script para executar os cenários faltantes com timeout maior
source /home/marshibs/ns3_env/bin/activate

export PYTHONPATH="/home/marshibs/ns-3-dev/build/bindings/python:/home/marshibs/ns-3-dev/build/lib:$PYTHONPATH"

RESULTADOS_DIR="/home/marshibs/redes/resultados"
mkdir -p "$RESULTADOS_DIR"

# Lista de cenários faltantes
CENARIOS=(
  "16 static tcp"
  "16 static mixed"
  "16 mobile tcp"
  "32 static cbr"
  "32 static tcp"
  "32 static mixed"
  "32 mobile cbr"
  "32 mobile tcp"
  "32 mobile mixed"
)

echo "Executando cenários faltantes ($(echo "${#CENARIOS[@]}" ) cenários)"
echo "Timeout: 600 segundos (10 minutos) por cenário"
echo ""

CENARIO_NUM=1
TOTAL=${#CENARIOS[@]}

for cenario in "${CENARIOS[@]}"; do
  read n_clientes mobilidade aplicacao <<< "$cenario"
  
  ARQUIVO="$RESULTADOS_DIR/c${n_clientes}_${mobilidade}_${aplicacao}.txt"
  
  if [ -f "$ARQUIVO" ]; then
    echo "[$CENARIO_NUM/$TOTAL] SKIP: c${n_clientes}_${mobilidade}_${aplicacao} (já existe)"
  else
    echo -n "[$CENARIO_NUM/$TOTAL] Executando: $n_clientes clientes, $mobilidade, $aplicacao... "
    
    if timeout 600 python3 /home/marshibs/redes/equipe_4_2s2025.py \
      --nClientes "$n_clientes" \
      --mobilidade "$mobilidade" \
      --aplicacao "$aplicacao" \
      --tempoSimulacao 60 > /tmp/sim_output_faltante.log 2>&1; then
      
      if [ -f "$ARQUIVO" ]; then
        echo "✓ OK"
      else
        echo "✗ ERRO: Arquivo não criado"
        tail -20 /tmp/sim_output_faltante.log
      fi
    else
      echo "✗ TIMEOUT/ERRO"
      tail -20 /tmp/sim_output_faltante.log
    fi
  fi
  
  ((CENARIO_NUM++))
  sleep 2
done

echo ""
TOTAL_FINAL=$(ls -1 "$RESULTADOS_DIR"/c*.txt 2>/dev/null | wc -l)
echo "Total final: $TOTAL_FINAL/36"
