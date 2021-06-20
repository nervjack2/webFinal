import sys
import getopt
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser

invalid_ip = [10, 127, 254, 1, 2, 169, 172, 192]

def getDstRandomIP(xterm_host_ip, num_host):
    randnum = randint(1,num_host)
    while f'10.0.0.{randnum}' == xterm_host_ip:
        randnum = randint(1,num_host)
    return '.'.join(['10','0','0',str(randnum)])

def getSrcRandomIP():
    first_ip = randint(1, 255)
    while first_ip in invalid_ip:
        first_ip = randint(1, 255)  
    src_ip = '.'.join([str(first_ip), str(randint(1,255)), str(randint(1,255)), str(randint(1,255))])
    return src_ip

def main(xterm_host_ip, num_host):
    if xterm_host_ip is  None or num_host is None:
        print('Type the following command to get some help.\npython3 flowGenerate.py -h')
        exit(0)
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    NUM = 50
    D_PORT = 80
    S_PORT = 2
    user=30
    dst=[]
    src=[]
    for i in range(user):
        dst_ip = getDstRandomIP(xterm_host_ip, num_host)
        src_ip = getSrcRandomIP()
        dst.append(dst_ip)
        src.append(src_ip)
    for i in range(NUM):
        for j in range(user):
            dst_ip = dst[j]
            src_ip = src[j]
            for p in range(randint(5, 15)):
                packets = Ether() / IP(dst=dst_ip,src=src_ip) / UDP(dport=D_PORT, sport=S_PORT)     
                sendp(packets, iface=interface.rstrip(), inter=0.01)
                print(f'Send packet: {repr(packets)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--xterm_host_ip', type=str, help='Xterm host ip.')
    parser.add_argument('--num_host', type=int, help='number of host node in the topology')
    args = parser.parse_args()
    main(**vars(args))












































