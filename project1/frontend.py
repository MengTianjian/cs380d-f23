import http
import random
import time
from threading import Lock

import xmlrpc.client
import xmlrpc.server
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

kvsServers = dict()
baseAddr = "http://localhost:"
baseServerPort = 9000

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

class FrontendRPCServer:
    # TODO: You need to implement details for these functions.

    ## put: This function routes requests from clients to proper
    ## servers that are responsible for inserting a new key-value
    ## pair or updating an existing one.
    def put(self, key, value):
        t = time.time()
        deadServerList = []
        for serverId in list(kvsServers):
            while True:
                try:
                    kvsServers[serverId].put(key, (value, t))
                    break
                except ConnectionRefusedError:
                    deadServerList.append(serverId)
                    break
                except:
                    continue
                # except http.client.HTTPException:
                #     continue
                # else:
                #     deadServerList.append(serverId)
                #     break
        for serverId in deadServerList:
            kvsServers.pop(serverId)
        return "Success"

    ## get: This function routes requests from clients to proper
    ## servers that are responsible for getting the value
    ## associated with the given key.
    def get(self, key):
        while len(kvsServers) > 0:
            serverId = list(kvsServers)[random.randint(0, len(kvsServers) - 1)]
            try:
                return kvsServers[serverId].get(key)
            except ConnectionRefusedError:
                kvsServers.pop(serverId)
                continue
            except:
                continue
        return "ERR_NOSERVERS"

    ## printKVPairs: This function routes requests to servers
    ## matched with the given serverIds.
    def printKVPairs(self, serverId):
        return kvsServers[serverId].printKVPairs()

    ## addServer: This function registers a new server with the
    ## serverId to the cluster membership.
    def addServer(self, serverId):
        if len(kvsServers) == 0:
            kvsServers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
            return "Success"
        kv_pairs = kvsServers[list(kvsServers)[random.randint(0, len(kvsServers) - 1)]].printKVPairs()
        kvsServers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
        if kv_pairs:
            kv_pairs = kv_pairs.split("\n")
            for kv_pair in kv_pairs:
                k, v = kv_pair.split(":")
                kvsServers[serverId].put(int(k), (int(v), 0))
        return "Success"

    ## listServer: This function prints out a list of servers that
    ## are currently active/alive inside the cluster.
    def listServer(self):
        serverList = []
        deadServerList = []
        for serverId in list(kvsServers):
            try:
                if kvsServers[serverId].isAlive():
                    serverList.append(serverId)
            except:
                deadServerList.append(serverId)
        for serverId in deadServerList:
            kvsServers.pop(serverId)
        if not serverList:
            return "ERR_NOSERVERS"
        return ", ".join([str(serverId) for serverId in sorted(serverList)])

    ## shutdownServer: This function routes the shutdown request to
    ## a server matched with the specified serverId to let the corresponding
    ## server terminate normally.
    def shutdownServer(self, serverId):
        result = kvsServers[serverId].shutdownServer()
        kvsServers.pop(serverId)
        return result

server = SimpleThreadedXMLRPCServer(("localhost", 8001))
server.register_instance(FrontendRPCServer())

server.serve_forever()
