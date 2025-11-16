#!/usr/bin/env python3
"""
Script para gerar gráficos dos resultados da simulação NS-3
Estilo similar ao Teste matu, mas com dados consolidados do projeto atual

Autor: Equipe 4
Data: Novembro 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams
import os

# Configurações de estilo
plt.style.use('seaborn-v0_8-darkgrid')
rcParams['figure.figsize'] = (14, 8)
rcParams['font.size'] = 11

# Paleta de cores contrastantes
CORES = {
    'CBR': '#0066CC',      # Azul intenso
    'TCP': '#CC0000',      # Vermelho intenso
    'MIXED': '#FFCC00'     # Amarelo/Ouro
}

# Caminhos
DADOS_CSV = "/home/marshibs/redes/dados/resultados.csv"
GRAFICOS_DIR = "/home/marshibs/redes/graficos"

# Criar diretório de gráficos
os.makedirs(GRAFICOS_DIR, exist_ok=True)

# Carregar dados
print("Carregando dados...")
df = pd.read_csv(DADOS_CSV)

# Preparar dados
df['Mobilidade'] = df['mobilidade'].str.capitalize()
df['Aplicacao'] = df['aplicacao'].str.upper()
df['Clientes'] = df['clientes'].astype(int)

# Ordenar clientes
clientes_order = [1, 2, 4, 8, 16, 32]
df['Clientes'] = pd.Categorical(df['Clientes'], categories=clientes_order, ordered=True)

print(f"Total de cenários carregados: {len(df)}")
print(f"Clientes: {sorted(df['Clientes'].unique())}")
print(f"Aplicações: {sorted(df['Aplicacao'].unique())}")
print(f"Mobilidades: {sorted(df['Mobilidade'].unique())}\n")

# Função para salvar gráfico
def salvar_grafico(nome, titulo_completo=False):
    plt.tight_layout()
    filepath = os.path.join(GRAFICOS_DIR, f'{nome}.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ {nome}.png")
    plt.close()

# ============== 1. GRÁFICOS DE ATRASO (DELAY) ==============
print("Gerando gráficos de ATRASO (Delay)...")

# 1.1 Atraso - Sem mobilidade
plt.figure(figsize=(13, 8))
df_static = df[df['Mobilidade'] == 'Static'].sort_values('Clientes')
for app in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
    plt.plot(dados['Clientes'], dados['delay'], 
             marker='o', linewidth=2.5, markersize=8, label=app, color=CORES[app])

plt.xlabel('Número de Clientes', fontsize=13, fontweight='bold')
plt.ylabel('Atraso Médio (ms)', fontsize=13, fontweight='bold')
plt.title('Atraso - Sem Mobilidade (UDP, TCP, Misto)', fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(clientes_order)
salvar_grafico('1_atraso_sem_mobilidade')

# 1.2 Atraso - Com mobilidade
plt.figure(figsize=(13, 8))
df_mobile = df[df['Mobilidade'] == 'Mobile'].sort_values('Clientes')
for app in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
    plt.plot(dados['Clientes'], dados['delay'], 
             marker='s', linewidth=2.5, markersize=8, label=app, color=CORES[app])

plt.xlabel('Número de Clientes', fontsize=13, fontweight='bold')
plt.ylabel('Atraso Médio (ms)', fontsize=13, fontweight='bold')
plt.title('Atraso - Com Mobilidade (UDP, TCP, Misto)', fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(clientes_order)
salvar_grafico('2_atraso_com_mobilidade')

# 1.3 Comparação lado a lado de atraso
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

for app in ['CBR', 'TCP', 'MIXED']:
    dados_static = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
    ax1.plot(dados_static['Clientes'], dados_static['delay'], 
             marker='o', linewidth=2.5, markersize=8, label=app, color=CORES[app])

ax1.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax1.set_ylabel('Atraso Médio (ms)', fontsize=12, fontweight='bold')
ax1.set_title('Sem Mobilidade', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(clientes_order)

for app in ['CBR', 'TCP', 'MIXED']:
    dados_mobile = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
    ax2.plot(dados_mobile['Clientes'], dados_mobile['delay'], 
             marker='s', linewidth=2.5, markersize=8, label=app, color=CORES[app])

ax2.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax2.set_ylabel('Atraso Médio (ms)', fontsize=12, fontweight='bold')
ax2.set_title('Com Mobilidade', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(clientes_order)

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '3_atraso_comparacao.png'), dpi=300, bbox_inches='tight')
print(f"✓ 3_atraso_comparacao.png")
plt.close()

# ============== 2. GRÁFICOS DE VAZÃO (THROUGHPUT) ==============
print("\nGerando gráficos de VAZÃO (Throughput)...")

# 2.1 Vazão - Sem mobilidade
plt.figure(figsize=(13, 8))
for app in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
    plt.plot(dados['Clientes'], dados['throughput'], 
             marker='o', linewidth=2.5, markersize=8, label=app, color=CORES[app])

plt.xlabel('Número de Clientes', fontsize=13, fontweight='bold')
plt.ylabel('Vazão Agregada (Mbps)', fontsize=13, fontweight='bold')
plt.title('Vazão - Sem Mobilidade', fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(clientes_order)
salvar_grafico('4_vazao_sem_mobilidade')

# 2.2 Vazão - Com mobilidade
plt.figure(figsize=(13, 8))
for app in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
    plt.plot(dados['Clientes'], dados['throughput'], 
             marker='s', linewidth=2.5, markersize=8, label=app, color=CORES[app])

plt.xlabel('Número de Clientes', fontsize=13, fontweight='bold')
plt.ylabel('Vazão Agregada (Mbps)', fontsize=13, fontweight='bold')
plt.title('Vazão - Com Mobilidade', fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(clientes_order)
salvar_grafico('5_vazao_com_mobilidade')

# 2.3 Comparação lado a lado de vazão
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

for app in ['CBR', 'TCP', 'MIXED']:
    dados_static = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
    ax1.plot(dados_static['Clientes'], dados_static['throughput'], 
             marker='o', linewidth=2.5, markersize=8, label=app, color=CORES[app])

ax1.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax1.set_ylabel('Vazão Agregada (Mbps)', fontsize=12, fontweight='bold')
ax1.set_title('Sem Mobilidade', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(clientes_order)

for app in ['CBR', 'TCP', 'MIXED']:
    dados_mobile = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
    ax2.plot(dados_mobile['Clientes'], dados_mobile['throughput'], 
             marker='s', linewidth=2.5, markersize=8, label=app, color=CORES[app])

ax2.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax2.set_ylabel('Vazão Agregada (Mbps)', fontsize=12, fontweight='bold')
ax2.set_title('Com Mobilidade', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(clientes_order)

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '6_vazao_comparacao.png'), dpi=300, bbox_inches='tight')
print(f"✓ 6_vazao_comparacao.png")
plt.close()

# ============== 3. GRÁFICOS DE PERDA DE PACOTES ==============
print("\nGerando gráficos de PERDA DE PACOTES...")

# 3.1 Perda - Sem mobilidade
plt.figure(figsize=(13, 8))
for app in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
    plt.plot(dados['Clientes'], dados['packet_loss'], 
             marker='o', linewidth=2.5, markersize=8, label=app, color=CORES[app])

plt.xlabel('Número de Clientes', fontsize=13, fontweight='bold')
plt.ylabel('Perda de Pacotes (%)', fontsize=13, fontweight='bold')
plt.title('Perda de Pacotes - Sem Mobilidade', fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(clientes_order)
salvar_grafico('7_perda_sem_mobilidade')

# 3.2 Perda - Com mobilidade
plt.figure(figsize=(13, 8))
for app in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
    plt.plot(dados['Clientes'], dados['packet_loss'], 
             marker='s', linewidth=2.5, markersize=8, label=app, color=CORES[app])

plt.xlabel('Número de Clientes', fontsize=13, fontweight='bold')
plt.ylabel('Perda de Pacotes (%)', fontsize=13, fontweight='bold')
plt.title('Perda de Pacotes - Com Mobilidade', fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xticks(clientes_order)
salvar_grafico('8_perda_com_mobilidade')

# 3.3 Comparação lado a lado de perda
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

for app in ['CBR', 'TCP', 'MIXED']:
    dados_static = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
    ax1.plot(dados_static['Clientes'], dados_static['packet_loss'], 
             marker='o', linewidth=2.5, markersize=8, label=app, color=CORES[app])

ax1.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax1.set_ylabel('Perda de Pacotes (%)', fontsize=12, fontweight='bold')
ax1.set_title('Sem Mobilidade', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(clientes_order)

for app in ['CBR', 'TCP', 'MIXED']:
    dados_mobile = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
    ax2.plot(dados_mobile['Clientes'], dados_mobile['packet_loss'], 
             marker='s', linewidth=2.5, markersize=8, label=app, color=CORES[app])

ax2.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
ax2.set_ylabel('Perda de Pacotes (%)', fontsize=12, fontweight='bold')
ax2.set_title('Com Mobilidade', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(clientes_order)

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '9_perda_comparacao.png'), dpi=300, bbox_inches='tight')
print(f"✓ 9_perda_comparacao.png")
plt.close()

# ============== 4. GRÁFICOS COMPARATIVOS ADICIONAIS ==============
print("\nGerando gráficos COMPARATIVOS...")

# 4.1 UDP vs TCP (todas as métricas)
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for idx, (metric, ylabel) in enumerate([
    ('throughput', 'Vazão (Mbps)'),
    ('delay', 'Atraso (ms)'),
    ('packet_loss', 'Perda (%)')
]):
    # Sem mobilidade
    ax = axes[0, idx]
    df_cbr = df_static[df_static['Aplicacao'] == 'CBR'].sort_values('Clientes')
    df_tcp = df_static[df_static['Aplicacao'] == 'TCP'].sort_values('Clientes')
    
    x = np.arange(len(clientes_order))
    width = 0.35
    
    ax.bar(x - width/2, df_cbr[metric], width, label='UDP (CBR)', alpha=0.8, color=CORES['CBR'])
    ax.bar(x + width/2, df_tcp[metric], width, label='TCP', alpha=0.8, color=CORES['TCP'])
    
    ax.set_xlabel('Clientes', fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(f'UDP vs TCP - {ylabel} (Sem Mobilidade)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(clientes_order)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Com mobilidade
    ax = axes[1, idx]
    df_cbr_m = df_mobile[df_mobile['Aplicacao'] == 'CBR'].sort_values('Clientes')
    df_tcp_m = df_mobile[df_mobile['Aplicacao'] == 'TCP'].sort_values('Clientes')
    
    ax.bar(x - width/2, df_cbr_m[metric], width, label='UDP (CBR)', alpha=0.8, color=CORES['CBR'])
    ax.bar(x + width/2, df_tcp_m[metric], width, label='TCP', alpha=0.8, color=CORES['TCP'])
    
    ax.set_xlabel('Clientes', fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(f'UDP vs TCP - {ylabel} (Com Mobilidade)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(clientes_order)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '10_udp_vs_tcp_comparativo.png'), dpi=300, bbox_inches='tight')
print(f"✓ 10_udp_vs_tcp_comparativo.png")
plt.close()

# 4.2 Impacto da mobilidade
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (metric, ylabel) in enumerate([
    ('throughput', 'Vazão (Mbps)'),
    ('delay', 'Atraso (ms)'),
    ('packet_loss', 'Perda (%)')
]):
    ax = axes[idx]
    
    for app in ['CBR', 'TCP', 'MIXED']:
        # Calcular diferença percentual
        static_data = df_static[df_static['Aplicacao'] == app].sort_values('Clientes')
        mobile_data = df_mobile[df_mobile['Aplicacao'] == app].sort_values('Clientes')
        
        # Resetar índices para alinhamento
        static_data = static_data.reset_index(drop=True)
        mobile_data = mobile_data.reset_index(drop=True)
        
        # Calcular mudança
        mudanca = ((mobile_data[metric] - static_data[metric]) / static_data[metric] * 100)
        
        ax.plot(clientes_order, mudanca.values, marker='o', linewidth=2.5, 
               markersize=8, label=app, color=CORES[app])
    
    ax.set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'Mudança (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Impacto da Mobilidade - {ylabel}', fontsize=13, fontweight='bold')
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(clientes_order)

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '11_impacto_mobilidade.png'), dpi=300, bbox_inches='tight')
print(f"✓ 11_impacto_mobilidade.png")
plt.close()

# 4.3 Escalabilidade (1 vs 32 clientes)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (metric, ylabel, title_suffix) in enumerate([
    ('throughput', 'Vazão (Mbps)', 'Escalabilidade de Vazão'),
    ('delay', 'Atraso (ms)', 'Escalabilidade de Atraso'),
    ('packet_loss', 'Perda (%)', 'Escalabilidade de Perda')
]):
    ax = axes[idx]
    
    x_labels = []
    c1_values = []
    c32_values = []
    
    for app in ['CBR', 'TCP', 'MIXED']:
        for mob in ['Static', 'Mobile']:
            label = f"{app}-{mob[0]}"
            x_labels.append(label)
            
            c1 = df[(df['Clientes'] == 1) & (df['Aplicacao'] == app) & 
                   (df['Mobilidade'] == mob)][metric].values
            c32 = df[(df['Clientes'] == 32) & (df['Aplicacao'] == app) & 
                    (df['Mobilidade'] == mob)][metric].values
            
            c1_values.append(c1[0] if len(c1) > 0 else 0)
            c32_values.append(c32[0] if len(c32) > 0 else 0)
    
    x = np.arange(len(x_labels))
    width = 0.35
    
    # Definir cores com base na aplicação
    colors_c1 = []
    colors_c32 = []
    for app in ['CBR', 'TCP', 'MIXED']:
        for mob in ['Static', 'Mobile']:
            colors_c1.append(CORES[app])
            colors_c32.append(CORES[app])
    
    ax.bar(x - width/2, c1_values, width, label='1 Cliente', alpha=0.7, color=colors_c1)
    ax.bar(x + width/2, c32_values, width, label='32 Clientes', alpha=0.9, color=colors_c32)
    
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title_suffix, fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '12_escalabilidade_1_vs_32.png'), dpi=300, bbox_inches='tight')
print(f"✓ 12_escalabilidade_1_vs_32.png")
plt.close()

# ============== RESUMO ==============
print("\n" + "="*70)
print("GRÁFICOS GERADOS COM SUCESSO!")
print("="*70)

graficos = len([f for f in os.listdir(GRAFICOS_DIR) if f.endswith('.png')])
print(f"\n✓ Total de gráficos: {graficos}")
print(f"✓ Diretório: {GRAFICOS_DIR}")

print("\nArquivos gerados:")
for f in sorted(os.listdir(GRAFICOS_DIR)):
    if f.endswith('.png'):
        size = os.path.getsize(os.path.join(GRAFICOS_DIR, f)) / 1024
        print(f"  • {f} ({size:.1f} KB)")

print("\n" + "="*70)
