
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import os 
import sys
import math 

class Tree(Topo):
    def __init__(self, Nhost):
        print('Initailize the tree topo.')
        self.Nedge = int(math.ceil(Nhost//2))
        self.Nhost = Nhost
        self.root = None  
        self.edge = []
        self.host = []
        Topo.__init__(self)
    def buildTopo(self):
        print('Build root switch.')
        self.root = self.addSwitch(str(1001))
        print('Build edge layer switches.')
        for i in range(self.Nedge):
            self.edge.append(self.addSwitch(str(2001+i)))
        print('Build hosts.')
        for i in range(self.Nhost):
            self.host.append(self.addHost(str(3001+i)))
    def buildLink(self):
        print('Build links between root and edge layer.')
        for i in range(self.Nedge):
            self.addLink(self.root,self.edge[i],bw=1000)
        print('Build links between edge layer and hosts.')
        for i in range(self.Nedge):
            self.addLink(self.edge[i], self.host[2*i],bw=100)
            if i == self.Nedge-1 and self.Nhost % 2 == 1: 
                continue
            self.addLink(self.edge[i], self.host[2*i+1],bw=100)

    
def pingTest(net):
    print("Start Test all network")
    net.pingAll()

def createTopo(Nhost):
    topo = Tree(int(Nhost))
    topo.buildTopo()
    topo.buildLink()
    print('Create mininet.')
    controllerIP = '127.0.0.1'
    controllerPort = 6633
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController('controller',controller=RemoteController,ip=controllerIP,port=controllerPort)
    net.start()
    dumpNodeConnections(net.hosts)
    
    # pingTest(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    if os.getuid() != 0:
        print('Permission denied.')
        exit(0)
    else:
        createTopo(sys.argv[1])
