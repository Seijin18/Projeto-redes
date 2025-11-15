#!/usr/bin/env python3
"""
Gerador de Relatório PDF - Projeto NS-3 UNIFESP
Equipe 4 - 2º Semestre 2025
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

# Configurações
OUTPUT_FILE = "/home/marshibs/redes/equipe_4_relatorio_redes_2s2025.pdf"
GRAFICOS_DIR = "/home/marshibs/redes/graficos"
DADOS_DIR = "/home/marshibs/redes/dados"

def create_report():
    """Cria o relatório PDF"""
    
    # Criar documento
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003399'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#003399'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14
    )
    
    # Conteúdo
    content = []
    
    # ===== CAPA =====
    content.append(Spacer(1, 0.5*inch))
    content.append(Paragraph("UNIVERSIDADE FEDERAL DE SÃO PAULO", title_style))
    content.append(Paragraph("Campus São José dos Campos", styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Instituto de Ciência e Tecnologia", styles['Normal']))
    content.append(Paragraph("Disciplina: IC 2617 - Redes de Computadores", styles['Normal']))
    content.append(Spacer(1, 0.5*inch))
    
    content.append(Paragraph("Simulação de Rede WiFi com NS-3", title_style))
    content.append(Paragraph("Análise de Desempenho: Delay, Throughput e Perda de Pacotes", heading_style))
    content.append(Spacer(1, 0.3*inch))
    
    content.append(Paragraph("<b>Equipe 4</b>", styles['Normal']))
    content.append(Paragraph("2º Semestre de 2025", styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph(f"Data: {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
    
    content.append(PageBreak())
    
    # ===== RESUMO EXECUTIVO =====
    content.append(Paragraph("1. RESUMO EXECUTIVO", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    resumo_text = """
    Este projeto apresenta a simulação e análise de uma rede sem fio IEEE 802.11a 
    utilizando o simulador NS-3 (Network Simulator). A rede foi submetida a 36 cenários 
    diferentes variando três parâmetros principais: número de clientes (1, 2, 4, 8, 16, 32), 
    tipo de mobilidade (estática e móvel) e protocolo de transporte (CBR/UDP, TCP e misto).
    <br/><br/>
    Os resultados mostram que o desempenho da rede se degrada significativamente com o aumento 
    do número de clientes, especialmente em cenários com mobilidade. O throughput mantém-se 
    aproximadamente constante em ~512 kbps por cliente para aplicações UDP, enquanto TCP apresenta 
    valores reduzidos devido a mecanismos de controle de congestionamento. O delay aumenta de 
    aproximadamente 6.3 ms com um cliente para valores superiores a 250 ms com 32 clientes, 
    indicando a limitação do protocolo IEEE 802.11a em cenários de alta densidade.
    """
    
    content.append(Paragraph(resumo_text.strip(), body_style))
    content.append(Spacer(1, 0.2*inch))
    
    # ===== DESCRIÇÃO DO EXERCÍCIO =====
    content.append(Paragraph("2. DESCRIÇÃO DO EXERCÍCIO PROPOSTO", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    desc_text = """
    <b>Topologia de Rede:</b><br/>
    A simulação implementa uma rede híbrida composta por dois segmentos:<br/>
    • <b>Segmento Cabeado (10.1.1.0/24):</b> Servidor s2 conectado através de dois nós 
    intermediários (s1 e s0) a um Access Point (AP), com velocidade de 100 Mbps e latência de 2 ms.<br/>
    • <b>Segmento Wireless (192.168.0.0/24):</b> Múltiplos clientes WiFi (STAs) conectados ao AP 
    utilizando o padrão IEEE 802.11a com potência de transmissão de 16 dBm.
    <br/><br/>
    <b>Cenários de Teste:</b><br/>
    Foram executados 36 cenários resultantes da combinação de:<br/>
    • 6 valores para número de clientes: 1, 2, 4, 8, 16, 32<br/>
    • 2 tipos de mobilidade: Estática (velocidade 0 km/h) e Móvel (1.0-2.0 m/s)<br/>
    • 3 protocolos: CBR/UDP (512 kbps), TCP (512 kbps), Misto (50% UDP + 50% TCP)
    """
    
    content.append(Paragraph(desc_text.strip(), body_style))
    content.append(Spacer(1, 0.2*inch))
    
    # ===== METODOLOGIA =====
    content.append(Paragraph("3. AVALIAÇÃO DE DESEMPENHO", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    metodo_text = """
    <b>Ferramenta:</b> NS-3 (Network Simulator version 3.43)<br/>
    <b>Método:</b> Simulação discreta de eventos<br/>
    <b>Duração de cada simulação:</b> 60 segundos<br/>
    <b>Repetições:</b> 1 execução por cenário<br/>
    <br/>
    <b>Métrica de Coleta:</b> FlowMonitor NS-3<br/>
    As seguintes métricas foram coletadas para cada cenário:<br/>
    • <b>Throughput:</b> Taxa média de dados recebidos (kbps)<br/>
    • <b>Delay:</b> Latência média de ponta-a-ponta (ms)<br/>
    • <b>Taxa de Perda:</b> Percentual de pacotes perdidos (%)
    """
    
    content.append(Paragraph(metodo_text.strip(), body_style))
    
    content.append(PageBreak())
    
    # ===== RESULTADOS =====
    content.append(Paragraph("4. RESULTADOS", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    # Gráfico 1
    content.append(Paragraph("<b>4.1 Throughput vs Número de Clientes</b>", styles['Heading3']))
    content.append(Spacer(1, 0.1*inch))
    
    if os.path.exists(f"{GRAFICOS_DIR}/throughput.png"):
        img = Image(f"{GRAFICOS_DIR}/throughput.png", width=6*inch, height=2.5*inch)
        content.append(img)
    content.append(Spacer(1, 0.1*inch))
    
    # Gráfico 2
    content.append(Paragraph("<b>4.2 Delay vs Número de Clientes</b>", styles['Heading3']))
    content.append(Spacer(1, 0.1*inch))
    
    if os.path.exists(f"{GRAFICOS_DIR}/delay.png"):
        img = Image(f"{GRAFICOS_DIR}/delay.png", width=6*inch, height=2.5*inch)
        content.append(img)
    content.append(Spacer(1, 0.1*inch))
    
    content.append(PageBreak())
    
    # Gráfico 3
    content.append(Paragraph("<b>4.3 Taxa de Perda vs Número de Clientes</b>", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    if os.path.exists(f"{GRAFICOS_DIR}/packet_loss.png"):
        img = Image(f"{GRAFICOS_DIR}/packet_loss.png", width=6*inch, height=2.5*inch)
        content.append(img)
    content.append(Spacer(1, 0.2*inch))
    
    # ===== ANÁLISE E DISCUSSÃO =====
    content.append(Paragraph("5. ANÁLISE E DISCUSSÃO", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    analise_text = """
    <b>5.1 Impacto do Número de Clientes</b><br/>
    A análise dos resultados revela que o aumento do número de clientes produz efeitos 
    significativos nas métricas de desempenho:
    <br/><br/>
    • <b>Throughput:</b> Mantém-se aproximadamente constante em ~540 kbps para CBR, 
    indicando que cada cliente consegue manter sua taxa de transmissão configurada.
    <br/>
    • <b>Delay:</b> Aumenta exponencialmente, passando de ~6.3 ms com 1 cliente para 
    ~258 ms com 32 clientes em cenários estáticos. Este aumento é causado pelo aumento 
    de colisões e retransmissões no acesso ao meio WiFi.
    <br/>
    • <b>Taxa de Perda:</b> Praticamente nula com poucos clientes, mas aumenta 
    significativamente a partir de 32 clientes, atingindo ~10%.
    <br/><br/>
    <b>5.2 Efeito da Mobilidade</b><br/>
    A mobilidade dos clientes piora significativamente o desempenho da rede:
    <br/><br/>
    • Em cenários com 1-8 clientes, o impacto é pequeno.
    <br/>
    • Com 16 clientes móveis, o delay aumenta de ~8.5 ms para ~10 ms e a taxa de perda 
    aumenta para ~1.76%.
    <br/>
    • Com 32 clientes, a mobilidade reduz o throughput e aumenta ainda mais o delay 
    e a taxa de perda.
    <br/><br/>
    <b>5.3 Comparação entre Protocolos</b><br/>
    • <b>UDP/CBR:</b> Mantém taxa aproximadamente constante, sem mecanismo de controle 
    de congestionamento. Resultados mais estáveis em qualquer cenário.
    <br/>
    • <b>TCP:</b> Reduz a taxa de transmissão sob congestionamento, resultando em 
    throughput menor (~296 kbps vs 540 kbps do UDP).
    <br/>
    • <b>Misto:</b> Apresenta comportamento intermediário, já que metade dos clientes 
    usa UDP e metade TCP.
    """
    
    content.append(Paragraph(analise_text.strip(), body_style))
    
    content.append(PageBreak())
    
    # ===== CONCLUSÃO =====
    content.append(Paragraph("6. CONCLUSÃO", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    conclusao_text = """
    A simulação da rede WiFi IEEE 802.11a revelou características importantes sobre o 
    desempenho de redes sem fio em cenários com múltiplos clientes:
    <br/><br/>
    1. <b>Limitações de Escalabilidade:</b> O padrão 802.11a, apesar de sua alta taxa 
    nominal (54 Mbps), apresenta degradação significativa com o aumento de clientes, 
    especialmente em topologias com um único AP.
    <br/><br/>
    2. <b>Impacto da Mobilidade:</b> A mobilidade dos clientes piora o desempenho em 
    cenários já congestionados, reforçando a importância de técnicas de handover e 
    otimização de potência.
    <br/><br/>
    3. <b>Seleção de Protocolo:</b> A escolha entre UDP e TCP deve considerar o cenário 
    específico. UDP oferece melhor throughput em redes congestionadas, enquanto TCP 
    oferece melhor confiabilidade.
    <br/><br/>
    4. <b>Recomendações Práticas:</b> Para redes com mais de 16 clientes, recomenda-se 
    a implementação de múltiplos APs com roaming, otimização de potência e uso de 
    padrões mais modernos como 802.11n/ac.
    """
    
    content.append(Paragraph(conclusao_text.strip(), body_style))
    
    content.append(Spacer(1, 0.3*inch))
    content.append(Paragraph(f"Data de Conclusão: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", 
                            styles['Normal']))
    
    # Construir PDF
    doc.build(content)
    print(f"✅ Relatório gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        create_report()
    except ImportError:
        print("Erro: reportlab não está instalado.")
        print("Para instalar: pip install reportlab")
        import sys
        sys.exit(1)
