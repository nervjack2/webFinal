
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import os 
import sys

class DataCenter(Topo):
    def __init__(self, Ncore, Nagg):
        print('Initailize the data center topo.')
        self.Ncore = Ncore 
        self.Nagg = Nagg 
        self.Nedge = Nagg
        self.Nhost = Nagg*2
        self.cores = []
        self.agg = []
        self.edge = []
        self.host = []
        Topo.__init__(self)
    def buildTopo(self):
        print('Build core layer switches.')
        for i in range(self.Ncore):
            self.cores.append(self.addSwitch(str(1001+i)))
        print('Build aggregation layer switches.')
        for i in range(self.Nagg):
            self.agg.append(self.addSwitch(str(2001+i)))
        print('Build edge layer switches.')
        for i in range(self.Nedge):
            self.edge.append(self.addSwitch(str(3001+i)))
        print('Build hosts.')
        for i in range(self.Nhost):
            self.host.append(self.addHost(str(4001+i)))
    def buildLink(self):
        print('Build links between cores and aggregation layer.')
        for i in range(0,self.Ncore,2):
            for j in range(0,self.Nagg,2):
                self.addLink(self.cores[i],self.agg[j],bw=1000)
        for i in range(1,self.Ncore,2):
            for j in range(1,self.Nagg,2):
                self.addLink(self.cores[i],self.agg[j],bw=1000)
        print('Build links between aggregation and edge layer.')
        for i in range(0,self.Nagg,2):
            self.addLink(self.agg[i],self.edge[i],bw=100)
            self.addLink(self.agg[i],self.edge[i+1],bw=100)
            self.addLink(self.agg[i+1],self.edge[i],bw=100)
            self.addLink(self.agg[i+1],self.edge[i+1],bw=100)
        print('Build links between edge layer and hosts.')
        for i in range(self.Nedge):
            self.addLink(self.edge[i],self.host[2*i])
            self.addLink(self.edge[i],self.host[2*i+1])
    
def enableSTP(Ncore, Nagg):
    for i in range(Ncore):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % (str(1001+i))
        os.system(cmd)
        print(cmd)
    for i in range(Nagg):
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % (str(2001+i))
        os.system(cmd)
        print(cmd) 
        cmd = "ovs-vsctl set Bridge %s stp_enable=true" % (str(3001+i))
        os.system(cmd)
        print(cmd) 

def pingTest(net):
    print("Start Test all network")
    net.pingAll()

def createTopo(Ncore, Nagg):
    topo = DataCenter(Ncore,Nagg)
    topo.buildTopo()
    topo.buildLink()
    print('Create mininet.')
    controllerIP = '127.0.0.1'
    controllerPort = 6633
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController('controller',controller=RemoteController,ip=controllerIP,port=controllerPort)
    net.start()
    print('Enable spanning tree protocols.')
    enableSTP(Ncore,Nagg)
    dumpNodeConnections(net.hosts)
    
    # pingTest(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    if os.getuid() != 0:
        print('Permission denied.')
        exit(0)
    else:
        createTopo(int(sys.argv[1]),int(sys.argv[2]))
