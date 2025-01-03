from os import listdir
from scapy.all import rdpcap
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw
from scapy.all import PcapReader
import sys
import csv
import random

def get_addnotations():
    """
    Input None
    Output: Data from addnontations.csv as a list
    Get Addnotation data from addnotations.csv
    """
    dataset_root = 'dataset'
    filenames = listdir(dataset_root)
    csv_file = None
    for filename in filenames:
        if 'csv' in filename:
            csv_file = filename
            break
    addnotations = []
    with open (dataset_root + '/' + csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            addnotations.append(row)

    return addnotations

def parse_capture_file(capture_file):
    addnotations = get_addnotations()

    # find capture_file. Assuming that a valid capture file is always provided
    for idx, data in enumerate(addnotations):
        if idx == 0:
            continue
        if capture_file == data[0]: # found the needed capture file
            capture_file_data = data
            break

    Player1 = {"IP": "", "Port": "", "Type": int()}
    Player2 = {"IP": "", "Port": "", "Type": int()}
    Player1["IP"] = capture_file_data[3].split(":")[0]
    Player1["Port"] = int(capture_file_data[3].split(":")[1])
    Player2["IP"] = capture_file_data[4].split(":")[0]
    Player2["Port"] = int(capture_file_data[4].split(":")[1])

    # class Human is encoded as class 0
    # class Bot is encoded as class 1
    Player1["Type"] = 0 if capture_file_data[8].split(":")[0] == "Human" else 1
    Player2["Type"] = 0 if capture_file_data[8].split(":")[1] == "Human" else 1

    # valid ip's and ports
    valid_ips = [Player1["IP"], Player2["IP"]]
    valid_ports = [Player1["Port"], Player2["Port"]]

    # # network stuff
    with PcapReader('dataset' + '/' + capture_file) as pcap_reader:
        for pkt in pcap_reader:
            if IP in pkt and UDP in pkt:
                ip_layer = pkt[IP]
                udp_layer = pkt[UDP]
                src_ip = ip_layer.src
                src_port = udp_layer.sport
                dst_ip = ip_layer.dst
                dst_port = udp_layer.dport

                if src_port not in valid_ports or dst_port not in valid_ports:
                    continue
                if src_ip not in valid_ips or dst_ip not in valid_ips:
                    continue

                # The packet has a valid port and a valid ip
                if Raw in pkt:
                    udp_packet_data = pkt[Raw].load # Has the ENet Header + 0.AD payload data
                    udp_packet_bytes = len(udp_packet_data)
                    for idx in range(0, udp_packet_bytes):
                        print(udp_packet_data[idx], end='   ')
                    print("END_PACKET")


# get filelist of capture directory
dataset_root = 'dataset'
capture_files = listdir(dataset_root)
for filename in capture_files:
    if '.pcapng' not in filename:
        capture_files.remove(filename)

# parse capture files
for capture_file in capture_files:
    parse_capture_file(capture_file)
    # aici faci vectorul mare de trasaturi care va fi trimis catre model. la vectoru asta contribuie fiecare capture file


# X - matricea ce contine datele
# Y - matricea ce contine addnotarile (label-urile) - clasele
# OUT - matricea ce contine ceea ce a prezis modelul
#X_train, Y_train - pentru antrenare
# X_val, Y_val - pentru validare
# OUT_train OUT_val - ceea ce a prezis modelul boss, pentru antrenare si validare


# dataset = capture_files
# random.seed()
# random.shuffle(dataset)

# 80 / 20 dataset split
# train_idx = round(len(dataset) * 0.8)
# dataset_train = dataset[0:train_idx]
# dataset_val = dataset[train_idx:]

# DIN PACHETE TREBUIE SA EXTRAGI TRASATURI BOSS
# TRE SA VEZI MAI INTAI CARE SUNT TRASATURILE SI APOI CUM LE EXTRAGI DIN TRAFIC
# AI DE PLM AGAIN