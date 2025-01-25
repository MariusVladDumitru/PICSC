from scapy.layers.inet import IP, UDP
from scapy.packet import Raw
from scapy.all import PcapReader
from os import listdir
import csv
from player import Player

def running_in_colab():
    """
    Checks if the script calling this function runs in Google Colab or not.
    I am using Google Colab for testing to speed up the development process, and i need to know if a script is running in there or not.

    Input: None

    Output: None
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False


def get_annotations():
    """
    Read data from addnotations.csv and return it as a list.
    Addnotations.csv fields are self - explanatory.

    Input None

    Output: [list] ->tt Data from addnontations.csv
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
    """
    Aggregates player data. Combines player info from Annotations.cvs(ip, port, type) with packets extracted from .pcapngfile.
    A player can have outbound(send packets) and inbound(receive packets) and are marked accordingly.
    Processes only one .pcapng file(provided as a parameter).
    For multiple .pcapng files, call this function for each of them.

    Input:
        capture file: [string] -> name of capture file

    Output:
        Player1, Player2: [Player] -> Player() type objects. Player1 represents data for Player1, Player2 represents data for Player2.
    """
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
                    udp_packet_data = pkt[Raw].load  # Has the ENet Header + 0.AD payload data - bytes class. These are the raw bytes after UDP header.
                    Player1.append_data_packet((udp_packet_data, 'outbound'))
                # Player1 receives the packet - inbound packet
                elif dst_port == Player1.get_port() and dst_ip == Player1.get_ip():
                    udp_packet_data = pkt[Raw].load  # Has the ENet Header + 0.AD payload data - bytes class. These are the raw bytes after UDP header.
                    Player1.append_data_packet((udp_packet_data, 'inbound'))

                # Player2 sends the packet - outbound packet
                if src_port == Player2.get_port() and src_ip == Player2.get_ip():
                    udp_packet_data = pkt[Raw].load  # Has the ENet Header + 0.AD payload data - bytes class. These are the raw bytes after UDP header.
                    Player2.append_data_packet((udp_packet_data, 'outbound'))
                # Player2 receives the packet - inbound packet
                elif dst_port == Player2.get_port() and dst_ip == Player2.get_ip():
                    udp_packet_data = pkt[Raw].load  # Has the ENet Header + 0.AD payload data - bytes class. These are the raw bytes after UDP header.
                    Player2.append_data_packet((udp_packet_data, 'inbound'))

            # packet does not have IP or UPD or Raw layers
            else:
                continue
    return Player1, Player2

if __name__ == "main":
    pass
