#! /usr/bin/env python
import socket, struct, os, array
from scapy.all import ETH_P_ALL
from scapy.all import select
from scapy.all import MTU
import netifaces
from time import gmtime, strftime

class bcolors:
    LILA = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NONE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class IPSniff:
 
    def __init__(self, interface_name, on_ip_incoming, on_ip_outgoing):
 
        self.interface_name = interface_name
        self.on_ip_incoming = on_ip_incoming
        self.on_ip_outgoing = on_ip_outgoing
 
        # The raw in (listen) socket is a L2 raw socket that listens
        # for all packets going through a specific interface.
        self.ins = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.ins.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
        self.ins.bind((self.interface_name, ETH_P_ALL))
 
    def __process_ipframe(self, pkt_type, ip_header, payload):
 
        # Extract the 20 bytes IP header, ignoring the IP options
        fields = struct.unpack('!BBHHHBBHII', ip_header)
 
        dummy_hdrlen = fields[0] & 0xf
        iplen = fields[2]
 
        ip_src = payload[12:16]
        ip_dst = payload[16:20]
        ip_frame = payload[0:iplen]
 
        if pkt_type == socket.PACKET_OUTGOING:
            if self.on_ip_outgoing is not None:
                self.on_ip_outgoing(ip_src, ip_dst, ip_frame)
 
        else:
            if self.on_ip_incoming is not None:
                self.on_ip_incoming(ip_src, ip_dst, ip_frame)
 
    def recv(self):
        while True:
 
            pkt, sa_ll = self.ins.recvfrom(MTU)
 
            if type == socket.PACKET_OUTGOING and self.on_ip_outgoing is None:
                continue
            elif self.on_ip_outgoing is None:
                continue
 
            if len(pkt) <= 0:
                break
 
            eth_header = struct.unpack('!6s6sH', pkt[0:14])
 
            dummy_eth_protocol = socket.ntohs(eth_header[2])
 
            if eth_header[2] != 0x800 :
                continue
 
            ip_header = pkt[14:34]
            payload = pkt[14:]
 
            self.__process_ipframe(sa_ll[2], ip_header, payload)

def sniff():
    ip_sniff = IPSniff(net, test_incoming_callback, test_outgoing_callback)
    ip_sniff.recv()
    
print('\033c')
NetIfaces = netifaces.interfaces()
Ifces = '  '.join([str(x) for x in NetIfaces] )
net = raw_input('Enter your network interface (you can choose from: ' + bcolors.YELLOW + Ifces + bcolors.NONE +'):\n   ')
        
test = 0
while test != None:
    print('\033c')
    test = str(raw_input('Choose traffic: 1) Incomming\t2) Outgoing\t3) Both:\n   '))
    if test == str(3):
        print('\033c')
        def test_incoming_callback(src, dst, frame):
            time = strftime("%d.%m %Y %H:%M:%S", gmtime())
            print('[' + bcolors.RED +' IN  ' + bcolors.NONE + ']\t'+time+'  src=%s\t     dst=%s\tframe len = %d'
            %(socket.inet_ntoa(src), socket.inet_ntoa(dst), len(frame)))
        def test_outgoing_callback(src, dst, frame):
            time = strftime("%d.%m %Y %H:%M:%S", gmtime())
            print('[' + bcolors.YELLOW +' OUT ' + bcolors.NONE + ']\t'+time+'  src=%s\t     dst=%s\tframe len = %d'
            %(socket.inet_ntoa(src), socket.inet_ntoa(dst), len(frame)))
        test = None
        sniff()
        
    if test == str(2):
        print('\033c')
        def test_incoming_callback(src, dst, frame):
            test = None
        def test_outgoing_callback(src, dst, frame):
            time = strftime("%d.%m %Y %H:%M:%S", gmtime())
            print('[' + bcolors.YELLOW +' OUT ' + bcolors.NONE + ']\t'+time+'  src=%s\t     dst=%s\t   frame len = %d'
            %(socket.inet_ntoa(src), socket.inet_ntoa(dst), len(frame)))
        sniff()
        
    if test == str(1):
        print('\033c')
        def test_incoming_callback(src, dst, frame):
            time = strftime("%d.%m %Y %H:%M:%S", gmtime())
            print('[' + bcolors.RED +' IN  ' + bcolors.NONE + ']\t'+time+'  src=%s\t     dst=%s\t   frame len = %d'
            %(socket.inet_ntoa(src), socket.inet_ntoa(dst), len(frame)))
        def test_outgoing_callback(src, dst, frame):
            test = None
        sniff()
