import sys
import argparse
from ns import ns

def main(argv):
    # 1. Processa argumentos usando argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--nClients", type=int, default=4, help="Number of Wi-Fi clients")
    parser.add_argument("--simTime", type=float, default=20.0, help="Simulation time (s)")
    parser.add_argument("--mobility", action="store_true", help="Enable random mobility for clients")
    parser.add_argument("--protocol", choices=["udp", "tcp", "mixed"], default="udp", help="Transport protocol")

    # Ignora argumentos extras que ns3 run adiciona
    args, unknown = parser.parse_known_args(argv[1:])

    nClients = args.nClients
    simTime = args.simTime
    mobility = args
    protocol = args.protocol

    # 2. Criação dos nós
    p2pNodes = ns.NodeContainer()
    p2pNodes.Create(2)  # AP e servidor

    wifiStaNodes = ns.NodeContainer()
    wifiStaNodes.Create(nClients)
    wifiApNode = p2pNodes.Get(0)

    # 3. Enlace cabeado entre AP e servidor
    p2p = ns.PointToPointHelper()
    p2p.SetDeviceAttribute("DataRate", ns.StringValue("100Mbps"))
    p2p.SetChannelAttribute("Delay", ns.StringValue("1ms"))
    p2pDevices = p2p.Install(p2pNodes)

    # 4. Configuração Wi-Fi
    wifi = ns.WifiHelper()
    wifi.SetStandard(ns.WIFI_STANDARD_80211g)

    phy = ns.YansWifiPhyHelper()
    channel = ns.YansWifiChannelHelper()
    channel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel")
    channel.AddPropagationLoss("ns3::LogDistancePropagationLossModel")
    phy.SetChannel(channel.Create())

    mac = ns.WifiMacHelper()
    ssid = ns.Ssid("EquipeX")

    # STA
    mac.SetType("ns3::StaWifiMac", "Ssid", ns.SsidValue(ssid),
                "ActiveProbing", ns.BooleanValue(False))
    staDevices = wifi.Install(phy, mac, wifiStaNodes)

    # AP
    mac.SetType("ns3::ApWifiMac", "Ssid", ns.SsidValue(ssid))
    apDevice = wifi.Install(phy, mac, wifiApNode)

    # 5. Mobilidade
    mobilityHelper = ns.MobilityHelper()
    if mobility:
        mobilityHelper.SetMobilityModel(
            "ns3::RandomWalk2dMobilityModel",
            "Bounds", ns.RectangleValue(ns.Rectangle(-50, 50, -50, 50))
        )
        mobilityHelper.Install(wifiStaNodes)
    else:
        mobilityHelper.SetMobilityModel("ns3::ConstantPositionMobilityModel")
        mobilityHelper.Install(wifiStaNodes)

    mobilityHelper.SetMobilityModel("ns3::ConstantPositionMobilityModel")
    mobilityHelper.Install(p2pNodes)

    # 6. Pilha de protocolos e endereçamento IP
    stack = ns.InternetStackHelper()
    stack.Install(wifiStaNodes)
    stack.Install(p2pNodes)

    address = ns.Ipv4AddressHelper()
    address.SetBase(ns.Ipv4Address("10.1.1.0"), ns.Ipv4Mask("255.255.255.0"))
    p2pInterfaces = address.Assign(p2pDevices)

    address.SetBase(ns.Ipv4Address("10.1.2.0"), ns.Ipv4Mask("255.255.255.0"))
    staInterfaces = address.Assign(staDevices)
    address.Assign(apDevice)

    # 7. Aplicações
    port = 5000
    serverApps = ns.ApplicationContainer()
    clientApps = ns.ApplicationContainer()

    for i in range(nClients):
        useUdp = (protocol == "udp") or (protocol == "mixed" and i % 2 == 0)
        if useUdp:
            udpServer = ns.UdpServerHelper(port + i)
            serverApps.Add(udpServer.Install(p2pNodes.Get(1)))

            # Usando InetSocketAddress para o cliente UDP
            udpClient = ns.UdpClientHelper(ns.InetSocketAddress(p2pInterfaces.GetAddress(1), port + i))
            udpClient.SetAttribute("MaxPackets", ns.UintegerValue(1000000))
            udpClient.SetAttribute("Interval", ns.TimeValue(ns.Seconds(0.01)))
            udpClient.SetAttribute("PacketSize", ns.UintegerValue(1024))
            clientApps.Add(udpClient.Install(wifiStaNodes.Get(i)))
        else:
            sinkAddress = ns.InetSocketAddress(p2pInterfaces.GetAddress(1), port + i)
            packetSink = ns.PacketSinkHelper("ns3::TcpSocketFactory",
                                                          ns.Address(sinkAddress))
            serverApps.Add(packetSink.Install(p2pNodes.Get(1)))

            onoff = ns.OnOffHelper("ns3::TcpSocketFactory",
                                               ns.Address(sinkAddress))
            onoff.SetAttribute("DataRate", ns.StringValue("10Mbps"))
            onoff.SetAttribute("PacketSize", ns.UintegerValue(1024))
            onoff.SetAttribute("StartTime", ns.TimeValue(ns.Seconds(1.0)))
            onoff.SetAttribute("StopTime", ns.TimeValue(ns.Seconds(simTime)))
            clientApps.Add(onoff.Install(wifiStaNodes.Get(i)))

    serverApps.Start(ns.Seconds(0.0))
    serverApps.Stop(ns.Seconds(simTime))
    clientApps.Start(ns.Seconds(1.0))
    clientApps.Stop(ns.Seconds(simTime))

    # 8. FlowMonitor
    flowmon = ns.FlowMonitorHelper()
    monitor = flowmon.InstallAll()

    ns.Simulator.Stop(ns.Seconds(simTime + 1))
    ns.Simulator.Run()

    # 9. Resultados
    monitor.CheckForLostPackets()
    classifier = flowmon.GetClassifier().GetObject(ns.Ipv4FlowClassifier.GetTypeId())
    stats = monitor.GetFlowStats()

    print("\n==== Resultados FlowMonitor ====")
    for flowId, flowStats in stats.items():
        t = classifier.FindFlow(flowId)
        print(f"Fluxo {flowId}: {t.sourceAddress} -> {t.destinationAddress}")
        print(f" Tx Packets: {flowStats.txPackets}")
        print(f" Rx Packets: {flowStats.rxPackets}")
        print(f" Lost Packets: {flowStats.lostPackets}")
        throughput = (flowStats.rxBytes * 8.0) / (simTime * 1000000.0)
        print(f" Throughput: {throughput:.6f} Mbps")
        if flowStats.rxPackets > 0:
            meanDelay = flowStats.delaySum.GetSeconds() / flowStats.rxPackets
            print(f" Mean Delay: {meanDelay:.6f} s")
        else:
            print(" Mean Delay: N/A")
        print("-----------------------------")

    ns.Simulator.Destroy()


if __name__ == "__main__":
    main(sys.argv)