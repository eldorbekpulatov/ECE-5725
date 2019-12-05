#!/usr/bin/env python
import os
import time
import random
import socket
import subprocess
from constants import BUFFER_SIZE, KEY
from multiprocessing import Process, Value, Array, Queue, Manager, Pool


def counter(sharedStruct):
    count = 0
    for k,v in sharedStruct.items():
        if v["isAlive"]: count+=1
    return count
    

def overrideDict(sharedStruct, newStruct):
    old_keys = sharedStruct.keys()
    used_keys = []
    for each in newStruct:
        used_keys.append(each[KEY])
        sharedStruct[each[KEY]] = each
    for old_k in old_keys:
        if old_k not in used_keys:
            del sharedStruct[old_k]


def sendMsg(player_ip, player_port, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((player_ip, player_port))
        s.send(str(data).encode())
        s.recv(BUFFER_SIZE)
        s.close()
    except Exception as e:
        print("Could NOT send MSG to", player_ip)
        print(e)


def listener(game): 
    soc = socket.socket()   
    soc.bind(("", game.pid)) 
    soc.listen(1) 
    while True: 
        # establish connection with client 
        conn, addr = soc.accept() 
        # data received from client 
        data = eval(conn.recv(BUFFER_SIZE).decode("UTF-8"))
        # update shared structure
        game.unassigned[data[KEY]]=data
        # send recipt & close
        conn.send(str(game.sid).encode()) 
        conn.close()
    soc.close() 
    
        
def manager(game): 
    soc = socket.socket()   
    soc.bind(("", game.sid)) 
    soc.listen(1) 
    while True: 
        # establish connection with client 
        conn, addr = soc.accept() 
        # data received from client 
        data = eval(conn.recv(BUFFER_SIZE).decode("UTF-8"))
        # update shared structure
        if data[KEY] in game.assignedA.keys():
            game.assignedA[data[KEY]] = data
        elif data[KEY] in game.assignedB.keys():
            game.assignedB[data[KEY]] = data
        else:
            game.unassigned[data[KEY]] = data

        game.notifyAll("update") # TODO
        
        # send recipt & close
        conn.send("successfully updated")
        conn.close()
    soc.close() 


class Game:
    def __init__(self, pub_id):
        # Shared Structures
        self.pid = pub_id
        self.ip = socket.gethostname()
        self.sid = random.randint(1000, 6553)
        self.proc = None

        # Thread Variables
        self.manager = Manager()
        self.unassigned = self.manager.dict()
        self.assignedA = self.manager.dict()
        self.assignedB = self.manager.dict()
        self.running = Value("i", 0)
   
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

    def notifyTeams(self, messege):
        d = self.get_teams()
        d["msg"] = messege
        pool = Pool(processes=4)
        for team in [self.assignedA, self.assignedB]:
            for k,v in team.items():
                pool.apply(sendMsg, args=(v["ip"], self.sid, d,))
        pool.close()
        pool.join()

    def notifyExtras(self, messege):
        d = self.get_teams()
        d["msg"] = messege
        pool = Pool(processes=4)
        for k,v in self.unassigned.items():
            pool.apply(sendMsg, args=(v["ip"], self.sid, d,))
        pool.close()
        pool.join()
    
    def notifyAll(self, messege):
        d = self.get_teams()
        d["msg"] = messege
        pool = Pool(processes=4)
        for team in [self.assignedA, self.assignedB, self.unassigned]:
            for k,v in team.items():
                pool.apply(sendMsg, args=(v["ip"], self.sid, d,))
        pool.close()
        pool.join()

    def whoWon(self):
        pool = Pool(processes=4)
        teams = [self.assignedA, self.assignedB]
        counts = pool.map(counter, teams)
        pool.close()
        pool.join()
        if counts[0] > counts[1]: return 1
        elif counts[1] > counts[0]: return 2
        else: return 0

    def override_teams(self, data):
        pool = Pool(processes=3)
        pool.apply(overrideDict, args=(self.assignedA, data["assignedA"],))
        pool.apply(overrideDict, args=(self.assignedB, data["assignedB"],))
        pool.apply(overrideDict, args=(self.unassigned, data["unassigned"],))
        pool.close()
        pool.join()
        
    def get_teams(self):
        return {"unassigned" : self.unassigned.values(), 
                "assignedA" : self.assignedA.values(), 
                "assignedB" : self.assignedB.values()}







  

