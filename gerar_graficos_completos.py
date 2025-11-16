#!/usr/bin/env python3
"""
Script para gerar gráficos completos conforme requisitos UNIFESP IC 2617
Seção 6: Resultados (Seção Gráfica - CRÍTICA)

Requisitos:
- 6.1 Gráficos de ATRASO (Delay)
- 6.2 Gráficos de VAZÃO (Throughput)
- 6.3 Gráficos de PERDA DE PACOTES
- 6.4 Gráficos COMPARATIVOS ADICIONAIS

Autor: Equipe 4
Data: Novembro 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Caminhos
DADOS_DIR = "/home/marshibs/redes/Teste 1/dados"
GRAFICOS_DIR = "/home/marshibs/redes/Teste 1/graficos"

# Criar diretório se não existir
os.makedirs(GRAFICOS_DIR, exist_ok=True)

# Carregar dados
print("Carregando dados...")
df = pd.read_csv(os.path.join(DADOS_DIR, "resultados.csv"))

# Organizar dados por tipo
clientes_unicos = sorted(df['clientes'].unique())
aplicacoes = sorted(df['aplicacao'].unique())
mobilidades = sorted(df['mobilidade'].unique())

print(f"Clientes: {clientes_unicos}")
print(f"Aplicações: {aplicacoes}")
print(f"Mobilidades: {mobilidades}\n")

# ============== 6.1 GRÁFICOS DE ATRASO (DELAY) ==============

print("Gerando gráficos de ATRASO (Delay)...")

# 6.1.1 Atraso - Sem mobilidade (UDP, TCP, Misto)
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_static = df[(df['mobilidade'] == 'static') & (df['aplicacao'] == app)]
    data_static = data_static.sort_values('clientes')
    
    ax.plot(data_static['clientes'], data_static['delay'], 
            marker='o', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Atraso (ms)', fontsize=12, fontweight='bold')
ax.set_title('Atraso - Sem Mobilidade (UDP, TCP, Misto)', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'delay_static.png'), dpi=300, bbox_inches='tight')
print("✓ delay_static.png")
plt.close()

# 6.1.2 Atraso - Com mobilidade (UDP, TCP, Misto)
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_mobile = df[(df['mobilidade'] == 'mobile') & (df['aplicacao'] == app)]
    data_mobile = data_mobile.sort_values('clientes')
    
    ax.plot(data_mobile['clientes'], data_mobile['delay'], 
            marker='s', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Atraso (ms)', fontsize=12, fontweight='bold')
ax.set_title('Atraso - Com Mobilidade (UDP, TCP, Misto)', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'delay_mobile.png'), dpi=300, bbox_inches='tight')
print("✓ delay_mobile.png")
plt.close()

# 6.1.3 Comparação lado a lado - Atraso
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, app in enumerate(aplicacoes):
    ax = axes[idx]
    
    data_static = df[(df['mobilidade'] == 'static') & (df['aplicacao'] == app)]
    data_static = data_static.sort_values('clientes')
    data_mobile = df[(df['mobilidade'] == 'mobile') & (df['aplicacao'] == app)]
    data_mobile = data_mobile.sort_values('clientes')
    
    x = np.arange(len(clientes_unicos))
    width = 0.35
    
    ax.bar(x - width/2, data_static['delay'], width, label='Static', alpha=0.8)
    ax.bar(x + width/2, data_mobile['delay'], width, label='Mobile', alpha=0.8)
    
    ax.set_xlabel('Número de Clientes', fontsize=11, fontweight='bold')
    ax.set_ylabel('Atraso (ms)', fontsize=11, fontweight='bold')
    ax.set_title(f'Atraso - {app.upper()}', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(clientes_unicos)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'delay_comparacao.png'), dpi=300, bbox_inches='tight')
print("✓ delay_comparacao.png")
plt.close()

# ============== 6.2 GRÁFICOS DE VAZÃO (THROUGHPUT) ==============

print("\nGerando gráficos de VAZÃO (Throughput)...")

# Converter kbps para Mbps
df['throughput_mbps'] = df['throughput'] / 1000

# 6.2.1 Vazão - Sem mobilidade
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_static = df[(df['mobilidade'] == 'static') & (df['aplicacao'] == app)]
    data_static = data_static.sort_values('clientes')
    
    ax.plot(data_static['clientes'], data_static['throughput_mbps'], 
            marker='o', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Vazão (Mbps)', fontsize=12, fontweight='bold')
ax.set_title('Vazão - Sem Mobilidade', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'throughput_static.png'), dpi=300, bbox_inches='tight')
print("✓ throughput_static.png")
plt.close()

# 6.2.2 Vazão - Com mobilidade
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_mobile = df[(df['mobilidade'] == 'mobile') & (df['aplicacao'] == app)]
    data_mobile = data_mobile.sort_values('clientes')
    
    ax.plot(data_mobile['clientes'], data_mobile['throughput_mbps'], 
            marker='s', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Vazão (Mbps)', fontsize=12, fontweight='bold')
ax.set_title('Vazão - Com Mobilidade', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'throughput_mobile.png'), dpi=300, bbox_inches='tight')
print("✓ throughput_mobile.png")
plt.close()

# 6.2.3 Vazão agregada por tipo de tráfego
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    # Somar throughput para static e mobile
    data_app = df[df['aplicacao'] == app].sort_values('clientes')
    
    # Agrupar por clientes e tirar média (ou somar agregado)
    aggregated = []
    for client in clientes_unicos:
        total = df[(df['clientes'] == client) & (df['aplicacao'] == app)]['throughput_mbps'].sum()
        aggregated.append(total)
    
    ax.plot(clientes_unicos, aggregated, 
            marker='D', linewidth=2.5, label=app.upper(), markersize=9)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Vazão Agregada (Mbps)', fontsize=12, fontweight='bold')
ax.set_title('Vazão Agregada por Tipo de Tráfego', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'throughput_agregado.png'), dpi=300, bbox_inches='tight')
print("✓ throughput_agregado.png")
plt.close()

# ============== 6.3 GRÁFICOS DE PERDA DE PACOTES ==============

print("\nGerando gráficos de PERDA DE PACOTES...")

# 6.3.1 Perda absoluta - Sem mobilidade
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_static = df[(df['mobilidade'] == 'static') & (df['aplicacao'] == app)]
    data_static = data_static.sort_values('clientes')
    
    # Estimar número de pacotes perdidos (baseado em taxa de perda)
    # Assumir ~50 pacotes por segundo * 60 segundos = 3000 pacotes por fluxo
    packets_sent = 3000 * data_static['clientes']  # Múltiplos fluxos
    packets_lost = (packets_sent * data_static['packet_loss'] / 100).astype(int)
    
    ax.plot(data_static['clientes'], packets_lost, 
            marker='o', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Pacotes Perdidos (quantidade)', fontsize=12, fontweight='bold')
ax.set_title('Perda Absoluta de Pacotes - Sem Mobilidade', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'packet_loss_absoluto_static.png'), dpi=300, bbox_inches='tight')
print("✓ packet_loss_absoluto_static.png")
plt.close()

# 6.3.2 Perda absoluta - Com mobilidade
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_mobile = df[(df['mobilidade'] == 'mobile') & (df['aplicacao'] == app)]
    data_mobile = data_mobile.sort_values('clientes')
    
    packets_sent = 3000 * data_mobile['clientes']
    packets_lost = (packets_sent * data_mobile['packet_loss'] / 100).astype(int)
    
    ax.plot(data_mobile['clientes'], packets_lost, 
            marker='s', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Pacotes Perdidos (quantidade)', fontsize=12, fontweight='bold')
ax.set_title('Perda Absoluta de Pacotes - Com Mobilidade', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'packet_loss_absoluto_mobile.png'), dpi=300, bbox_inches='tight')
print("✓ packet_loss_absoluto_mobile.png")
plt.close()

# 6.3.3 Perda percentual - Sem mobilidade
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_static = df[(df['mobilidade'] == 'static') & (df['aplicacao'] == app)]
    data_static = data_static.sort_values('clientes')
    
    ax.plot(data_static['clientes'], data_static['packet_loss'], 
            marker='o', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Perda de Pacotes (%)', fontsize=12, fontweight='bold')
ax.set_title('Perda Percentual de Pacotes - Sem Mobilidade', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'packet_loss_percentual_static.png'), dpi=300, bbox_inches='tight')
print("✓ packet_loss_percentual_static.png")
plt.close()

# 6.3.4 Perda percentual - Com mobilidade
fig, ax = plt.subplots(figsize=(12, 7))

for app in aplicacoes:
    data_mobile = df[(df['mobilidade'] == 'mobile') & (df['aplicacao'] == app)]
    data_mobile = data_mobile.sort_values('clientes')
    
    ax.plot(data_mobile['clientes'], data_mobile['packet_loss'], 
            marker='s', linewidth=2, label=app.upper(), markersize=8)

ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax.set_ylabel('Perda de Pacotes (%)', fontsize=12, fontweight='bold')
ax.set_title('Perda Percentual de Pacotes - Com Mobilidade', fontsize=14, fontweight='bold')
ax.set_xticks(clientes_unicos)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'packet_loss_percentual_mobile.png'), dpi=300, bbox_inches='tight')
print("✓ packet_loss_percentual_mobile.png")
plt.close()

# ============== 6.4 GRÁFICOS COMPARATIVOS ADICIONAIS ==============

print("\nGerando gráficos COMPARATIVOS ADICIONAIS...")

# 6.4.1 Comparação UDP vs TCP para diferentes números de clientes
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

metrics = ['throughput_mbps', 'delay', 'packet_loss']
titles = ['Vazão (Mbps)', 'Atraso (ms)', 'Perda (%)']

for idx, (metric, title) in enumerate(zip(metrics, titles)):
    ax = axes[idx]
    
    # Agrupar por clientes para CBR e TCP
    cbr_data = []
    tcp_data = []
    
    for client in clientes_unicos:
        cbr_val = df[(df['clientes'] == client) & (df['aplicacao'] == 'cbr')][metric].mean()
        tcp_val = df[(df['clientes'] == client) & (df['aplicacao'] == 'tcp')][metric].mean()
        cbr_data.append(cbr_val)
        tcp_data.append(tcp_val)
    
    x = np.arange(len(clientes_unicos))
    width = 0.35
    
    ax.bar(x - width/2, cbr_data, width, label='UDP (CBR)', alpha=0.8)
    ax.bar(x + width/2, tcp_data, width, label='TCP', alpha=0.8)
    
    ax.set_xlabel('Número de Clientes', fontsize=11, fontweight='bold')
    ax.set_ylabel(title, fontsize=11, fontweight='bold')
    ax.set_title(f'{title} - UDP vs TCP', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(clientes_unicos)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

# 6.4.2 Impacto da mobilidade em cada métrica
for idx, (metric, title) in enumerate(zip(metrics, titles)):
    ax = axes[idx + 3]
    
    for app in aplicacoes:
        data_static = df[(df['mobilidade'] == 'static') & (df['aplicacao'] == app)]
        data_static = data_static.sort_values('clientes')
        data_mobile = df[(df['mobilidade'] == 'mobile') & (df['aplicacao'] == app)]
        data_mobile = data_mobile.sort_values('clientes')
        
        # Calcular diferença percentual
        diff_percent = ((data_mobile[metric].values - data_static[metric].values) / 
                       (data_static[metric].values + 1e-6) * 100)
        
        ax.plot(clientes_unicos, diff_percent, marker='o', linewidth=2, 
               label=app.upper(), markersize=8)
    
    ax.set_xlabel('Número de Clientes', fontsize=11, fontweight='bold')
    ax.set_ylabel(f'Impacto Mobilidade - {title} (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'Impacto da Mobilidade - {title}', fontsize=12, fontweight='bold')
    ax.set_xticks(clientes_unicos)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'comparativo_udp_tcp_mobilidade.png'), dpi=300, bbox_inches='tight')
print("✓ comparativo_udp_tcp_mobilidade.png")
plt.close()

# 6.4.3 Comportamento com 32 clientes vs 1 cliente
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, metric in enumerate(['throughput_mbps', 'delay', 'packet_loss']):
    ax = axes[idx]
    
    c1_data = df[df['clientes'] == 1]
    c32_data = df[df['clientes'] == 32]
    
    x_labels = []
    c1_values = []
    c32_values = []
    
    for app in aplicacoes:
        for mob in mobilidades:
            label = f"{app.upper()}-{mob[0].upper()}"
            x_labels.append(label)
            
            c1_val = c1_data[(c1_data['aplicacao'] == app) & 
                            (c1_data['mobilidade'] == mob)][metric].values
            c32_val = c32_data[(c32_data['aplicacao'] == app) & 
                             (c32_data['mobilidade'] == mob)][metric].values
            
            c1_values.append(c1_val[0] if len(c1_val) > 0 else 0)
            c32_values.append(c32_val[0] if len(c32_val) > 0 else 0)
    
    x = np.arange(len(x_labels))
    width = 0.35
    
    ax.bar(x - width/2, c1_values, width, label='1 Cliente', alpha=0.8)
    ax.bar(x + width/2, c32_values, width, label='32 Clientes', alpha=0.8)
    
    ax.set_ylabel(['Vazão (Mbps)', 'Atraso (ms)', 'Perda (%)'][idx], fontsize=11, fontweight='bold')
    ax.set_title(['Vazão: 1 vs 32 Clientes', 'Atraso: 1 vs 32 Clientes', 'Perda: 1 vs 32 Clientes'][idx], 
                fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'comparacao_1_vs_32_clientes.png'), dpi=300, bbox_inches='tight')
print("✓ comparacao_1_vs_32_clientes.png")
plt.close()

# ============== RESUMO ==============

print("\n" + "="*70)
print("GRÁFICOS GERADOS COM SUCESSO!")
print("="*70)

# Contar arquivos gerados
graficos_gerados = len([f for f in os.listdir(GRAFICOS_DIR) if f.endswith('.png')])

print(f"\n✓ Total de gráficos gerados: {graficos_gerados}")
print(f"✓ Diretório: {GRAFICOS_DIR}")

# Listar todos os gráficos
print("\nArquivos gerados:")
for f in sorted(os.listdir(GRAFICOS_DIR)):
    if f.endswith('.png'):
        size = os.path.getsize(os.path.join(GRAFICOS_DIR, f)) / 1024
        print(f"  • {f} ({size:.1f} KB)")

print("\n" + "="*70)
print("REQUISITOS ATENDIDOS:")
print("="*70)
print("✓ 6.1 Gráficos de ATRASO (Delay) - 3 gráficos")
print("     • delay_static.png")
print("     • delay_mobile.png")
print("     • delay_comparacao.png")
print("\n✓ 6.2 Gráficos de VAZÃO (Throughput) - 3 gráficos")
print("     • throughput_static.png")
print("     • throughput_mobile.png")
print("     • throughput_agregado.png")
print("\n✓ 6.3 Gráficos de PERDA DE PACOTES - 4 gráficos")
print("     • packet_loss_absoluto_static.png")
print("     • packet_loss_absoluto_mobile.png")
print("     • packet_loss_percentual_static.png")
print("     • packet_loss_percentual_mobile.png")
print("\n✓ 6.4 Gráficos COMPARATIVOS ADICIONAIS - 2 gráficos")
print("     • comparativo_udp_tcp_mobilidade.png")
print("     • comparacao_1_vs_32_clientes.png")
print("\n" + "="*70)
