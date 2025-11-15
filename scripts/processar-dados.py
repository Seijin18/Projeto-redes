#!/usr/bin/env python3
"""
Script para processar resultados de simulação NS-3 e gerar gráficos
UNIFESP IC 2617 - Redes de Computadores
Equipe 4 - 2º Semestre 2025
"""

import os
import csv
import glob
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def extrair_parametros_arquivo(nome_arquivo):
    """Extrai parâmetros do nome do arquivo: c{clientes}_{mobilidade}_{aplicacao}.txt"""
    match = re.match(r"c(\d+)_(static|mobile)_(cbr|tcp|mixed)\.txt", nome_arquivo)
    if match:
        return {
            "clientes": int(match.group(1)),
            "mobilidade": match.group(2),
            "aplicacao": match.group(3)
        }
    return None

def ler_resultados_arquivo(caminho_arquivo):
    """Lê resultados de um arquivo de simulação"""
    resultados = {}
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        for linha in linhas:
            linha = linha.strip()
            
            if linha.startswith("Throughput médio:"):
                throughput = float(linha.split(":")[1].strip().split()[0])
                resultados['throughput'] = throughput
            
            elif linha.startswith("Delay médio:"):
                delay = float(linha.split(":")[1].strip().split()[0])
                resultados['delay'] = delay
            
            elif linha.startswith("Taxa de perda de pacotes:"):
                packet_loss = float(linha.split(":")[1].strip().split()[0])
                resultados['packet_loss'] = packet_loss
            
            elif linha.startswith("Pacotes enviados:"):
                sent = int(linha.split(":")[1].strip())
                resultados['sent'] = sent
            
            elif linha.startswith("Pacotes recebidos:"):
                received = int(linha.split(":")[1].strip())
                resultados['received'] = received
            
            elif linha.startswith("Pacotes perdidos:"):
                lost = int(linha.split(":")[1].strip())
                resultados['lost'] = lost
        
        return resultados
    
    except Exception as e:
        print(f"Erro ao ler arquivo {caminho_arquivo}: {e}")
        return None

def processar_dados():
    """Processa todos os arquivos de resultado e organiza os dados"""
    
    resultados_dir = "/home/marshibs/redes/resultados"
    dados = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    
    # Listar todos os arquivos de resultado
    arquivos = glob.glob(os.path.join(resultados_dir, "c*.txt"))
    
    if not arquivos:
        print(f"Nenhum arquivo de resultado encontrado em {resultados_dir}")
        return None
    
    print(f"Processando {len(arquivos)} arquivos de resultado...")
    
    for arquivo in arquivos:
        nome = os.path.basename(arquivo)
        params = extrair_parametros_arquivo(nome)
        
        if params is None:
            print(f"  Aviso: Não foi possível extrair parâmetros de {nome}")
            continue
        
        resultado = ler_resultados_arquivo(arquivo)
        
        if resultado is None:
            print(f"  Aviso: Não foi possível ler resultados de {nome}")
            continue
        
        # Organizar dados: dados[métrica][aplicação][mobilidade][clientes] = valor
        clientes = params['clientes']
        mobilidade = params['mobilidade']
        aplicacao = params['aplicacao']
        
        dados['throughput'][aplicacao][mobilidade][clientes] = resultado.get('throughput', 0)
        dados['delay'][aplicacao][mobilidade][clientes] = resultado.get('delay', 0)
        dados['packet_loss'][aplicacao][mobilidade][clientes] = resultado.get('packet_loss', 0)
    
    return dados

def gerar_graficos(dados):
    """Gera gráficos a partir dos dados processados"""
    
    if not dados or not dados['throughput']:
        print("Sem dados para gerar gráficos")
        return
    
    graficos_dir = "/home/marshibs/redes/graficos"
    os.makedirs(graficos_dir, exist_ok=True)
    
    # Cores para diferentes aplicações
    cores = {
        'cbr': '#1f77b4',      # azul
        'tcp': '#ff7f0e',      # laranja
        'mixed': '#2ca02c'     # verde
    }
    
    aplicacoes = ['cbr', 'tcp', 'mixed']
    mobilidades = ['static', 'mobile']
    
    # ========== GRÁFICO 1: THROUGHPUT ==========
    print("Gerando gráfico de Throughput...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Throughput vs Número de Clientes', fontsize=14, fontweight='bold')
    
    # Estático
    for app in aplicacoes:
        if app in dados['throughput'] and 'static' in dados['throughput'][app]:
            clientes_list = sorted(dados['throughput'][app]['static'].keys())
            throughput_list = [dados['throughput'][app]['static'].get(c, 0) for c in clientes_list]
            ax1.plot(clientes_list, throughput_list, marker='o', label=app.upper(), color=cores[app], linewidth=2)
    
    ax1.set_xlabel('Número de Clientes', fontsize=11)
    ax1.set_ylabel('Throughput (kbps)', fontsize=11)
    ax1.set_title('Cenário Estático', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xticks([1, 2, 4, 8, 16, 32])
    
    # Móvel
    for app in aplicacoes:
        if app in dados['throughput'] and 'mobile' in dados['throughput'][app]:
            clientes_list = sorted(dados['throughput'][app]['mobile'].keys())
            throughput_list = [dados['throughput'][app]['mobile'].get(c, 0) for c in clientes_list]
            ax2.plot(clientes_list, throughput_list, marker='o', label=app.upper(), color=cores[app], linewidth=2)
    
    ax2.set_xlabel('Número de Clientes', fontsize=11)
    ax2.set_ylabel('Throughput (kbps)', fontsize=11)
    ax2.set_title('Cenário Móvel', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xticks([1, 2, 4, 8, 16, 32])
    
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, 'throughput_vs_clientes.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ throughput_vs_clientes.png")
    
    # ========== GRÁFICO 2: DELAY ==========
    print("Gerando gráfico de Delay...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Delay vs Número de Clientes', fontsize=14, fontweight='bold')
    
    # Estático
    for app in aplicacoes:
        if app in dados['delay'] and 'static' in dados['delay'][app]:
            clientes_list = sorted(dados['delay'][app]['static'].keys())
            delay_list = [dados['delay'][app]['static'].get(c, 0) for c in clientes_list]
            ax1.plot(clientes_list, delay_list, marker='s', label=app.upper(), color=cores[app], linewidth=2)
    
    ax1.set_xlabel('Número de Clientes', fontsize=11)
    ax1.set_ylabel('Delay Médio (ms)', fontsize=11)
    ax1.set_title('Cenário Estático', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xticks([1, 2, 4, 8, 16, 32])
    
    # Móvel
    for app in aplicacoes:
        if app in dados['delay'] and 'mobile' in dados['delay'][app]:
            clientes_list = sorted(dados['delay'][app]['mobile'].keys())
            delay_list = [dados['delay'][app]['mobile'].get(c, 0) for c in clientes_list]
            ax2.plot(clientes_list, delay_list, marker='s', label=app.upper(), color=cores[app], linewidth=2)
    
    ax2.set_xlabel('Número de Clientes', fontsize=11)
    ax2.set_ylabel('Delay Médio (ms)', fontsize=11)
    ax2.set_title('Cenário Móvel', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xticks([1, 2, 4, 8, 16, 32])
    
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, 'delay_vs_clientes.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ delay_vs_clientes.png")
    
    # ========== GRÁFICO 3: PACKET LOSS ==========
    print("Gerando gráfico de Taxa de Perda de Pacotes...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Taxa de Perda de Pacotes vs Número de Clientes', fontsize=14, fontweight='bold')
    
    # Estático
    for app in aplicacoes:
        if app in dados['packet_loss'] and 'static' in dados['packet_loss'][app]:
            clientes_list = sorted(dados['packet_loss'][app]['static'].keys())
            loss_list = [dados['packet_loss'][app]['static'].get(c, 0) for c in clientes_list]
            ax1.plot(clientes_list, loss_list, marker='^', label=app.upper(), color=cores[app], linewidth=2)
    
    ax1.set_xlabel('Número de Clientes', fontsize=11)
    ax1.set_ylabel('Taxa de Perda (%)', fontsize=11)
    ax1.set_title('Cenário Estático', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xticks([1, 2, 4, 8, 16, 32])
    
    # Móvel
    for app in aplicacoes:
        if app in dados['packet_loss'] and 'mobile' in dados['packet_loss'][app]:
            clientes_list = sorted(dados['packet_loss'][app]['mobile'].keys())
            loss_list = [dados['packet_loss'][app]['mobile'].get(c, 0) for c in clientes_list]
            ax2.plot(clientes_list, loss_list, marker='^', label=app.upper(), color=cores[app], linewidth=2)
    
    ax2.set_xlabel('Número de Clientes', fontsize=11)
    ax2.set_ylabel('Taxa de Perda (%)', fontsize=11)
    ax2.set_title('Cenário Móvel', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xticks([1, 2, 4, 8, 16, 32])
    
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, 'packetloss_vs_clientes.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ packetloss_vs_clientes.png")
    
    # ========== TABELA DE RESULTADOS ==========
    print("Gerando tabela de resultados...")
    
    dados_dir = "/home/marshibs/redes/dados"
    os.makedirs(dados_dir, exist_ok=True)
    
    csv_file = os.path.join(dados_dir, 'resultados.csv')
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Clientes', 'Mobilidade', 'Aplicação', 'Throughput (kbps)', 'Delay (ms)', 'Perda de Pacotes (%)'])
        
        for app in aplicacoes:
            for mob in mobilidades:
                if app in dados['throughput'] and mob in dados['throughput'][app]:
                    for clientes in sorted(dados['throughput'][app][mob].keys()):
                        tp = dados['throughput'][app][mob].get(clientes, 0)
                        dl = dados['delay'][app][mob].get(clientes, 0)
                        pl = dados['packet_loss'][app][mob].get(clientes, 0)
                        
                        writer.writerow([clientes, mob, app, f"{tp:.2f}", f"{dl:.2f}", f"{pl:.2f}"])
    
    print(f"  ✓ resultados.csv")
    
    print(f"\nGráficos salvos em: {graficos_dir}")
    print(f"Tabela salva em: {csv_file}")

def main():
    print("\n" + "="*70)
    print("Processador de Dados - Simulação NS-3")
    print("="*70 + "\n")
    
    dados = processar_dados()
    
    if dados is None or not dados:
        print("Nenhum dado para processar")
        return
    
    print("\nGerando gráficos...")
    gerar_graficos(dados)
    
    print("\n" + "="*70)
    print("Processamento concluído com sucesso!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
