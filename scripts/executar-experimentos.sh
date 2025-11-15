#!/bin/bash
# Script para executar todos os 36 cenários de simulação
# UNIFESP IC 2617 - Redes de Computadores
# Equipe 4 - 2º Semestre 2025

EQUIPE_ID="4"
RESULTADOS_DIR="/home/marshibs/redes/resultados"
PYTHON_SCRIPT="/home/marshibs/redes/equipe_${EQUIPE_ID}_2s2025.py"

# Criar diretório de resultados se não existir
mkdir -p "$RESULTADOS_DIR"

# Configuração: ns-3 deve estar em ~/.local/lib/python3.X/site-packages ou instalado globalmente
# Se estiver usando ns-3 em um local específico, adicione ao PYTHONPATH

echo "=========================================="
echo "Simulação NS-3 - UNIFESP IC 2617"
echo "Executando 36 cenários"
echo "=========================================="
echo ""

# Contadores
total_cenarios=0
cenarios_completados=0
cenarios_falhados=0

# Arrays para os parâmetros
declare -a clientes=(1 2 4 8 16 32)
declare -a mobilidades=("static" "mobile")
declare -a aplicacoes=("cbr" "tcp" "mixed")

# Tempo de simulação
tempo_simulacao=60

# Calcular total
total_cenarios=$((${#clientes[@]} * ${#mobilidades[@]} * ${#aplicacoes[@]}))

echo "Total de cenários a executar: $total_cenarios"
echo "Tempo estimado de simulação: ~$(($total_cenarios * $tempo_simulacao / 60)) minutos"
echo ""

# Timestamp inicial
inicio=$(date +%s)

# Loop sobre todos os cenários
cenario=0
for nclientes in "${clientes[@]}"; do
    for mobilidade in "${mobilidades[@]}"; do
        for aplicacao in "${aplicacoes[@]}"; do
            cenario=$((cenario + 1))
            
            echo "[$cenario/$total_cenarios] Executando: $nclientes clientes, $mobilidade, $aplicacao..."
            
            # Executar simulação
            python3 "$PYTHON_SCRIPT" \
                --nClientes "$nclientes" \
                --mobilidade "$mobilidade" \
                --aplicacao "$aplicacao" \
                --tempoSimulacao "$tempo_simulacao" 2>&1 | tail -20
            
            if [ $? -eq 0 ]; then
                cenarios_completados=$((cenarios_completados + 1))
                echo "  ✓ Cenário $cenario concluído com sucesso"
            else
                cenarios_falhados=$((cenarios_falhados + 1))
                echo "  ✗ Erro ao executar cenário $cenario"
            fi
            
            echo ""
        done
    done
done

# Timestamp final
fim=$(date +%s)
duracao=$((fim - inicio))
horas=$((duracao / 3600))
minutos=$(((duracao % 3600) / 60))
segundos=$((duracao % 60))

# Relatório final
echo "=========================================="
echo "RESUMO DA EXECUÇÃO"
echo "=========================================="
echo "Total de cenários: $total_cenarios"
echo "Cenários completados: $cenarios_completados"
echo "Cenários falhados: $cenarios_falhados"
echo "Tempo total: ${horas}h ${minutos}m ${segundos}s"
echo "=========================================="
echo ""

# Listar arquivos gerados
echo "Arquivos de resultados gerados:"
ls -lh "$RESULTADOS_DIR"/*.txt 2>/dev/null | wc -l
echo "arquivo(s)"

echo ""
echo "Para processar os dados, execute:"
echo "  python3 scripts/processar-dados.py"
