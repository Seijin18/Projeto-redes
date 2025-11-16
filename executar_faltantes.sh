#!/bin/bash

# Script para executar apenas os cenários faltantes (32 clientes)
# Com logging detalhado em arquivo

# Ativar virtual environment
source /home/marshibs/ns3_env/bin/activate

# Configurar PYTHONPATH
export PYTHONPATH="/home/marshibs/ns-3-dev/build/bindings/python:/home/marshibs/ns-3-dev/build/lib:$PYTHONPATH"

# Diretório de destino
RESULTADOS_DIR="/home/marshibs/redes/resultados"
LOG_FILE="/home/marshibs/redes/execucao_faltantes.log"

mkdir -p "$RESULTADOS_DIR"

# Inicializar log
echo "========================================================================" > "$LOG_FILE"
echo "EXECUÇÃO DOS CENÁRIOS FALTANTES (32 clientes)" >> "$LOG_FILE"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "========================================================================" | tee -a "$LOG_FILE"
echo "EXECUÇÃO DOS CENÁRIOS FALTANTES (32 clientes)"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================================================" | tee -a "$LOG_FILE"
echo ""

# Cenários faltantes (apenas 32 clientes)
CENARIOS=(
  "32 static cbr"
  "32 static tcp"
  "32 static mixed"
  "32 mobile cbr"
  "32 mobile tcp"
  "32 mobile mixed"
)

TOTAL=6
ATUAL=1
TEMPO_INICIO=$(date +%s)

for config in "${CENARIOS[@]}"; do
  read N_CLIENTES MOBILIDADE APLICACAO <<< "$config"
  ARQUIVO_RESULTADO="$RESULTADOS_DIR/c${N_CLIENTES}_${MOBILIDADE}_${APLICACAO}.txt"
  
  TEMPO_CENARIO_INICIO=$(date +%s)
  
  # Verificar se já existe
  if [ -f "$ARQUIVO_RESULTADO" ]; then
    echo "[$ATUAL/$TOTAL] SKIP: c${N_CLIENTES}_${MOBILIDADE}_${APLICACAO} (já existe)" | tee -a "$LOG_FILE"
    ((ATUAL++))
    continue
  fi
  
  MSG="[$ATUAL/$TOTAL] Executando: N=$N_CLIENTES, Mobilidade=$MOBILIDADE, Aplicação=$APLICACAO..."
  echo "$MSG" | tee -a "$LOG_FILE"
  
  # Executar simulação com timeout de 30 minutos
  if timeout 1800 python3 /home/marshibs/redes/equipe_4_2s2025.py \
      --nClientes "$N_CLIENTES" \
      --mobilidade "$MOBILIDADE" \
      --aplicacao "$APLICACAO" \
      --tempoSimulacao 60 >> "$LOG_FILE" 2>&1; then
    
    TEMPO_CENARIO_FIM=$(date +%s)
    TEMPO_CENARIO=$((TEMPO_CENARIO_FIM - TEMPO_CENARIO_INICIO))
    MINUTOS_CENARIO=$((TEMPO_CENARIO / 60))
    SEGUNDOS_CENARIO=$((TEMPO_CENARIO % 60))
    
    if [ -f "$ARQUIVO_RESULTADO" ]; then
      echo "[$ATUAL/$TOTAL] ✓ OK (${MINUTOS_CENARIO}m ${SEGUNDOS_CENARIO}s)" | tee -a "$LOG_FILE"
    else
      echo "[$ATUAL/$TOTAL] ✗ ERRO: Arquivo não criado" | tee -a "$LOG_FILE"
    fi
  else
    TEMPO_CENARIO_FIM=$(date +%s)
    TEMPO_CENARIO=$((TEMPO_CENARIO_FIM - TEMPO_CENARIO_INICIO))
    MINUTOS_CENARIO=$((TEMPO_CENARIO / 60))
    SEGUNDOS_CENARIO=$((TEMPO_CENARIO % 60))
    echo "[$ATUAL/$TOTAL] ✗ TIMEOUT/ERRO (${MINUTOS_CENARIO}m ${SEGUNDOS_CENARIO}s)" | tee -a "$LOG_FILE"
  fi
  
  echo "" | tee -a "$LOG_FILE"
  ((ATUAL++))
  
  # Pausa entre execuções
  sleep 2
done

TEMPO_FIM=$(date +%s)
TEMPO_TOTAL=$((TEMPO_FIM - TEMPO_INICIO))
MINUTOS=$((TEMPO_TOTAL / 60))
SEGUNDOS=$((TEMPO_TOTAL % 60))

echo "========================================================================" | tee -a "$LOG_FILE"
echo "EXECUÇÃO CONCLUÍDA"
echo "Tempo total: ${MINUTOS}m ${SEGUNDOS}s" | tee -a "$LOG_FILE"
echo "========================================================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Resumo final
TOTAL_FILES=$(ls -1 "$RESULTADOS_DIR"/c*.txt 2>/dev/null | wc -l)
echo "Resumo:" | tee -a "$LOG_FILE"
echo "  • Arquivos gerados: $TOTAL_FILES/36" | tee -a "$LOG_FILE"
echo "  • Log salvo em: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Listar arquivos faltantes
FALTANTES=()
for N in 32; do
  for MOB in static mobile; do
    for APP in cbr tcp mixed; do
      if [ ! -f "$RESULTADOS_DIR/c${N}_${MOB}_${APP}.txt" ]; then
        FALTANTES+=("c${N}_${MOB}_${APP}")
      fi
    done
  done
done

if [ ${#FALTANTES[@]} -eq 0 ]; then
  echo "✓ TODOS OS 36 CENÁRIOS FORAM COMPLETADOS COM SUCESSO!" | tee -a "$LOG_FILE"
else
  echo "✗ Cenários ainda faltando:" | tee -a "$LOG_FILE"
  for f in "${FALTANTES[@]}"; do
    echo "  • $f" | tee -a "$LOG_FILE"
  done
fi

echo "" | tee -a "$LOG_FILE"
echo "========================================================================" | tee -a "$LOG_FILE"
