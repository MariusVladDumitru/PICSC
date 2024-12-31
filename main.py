from os import listdir
import csv


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

print(addnotations)
# This may be deleted in the future
# Positions in these lists are correlated with each other: each position is the index of the row in the csv file
# Ex: FileName[x] is correlated with GameType[x], Map[x], Player1["IP"][x], Player1["Port"][x], Player1["Bot_Difficulty"][x], Player1["Bot_Behavior"][x], Player1["Types"][x] Player2["IP"][x], Player2["Port"][x], Player2["Bot_Difficulty"][x], Player2["Bot_Behavior"][x], Player2["Types"][x], Server[x], Client[x], WhoIsMe[x]
FileName = []
GameType = []
Map = []
Player1 = {"IP": [], "Port": [], "Types": [], "Bot_Difficulty": [] , "Bot_Behavior": []}
Player2 = {"IP": [], "Port": [], "Types": [], "Bot_Difficulty": [] , "Bot_Behavior": []}
Server = []
Client = []
WhoIsMe = []
Observation = []

for idx, value in enumerate(addnotations):
    if idx == 0:
        continue
    FileName.append(value[0])
    GameType.append(value[1])
    Map.append(value[2])
    Player1["IP"].append(value[3].split(":")[0])
    Player1["Port"].append(value[3].split(":")[1])
    Player2["IP"].append(value[4].split(":")[0])
    Player2["Port"].append(value[4].split(":")[1])
    Server.append(value[5])
    Client.append(value[6])
    WhoIsMe.append(value[7])
    Player1["Types"].append(value[8].split(":")[0])
    Player2["Types"].append(value[8].split(":")[1])
    Player1["Bot_Difficulty"].append(value[9].split(":")[0])
    Player2["Bot_Difficulty"].append(value[9].split(":")[1])
    Player1["Bot_Behavior"].append(value[10].split(":")[0])
    Player2["Bot_Behavior"].append(value[10].split(":")[1])
    Observation.append(value[11])

# check if lists are correct
# for idx, value in enumerate(addnotations):
#     if idx == 0:
#         continue
#     print("CSV ROW: ", idx, "Value:", value)
#     print("Filename:", FileName[idx - 1], "GameType:", GameType[idx - 1], "Map:", Map[idx - 1], "Player1:", "IP:", Player1["IP"][idx - 1], "Port:",  Player1["Port"][idx - 1], "Types:", Player1["Types"][idx - 1], "Bot_Difficulty:", Player1["Bot_Difficulty"][idx - 1], "Bot_Behavior", Player1["Bot_Behavior"][idx - 1], "Player2:", "IP:", Player2["IP"][idx - 1], "Port:", Player2["Port"][idx - 1], "Types:", Player2["Types"][idx - 1], "Bot_Difficulty:", Player2["Bot_Difficulty"][idx - 1], "Bot_Behavior:", Player2["Bot_Behavior"][idx - 1], "Server:", Server[idx - 1], "Client:", Client[idx - 1], "WhoIsMe:", WhoIsMe[idx - 1], "Observation:", Observation[idx - 1], '\n')

from scapy.all import rdpcap
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw

packets = rdpcap(dataset_root + '/' + FileName[0])

# Iterate over packets and print a summary
# for pkt in packets:
#     print(pkt.summary())


# for pkt in packets:
#     # Check if this packet has an IP layer
#     if IP in pkt:
#         src_ip = pkt[IP].src
#         dst_ip = pkt[IP].dst
#
#         print(f"Source IP: {src_ip} --> Destination IP: {dst_ip}")

for pkt in packets:
    # Check if the packet has IP and UDP layers
    if IP in pkt and UDP in pkt:
        ip_layer = pkt[IP]
        udp_layer = pkt[UDP]

        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        src_port = udp_layer.sport
        dst_port = udp_layer.dport

        print(f"UDP Packet: {src_ip}:{src_port} --> {dst_ip}:{dst_port}")

        # If there's raw payload data, print it
        if Raw in pkt:
            raw_data = pkt[Raw].load
            print(f"Payload (Raw Data): {raw_data}")

        print("-" * 50)

    # DIN PACHETE TREBUIE SA EXTRAGI TRASATURI BOSS
    # TRE SA VEZI MAI INTAI CARE SUNT TRASATURILE SI APOI CUM LE EXTRAGI DIN TRAFIC
    # AI DE PLM AGAIN