import requests
import RPi.GPIO as io
import time
import datetime
import subprocess
import os
import signal
from multiprocessing import Pool

pool = Pool(processes=1)

io.setmode(io.BOARD)
io.setup(3, io.OUT, initial=0) # for lock 
io.setup(5, io.IN)  # for taking input thar door is closed or open using magnet
io.setup(7, io.IN)  # signal from the mobile to open the door
#io.setup(8, io.OUT, initial=0)
io.setup(10, io.OUT, initial=0) # led
#io.output(8, 1)

def lol(url1, obj, token, file_):
	print('Video upload start')
	db = requests.post(url=url1, data=obj, headers=token, files=file_)
	os.system("rm -rf video3.mp4 vid1.h264")
	print('Video uploaded')

url = "https://lockerapi.herokuapp.com/api/locker/1"
url1 = "https://lockerapi.herokuapp.com/api/locker/1/logs"
token = {'Authorization':'Token 72f2e8af6c8161035a59a7d38773b1092a542be7'}
print(token)
print(str(datetime.datetime.now()))
data = {'accessible' : False}
token_request = requests.patch(url=url, data=data, headers=token)
i=10
prestat=0
stat=0
status=0
file_start = ''
open_time='abc'
while(True):
	token_request = requests.get(url=url, headers=token)
	token_request = token_request.json()
	print(token_request)
	if(token_request["accessible"]):
		print('opening the lock')
		flag=False
		io.output(10, 1)
		io.output(3, 1)
		for k in range(25):
			prestat=status
			status = io.input(5)
			stat=status
			if status == 1:
				if prestat==0:
					open_time=str(datetime.datetime.now())
					file_start = subprocess.Popen(["raspivid -o vid1.h264 -t 600000 -w 480 -h 360 -fps 15"], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
					print('Video start')
				print('door is opened')
				data = {'open_status' : True}
				token_request = requests.patch(url=url, data=data, headers=token)
			else:
				if prestat==1:
					os.killpg(os.getpgid(file_start.pid), signal.SIGTERM)
					os.system("ls")
					os.system("MP4Box -add vid1.h264 video3.mp4 -fps 15")
					os.system("ls")
					vid = open("video3.mp4", 'rb')
					obj={'open_time': open_time, 'close_time': str(datetime.datetime.now()), 'locker': 1}
					#pool.apply_async(lol, (url1, obj, token, {'file':vid})) 
					data = {'open_status' : False}
					token_request = requests.patch(url=url, data=data, headers=token)
					db = requests.post(url=url1, data=obj, headers=token, files={'file':vid})
					os.system("rm -rf video3.mp4 vid1.h264")
					flag=True
					break
				print('door is closed')
			#print(token_request.text)
			time.sleep(1)
		if not flag:
			for j in range(5):
				status = io.input(5)
				if status == 1:
					if prestat==0:
						open_time=str(datetime.datetime.now())
						file_start = subprocess.Popen(["raspivid -o vid1.h264 -t 600000 -w 480 -h 360 -fps 15"], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
					print('door is opened')
					data = {'open_status' : True}
					token_request = requests.patch(url=url, data=data, headers=token)
				else:
					if prestat==1:
						os.killpg(os.getpgid(file_start.pid), signal.SIGTERM)
						os.system("MP4Box -add vid1.h264 video3.mp4 -fps 15")
						vid = open("video3.mp4", 'rb')
						obj={'open_time': open_time, 'close_time': str(datetime.datetime.now()), 'locker': 1}
						#pool.apply_async(lol, (url1, obj, token, {'file':vid}))
						data = {'open_status' : False}
						token_request = requests.patch(url=url, data=data, headers=token)
						db = requests.post(url=url1, data=obj, headers=token, files={'file':vid})
						os.system("rm -rf video3.mp4 vid1.h264")
						break
					print('door is closed')
				io.output(10, 0)
				time.sleep(0.5)
				io.output(10, 1)
				time.sleep(0.5)
		print('closing the lock')
		io.output(10, 0)
		io.output(3, 0)
		data = {'accessible' : False}
		token_request = requests.patch(url=url, data=data, headers=token)
	i=i-1



