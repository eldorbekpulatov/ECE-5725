#!/usr/bin/env python
import os
import time
import random 
import subprocess
from flask import Flask, jsonify, render_template, request, make_response
from multiprocessing import Process, Pipe, Queue
from server import Game, listener
from constants import GAMES

app = Flask(__name__, static_url_path='/static')  

@app.route('/', methods=['GET'])  
def welcome():  
    return render_template("welcome.html") 


@app.route('/game', methods=['GET'])   
@app.route('/game/', methods=['GET'])  
@app.route('/game/<int:game_id>', methods=['GET'])
def newgame(game_id=None):
    global GAMES
    if game_id in GAMES: 
        g = GAMES[game_id]
        return render_template("newgame.html", id=g.pid, ip=g.ip)
    elif game_id == None:
        rand_id = random.randint(1000, 6553)
        while (rand_id in GAMES):
            rand_id = random.randint(1000, 6553)
        g = Game(rand_id)
        GAMES[rand_id] = g
        if not g.isListening():
            g.startListening()
        return render_template("newgame.html", id=g.pid, ip=g.ip)
    else:
        return render_template("404.html", id=game_id)
 

@app.route('/start/<int:game_id>', methods=['GET'])
def startgame(game_id=None):
    global GAMES
    if game_id in GAMES: 
        g = GAMES[game_id]
        g.stopListening()
        g.running.value = 1
        if not g.isPlaying():
            g.startPlaying()
        g.notifyTeams("start")
        g.notifyExtras("stop")
        return render_template("startgame.html", id=g.pid, ip=g.ip)
    else:
        return render_template("404.html", id=game_id)


@app.route('/stop/<int:game_id>', methods=['GET'])
def stopgame(game_id=None):
    global GAMES
    if game_id in GAMES: 
        g = GAMES[game_id]
        g.running.value = 0
        g.stopPlaying()
        g.notifyTeams("stop")
        winner = g.whoWon() # 0 1 2
        return render_template("stopgame.html", id=g.pid, ip=g.ip, outcome=winner)
    else:
        return render_template("404.html", id=game_id)
    

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    global GAMES
    game_id = request.args.get('port', 0, type=int)
    if game_id in GAMES: 
        g = GAMES[game_id]
        if request.method == 'POST':
            data = eval(request.data)
            if(not g.running.value):
                g.override_teams(data) # must complete
        resp = make_response(g.get_teams())
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status_code = 200
        return resp
    else:
        g = Game(-1)
        resp = make_response(g.get_teams())
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status_code = 200
        return resp


if __name__ == '__main__':  
    app.run(debug = True)  
