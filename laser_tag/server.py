#!/usr/bin/python2.7
import os
import time
import random
import socket
import subprocess
from constants import IPSTR, BUFFER_SIZE, KEY
from multiprocessing import Process, Value, Array, Queue, Manager, Pool
#import copy_reg
#import types
#
#
#def _pickle_method(m):
#    if m.im_self is None:
#        return getattr, (m.im_class, m.im_func.func_name)
#    else:
#        return getattr, (m.im_self, m.im_func.func_name)
#
#copy_reg.pickle(types.MethodType, _pickle_method)

def overrideDict(sharedStruct, newStruct):
    old_keys = sharedStruct.keys()
    used_keys = []
    for each in newStruct:
        used_keys.append(each[KEY])
        sharedStruct[each[KEY]] = each
    for old_k in old_keys:
        if old_k not in used_keys:
            del sharedStruct[old_k]


def listener(game): 
    soc = socket.socket()   
    soc.bind(("", game.pid)) 
    soc.listen(5) 
    print("listening to ", game.pid)
    while True: 
        # establish connection with client 
        conn, addr = soc.accept() 
        # data received from client 
        data = eval(conn.recv(BUFFER_SIZE))
        # update shared structure
        game.unassigned[data[KEY]]=data
        # send recipt & close
        conn.send(str(game.sid)) 
        conn.close()
    soc.close() 


def sendMsg(player_ip, player_port, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((player_ip, player_port))
        s.send(str(data))
        s.recv(BUFFER_SIZE)
        s.close()
    except Exception as e:
        print("Could NOT send MSG to", player_ip)
        print(e)
        
        
def manager(game): 
    soc = socket.socket()   
    soc.bind(("", game.sid)) 
    soc.listen(5) 
    while True: 
        # establish connection with client 
        conn, addr = soc.accept() 
        # data received from client 
        data = eval(conn.recv(BUFFER_SIZE))

        # update shared structure
        if data[KEY] in game.assignedA.keys():
            game.assignedA[data[KEY]] = data
        elif data[KEY] in game.assignedB.keys():
            game.assignedB[data[KEY]] = data
        else:
            game.unassigned[data[KEY]] = data

        d = game.get_teams()
        msg = "start"
        d["msg"] = msg
        print(d)

        pool = Pool(processes=4)
        for team in [game.assignedA, game.assignedB, game.unassigned]:
            for k,v in team.items():
                pool.apply(sendMsg, args=(v["ip"], game.sid, d,))
        
        # send recipt & close
        conn.send("successfully updated")
        conn.close()
    soc.close() 




class Game:
    def __init__(self, pub_id):
        # Shared Structures
        self.pid = pub_id
        self.ip = subprocess.check_output(IPSTR, shell=True).decode("utf-8")[:-1]

        # Thread Variables
        self.manager = Manager()
        self.unassigned = self.manager.dict()
        self.assignedA = self.manager.dict()
        self.assignedB = self.manager.dict()
        self.running = Value("i", 0)

        # private structures
        self.proc = None
        self.sid = random.randint(0, 6553)

        
    def startListening(self):
        while not self.proc:
            self.proc = Process(target=listener, args=(self,))
        self.proc.start()

    def stopListening(self):
        while self.proc.is_alive():
            self.proc.terminate()
        self.proc = None

    def isListening(self):
        if not self.running.value and self.proc:
            return self.proc.is_alive()
        return False

    def startPlaying(self):
        while not self.proc:
            self.proc = Process(target=manager, args=(self,))
        self.proc.start()

    def stopPlaying(self):
        while self.proc.is_alive():
            self.proc.terminate()
        self.proc = None

    def isPlaying(self):
        if self.running.value and self.proc:
            return self.proc.is_alive()
        return False

    def override_teams(self, data):
        pool = Pool(processes=3)
        pool.apply(overrideDict, args=(self.assignedA, data["assignedA"],))
        pool.apply(overrideDict, args=(self.assignedB, data["assignedB"],))
        pool.apply(overrideDict, args=(self.unassigned, data["unassigned"],))
        
    def get_teams(self):
        return {"unassigned" : self.unassigned.values(), 
                "assignedA" : self.assignedA.values(), 
                "assignedB" : self.assignedB.values()}



        
# SERVER_IP = '192.168.1.26'
# SERVER_PORT = 5639

# game = Game(SERVER_PORT)

# game.startListening()
# start_time = time.time()
# while time.time() - start_time < 3:
#     print game.unassigned
# game.stopListening()
# print "stopped listening"


# game.startPlaying()
# while True:
#     # if not game.eventQ.empty():
#         # print game.unassigned
#         # d = game.eventQ.get(False)
#         # print d
    
#         # print game.unassigned
#         # call to notify all
#     game.get_teams()
    
# game.stopPlaying()







  

