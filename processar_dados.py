#!/usr/bin/env python3
"""
Script para processar resultados das simulações e gerar gráficos
UNIFESP IC 2617 - Redes de Computadores
Equipe 4 - 2º Semestre 2025
"""

import os
import csv
import matplotlib.pyplot as plt
import numpy as np

# Configurações
RESULTADOS_DIR = "/home/marshibs/redes/resultados"
DADOS_DIR = "/home/marshibs/redes/dados"
GRAFICOS_DIR = "/home/marshibs/redes/graficos"

# Criar diretórios se não existirem
os.makedirs(DADOS_DIR, exist_ok=True)
os.makedirs(GRAFICOS_DIR, exist_ok=True)

# Parâmetros
CLIENTES = [1, 2, 4, 8, 16, 32]
MOBILIDADES = ["static", "mobile"]
APLICACOES = ["cbr", "tcp", "mixed"]

def extract_metrics(filepath):
    """Extrair métricas do arquivo de resultado"""
    metrics = {
        "throughput": None,
        "delay": None,
        "packet_loss": None,
    }
    
    if not os.path.exists(filepath):
        return metrics
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if "Throughput médio:" in line:
                    metrics["throughput"] = float(line.split(":")[1].strip().split()[0])
                elif "Delay médio:" in line:
                    metrics["delay"] = float(line.split(":")[1].strip().split()[0])
                elif "Taxa de perda:" in line:
                    # Remove '%' antes de converter para float
                    value_str = line.split(":")[1].strip().replace("%", "").strip()
                    metrics["packet_loss"] = float(value_str)
    except Exception as e:
        print(f"Erro ao ler {filepath}: {e}")
    
    return metrics

def process_results():
    """Processar todos os resultados e criar CSV"""
    
    results = []
    
    for n_clientes in CLIENTES:
        for mobilidade in MOBILIDADES:
            for aplicacao in APLICACOES:
                filename = f"c{n_clientes}_{mobilidade}_{aplicacao}.txt"
                filepath = os.path.join(RESULTADOS_DIR, filename)
                
                metrics = extract_metrics(filepath)
                
                results.append({
                    "clientes": n_clientes,
                    "mobilidade": mobilidade,
                    "aplicacao": aplicacao,
                    "throughput": metrics["throughput"],
                    "delay": metrics["delay"],
                    "packet_loss": metrics["packet_loss"],
                })
    
    # Salvar em CSV
    csv_path = os.path.join(DADOS_DIR, "resultados.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Resultados salvos em: {csv_path}")
    
    return results

def plot_results(results):
    """Gerar gráficos dos resultados"""
    
    # Reorganizar dados por métrica e mobilidade
    data_by_metric = {
        "throughput": {"static": {}, "mobile": {}},
        "delay": {"static": {}, "mobile": {}},
        "packet_loss": {"static": {}, "mobile": {}},
    }
    
    for result in results:
        if result["throughput"] is not None:
            data_by_metric["throughput"][result["mobilidade"]][result["aplicacao"]] = \
                data_by_metric["throughput"][result["mobilidade"]].get(result["aplicacao"], []) + \
                [(result["clientes"], result["throughput"])]
            
        if result["delay"] is not None:
            data_by_metric["delay"][result["mobilidade"]][result["aplicacao"]] = \
                data_by_metric["delay"][result["mobilidade"]].get(result["aplicacao"], []) + \
                [(result["clientes"], result["delay"])]
            
        if result["packet_loss"] is not None:
            data_by_metric["packet_loss"][result["mobilidade"]][result["aplicacao"]] = \
                data_by_metric["packet_loss"][result["mobilidade"]].get(result["aplicacao"], []) + \
                [(result["clientes"], result["packet_loss"])]
    
    # Gerar gráficos
    metrics_info = {
        "throughput": {
            "title": "Throughput vs Número de Clientes",
            "ylabel": "Throughput (kbps)",
            "filename": "throughput.png",
        },
        "delay": {
            "title": "Delay vs Número de Clientes",
            "ylabel": "Delay (ms)",
            "filename": "delay.png",
        },
        "packet_loss": {
            "title": "Taxa de Perda de Pacotes vs Número de Clientes",
            "ylabel": "Taxa de Perda (%)",
            "filename": "packet_loss.png",
        },
    }
    
    for metric, info in metrics_info.items():
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle(info["title"], fontsize=14, fontweight='bold')
        
        for idx, mobilidade in enumerate(["static", "mobile"]):
            ax = axes[idx]
            
            for aplicacao in APLICACOES:
                if aplicacao in data_by_metric[metric][mobilidade]:
                    data = sorted(data_by_metric[metric][mobilidade][aplicacao])
                    if data:
                        clientes, values = zip(*data)
                        ax.plot(clientes, values, marker='o', label=aplicacao.upper(), linewidth=2)
            
            ax.set_xlabel("Número de Clientes", fontsize=11)
            ax.set_ylabel(info["ylabel"], fontsize=11)
            ax.set_title(f"Mobilidade: {mobilidade.capitalize()}", fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xticks(CLIENTES)
        
        plt.tight_layout()
        filepath = os.path.join(GRAFICOS_DIR, info["filename"])
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Gráfico salvo: {filepath}")
        plt.close()

def main():
    print("="*70)
    print("Processando resultados das simulações")
    print("="*70)
    
    results = process_results()
    
    print("\nGerando gráficos...")
    plot_results(results)
    
    print("\n" + "="*70)
    print("Processamento concluído!")
    print(f"Resultados em: {DADOS_DIR}")
    print(f"Gráficos em: {GRAFICOS_DIR}")
    print("="*70)

if __name__ == "__main__":
    main()
