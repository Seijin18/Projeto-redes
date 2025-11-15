#!/bin/bash

# Script para executar todos os 36 cenários da simulação
# UNIFESP IC 2617 - Redes de Computadores
# Equipe 4 - 2º Semestre 2025

# Ativar virtual environment
source /home/marshibs/ns3_env/bin/activate

# Diretório de destino
RESULTADOS_DIR="/home/marshibs/redes/resultados"
mkdir -p "$RESULTADOS_DIR"

# Configurar PYTHONPATH
export PYTHONPATH="/home/marshibs/ns-3-dev/build/bindings/python:/home/marshibs/ns-3-dev/build/lib:$PYTHONPATH"

# Parâmetros
CLIENTES=(1 2 4 8 16 32)
MOBILIDADES=("static" "mobile")
APLICACOES=("cbr" "tcp" "mixed")
TEMPO_SIMULACAO=60  # Conforme especificação UNIFESP

TOTAL_CENARIOS=36
CENARIO_ATUAL=1

echo "========================================================================"
echo "Executando 36 cenários de simulação NS-3"
echo "========================================================================"
echo "Total de cenários: $TOTAL_CENARIOS"
echo "Diretório de resultados: $RESULTADOS_DIR"
echo "Tempo de simulação: ${TEMPO_SIMULACAO}s"
echo "========================================================================"
echo ""

TEMPO_INICIO=$(date +%s)

# Iterar sobre todos os cenários
for N_CLIENTES in "${CLIENTES[@]}"; do
    for MOBILIDADE in "${MOBILIDADES[@]}"; do
        for APLICACAO in "${APLICACOES[@]}"; do
            ARQUIVO_RESULTADO="$RESULTADOS_DIR/c${N_CLIENTES}_${MOBILIDADE}_${APLICACAO}.txt"
            
            # Skip if already exists
            if [ -f "$ARQUIVO_RESULTADO" ]; then
                echo "[$CENARIO_ATUAL/36] SKIP: c${N_CLIENTES}_${MOBILIDADE}_${APLICACAO} (já existe)"
                ((CENARIO_ATUAL++))
                continue
            fi
            
            echo -n "[$CENARIO_ATUAL/36] Executando: N=$N_CLIENTES, Mobilidade=$MOBILIDADE, Aplicação=$APLICACAO... "
            
            # Executar simulação com timeout maior (600 segundos = 10 minutos)
            if timeout 600 python3 /home/marshibs/redes/equipe_4_2s2025.py \
                --nClientes "$N_CLIENTES" \
                --mobilidade "$MOBILIDADE" \
                --aplicacao "$APLICACAO" \
                --tempoSimulacao "$TEMPO_SIMULACAO" > /tmp/sim_output.log 2>&1; then
                
                if [ -f "$ARQUIVO_RESULTADO" ]; then
                    echo "✓ OK"
                else
                    echo "✗ ERRO: Arquivo não criado"
                fi
            else
                echo "✗ ERRO ou TIMEOUT"
            fi
            
            ((CENARIO_ATUAL++))
            
            # Pequena pausa entre cenários
            sleep 2
        done
    done
done

TEMPO_FIM=$(date +%s)
TEMPO_TOTAL=$((TEMPO_FIM - TEMPO_INICIO))
MINUTOS=$((TEMPO_TOTAL / 60))
SEGUNDOS=$((TEMPO_TOTAL % 60))

echo ""
echo "========================================================================"
echo "Simulações concluídas!"
echo "Tempo total: ${MINUTOS}m ${SEGUNDOS}s"
echo "Arquivos salvos em: $RESULTADOS_DIR"
echo "========================================================================"

# Listar arquivos gerados
echo ""
echo "Arquivos gerados:"
TOTAL_FILES=$(ls -1 "$RESULTADOS_DIR"/c*.txt 2>/dev/null | wc -l)
echo "Total: $TOTAL_FILES/36"

