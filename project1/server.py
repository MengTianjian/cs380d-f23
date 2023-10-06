import argparse
import xmlrpc.client
import xmlrpc.server

serverId = 0
basePort = 9000

class KVSRPCServer:
    # TODO: You need to implement details for these functions.
    data = dict()

    ## put: Insert a new-key-value pair or updates an existing
    ## one with new one if the same key already exists.
    def put(self, key, value):
        if key not in self.data or value[1] > self.data[key][1]:
            self.data[key] = value
        return "Success"
        # return "[Server " + str(serverId) + "] Receive a put request: " + "Key = " + str(key) + ", Val = " + str(value)

    ## get: Get the value associated with the given key.
    def get(self, key):
        if key not in self.data:
            return "ERR_KEY"
        return self.data[key][0]
        # return "[Server " + str(serverId) + "] Receive a get request: " + "Key = " + str(key)

    ## printKVPairs: Print all the key-value pairs at this server.
    def printKVPairs(self):
        result = []
        for k, v in self.data.items():
            result.append('{}:{}'.format(k, v[0]))
        return '\n'.join(result)
        # return "[Server " + str(serverId) + "] Receive a request printing all KV pairs stored in this server"

    ## shutdownServer: Terminate the server itself normally.
    def shutdownServer(self):
        return "[Server " + str(serverId) + "] Receive a request for a normal shutdown"

    def isAlive(self):
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '''To be added.''')

    parser.add_argument('-i', '--id', nargs=1, type=int, metavar='I',
                        help='Server id (required)', dest='serverId', required=True)

    args = parser.parse_args()

    serverId = args.serverId[0]

    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", basePort + serverId))
    server.register_instance(KVSRPCServer())

    server.serve_forever()
