from scapy.layers.inet import IP, UDP
from scapy.packet import Raw
from scapy.all import PcapReader
from os import listdir
import csv
from player import Player

def running_in_colab():
    """
    Check if i am running in google colab or not

   I need google colab in order to speed things up
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False


def get_annotations():
    """
    Input None
    Output: Data from addnontations.csv as a list
    Get Addnotation data from addnotations.csv
    """

    if running_in_colab():
        dataset_root ='/content/drive/MyDrive/Datasets/PICSC'
    else:
        dataset_root = '../dataset'
    filenames = listdir(dataset_root)
    csv_file = None
    for filename in filenames:
        if 'csv' in filename:
            csv_file = filename
            break
    annotations = []
    with open (dataset_root + '/' + csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            annotations.append(row)
    annotations = annotations[1:] # Eliminate Annotations Header
    return annotations

def parse_capture_file(capture_file):
    # get dataset annotations
    annotations = get_annotations()
    # find capture_file in addontations data. Assuming that a valid capture file is always provided
    capture_file_data = None
    for value in annotations:
        if capture_file == value[0]:  # found the needed capture file
            capture_file_data = value
            break
    Player1 = Player()
    Player2 = Player()

    # Player1 is index3 in annotations
    # Player2 is index4 in annotations
    Player1.set_ip(capture_file_data[3].split(":")[0])
    Player1.set_port(int(capture_file_data[3].split(":")[1]))
    Player2.set_ip(capture_file_data[4].split(":")[0])
    Player2.set_port(int(capture_file_data[4].split(":")[1]))

    # class Human is encoded as class 0
    # class Bot is encoded as class 1
    Player1.set_type(0 if capture_file_data[3].split(":")[2] == "Human" else 1)
    Player2.set_type(0 if capture_file_data[4].split(":")[2] == "Human" else 1)

    valid_ips = [Player1.get_ip(), Player2.get_ip()]
    valid_ports = [Player1.get_port(), Player2.get_port()]
    # go through the list of packets for the current .pcapng file
    # Read all the packets in .pcapng file an put them in a list - This might speed things up
    if running_in_colab():
        dataset_root = '/content/drive/MyDrive/Datasets/PICSC'
    else:
        dataset_root = '../dataset'
    with PcapReader(dataset_root + '/' + capture_file) as pcap_reader:  # read a packet from the .pcapng
        for pkt in pcap_reader:
           # packet needs to have IP, UDP and Raw Layers or else discard the packet
            if IP in pkt and UDP in pkt and Raw in pkt: # checking this here, no need to check this in other places
                # ip_layer
                ip_layer = pkt[IP]

                # udp_layer
                udp_layer = pkt[UDP]

                # source ip and source port
                src_ip = ip_layer.src
                src_port = udp_layer.sport

                # destination ip and destination port
                dst_ip = ip_layer.dst
                dst_port = udp_layer.dport

                # if packet does not have relevant ip's and ports for current file capture, move forward
                if src_port not in valid_ports or dst_port not in valid_ports:  # source or destination port not valid
                    continue
                if src_ip not in valid_ips or dst_ip not in valid_ips:  # source or destination ip not valid
                    continue

                # Player1 sends the packet - outbound packet
                if src_port == Player1.get_port() and src_ip == Player1.get_ip():
                    Player1.append_data_packet((pkt, 'outbound'))
                # Player1 receives the packet - inbound packet
                elif dst_port == Player1.get_port() and dst_ip == Player1.get_ip():
                    Player1.append_data_packet((pkt, 'inbound'))

                # Player2 sends the packet - outbound packet
                if src_port == Player2.get_port() and src_ip == Player2.get_ip():
                    Player2.append_data_packet((pkt, 'outbound'))
                # Player2 receives the packet - inbound packet
                elif dst_port == Player2.get_port() and dst_ip == Player2.get_ip():
                    Player2.append_data_packet((pkt, 'inbound'))
            # packet does not have IP or UPD or Raw layers
            else:
                continue
    return Player1, Player2



# def OLD_parse_capture_file(capture_file, player):
#     """
#     Input:
#         capture_file: string -> name of capture file
#         player: string -> player to aggregate data for. Can have values P1, P2, P1+P1
#
#     Output: 2 dictionaries dat aggregates Player1 and Player2 data.
#
#     Aggregates either one player or both players information into to dictionaries with the fields:
#     IP -> string: player IP
#     Port -> int: player port
#     Type -> int: 0 - player is human
#                  1 - player is bot
#     Data -> list: each member is a series of bytes, associated with player, extracted from pcapng file's UDP traffic payload. This is the relevant data where features will be extracted from.
#
#     Call this function with:
#     P1, P2 = dp.parse_capture_file(capture_file, "P1+P2") -> player1 and player2
#     P1 = dp.parse_capture_file(capture_file, "P1") -> only player1
#     P2 = dp.parse_capture_file(capture_file, "P2") -> only player2
#
#     """
#     if player not in ["P1", "P2", "P1+P2"]:
#         raise TypeError(f"player argument is: {player} . Correct values are P1, P2, P1+P2")
#
#     # get dataset annotations
#     annotations = get_annotations()
#
#     # find capture_file in addontations data. Assuming that a valid capture file is always provided
#     capture_file_data = None
#     for value in annotations:
#         if capture_file == value[0]: # found the needed capture file
#             capture_file_data = value
#             break
#
#     match player:
#         case "P1+P2":
#             # The Data files from Player1 and Player2 contains the udp payload bytes extracted from relevant packets, WHEN THE SOURCE IS EITHER PLAYER1 or PLAYER2
#             # The source is important because that is the one who generates the relevant data for the model(human or bot)
#             # The destination is the one that received the payload, it does not generate it.
#             Player1 = {"IP": "", "Port": int(), "Type": int(), "Data":[]} # Data contains the bytes extracted from packets when player1 is the source
#             Player2 = {"IP": "", "Port": int(), "Type": int(), "Data":[]}# Data containts the bytes extracted from packets when player2 is the source
#             Player1["IP"] = capture_file_data[3].split(":")[0] # Player1 is index3 in addnotations
#             Player1["Port"] = int(capture_file_data[3].split(":")[1]) # Player2 is index 4 in addnotations
#             Player2["IP"] = capture_file_data[4].split(":")[0]
#             Player2["Port"] = int(capture_file_data[4].split(":")[1])
#
#             # class Human is encoded as class 0
#             # class Bot is encoded as class 1
#             Player1["Type"] = 0 if capture_file_data[3].split(":")[2] == "Human" else 1 # Player1 is index3 in addnotations
#             Player2["Type"] = 0 if capture_file_data[4].split(":")[2] == "Human" else 1 # Player2 is index 4 in addnotations
#
#             # valid ip's and ports for current file capture.
#             valid_ips = [Player1["IP"], Player2["IP"]]
#             valid_ports = [Player1["Port"], Player2["Port"]]
#
#         case "P1":
#             Player1 = {"IP": "", "Port": int(), "Type": int(), "Data": []}
#             Player1["IP"] = capture_file_data[3].split(":")[0]
#             Player1["Port"] = int(capture_file_data[3].split(":")[1])
#             Player1["Type"] = 0 if capture_file_data[3].split(":")[2] == "Human" else 1
#             valid_ips = [Player1["IP"]]
#             valid_ports = [Player1["Port"]]
#
#         case "P2":
#             Player2 = {"IP": "", "Port": int(), "Type": int(), "Data": []}
#             Player2["IP"] = capture_file_data[4].split(":")[0]
#             Player2["Port"] = int(capture_file_data[4].split(":")[1])
#             Player2["Type"] = 0 if capture_file_data[4].split(":")[2] == "Human" else 1
#             valid_ips = [Player2["IP"]]
#             valid_ports = [Player2["Port"]]
#
#     # network stuff
#     if running_in_colab():
#         dataset_root = '/content/drive/MyDrive/Datasets/PICSC'
#     else:
#         dataset_root = '../dataset'
#     with PcapReader(dataset_root + '/' + capture_file) as pcap_reader: # read a packet from the .pcapng
#         for pkt in pcap_reader:
#             # Does packet have IP and UDP layers ?
#             if IP in pkt and UDP in pkt:
#                 # ip_layers
#                 ip_layer = pkt[IP]
#
#                 # udp_layer
#                 udp_layer = pkt[UDP]
#
#                 # source ip and source port
#                 src_ip = ip_layer.src
#                 src_port = udp_layer.sport
#
#                 # destination ip and destination port
#                 dst_ip = ip_layer.dst
#                 dst_port = udp_layer.dport
#
#                 match player:
#                     case "P1+P2":
#                         # if packet does not have relevant ip's and ports for current file capture, move forward
#                         if src_port not in valid_ports or dst_port not in valid_ports: # source or destination port not valid
#                             continue
#                         if src_ip not in valid_ips or dst_ip not in valid_ips: # source or destination ip not valid
#                             continue
#
#                     case _:
#                         # for only one player P1 or P2, his ports and ip's need to be the source only(the source is the one generating relevant info), don't care about the destination.
#                         # this also predetermines that P1/P2 is the generator(source ip and port)
#                         if src_port not in valid_ports:
#                             continue
#                         if src_ip not in valid_ips:
#                             continue
#
#                 # # The packet has a valid port and a valid ip
#                 if Raw in pkt:
#                     udp_packet_data = pkt[Raw].load # Has the ENet Header + 0.AD payload data - bytes class. These are the raw bytes after UDP header.
#                     # udp_packet_data_len = len(udp_packet_data) ->  the number of bytes Enet Header + 0AD Data has. Just use len(PlayerX["Data]["i]) to get the number of bytes, no need to make a separate dict field for this.
#                     match player:
#                         case "P1+P2":
#                             # append packet payload to Player1
#                             if src_ip == Player1["IP"] and src_port == Player1["Port"]:
#                                 Player1["Data"].append(udp_packet_data)
#
#                             # append packet payload to Player2
#                             if src_ip == Player2["IP"] and src_port == Player2["Port"]:
#                                 Player2["Data"].append(udp_packet_data)
#
#                         case "P1":
#                             if src_ip == Player1["IP"] and src_port == Player1["Port"]:
#                                 Player1["Data"].append(udp_packet_data)
#
#                         case "P2":
#                             if src_ip == Player2["IP"] and src_port == Player2["Port"]:
#                                 Player2["Data"].append(udp_packet_data)
#
#                 else:
#                     # packet has no raw data, move on
#                     continue
#             else:
#                 # packet does not have IP and UDP layers, move on
#                 continue
#
#     match player:
#         case "P1+P2":
#             return Player1, Player2
#
#         case "P1":
#             return Player1
#
#         case "P2":
#             return Player2

if __name__ == "main":
    pass