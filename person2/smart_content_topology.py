#!/usr/bin/env python3
"""Starter Mininet topology for the Smart Content Delivery System.

Client: h1 (10.0.0.1)
Server 1: h2 (10.0.0.2)
Server 2: h3 (10.0.0.3)
Switches s1, s2, s3 use a remote OpenFlow 1.3 controller.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


class SmartContentTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')

        client = self.addHost('h1', ip='10.0.0.1/24')
        server1 = self.addHost('h2', ip='10.0.0.2/24')
        server2 = self.addHost('h3', ip='10.0.0.3/24')

        self.addLink(client, s1, bw=20, delay='2ms')
        self.addLink(s1, s2, bw=20, delay='2ms')
        self.addLink(s1, s3, bw=20, delay='2ms')
        self.addLink(s2, server1, bw=20, delay='2ms')
        self.addLink(s3, server2, bw=20, delay='2ms')


def run():
    topo = SmartContentTopo()
    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True,
        waitConnected=True
    )
    net.addController('c0', controller=RemoteController,
                      ip='127.0.0.1', port=6653)
    net.start()
    info('\\n*** Network ready. Hosts: h1 client, h2/h3 content servers.\\n')
    info('*** Try: h1 ping -c 2 h2 ; h1 ping -c 2 h3\\n')
    info('*** Type "links" to inspect links; type "exit" to stop.\\n')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
