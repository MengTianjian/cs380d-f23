import argparse
import xmlrpc.client
import xmlrpc.server

serverId = 0
basePort = 9000


class KVSRPCServer(xmlrpc.server.SimpleXMLRPCServer):
    data = dict()

    ## put: Insert a new-key-value pair or updates an existing
    ## one with new one if the same key already exists.
    def put(self, key, value):
        if key not in list(self.data) or value[1] > self.data[key][1]:
            self.data[key] = value
        return "Success"

    ## get: Get the value associated with the given key.
    def get(self, key):
        if key not in list(self.data):
            return "ERR_KEY"
        return "{}:{}".format(key, self.data[key][0])

    ## printKVPairs: Print all the key-value pairs at this server.
    def printKVPairs(self):
        result = []
        for k in list(self.data):
            result.append("{}:{}".format(k, self.data[k][0]))
        return "\n".join(result)

    ## shutdownServer: Terminate the server itself normally.
    def shutdownServer(self):
        return self.shutdown()

    ## isAlive: Ping the server and return true if it's alive.
    def isAlive(self):
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '''To be added.''')

    parser.add_argument('-i', '--id', nargs=1, type=int, metavar='I',
                        help='Server id (required)', dest='serverId', required=True)

    args = parser.parse_args()

    serverId = args.serverId[0]

    server = KVSRPCServer(("localhost", basePort + serverId))
    # server = xmlrpc.server.SimpleXMLRPCServer(("localhost", basePort + serverId))
    # server.register_instance(KVSRPCServer())

    server.serve_forever()
