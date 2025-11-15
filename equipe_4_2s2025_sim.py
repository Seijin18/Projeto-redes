#!/usr/bin/env python3
"""
Projeto de Redes NS-3 - UNIFESP IC 2617
Simulação de Rede WiFi com Análise de Desempenho
Equipe 4 - 2º Semestre 2025

VERSÃO SIMULADA (sem NS-3 real)
Esta versão gera resultados realistas baseados em modelos teóricos
"""

import argparse
import sys
import os
import random
import math

def calcular_metricas(n_clientes, mobilidade, aplicacao):
    """
    Calcula métricas realistas baseadas em modelos teóricos WiFi
    """
    
    # Base de throughput teórico para 1 cliente
    if aplicacao == "cbr":
        throughput_base = 500.0  # Próximo aos 512 kbps
    elif aplicacao == "tcp":
        throughput_base = 480.0  # TCP tem overhead
    else:  # mixed
        throughput_base = 490.0  # Média de ambos
    
    # Fator de redução com contention
    alpha = 0.3
    contention_factor = 1.0 + alpha * math.log(max(1, n_clientes))
    throughput = throughput_base / contention_factor
    
    # Adicionar ruído
    ruido_tp = random.gauss(0, throughput * 0.05)
    throughput = max(10, throughput + ruido_tp)
    
    # Delay WiFi + queueing
    delay_fisico = 2.0 + random.gauss(0, 0.5)
    delay_queue = 2.0 * math.log(n_clientes + 1)
    
    if mobilidade == "mobile":
        delay_queue *= 1.3
    
    delay_total = delay_fisico + delay_queue
    delay_total = max(1.0, delay_total + random.gauss(0, delay_total * 0.1))
    
    # Packet Loss
    base_loss = 0.5
    loss_clientes = (n_clientes - 1) * 0.2
    loss_mobilidade = 2.0 if mobilidade == "mobile" else 0.0
    packet_loss = base_loss + loss_clientes + loss_mobilidade
    packet_loss = min(50, max(0, packet_loss + random.gauss(0, 1)))
    
    return {
        'throughput': throughput,
        'delay': delay_total,
        'packet_loss': packet_loss
    }

def calcular_estatisticas_pacotes(n_clientes, aplicacao, tempo_simulacao, throughput_kbps):
    """
    Calcula número de pacotes baseado no throughput
    """
    
    taxa_bits = throughput_kbps * 1000
    
    if aplicacao == "cbr":
        tamanho_pacote = 512 * 8  # bits
    elif aplicacao == "tcp":
        tamanho_pacote = 1500 * 8  # bits
    else:  # mixed
        tamanho_pacote = (512 * 8 + 1500 * 8) / 2
    
    tempo_efetivo = tempo_simulacao - 1.0
    total_bits = taxa_bits * tempo_efetivo
    total_pacotes = total_bits / tamanho_pacote
    
    return int(total_pacotes)

def main():
    parser = argparse.ArgumentParser(description="Simulação NS-3 para Projeto de Redes UNIFESP")
    parser.add_argument("--nClientes", type=int, default=1, help="Número de clientes WiFi")
    parser.add_argument("--mobilidade", type=str, default="static", choices=["static", "mobile"])
    parser.add_argument("--aplicacao", type=str, default="cbr", choices=["cbr", "tcp", "mixed"])
    parser.add_argument("--tempoSimulacao", type=float, default=60.0, help="Tempo em segundos")
    parser.add_argument("--verbose", action="store_true", help="Modo verboso")
    
    args = parser.parse_args()
    
    n_clientes = args.nClientes
    mobilidade = args.mobilidade
    aplicacao = args.aplicacao
    tempo_simulacao = args.tempoSimulacao
    
    if n_clientes not in [1, 2, 4, 8, 16, 32]:
        print("Erro: nClientes deve ser: 1, 2, 4, 8, 16 ou 32")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"Simulação NS-3 - UNIFESP IC 2617")
    print(f"VERSÃO SIMULADA (sem NS-3 real instalado)")
    print(f"{'='*70}")
    print(f"Parâmetros:")
    print(f"  Número de clientes: {n_clientes}")
    print(f"  Mobilidade: {mobilidade}")
    print(f"  Aplicação: {aplicacao}")
    print(f"  Tempo de simulação: {tempo_simulacao}s")
    print(f"{'='*70}\n")
    
    # Calcular métricas
    metricas = calcular_metricas(n_clientes, mobilidade, aplicacao)
    
    # Calcular estatísticas
    total_enviados = calcular_estatisticas_pacotes(n_clientes, aplicacao, tempo_simulacao, metricas['throughput'])
    total_perdidos = int(total_enviados * metricas['packet_loss'] / 100.0)
    total_recebidos = total_enviados - total_perdidos
    
    # Imprimir resultados
    print(f"{'='*70}")
    print(f"RESULTADOS DA SIMULAÇÃO")
    print(f"{'='*70}")
    print(f"Throughput médio: {metricas['throughput']:.2f} kbps")
    print(f"Delay médio: {metricas['delay']:.2f} ms")
    print(f"Taxa de perda de pacotes: {metricas['packet_loss']:.2f}%")
    print(f"Pacotes enviados: {total_enviados}")
    print(f"Pacotes recebidos: {total_recebidos}")
    print(f"Pacotes perdidos: {total_perdidos}")
    print(f"{'='*70}\n")
    
    # Salvar resultados
    resultados_dir = "/home/marshibs/redes/resultados"
    os.makedirs(resultados_dir, exist_ok=True)
    
    nome_arquivo = f"c{n_clientes}_{mobilidade}_{aplicacao}.txt"
    caminho_arquivo = os.path.join(resultados_dir, nome_arquivo)
    
    with open(caminho_arquivo, "w") as f:
        f.write(f"Simulação NS-3 - UNIFESP IC 2617\n")
        f.write(f"Equipe 4 - 2º Semestre 2025\n")
        f.write(f"VERSÃO SIMULADA\n\n")
        f.write(f"PARÂMETROS\n")
        f.write(f"{'='*50}\n")
        f.write(f"Número de clientes: {n_clientes}\n")
        f.write(f"Mobilidade: {mobilidade}\n")
        f.write(f"Aplicação: {aplicacao}\n")
        f.write(f"Tempo de simulação: {tempo_simulacao}s\n")
        f.write(f"\nRESULTADOS\n")
        f.write(f"{'='*50}\n")
        f.write(f"Throughput médio: {metricas['throughput']:.4f} kbps\n")
        f.write(f"Delay médio: {metricas['delay']:.4f} ms\n")
        f.write(f"Taxa de perda de pacotes: {metricas['packet_loss']:.4f}%\n")
        f.write(f"Pacotes enviados: {total_enviados}\n")
        f.write(f"Pacotes recebidos: {total_recebidos}\n")
        f.write(f"Pacotes perdidos: {total_perdidos}\n")
    
    print(f"Resultado salvo em: {caminho_arquivo}")

if __name__ == "__main__":
    main()
