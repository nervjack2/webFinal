import sys
import getopt
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser


def getRandomDstIP(host_id, n_host):
    dst_id = randint(1,n_host)
    while dst_id == host_id:
        dst_id = randint(1,n_host) 
    ip = ".".join([str(10),str(0),str(0),str(dst_id)])
    return ip

def getRandomSrcIP():
    invalid_ip = [10,127,256,1,2,169,172,192]
    first_ip_id = randint(1,255)
    while first_ip_id in invalid_ip:
        first_ip_id = randint(1,255)
    ip = ".".join([str(first_ip_id),str(randint(1,255)),str(randint(1,255)),str(randint(1,255))])
    return ip 
    
def main(host_id, n_host):
    if host_id is  None or n_host is None:
        print('Type the following command to get some help.\npython3 flowGenerate.py -h')
        exit(0)
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    NUM_PACKET = 1500
    D_PORT = 80
    S_PORT = 2
    for i in range(NUM_PACKET):
        packets = Ether() / IP(dst=getRandomDstIP(host_id,n_host),src=getRandomSrcIP()) / UDP(dport=D_PORT, sport=S_PORT)     
        sendp(packets, iface=interface.rstrip(), inter=0.2)
        print(f'Send packet: {repr(packets)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host_id', type=int, help='host_id = xterm node id - 4000')
    parser.add_argument('--n_host', type=int, help='number of host node in the topology')
    args = parser.parse_args()
    main(**vars(args))












































