#!/usr/bin/env python3
"""
Refatoração do seu script ns-3 (compatível com ns-3.43 Python bindings).
Opção B: script limpo, organizado por funções, com comentários e validações.

Como executar (coloque este arquivo em "scratch/" do ns-3 e rode):
    ./ns3 run scratch/ns3_t5_refactored.py -- --nClients 6 --protocol mixed --mobility

Observações:
- Usa objetos Address (via ConvertTo()) onde necessário (correção do erro original).
- Suporta protocolos: 'udp', 'tcp', 'mixed'.
- Mobilidade opcional (random walk para STAs, posições fixas para AP e P2P nodes).
- Inclui FlowMonitor para métricas simples.
"""

import sys
import argparse
try:
    from ns import ns
except ModuleNotFoundError:
    raise SystemExit(
        "Error: ns3 Python module not found; Python bindings may not be enabled or your PYTHONPATH might not be properly configured"
    )


def parse_args(argv):
    parser = argparse.ArgumentParser(description="ns-3 refactored example: WiFi + P2P + mixed UDP/TCP apps")
    parser.add_argument("--nClients", type=int, default=4, help="Número de clientes WiFi (STAs)")
    parser.add_argument("--simTime", type=float, default=20.0, help="Tempo de simulação em segundos")
    parser.add_argument("--mobility", action="store_true", help="Ativa mobilidade para STAs")
    parser.add_argument("--protocol", type=str, default="udp", choices=["udp", "tcp", "mixed"], help="Protocolo: udp, tcp ou mixed")
    return parser.parse_args(argv[1:])


def enable_logging():
    # Ative logs das aplicações Echo (útil para debug)
    ns.LogComponentEnable("UdpEchoClientApplication", ns.LOG_LEVEL_INFO)
    ns.LogComponentEnable("UdpEchoServerApplication", ns.LOG_LEVEL_INFO)


def create_nodes(n_clients):
    # p2pNodes: [AP, Server]
    p2pNodes = ns.NodeContainer()
    p2pNodes.Create(2)

    # wifi STAs
    wifiStaNodes = ns.NodeContainer()
    wifiStaNodes.Create(n_clients)

    wifiApNode = p2pNodes.Get(0)  # AP ligado ao primeiro p2p node
    return p2pNodes, wifiStaNodes, wifiApNode


def setup_p2p(p2pNodes):
    p2p = ns.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.StringValue("100Mbps"))
    p2p.SetChannelAttribute("Delay", ns.StringValue("1ms"))
    p2pDevices = p2p.Install(p2pNodes)
    return p2p, p2pDevices


def setup_wifi(wifiStaNodes, wifiApNode):
    wifi = ns.WifiHelper()
    wifi.SetStandard(ns.WIFI_STANDARD_80211g)

    phy = ns.YansWifiPhyHelper()
    channel = ns.YansWifiChannelHelper()
    channel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel")
    channel.AddPropagationLoss("ns3::LogDistancePropagationLossModel")
    phy.SetChannel(channel.Create())

    mac = ns.WifiMacHelper()
    ssid = ns.Ssid("EquipeX")

    mac.SetType("ns3::StaWifiMac",
            "Ssid", ns.SsidValue(ssid),
            "ActiveProbing", ns.BooleanValue(True))
    staDevices = wifi.Install(phy, mac, wifiStaNodes)

    mac.SetType("ns3::ApWifiMac", "Ssid", ns.SsidValue(ssid))
    apDevice = wifi.Install(phy, mac, wifiApNode)

    return wifi, phy, mac, staDevices, apDevice


def setup_mobility(wifiStaNodes, p2pNodes, mobility_enabled):
    mobility = ns.MobilityHelper()
    if mobility_enabled:
        # Random walk para STAs
        mobility.SetMobilityModel(
            "ns3::RandomWalk2dMobilityModel",
            "Bounds",
            ns.RectangleValue(ns.Rectangle(-50, 50, -50, 50)),
        )
    else:
        mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")

    mobility.Install(wifiStaNodes)

    # AP e p2p nodes (fixos)
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
    mobility.Install(p2pNodes)


def install_network_stack(wifiStaNodes, p2pNodes, p2pDevices, staDevices, apDevice):
    stack = ns.InternetStackHelper()
    stack.Install(wifiStaNodes)
    stack.Install(p2pNodes)

    address = ns.Ipv4AddressHelper()
    address.SetBase(ns.Ipv4Address("10.1.1.0"), ns.Ipv4Mask("255.255.255.0"))
    p2pInterfaces = address.Assign(p2pDevices)

    address.SetBase(ns.Ipv4Address("10.1.2.0"), ns.Ipv4Mask("255.255.255.0"))
    staInterfaces = address.Assign(staDevices)
    # assign AP device an address in the same network as STAs
    apInterfaces = address.Assign(apDevice)

    return p2pInterfaces, staInterfaces, apInterfaces


def install_applications(p2pNodes, wifiStaNodes, p2pInterfaces, nClients, protocol, simTime, port_base=5000):
    serverApps = ns.ApplicationContainer()
    clientApps = ns.ApplicationContainer()

    # Endereço do servidor como Ipv4Address (para TCP) e Address (para UdpEchoClient)
    server_ipv4 = p2pInterfaces.GetAddress(1)  # Ipv4Address
    server_addr_for_udp = server_ipv4.ConvertTo()  # Address

    for i in range(nClients):
        port = port_base + i
        useUdp = (protocol == "udp") or (protocol == "mixed" and i % 2 == 0)

        if useUdp:
            # UDP server
            udpEchoServer = ns.UdpEchoServerHelper(port)
            serverApps.Add(udpEchoServer.Install(p2pNodes.Get(1)))

            # UDP client -> construtor espera um Address + port
            udpClient = ns.UdpEchoClientHelper(server_addr_for_udp, port)
            udpClient.SetAttribute("MaxPackets", ns.UintegerValue(1000000))
            udpClient.SetAttribute("Interval", ns.TimeValue(ns.Seconds(0.01)))
            udpClient.SetAttribute("PacketSize", ns.UintegerValue(1024))
            clientApps.Add(udpClient.Install(wifiStaNodes.Get(i)))

        else:
            # TCP: PacketSink (server) e OnOff (client)
            # Construímos o InetSocketAddress e então convertemos para Address explícito
            # porque alguns bindings do Python exigem a forma "Address" concretizada.
            sinkAddress = ns.InetSocketAddress(server_ipv4, port)
            sinkAddressAddr = sinkAddress.ConvertTo()

            packetSink = ns.PacketSinkHelper("ns3::TcpSocketFactory", sinkAddressAddr)
            serverApps.Add(packetSink.Install(p2pNodes.Get(1)))

            onoff = ns.OnOffHelper("ns3::TcpSocketFactory", sinkAddressAddr)
            onoff.SetAttribute("DataRate", ns.StringValue("10Mbps"))
            onoff.SetAttribute("PacketSize", ns.UintegerValue(1024))
            onoff.SetAttribute("StartTime", ns.TimeValue(ns.Seconds(1.0)))
            onoff.SetAttribute("StopTime", ns.TimeValue(ns.Seconds(simTime)))
            clientApps.Add(onoff.Install(wifiStaNodes.Get(i)))

    # Start/Stop times
    serverApps.Start(ns.Seconds(0.0))
    serverApps.Stop(ns.Seconds(simTime))
    clientApps.Start(ns.Seconds(1.0))
    clientApps.Stop(ns.Seconds(simTime))

    return serverApps, clientApps


def run_simulation(simTime):
    flowmon = ns.FlowMonitorHelper()
    monitor = flowmon.InstallAll()

    ns.Simulator.Stop(ns.Seconds(simTime + 1))
    ns.Simulator.Run()

    # Resultados
    monitor.CheckForLostPackets()
    classifier = flowmon.GetClassifier()
    stats = monitor.GetFlowStats()

    print("==== Resultados FlowMonitor ====")

    for pair in stats:
        fid = pair.first             # flowId correto
        flowStats = pair.second      # FlowStats correto

        t = classifier.FindFlow(fid)

        print(f"Fluxo {fid}: {t.sourceAddress} -> {t.destinationAddress}")
        print(f" Tx Packets: {flowStats.txPackets}")
        print(f" Rx Packets: {flowStats.rxPackets}")
        print(f" Lost Packets: {flowStats.lostPackets}")

        throughput = (flowStats.rxBytes * 8.0) / (simTime * 1e6)
        print(f" Throughput: {throughput:.6f} Mbps")

        if flowStats.rxPackets > 0:
            meanDelay = flowStats.delaySum.GetSeconds() / flowStats.rxPackets
            print(f" Mean Delay: {meanDelay:.6f} s")
        else:
            print(" Mean Delay: N/A")

        print("-----------------------------")

    ns.Simulator.Destroy()


def main(argv):
    args = parse_args(argv)
    print(f"Parâmetros: nClients={args.nClients}, simTime={args.simTime}, mobility={args.mobility}, protocol={args.protocol}")

    ns.LogComponentEnable("UdpEchoServerApplication", ns.LOG_LEVEL_INFO)
    ns.LogComponentEnable("UdpEchoClientApplication", ns.LOG_LEVEL_INFO)
    ns.LogComponentEnable("PacketSink", ns.LOG_LEVEL_INFO)
    enable_logging()

    # 1. nós
    p2pNodes, wifiStaNodes, wifiApNode = create_nodes(args.nClients)

    # 2. p2p
    p2p, p2pDevices = setup_p2p(p2pNodes)

    # 3. wifi
    wifi, phy, mac, staDevices, apDevice = setup_wifi(wifiStaNodes, wifiApNode)

    # 4. mobilidade
    setup_mobility(wifiStaNodes, p2pNodes, args.mobility)

    # 5. pilha de protocolos e IPs
    p2pInterfaces, staInterfaces, apInterfaces = install_network_stack(
        wifiStaNodes, p2pNodes, p2pDevices, staDevices, apDevice
    )
    
    ns.Ipv4GlobalRoutingHelper.PopulateRoutingTables()
    
    # 6. aplicações
    serverApps, clientApps = install_applications(
        p2pNodes, wifiStaNodes, p2pInterfaces, args.nClients, args.protocol, args.simTime
    )

    # 7. rodar
    run_simulation(args.simTime)


if __name__ == "__main__":
    main(sys.argv)