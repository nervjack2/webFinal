import sys
import getopt
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser


def getRandomIP(xterm_host_ip, num_host):
    randnum = randint(1,num_host)
    while f'10.0.0.{randnum}' == xterm_host_ip:
        randnum = randint(1,num_host)
    return f'10.0.0.{randnum}'

    
def main(xterm_host_ip, num_host):
    if xterm_host_ip is  None or num_host is None:
        print('Type the following command to get some help.\npython3 flowGenerate.py -h')
        exit(0)
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    NUM_PACKET = 1500
    D_PORT = 80
    S_PORT = 2
    for i in range(NUM_PACKET):
        packets = Ether() / IP(dst=getRandomIP(xterm_host_ip,num_host),src=getRandomIP(xterm_host_ip,num_host)) / UDP(dport=D_PORT, sport=S_PORT)     
        sendp(packets, iface=interface.rstrip(), inter=0.2)
        print(f'Send packet: {repr(packets)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--xterm_host_ip', type=str, help='Xterm host ip.')
    parser.add_argument('--num_host', type=int, help='number of host node in the topology')
    args = parser.parse_args()
    main(**vars(args))












































