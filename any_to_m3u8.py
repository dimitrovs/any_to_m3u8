#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import socket
import subprocess
import shlex
import os
import time
import pipes
from BaseHTTPServer import HTTPServer

# CONFIG PARAMETERS

SERVER_URL = 'http://your-url.com/' # Your server's public URL
#HOST = '::' # Listen on all IPs (IPv6)
HOST = '0.0.0.0' # Listen on all IPs (IPv4)
PORT = 80 # 
DEBUG = False

# END CONFIG

logfile = open('result.log','w')
current_url = ''
current_process = None

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_HEAD(self):
	print 'got HEAD request'
	self.protocol_version='HTTP/1.0'
	self.send_response('200')
    def do_GET(self):
	global current_url
	global current_process
        if self.path[5:7] == ':/':
		url = pipes.quote(self.path[1:])
		if url != current_url:
			if current_process:
				# print "New URL requested. FFMPEG process detected. Terminating FFMPEG."
				try:
					current_process.kill()
					# print "Waiting for FFMPEG to terminate..."
					current_process.wait()
					# print "FFMPEG terminated. Cleaning up files."
				except:
					# print "Exception while terminating FFMPEG. Proceeeding." 
					pass
				current_process = None
			else:
				# print "New URL requested. No FFMPEG process detected. Proceeeding."
				pass
			[os.remove(f) for f in os.listdir(".") if f.endswith(".ts") or f.endswith(".m3u8")]
			if DEBUG:
				popen_args = shlex.split("ffmpeg -i "+url+" -acodec copy -vcodec copy -bsf:v h264_mp4toannexb -flags -global_header -hls_time 5 -hls_wrap 15 -hls_flags delete_segments -hls_base_url "+SERVER_URL+" out.m3u8")
			else:
				popen_args = shlex.split("ffmpeg -v -8 -i "+url+" -acodec copy -vcodec copy -bsf:v h264_mp4toannexb -flags -global_header -hls_time 5 -hls_wrap 15 -hls_flags delete_segments -hls_base_url "+SERVER_URL+" out.m3u8")
			current_process = subprocess.Popen(popen_args,stderr=subprocess.STDOUT,stdout=logfile)
			attempt = 0
			while not os.path.exists('out.m3u8') and current_process.poll() is None:
				attempt += 1
				time.sleep(2)
				if attempt > 30:
					break
		current_url = url
		self.protocol_version='HTTP/1.0'
        	self.send_response(302)
        	self.send_header('Location', SERVER_URL+'out.m3u8')
        	self.end_headers()
        else:
		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

Handler = MyRequestHandler
server = None

if is_valid_ipv6_address(HOST):
	server = HTTPServerV6((HOST, PORT), Handler)
elif is_valid_ipv4_address(HOST):
	server = SocketServer.TCPServer((HOST, PORT), Handler)
else:
	print "ERROR: The HOST configuration parameter is not a valid IPv4 or IPv6 address."

if server:
	server.serve_forever()
