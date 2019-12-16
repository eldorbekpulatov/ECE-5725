#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request, make_response


app = Flask(__name__, static_url_path='/static') 
GAMES = {}

@app.route('/', methods=['GET'])  
def main():  
    return render_template("main.html") 

# @app.route('/game', methods=['GET'])  
# def main():  
#     return render_template("main.html") 
if __name__ == '__main__':  
    app.run(debug = True)  
