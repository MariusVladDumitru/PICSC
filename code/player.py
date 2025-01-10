from typing import Literal

class Player():
    def __init__(self, IP=str(), Port=int(), Type=int(), DataPackets=[]):
        """
            Initialize a Player object
            Input:
                IP: [string] -> player IP
                Port: [int] -> player port
                Type: [int] -> player type aka Human or Bot. 0 is Human, 1 is Bot
                DataPackets: list -> a list of available data packets (outbond and inbound) extracted from pcapng files relevant to current player. Each member is a tuple (packet, 'outbound'/'inbound')
        """
        self.set_player_info(IP, Port, Type, DataPackets)

    def __check_member_types(self, IP, Port, Type, DataPackets):
        if not isinstance(IP, str) and IP != None:
            raise TypeError(f"IP needs to be a string, but got {type(IP).__name__}")

        if not isinstance(Port, int) and Port != None:
            raise TypeError(f"Port needs to be an int, but got {type(Port).__name__}")

        if Type not in [0, 1] and Type != None:
            raise TypeError(f"Type needs to be Human or Bot, but got {Type}")

        if not isinstance(DataPackets, list) and DataPackets != None:
            raise TypeError(f"DataPackets needs to be a list of packets, but got {type(DataPackets).__name__}")

    def set_player_info(self, IP, Port, Type, DataPackets):
       self.__check_member_types(IP, Port, Type, DataPackets)
       self.__IP = IP
       self.__Port = Port
       self.__Type = Type
       self.__DataPackets = DataPackets

    def get_player_info(self):
        return self.__IP, self.__Port, self.__Type, self.__DataPackets

    def set_ip(self, IP):
        if not isinstance(IP, str) and IP != None:
            raise TypeError(f"IP needs to be a string, but got {type(IP).__name__}")
        self.__IP = IP

    def get_ip(self):
        return self.__IP

    def set_port(self, Port):
        if not isinstance(Port, int) and Port != None:
            raise TypeError(f"Port needs to be an int, but got {type(Port).__name__}")
        self.__Port = Port

    def get_port(self):
        return self.__Port

    def set_type(self, Type):
        if Type not in [0, 1] and Type != None:
            raise TypeError(f"Type needs to be Human or Bot, but got {Type}")
        self.__Type = Type

    def get_type(self):
        return self.__Type

    def set_DataPackets(self, DataPackets):
        if not isinstance(DataPackets, list) and DataPackets != None:
            raise TypeError(f"DataPackets needs to be a list of packets, but got {type(DataPackets).__name__}")
        self.__DataPackets = DataPackets

    def get_DataPackets(self):
        return self.__DataPackets

    def append_data_packet(self, pkt):
        self.__DataPackets.append(pkt)