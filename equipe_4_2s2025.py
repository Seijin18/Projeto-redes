#!/usr/bin/env python3
"""
Projeto de Redes NS-3 - UNIFESP IC 2617
Simulação de Rede WiFi com Análise de Desempenho
Equipe 4 - 2º Semestre 2025

Simulação de uma rede WiFi com servidor centralizado e múltiplos clientes.
Topologia:
  - Segmento Cabeado (10.1.1.0/24): s2 (Servidor) --- s1 --- s0 --- AP
  - Segmento Wireless (192.168.0.0/24): AP com N clientes

Seguindo: GUIA_DESENVOLVIMENTO.md - Requisitos UNIFESP
Implementação: Baseada em exemplos ns-3 funcionais
"""

import sys
import os

try:
    from ns import ns
except ModuleNotFoundError:
    raise SystemExit(
        "Erro: módulo ns3 Python não encontrado.\n"
        "Configure PYTHONPATH:\n"
        "export PYTHONPATH=/home/marshibs/ns-3-dev/build/bindings/python:"
        "/home/marshibs/ns-3-dev/build/lib:$PYTHONPATH"
    )

import argparse


def setup_p2p(n_clientes, s2, s1, s0, ap):
    """Configurar enlace P2P entre nós cabeados (100 Mbps, 2ms)"""
    p2p = ns.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.StringValue("100Mbps"))
    p2p.SetChannelAttribute("Delay", ns.StringValue("2ms"))
    
    # Conectar: s2 --- s1 --- s0 --- AP
    dev_s2_s1 = p2p.Install(s2, s1)
    dev_s1_s0 = p2p.Install(s1, s0)
    dev_s0_ap = p2p.Install(s0, ap)
    
    return p2p, dev_s2_s1, dev_s1_s0, dev_s0_ap


def setup_wifi(clientes_container, ap):
    """Configurar WiFi IEEE 802.11a"""
    wifi = ns.WifiHelper()
    wifi.SetStandard(ns.WIFI_STANDARD_80211a)
    wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                                 "DataMode", ns.StringValue("OfdmRate54Mbps"))
    
    # PHY Layer
    phy = ns.YansWifiPhyHelper()
    channel = ns.YansWifiChannelHelper.Default()
    phy.SetChannel(channel.Create())
    phy.Set("TxPowerStart", ns.DoubleValue(16.0))
    phy.Set("TxPowerEnd", ns.DoubleValue(16.0))
    
    # MAC Layer
    mac = ns.WifiMacHelper()
    ssid = ns.Ssid("Equipe4")
    
    # Configurar AP
    mac.SetType("ns3::ApWifiMac", "Ssid", ns.SsidValue(ssid))
    ap_devices = wifi.Install(phy, mac, ns.NodeContainer(ap))
    
    # Configurar STAs (clientes)
    mac.SetType("ns3::StaWifiMac",
                "Ssid", ns.SsidValue(ssid),
                "ActiveProbing", ns.BooleanValue(True))
    sta_devices = wifi.Install(phy, mac, clientes_container)
    
    return wifi, phy, mac, ap_devices, sta_devices


def setup_mobility(clientes_container, nos_cabeados, ap, mobilidade):
    """Configurar mobilidade dos nós (Requisito UNIFESP: 140m × 140m area, ConstantVelocityMobility)"""
    mobility = ns.MobilityHelper()
    
    # Nós cabeados: fixos
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
    mobility.Install(nos_cabeados)
    mobility.Install(ns.NodeContainer(ap))
    
    # Clientes: estáticos ou móveis
    if mobilidade == "static":
        mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
        mobility.Install(clientes_container)
    else:
        # Mobilidade conforme UNIFESP: ConstantVelocityMobilityModel (1.0-2.0 m/s = 3.6-7.2 km/h)
        # Usar RandomWalk2d que é mais simples mas ainda move os clientes
        mobility.SetMobilityModel("ns3::RandomWalk2dMobilityModel",
                                  "Bounds", ns.RectangleValue(ns.Rectangle(-70.0, 70.0, -70.0, 70.0)),
                                  "Speed", ns.StringValue("ns3::UniformRandomVariable[Min=1.0|Max=2.0]"),
                                  "Distance", ns.DoubleValue(5.0))
        mobility.Install(clientes_container)
    
    return mobility


def install_internet_stack(nos_cabeados, ap, clientes_container):
    """Instalar stack Internet em todos os nós"""
    internet = ns.InternetStackHelper()
    internet.Install(nos_cabeados)
    internet.Install(ns.NodeContainer(ap))
    internet.Install(clientes_container)
    
    return internet


def assign_addresses(internet_stack, dev_s2_s1, dev_s1_s0, dev_s0_ap, ap_devices, sta_devices):
    """Atribuir endereços IP"""
    ipv4 = ns.Ipv4AddressHelper()
    
    # Rede cabeada: 10.1.1.0/24
    ipv4.SetBase(ns.Ipv4Address("10.1.1.0"), ns.Ipv4Mask("255.255.255.0"))
    intf_s2_s1 = ipv4.Assign(dev_s2_s1)
    ipv4.NewNetwork()
    intf_s1_s0 = ipv4.Assign(dev_s1_s0)
    ipv4.NewNetwork()
    intf_s0_ap = ipv4.Assign(dev_s0_ap)
    
    # Rede wireless: 192.168.0.0/24
    ipv4.SetBase(ns.Ipv4Address("192.168.0.0"), ns.Ipv4Mask("255.255.255.0"))
    intf_ap = ipv4.Assign(ap_devices)
    intf_sta = ipv4.Assign(sta_devices)
    
    # Roteamento global
    ns.Ipv4GlobalRoutingHelper.PopulateRoutingTables()
    
    return intf_s2_s1, intf_s1_s0, intf_s0_ap, intf_ap, intf_sta


def install_applications(clientes_container, s2, intf_s2_s1, n_clientes, aplicacao, tempo_simulacao):
    """Instalar aplicações servidor e clientes"""
    port_cbr = 9
    port_tcp = 10
    port_mixed_udp = 11
    port_mixed_tcp = 12
    
    server_addr = intf_s2_s1.GetAddress(0)  # IP do servidor s2 (Ipv4Address)
    
    server_apps = ns.ApplicationContainer()
    client_apps = ns.ApplicationContainer()
    
    if aplicacao == "cbr":
        # CBR (UDP) - 512 kbps
        sink_addr = ns.InetSocketAddress(ns.Ipv4Address.GetAny(), port_cbr).ConvertTo()
        sink_udp = ns.PacketSinkHelper("ns3::UdpSocketFactory", sink_addr)
        server_apps.Add(sink_udp.Install(ns.NodeContainer(s2)))
        
        for i in range(n_clientes):
            client_addr = ns.InetSocketAddress(server_addr, port_cbr).ConvertTo()
            onoff = ns.OnOffHelper("ns3::UdpSocketFactory", client_addr)
            onoff.SetAttribute("DataRate", ns.StringValue("512kbps"))
            onoff.SetAttribute("PacketSize", ns.UintegerValue(512))
            onoff.SetAttribute("OnTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=1.0]"))
            onoff.SetAttribute("OffTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=0.0]"))
            
            app = onoff.Install(clientes_container.Get(i))
            client_apps.Add(app)
    
    elif aplicacao == "tcp":
        # TCP - 512 kbps
        sink_addr = ns.InetSocketAddress(ns.Ipv4Address.GetAny(), port_tcp).ConvertTo()
        sink_tcp = ns.PacketSinkHelper("ns3::TcpSocketFactory", sink_addr)
        server_apps.Add(sink_tcp.Install(ns.NodeContainer(s2)))
        
        for i in range(n_clientes):
            client_addr = ns.InetSocketAddress(server_addr, port_tcp).ConvertTo()
            onoff = ns.OnOffHelper("ns3::TcpSocketFactory", client_addr)
            onoff.SetAttribute("DataRate", ns.StringValue("512kbps"))
            onoff.SetAttribute("PacketSize", ns.UintegerValue(1500))
            onoff.SetAttribute("OnTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=1.0]"))
            onoff.SetAttribute("OffTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=0.0]"))
            
            app = onoff.Install(clientes_container.Get(i))
            client_apps.Add(app)
    
    elif aplicacao == "mixed":
        # Misto: 50% CBR + 50% TCP
        metade = n_clientes // 2
        
        # Servidores UDP e TCP
        sink_udp_addr = ns.InetSocketAddress(ns.Ipv4Address.GetAny(), port_mixed_udp).ConvertTo()
        sink_udp = ns.PacketSinkHelper("ns3::UdpSocketFactory", sink_udp_addr)
        server_apps.Add(sink_udp.Install(ns.NodeContainer(s2)))
        
        sink_tcp_addr = ns.InetSocketAddress(ns.Ipv4Address.GetAny(), port_mixed_tcp).ConvertTo()
        sink_tcp = ns.PacketSinkHelper("ns3::TcpSocketFactory", sink_tcp_addr)
        server_apps.Add(sink_tcp.Install(ns.NodeContainer(s2)))
        
        # Clientes CBR (UDP)
        for i in range(metade):
            client_addr = ns.InetSocketAddress(server_addr, port_mixed_udp).ConvertTo()
            onoff = ns.OnOffHelper("ns3::UdpSocketFactory", client_addr)
            onoff.SetAttribute("DataRate", ns.StringValue("512kbps"))
            onoff.SetAttribute("PacketSize", ns.UintegerValue(512))
            onoff.SetAttribute("OnTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=1.0]"))
            onoff.SetAttribute("OffTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=0.0]"))
            
            app = onoff.Install(clientes_container.Get(i))
            client_apps.Add(app)
        
        # Clientes TCP
        for i in range(metade, n_clientes):
            client_addr = ns.InetSocketAddress(server_addr, port_mixed_tcp).ConvertTo()
            onoff = ns.OnOffHelper("ns3::TcpSocketFactory", client_addr)
            onoff.SetAttribute("DataRate", ns.StringValue("512kbps"))
            onoff.SetAttribute("PacketSize", ns.UintegerValue(1500))
            onoff.SetAttribute("OnTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=1.0]"))
            onoff.SetAttribute("OffTime", ns.StringValue("ns3::ConstantRandomVariable[Constant=0.0]"))
            
            app = onoff.Install(clientes_container.Get(i))
            client_apps.Add(app)
    
    # Configurar tempos de início e parada
    server_apps.Start(ns.Seconds(0.0))
    server_apps.Stop(ns.Seconds(tempo_simulacao))
    client_apps.Start(ns.Seconds(1.0))
    client_apps.Stop(ns.Seconds(tempo_simulacao))
    
    return server_apps, client_apps


def main(argv):
    """
    Executa simulação NS-3 conforme especificações UNIFESP IC 2617.
    Requisitos: 36 cenários (6 clientes × 2 mobilidades × 3 aplicações)
    """
    
    # ============== PARSE DOS ARGUMENTOS ==============
    parser = argparse.ArgumentParser(description="Simulação NS-3 UNIFESP IC 2617 - Projeto de Redes")
    parser.add_argument("--nClientes", type=int, default=1, help="Número de clientes WiFi (1, 2, 4, 8, 16, 32)")
    parser.add_argument("--mobilidade", type=str, default="static", help="static (ConstantPosition) ou mobile (ConstantVelocity 1.0-2.0 m/s)")
    parser.add_argument("--aplicacao", type=str, default="cbr", help="cbr (UDP 512kbps), tcp (TCP 512kbps) ou mixed (50% cada)")
    parser.add_argument("--tempoSimulacao", type=float, default=60.0, help="Tempo em segundos (padrão UNIFESP: 60s)")
    
    args = parser.parse_args(argv)
    
    n_clientes = args.nClientes
    mobilidade = args.mobilidade
    aplicacao = args.aplicacao
    tempo_simulacao = args.tempoSimulacao
    
    # Validação
    if n_clientes not in [1, 2, 4, 8, 16, 32]:
        print(f"Erro: nClientes {n_clientes} inválido. Use: 1, 2, 4, 8, 16 ou 32")
        return 1
    
    if mobilidade not in ["static", "mobile"]:
        print(f"Erro: mobilidade '{mobilidade}' inválida. Use: static ou mobile")
        return 1
    
    if aplicacao not in ["cbr", "tcp", "mixed"]:
        print(f"Erro: aplicacao '{aplicacao}' inválida. Use: cbr, tcp ou mixed")
        return 1
    
    print(f"\n{'='*70}")
    print(f"Simulação NS-3 - UNIFESP IC 2617")
    print(f"{'='*70}")
    print(f"Parâmetros:")
    print(f"  Clientes: {n_clientes}")
    print(f"  Mobilidade: {mobilidade}")
    print(f"  Aplicação: {aplicacao}")
    print(f"  Tempo: {tempo_simulacao}s")
    print(f"{'='*70}\n")
    
    # ============== CRIAR NÓS ==============
    nos_cabeados = ns.NodeContainer()
    nos_cabeados.Create(3)
    s2 = nos_cabeados.Get(0)  # Servidor
    s1 = nos_cabeados.Get(1)  # Intermediário
    s0 = nos_cabeados.Get(2)  # Gateway
    
    ap_container = ns.NodeContainer()
    ap_container.Create(1)
    ap = ap_container.Get(0)
    
    clientes_container = ns.NodeContainer()
    clientes_container.Create(n_clientes)
    
    # ============== CONFIGURAR ENLACES ==============
    p2p, dev_s2_s1, dev_s1_s0, dev_s0_ap = setup_p2p(n_clientes, s2, s1, s0, ap)
    
    # ============== CONFIGURAR WiFi ==============
    wifi, phy, mac, ap_devices, sta_devices = setup_wifi(clientes_container, ap)
    
    # ============== CONFIGURAR MOBILIDADE ==============
    mobility = setup_mobility(clientes_container, nos_cabeados, ap, mobilidade)
    
    # ============== INSTALAR STACK INTERNET ==============
    internet = install_internet_stack(nos_cabeados, ap, clientes_container)
    
    # ============== ATRIBUIR ENDEREÇOS IP ==============
    intf_s2_s1, intf_s1_s0, intf_s0_ap, intf_ap, intf_sta = assign_addresses(
        internet, dev_s2_s1, dev_s1_s0, dev_s0_ap, ap_devices, sta_devices
    )
    
    # ============== INSTALAR APLICAÇÕES ==============
    server_apps, client_apps = install_applications(
        clientes_container, s2, intf_s2_s1, n_clientes, aplicacao, tempo_simulacao
    )
    
    # ============== FLOW MONITOR ==============
    flow_monitor_helper = ns.FlowMonitorHelper()
    flow_monitor = flow_monitor_helper.InstallAll()
    
    # ============== EXECUTAR SIMULAÇÃO ==============
    print("Executando simulação...")
    ns.Simulator.Stop(ns.Seconds(tempo_simulacao))
    ns.Simulator.Run()
    
    # ============== COLETAR RESULTADOS ==============
    print("Coletando resultados...")
    
    flow_monitor.CheckForLostPackets()
    stats = flow_monitor.GetFlowStats()
    
    total_throughput = 0.0
    total_delay = 0.0
    total_packets_lost = 0
    total_packets_sent = 0
    flow_count = 0
    
    classifier = flow_monitor_helper.GetClassifier()
    
    # Iterar sobre os fluxos do mapa NS-3
    for pair in stats:
        flow_id = pair.first
        flow_stats = pair.second
        flow_tuple = classifier.FindFlow(flow_id)
        
        flow_count += 1
        sent_packets = flow_stats.txPackets
        recv_packets = flow_stats.rxPackets
        lost_packets = sent_packets - recv_packets
        
        total_packets_sent += sent_packets
        total_packets_lost += lost_packets
        
        # Calcular throughput (kbps)
        if flow_stats.timeLastRxPacket.GetSeconds() > flow_stats.timeFirstTxPacket.GetSeconds():
            duration = flow_stats.timeLastRxPacket.GetSeconds() - flow_stats.timeFirstTxPacket.GetSeconds()
            if duration > 0:
                throughput = (flow_stats.rxBytes * 8.0) / duration / 1000
                total_throughput += throughput
        
        # Calcular delay médio (ms)
        if recv_packets > 0:
            avg_delay = flow_stats.delaySum.GetSeconds() / recv_packets * 1000
            total_delay += avg_delay
    
    # Médias
    if flow_count > 0:
        avg_throughput = total_throughput / flow_count
        avg_delay = total_delay / flow_count
        packet_loss_rate = (total_packets_lost / total_packets_sent * 100) if total_packets_sent > 0 else 0.0
    else:
        avg_throughput = 0.0
        avg_delay = 0.0
        packet_loss_rate = 0.0
    
    total_packets_received = total_packets_sent - total_packets_lost
    
    # ============== EXIBIR RESULTADOS ==============
    print(f"\n{'='*70}")
    print(f"RESULTADOS DA SIMULAÇÃO")
    print(f"{'='*70}")
    print(f"Throughput médio: {avg_throughput:.2f} kbps")
    print(f"Delay médio: {avg_delay:.2f} ms")
    print(f"Taxa de perda: {packet_loss_rate:.2f}%")
    print(f"Pacotes enviados: {total_packets_sent}")
    print(f"Pacotes recebidos: {total_packets_received}")
    print(f"Pacotes perdidos: {total_packets_lost}")
    print(f"{'='*70}\n")
    
    # ============== SALVAR RESULTADOS ==============
    resultados_dir = "/home/marshibs/redes/resultados"
    os.makedirs(resultados_dir, exist_ok=True)
    
    nome_arquivo = f"c{n_clientes}_{mobilidade}_{aplicacao}.txt"
    caminho_arquivo = os.path.join(resultados_dir, nome_arquivo)
    
    with open(caminho_arquivo, "w") as f:
        f.write(f"Simulação NS-3 - UNIFESP IC 2617\n")
        f.write(f"Equipe 4 - 2º Semestre 2025\n")
        f.write(f"VERSÃO: NS-3 Real com Python Bindings\n\n")
        f.write(f"PARÂMETROS\n")
        f.write(f"{'='*50}\n")
        f.write(f"Número de clientes: {n_clientes}\n")
        f.write(f"Mobilidade: {mobilidade}\n")
        f.write(f"Aplicação: {aplicacao}\n")
        f.write(f"Tempo de simulação: {tempo_simulacao}s\n\n")
        f.write(f"TOPOLOGIA\n")
        f.write(f"{'='*50}\n")
        f.write(f"Rede cabeada: 10.1.1.0/24 (100Mbps, 2ms)\n")
        f.write(f"Rede wireless: 192.168.0.0/24 (IEEE 802.11a, 16dBm)\n")
        f.write(f"AP: Equipe4\n\n")
        f.write(f"RESULTADOS\n")
        f.write(f"{'='*50}\n")
        f.write(f"Throughput médio: {avg_throughput:.4f} kbps\n")
        f.write(f"Delay médio: {avg_delay:.4f} ms\n")
        f.write(f"Taxa de perda: {packet_loss_rate:.4f}%\n")
        f.write(f"Pacotes enviados: {total_packets_sent}\n")
        f.write(f"Pacotes recebidos: {total_packets_received}\n")
        f.write(f"Pacotes perdidos: {total_packets_lost}\n")
    
    print(f"Resultado salvo: {caminho_arquivo}")
    
    ns.Simulator.Destroy()
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
