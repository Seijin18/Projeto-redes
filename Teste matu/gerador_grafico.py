import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams

# Configurações de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
rcParams['figure.figsize'] = (12, 8)
rcParams['font.size'] = 12

# Carregar os dados
df = pd.read_csv('comparacao - comparacao.csv.csv')

# Preparar os dados
df['Mobilidade'] = df['Mobilidade'].str.capitalize()
df['Aplicacao'] = df['Aplicacao'].str.replace('mobile_', '').str.replace('static_', '')
df['Aplicacao'] = df['Aplicacao'].str.upper()

# Ordenar os clientes
clientes_order = [1, 2, 4, 8, 16, 32]
df['Clientes'] = pd.Categorical(df['Clientes'], categories=clientes_order, ordered=True)

# Função para salvar gráficos
def salvar_grafico(nome):
    plt.tight_layout()
    plt.savefig(f'{nome}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{nome}.pdf', bbox_inches='tight')
    plt.show()

# 1. GRÁFICOS DE ATRASO (DELAY)
print("Gerando gráficos de ATRASO...")

# 1.1 Atraso - Sem mobilidade
plt.figure(figsize=(14, 8))
df_static = df[df['Mobilidade'] == 'Static']
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Delay_Medio_ms'], 
             marker='o', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Atraso Médio (ms)', fontsize=14, fontweight='bold')
plt.title('ATRASO - Cenário SEM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.yscale('log')
salvar_grafico('atraso_sem_mobilidade')

# 1.2 Atraso - Com mobilidade
plt.figure(figsize=(14, 8))
df_mobile = df[df['Mobilidade'] == 'Mobile']
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Delay_Medio_ms'], 
             marker='s', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Atraso Médio (ms)', fontsize=14, fontweight='bold')
plt.title('ATRASO - Cenário COM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.yscale('log')
salvar_grafico('atraso_com_mobilidade')

# 1.3 Comparação lado a lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Sem mobilidade
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == aplicacao]
    ax1.plot(dados['Clientes'], dados['Delay_Medio_ms'], 
             marker='o', linewidth=3, markersize=8, label=f'{aplicacao}')

ax1.set_xlabel('Número de Clientes', fontsize=14, fontweight='bold')
ax1.set_ylabel('Atraso Médio (ms)', fontsize=14, fontweight='bold')
ax1.set_title('SEM Mobilidade', fontsize=16, fontweight='bold')
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')

# Com mobilidade
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == aplicacao]
    ax2.plot(dados['Clientes'], dados['Delay_Medio_ms'], 
             marker='s', linewidth=3, markersize=8, label=f'{aplicacao}')

ax2.set_xlabel('Número de Clientes', fontsize=14, fontweight='bold')
ax2.set_ylabel('Atraso Médio (ms)', fontsize=14, fontweight='bold')
ax2.set_title('COM Mobilidade', fontsize=16, fontweight='bold')
ax2.legend(fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')

plt.suptitle('COMPARAÇÃO DE ATRASO - COM E SEM MOBILIDADE', fontsize=18, fontweight='bold')
salvar_grafico('atraso_comparacao_lado_a_lado')

# 2. GRÁFICOS DE VAZÃO (THROUGHPUT)
print("Gerando gráficos de VAZÃO...")

# 2.1 Vazão - Sem mobilidade
plt.figure(figsize=(14, 8))
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Throughput_Medio_Mbps'], 
             marker='o', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Vazão Média (Mbps)', fontsize=14, fontweight='bold')
plt.title('VAZÃO - Cenário SEM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
salvar_grafico('vazao_sem_mobilidade')

# 2.2 Vazão - Com mobilidade
plt.figure(figsize=(14, 8))
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Throughput_Medio_Mbps'], 
             marker='s', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Vazão Média (Mbps)', fontsize=14, fontweight='bold')
plt.title('VAZÃO - Cenário COM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
salvar_grafico('vazao_com_mobilidade')

# 2.3 Vazão agregada por tipo de tráfego
plt.figure(figsize=(16, 10))
aplicacoes = ['CBR', 'TCP', 'MIXED']
width = 0.25
x = np.arange(len(clientes_order))

for i, aplicacao in enumerate(aplicacoes):
    dados_static = df_static[df_static['Aplicacao'] == aplicacao]
    dados_mobile = df_mobile[df_mobile['Aplicacao'] == aplicacao]
    
    plt.bar(x + i*width, dados_static['Throughput_Medio_Mbps'], 
            width, label=f'{aplicacao} - Static', alpha=0.8)
    plt.bar(x + i*width, dados_mobile['Throughput_Medio_Mbps'], 
            width, label=f'{aplicacao} - Mobile', alpha=0.6, hatch='//')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Vazão Média (Mbps)', fontsize=14, fontweight='bold')
plt.title('VAZÃO AGREGADA POR TIPO DE TRÁFEGO', fontsize=16, fontweight='bold')
plt.xticks(x + width, clientes_order)
plt.legend(fontsize=10, ncol=3)
plt.grid(True, alpha=0.3)
salvar_grafico('vazao_agregada')

# 3. GRÁFICOS DE PERDA DE PACOTES
print("Gerando gráficos de PERDA DE PACOTES...")

# 3.1 Perda absoluta - Sem mobilidade
plt.figure(figsize=(14, 8))
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Pacotes_Perdidos'], 
             marker='o', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Pacotes Perdidos (Absoluto)', fontsize=14, fontweight='bold')
plt.title('PERDA DE PACOTES (Absoluto) - SEM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.yscale('log')
salvar_grafico('perda_absoluta_sem_mobilidade')

# 3.2 Perda absoluta - Com mobilidade
plt.figure(figsize=(14, 8))
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Pacotes_Perdidos'], 
             marker='s', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Pacotes Perdidos (Absoluto)', fontsize=14, fontweight='bold')
plt.title('PERDA DE PACOTES (Absoluto) - COM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.yscale('log')
salvar_grafico('perda_absoluta_com_mobilidade')

# 3.3 Perda percentual - Sem mobilidade
plt.figure(figsize=(14, 8))
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_static[df_static['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Taxa_Perda_%'], 
             marker='o', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Taxa de Perda (%)', fontsize=14, fontweight='bold')
plt.title('PERDA DE PACOTES (Percentual) - SEM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
salvar_grafico('perda_percentual_sem_mobilidade')

# 3.4 Perda percentual - Com mobilidade
plt.figure(figsize=(14, 8))
for aplicacao in ['CBR', 'TCP', 'MIXED']:
    dados = df_mobile[df_mobile['Aplicacao'] == aplicacao]
    plt.plot(dados['Clientes'], dados['Taxa_Perda_%'], 
             marker='s', linewidth=3, markersize=8, label=f'{aplicacao}')

plt.xlabel('Número de Clientes', fontsize=14, fontweight='bold')
plt.ylabel('Taxa de Perda (%)', fontsize=14, fontweight='bold')
plt.title('PERDA DE PACOTES (Percentual) - COM Mobilidade', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
salvar_grafico('perda_percentual_com_mobilidade')

# 4. GRÁFICOS COMPARATIVOS ADICIONAIS
print("Gerando gráficos comparativos adicionais...")

# 4.1 Comparação UDP vs TCP para diferentes números de clientes
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

metricas = ['Throughput_Medio_Mbps', 'Delay_Medio_ms', 'Taxa_Perda_%']
nomes_metricas = ['Vazão (Mbps)', 'Atraso (ms)', 'Perda (%)']

for i, (metrica, nome_metrica) in enumerate(zip(metricas, nomes_metricas)):
    # Sem mobilidade
    for aplicacao in ['CBR', 'TCP']:
        dados = df_static[df_static['Aplicacao'] == aplicacao]
        axes[i].plot(dados['Clientes'], dados[metrica], 
                    marker='o' if aplicacao == 'CBR' else 's', 
                    linewidth=3, markersize=8, label=f'{aplicacao} - Static')
    
    # Com mobilidade
    for aplicacao in ['CBR', 'TCP']:
        dados = df_mobile[df_mobile['Aplicacao'] == aplicacao]
        axes[i].plot(dados['Clientes'], dados[metrica], 
                    marker='o' if aplicacao == 'CBR' else 's', 
                    linewidth=3, markersize=8, label=f'{aplicacao} - Mobile',
                    linestyle='--')
    
    axes[i].set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
    axes[i].set_ylabel(nome_metrica, fontsize=12, fontweight='bold')
    axes[i].set_title(f'UDP vs TCP - {nome_metrica}', fontsize=14, fontweight='bold')
    axes[i].legend(fontsize=10)
    axes[i].grid(True, alpha=0.3)
    
    if metrica == 'Delay_Medio_ms':
        axes[i].set_yscale('log')

# 4.2 Impacto da mobilidade em cada métrica
for i, (metrica, nome_metrica) in enumerate(zip(metricas, nomes_metricas), 3):
    for aplicacao in ['CBR', 'TCP', 'MIXED']:
        dados_static = df_static[df_static['Aplicacao'] == aplicacao]
        dados_mobile = df_mobile[df_mobile['Aplicacao'] == aplicacao]
        
        impacto = (dados_mobile[metrica].values - dados_static[metrica].values) / dados_static[metrica].values * 100
        
        axes[i].plot(dados_static['Clientes'], impacto, 
                    marker='o', linewidth=3, markersize=8, label=aplicacao)
    
    axes[i].set_xlabel('Número de Clientes', fontsize=12, fontweight='bold')
    axes[i].set_ylabel('Variação (%)', fontsize=12, fontweight='bold')
    axes[i].set_title(f'Impacto da Mobilidade - {nome_metrica}', fontsize=14, fontweight='bold')
    axes[i].legend(fontsize=10)
    axes[i].grid(True, alpha=0.3)
    axes[i].axhline(y=0, color='red', linestyle='-', alpha=0.8)

plt.suptitle('ANÁLISE COMPARATIVA DETALHADA - UDP vs TCP E IMPACTO DA MOBILIDADE', 
             fontsize=18, fontweight='bold', y=0.98)
salvar_grafico('analise_comparativa_detalhada')

# 5. GRÁFICO COMPORTAMENTO COM 32 CLIENTES VS 1 CLIENTE
print("Gerando gráfico comparativo 32 vs 1 clientes...")

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Selecionar dados para 1 e 32 clientes
df_1 = df[df['Clientes'] == 1]
df_32 = df[df['Clientes'] == 32]

metricas_comparacao = ['Throughput_Medio_Mbps', 'Delay_Medio_ms', 'Taxa_Perda_%']
titulos_comparacao = ['Vazão (Mbps)', 'Atraso (ms)', 'Perda (%)']

for i, (metrica, titulo) in enumerate(zip(metricas_comparacao, titulos_comparacao)):
    x_pos = np.arange(len(df_1))
    width = 0.35
    
    valores_1 = df_1[metrica].values
    valores_32 = df_32[metrica].values
    
    axes[i].bar(x_pos - width/2, valores_1, width, label='1 Cliente', alpha=0.8)
    axes[i].bar(x_pos + width/2, valores_32, width, label='32 Clientes', alpha=0.8)
    
    axes[i].set_xlabel('Cenários', fontsize=12, fontweight='bold')
    axes[i].set_ylabel(titulo, fontsize=12, fontweight='bold')
    axes[i].set_title(f'Comparação 1 vs 32 Clientes - {titulo}', fontsize=14, fontweight='bold')
    axes[i].set_xticks(x_pos)
    axes[i].set_xticklabels([f'{row.Aplicacao}\n{row.Mobilidade}' for _, row in df_1.iterrows()], 
                           rotation=45, ha='right')
    axes[i].legend(fontsize=10)
    axes[i].grid(True, alpha=0.3)

plt.suptitle('COMPARAÇÃO EXTREMA: 1 CLIENTE vs 32 CLIENTES', fontsize=16, fontweight='bold')
salvar_grafico('comparacao_extrema_1_vs_32')

# 6. RESUMO ESTATÍSTICO
print("Gerando resumo estatístico...")

# Calcular estatísticas resumidas
resumo = df.groupby(['Mobilidade', 'Aplicacao', 'Clientes']).agg({
    'Throughput_Medio_Mbps': 'mean',
    'Delay_Medio_ms': 'mean', 
    'Taxa_Perda_%': 'mean',
    'Pacotes_Perdidos': 'mean'
}).round(3)

print("=" * 80)
print("RESUMO ESTATÍSTICO DOS DADOS")
print("=" * 80)
print(resumo)

# Salvar resumo em CSV
resumo.to_csv('resumo_estatistico.csv')
print("\nResumo estatístico salvo em 'resumo_estatistico.csv'")

print("\n✅ Todos os gráficos foram gerados com sucesso!")
print("📊 Gráficos salvos em PNG e PDF")
print("📈 Análise completa disponível para o relatório")