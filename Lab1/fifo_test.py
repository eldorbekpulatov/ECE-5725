import os
import subprocess

acceptable_cmds = ['pause', 'quit', 'seek 10', 'seek -10']

mplayer_cmd = ''

while (mplayer_cmd != 'quit'):
	
	mplayer_cmd = raw_input("Enter a command for mplayer: ")
	
	while (mplayer_cmd not in acceptable_cmds):
		mplayer_cmd = raw_input("Enter a command for mplayer: ")
		
	cmd = 'echo "' + mplayer_cmd + '" > $(pwd)/video_fifo'
	subprocess.check_output(cmd, shell=True)

