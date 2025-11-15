# Projeto de Simulação de Redes NS-3 - UNIFESP IC 2617

**Equipe 4 - 2º Semestre 2025**  
**Data de Entrega: 18 de Novembro de 2025**

## Descrição do Projeto

Este projeto implementa uma simulação de rede WiFi com análise de desempenho usando o simulador NS-3 (Network Simulator 3). O objetivo é avaliar o impacto de diferentes fatores na performance da rede:

- **Número de clientes**: 1, 2, 4, 8, 16 e 32
- **Cenários de mobilidade**: Estático e Móvel
- **Tipos de aplicação**: CBR (UDP), TCP e Misto

**Total de 36 cenários testados**

## Topologia da Rede

```
SEGMENTO CABEADO (10.1.1.0/24):
    s2 (Servidor) --- s1 --- s0 --- AP

SEGMENTO WIRELESS (192.168.0.0/24):
    c0, c1, c2, ... , cn (Clientes WiFi)
           |
          AP (Access Point)
```

### Características Técnicas

| Parâmetro | Valor |
|-----------|-------|
| Padrão WiFi | IEEE 802.11a |
| Potência de transmissão | 16 dBm |
| Taxa de dados (CBR) | 512 kbps |
| Taxa de dados (TCP) | 512 kbps |
| Tamanho do quadro UDP | 512 bytes |
| Tamanho do quadro TCP | 1500 bytes |
| Área de simulação | 140m × 140m |
| Tempo de simulação | 60 segundos |
| Enlace P2P | 100 Mbps, 2ms |
| SSID AP | Equipe4 |

## Estrutura de Arquivos

```
projeto-redes/
├── equipe_4_2s2025.py                 # ARQUIVO PRINCIPAL (simulação)
├── equipe_4_relatorio_redes_2s2025.pdf # RELATÓRIO (gerar posteriormente)
├── scripts/
│   ├── executar-experimentos.sh        # Automação dos 36 cenários
│   └── processar-dados.py              # Processamento e gráficos
├── resultados/
│   ├── c1_static_cbr.txt
│   ├── c1_static_tcp.txt
│   ├── c1_static_mixed.txt
│   ├── ... (36 arquivos totais)
├── dados/
│   └── resultados.csv                  # Consolidado em CSV
├── graficos/
│   ├── throughput_vs_clientes.png
│   ├── delay_vs_clientes.png
│   └── packetloss_vs_clientes.png
├── README.md                           # Este arquivo
└── NOTAS_IMPLEMENTACAO.txt             # Notas técnicas
```

## Pré-requisitos

### Dependências Obrigatórias

1. **NS-3**: Simulador de redes
   ```bash
   # Instalação (se ainda não estiver instalado)
   # Consulte: https://www.nsnam.org/docs/installation/index.html
   ```

2. **Python 3.6+**: Com suporte a ns-3
   ```bash
   python3 --version
   ```

3. **Bibliotecas Python**:
   ```bash
   pip3 install matplotlib numpy
   ```

## Como Executar

### Opção 1: Executar um Cenário Específico

```bash
cd /home/marshibs/redes

# Sintaxe:
python3 equipe_4_2s2025.py --nClientes <N> --mobilidade <static|mobile> --aplicacao <cbr|tcp|mixed>

# Exemplo 1: 1 cliente, estático, CBR
python3 equipe_4_2s2025.py --nClientes 1 --mobilidade static --aplicacao cbr

# Exemplo 2: 4 clientes, móvel, TCP
python3 equipe_4_2s2025.py --nClientes 4 --mobilidade mobile --aplicacao tcp

# Exemplo 3: 8 clientes, móvel, misto com verbose
python3 equipe_4_2s2025.py --nClientes 8 --mobilidade mobile --aplicacao mixed --verbose
```

### Opção 2: Executar Todos os 36 Cenários (Automático)

```bash
chmod +x /home/marshibs/redes/scripts/executar-experimentos.sh
/home/marshibs/redes/scripts/executar-experimentos.sh
```

**Tempo estimado**: ~36 minutos (60s × 36 cenários)

### Opção 3: Processar Dados e Gerar Gráficos

Após executar as simulações:

```bash
python3 /home/marshibs/redes/scripts/processar-dados.py
```

Isso irá:
- Ler todos os arquivos de resultado
- Processar os dados
- Gerar 3 gráficos PNG
- Exportar tabela CSV

## Parâmetros do Simulador

### Parâmetros de Linha de Comando

```
--nClientes N         : Número de clientes WiFi (1, 2, 4, 8, 16, 32)
--mobilidade TYPE     : Tipo de mobilidade (static ou mobile)
--aplicacao APP       : Tipo de aplicação (cbr, tcp ou mixed)
--tempoSimulacao T    : Tempo de simulação em segundos (default: 60)
--verbose            : Ativa logs detalhados
--help               : Mostra ajuda
```

## Saídas Geradas

### Arquivos de Resultado (resultados/)
Cada arquivo contém:
- Parâmetros da simulação
- Throughput médio (kbps)
- Delay médio (ms)
- Taxa de perda de pacotes (%)
- Estatísticas de pacotes

### Gráficos (graficos/)
1. **throughput_vs_clientes.png**: Vazão vs número de clientes
2. **delay_vs_clientes.png**: Atraso vs número de clientes
3. **packetloss_vs_clientes.png**: Perda de pacotes vs número de clientes

Cada gráfico mostra comparação entre:
- CBR (UDP)
- TCP
- Misto (50% CBR + 50% TCP)

Para cenários:
- Estático (esquerda)
- Móvel (direita)

### Tabela de Resultados (dados/resultados.csv)
Formato CSV com todos os valores consolidados para análise.

## Interpretação dos Resultados

### Throughput (Vazão)
- Medido em kbps
- Esperado próximo a 512 kbps para CBR e TCP
- Diminui com aumento de clientes
- Móvel pode ter valores menores que estático

### Delay (Atraso)
- Medido em milissegundos (ms)
- Aumenta com congestionamento
- TCP geralmente tem delay maior que CBR
- Mobilidade pode aumentar o delay

### Packet Loss (Perda de Pacotes)
- Percentual de pacotes perdidos
- Idealmente próximo a 0%
- Aumenta significativamente com muitos clientes
- Móvel pode ter maior taxa de perda

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'ns'"

**Causa**: NS-3 Python bindings não estão instalados corretamente

**Solução**:
```bash
# Verificar instalação de ns-3
python3 -c "import ns.core; print(ns.core.__file__)"

# Instalar dependências corretas (Ubuntu/Debian)
sudo apt-get install python3-dev libboost-dev

# Compilar ns-3 com suporte a Python (consulte documentação oficial)
```

### Erro: "Permission denied: scripts/executar-experimentos.sh"

**Solução**:
```bash
chmod +x scripts/executar-experimentos.sh
```

### Simulação muito lenta com 32 clientes

**Normal**: 32 clientes com 512 kbps pode levar até 2-3 minutos por cenário

**Otimizações**:
- Reduzir tempo de simulação para testes: `--tempoSimulacao 30`
- Executar em paralelo em múltiplos terminais
- Usar máquina com mais recursos

## Notas Importantes

1. **Convergência de Rota**: WiFi leva alguns segundos para estabelecer conexão (aplicações iniciam em 1.0s)

2. **Variabilidade**: Resultados podem variar levemente entre execuções devido à aleatoriedade

3. **Mobilidade**: O modelo RandomWalk2d faz clientes se moverem aleatoriamente em [-70, 70] × [-70, 70]

4. **Nomeação de Arquivos**: Manter formato `c{clientes}_{mobilidade}_{aplicacao}.txt` para compatibilidade com processador

## Próximas Etapas

1. ✓ Implementação do simulador
2. ✓ Testes iniciais (1-2 cenários)
3. ⭐ Executar todos os 36 cenários
4. ⭐ Processar dados e gerar gráficos
5. ⭐ Criar relatório técnico
6. ⭐ Entrega até 18/11/2025 23:59

## Referências

- [NS-3 Documentation](https://www.nsnam.org/docs/)
- [NS-3 API](https://www.nsnam.org/docs/doxygen/index.html)
- [IEEE 802.11a Specification](https://en.wikipedia.org/wiki/IEEE_802.11a)

## Contato e Suporte

Para dúvidas sobre a implementação:
1. Consulte o arquivo GUIA_DESENVOLVIMENTO.md
2. Revise a documentação oficial do NS-3
3. Verifique NOTAS_IMPLEMENTACAO.txt

---

**Status**: Projeto em desenvolvimento  
**Última atualização**: 14 de Novembro de 2025
