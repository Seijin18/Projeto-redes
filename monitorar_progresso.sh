#!/bin/bash

# Script para monitorar o progresso das simulações

RESULTADOS_DIR="/home/marshibs/redes/resultados"

echo "Monitor de Progresso das Simulações"
echo "===================================="
echo ""

while true; do
    TOTAL=$(ls -1 "$RESULTADOS_DIR"/c*.txt 2>/dev/null | wc -l)
    echo "Cenários completados: $TOTAL/36"
    
    # Mostrar últimos cenários concluídos
    echo ""
    echo "Últimos arquivos gerados:"
    ls -1rt "$RESULTADOS_DIR"/c*.txt 2>/dev/null | tail -3 | xargs -I {} basename {}
    
    # Verificar se o script ainda está rodando
    if ps aux | grep "executar_experimentos.sh" | grep -v grep > /dev/null; then
        echo ""
        echo "Status: Executando..."
        sleep 30
    else
        echo ""
        echo "Status: Finalizado!"
        break
    fi
    
    echo ""
    echo "---"
    echo ""
done

echo ""
echo "Total final: $TOTAL/36"
