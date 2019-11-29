IPSTR = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| tail -n 1"
SERVER_IP = '192.168.1.26'
BUFFER_SIZE = 128
GAMES = {}   
KEY = "ip"