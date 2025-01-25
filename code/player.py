
class Player():
    """
        Class that describes a player.
        BIG NOTE: For all setter methods, i do not perform checks on the input data. This is to speed up the execution of the project.
        MAKE SURE, BEFORE USING ANY SETTER METHOD, that ALL DATA HAVE THE CORRECT TYPE AND STRUCTURE.
    """
    def __init__(self, IP=str(), Port=int(), Type=int(), DataPackets=[]):
        """
            Private Methond.
            Constructor.
            Initialize a Player object.
            Input:
                IP: [string] -> player IP.
                Port: [int] -> player port.
                Type: [int] -> player type aka Human or Bot. 0 is Human, 1 is Bot.
                DataPackets: [list] -> a list of tuples representing the current player data packets (outbond and inbound) extracted from pcapng files.
                                       Each member of the list is a tuple of format (packet, 'outbound'/'inbound'), represents a single packet with it's direction('inbound packet' or 'outbound packet'):
                                                outbound: [string] -> current player sends the packet.
                                                inbound: [string] -> current player receives the packet.
                                                packet: [bytes] -> a stream of bytes representing the current packet UDP payload data (data of interest). This data is encoded and needs to be decoded later.

        """

        self.set_player_info(IP, Port, Type, DataPackets)

    def set_player_info(self, IP, Port, Type, DataPackets):
        """
            Public Method.
            Set player data to input parameters.
            Make sure all input parameters have correct types and structures.

            Input:
                IP: [string] -> player IP.
                Port: [int] -> player port.
                Type: [int] -> player type aka Human or Bot. 0 is Human, 1 is Bot.
                DataPackets: [list] -> Check description in class constructor(line 17)

            Output: None.

        """

        self.__IP = IP
        self.__Port = Port
        self.__Type = Type
        self.__DataPackets = DataPackets

    def get_player_info(self):
        """
        Public Method.
        Get Player Data.

        Input: None.

        Output:
                IP: [string] -> player IP.
                Port: [int] -> player port.
                Type: [int] -> player type aka Human or Bot. 0 is Human, 1 is Bot.
                DataPackets: [list] -> Check description in class constructor(line 17)
        """

        return self.__IP, self.__Port, self.__Type, self.__DataPackets

    def set_ip(self, IP):
        """
            Public Method.
            Set Player IP to input parameter.
            Make sure IP has correct type.

            Input:
                IP: [int] -> player IP.

            Output: None.
        """

        self.__IP = IP

    def get_ip(self):
        """
        Public Method.
        Get Player IP.

        Input: None

        Output:
            IP: [int] -> player ip.
        """

        return self.__IP

    def set_port(self, Port):
        """
            Public Method.
            Set Player port to input parameter.
            Make sure Port has correct type.

            Input:
                Port: [int] -> player port.

            Output: None.
        """

        self.__Port = Port

    def get_port(self):
        """
            Public Method.
            Get Player Port.

            Input: None.

            Output:
               self.__Port: [int] -> Player Port.
        """

        return self.__Port

    def set_type(self, Type):
        """
            Public Method.
            Make sure Type has the correct data type.
            Set Player Type to input parameter. 0 is Human. 1 is Bot.

            Input:
                Type: [int] -> player type. 0 is Human. 1 is Bot.

            Output: None.
        """

        self.__Type = Type

    def get_type(self):
        """
        Public Method.
        Get Player Type. 0 is Human. 1 is Bot.

        Input: None.

        Output:
            self.__Type: [int] -> player type. 0 is Human. 1 is Bot.
        """

        return self.__Type

    def set_DataPackets(self, DataPackets):
        """
            Public Method.
            Set Player DataPackets to input parameter. Make sure DataPackets has the correct structure.

            Input:
                DataPackets: [list] -> check description in class constructor (line 17)

               Output: None.
        """

        self.__DataPackets = DataPackets

    def get_DataPackets(self):
        """
            Public Method.
            Get DataPackets.

            Input: None

            Output:
                DataPackets: [list] -> check description in class constructor (line 17)
        """
        return self.__DataPackets

    def append_data_packet(self, pkt):
        """
        Public Methods
        Appends new data to self.__DataPackets

        Input:
            pkt: (bytes, 'inbound'/ 'outboud') -> see DataPackets description in class constructor (line 17)
        """
        self.__DataPackets.append(pkt)