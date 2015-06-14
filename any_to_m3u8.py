#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import subprocess
import os.path
import time
import pipes

# CONFIG PARAMETERS

SERVER_URL = 'http://your_server.com:14703/' # Your server's public URL
HOST = '0.0.0.0' # Listen on on all IPs
PORT = 14703 # 
DEBUG = False
# END CONFIG

current_url = ''

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_HEAD(self):
	print 'got HEAD request'
	self.protocol_version='HTTP/1.0'
	self.send_response('200')
    def do_GET(self):
	global current_url
        if self.path[5:7] == ':/':
		url = pipes.quote(self.path[1:])
		if url != current_url:
			subprocess.call("/usr/bin/killall -9 ffmpeg", shell=True)
			subprocess.call("rm -rf *.ts", shell=True)
			subprocess.call("rm -rf *.m3u8", shell=True)
			if DEBUG:
				subprocess.Popen("ffmpeg -i "+url+" -acodec copy -vcodec copy -bsf:v h264_mp4toannexb -flags -global_header -hls_wrap 15 -hls_flags delete_segments -hls_base_url "+SERVER_URL+" out.m3u8 2> result.log &",shell=True)
			else:
				subprocess.Popen("ffmpeg -loglevel 0 -i "+url+" -acodec copy -vcodec copy -bsf:v h264_mp4toannexb -flags -global_header -hls_wrap 15 -hls_flags delete_segments -hls_base_url "+SERVER_URL+" out.m3u8 2> /dev/null &",shell=True)
			attempt = 0
			while not os.path.exists('out0.ts'):
				time.sleep(2)
				attempt += 1
				if attempt > 30:
					break
		current_url = url
		self.protocol_version='HTTP/1.0'
        	self.send_response(302)
        	self.send_header('Location', SERVER_URL+'out.m3u8')
        	self.end_headers()
        else:
		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer((HOST, PORT), Handler)

server.serve_forever()
