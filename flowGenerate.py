import sys
import getopt
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser


def getDstRandomIP(xterm_host_ip, num_host):
    randnum = randint(1,num_host)
    while f'10.0.0.{randnum}' == xterm_host_ip:
        randnum = randint(1,num_host)
    return f'10.0.0.{randnum}'

def getSrcRandomIP(xterm_host_ip):
    invalid_ip = [10, 127, 256, 1, 2, 169, 172, 192]
    first_ip = randint(1, 256)
    while first_ip in invalid_ip:
        first_ip = randint(1, 256) 
    src_ip = '.'.join([str(first_ip), str(randint(1,256)), str(randint(1,256)), str(randint(1,256))])
    return src_ip

def main(xterm_host_ip, num_host):
    if xterm_host_ip is  None or num_host is None:
        print('Type the following command to get some help.\npython3 flowGenerate.py -h')
        exit(0)
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    NUM_PACKET = 1500
    D_PORT = 80
    S_PORT = 2
    for i in range(NUM_PACKET):
        dst_ip = getDstRandomIP(xterm_host_ip, num_host)
        src_ip = getSrcRandomIP(xterm_host_ip)
        packets = Ether() / IP(dst=dst_ip,src=src_ip) / UDP(dport=D_PORT, sport=S_PORT)     
        sendp(packets, iface=interface.rstrip(), inter=0.2)
        print(f'Send packet: {repr(packets)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--xterm_host_ip', type=str, help='Xterm host ip.')
    parser.add_argument('--num_host', type=int, help='number of host node in the topology')
    args = parser.parse_args()
    main(**vars(args))












































