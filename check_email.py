from validate_email import validate_email
from threading import Thread
import threading, time, pandas, queue, sys

def init(INPUT):
	global write, threads, q, lock, emails, dfc, NUM_OF_EMAIL, OUTPUT, live_cnt, dead_cnt
	live_cnt = 0
	dead_cnt = 0
	write = []
	threads = []
	q = queue.Queue()
	lock = threading.Lock()
	emails = []
	dfc = pandas.read_excel(INPUT)
	NUM_OF_EMAIL = len(dfc['Email'])
	OUTPUT = "PROCESSED_" + INPUT

def create_task(emails):
	i = 0
	while q.qsize() < NUM_OF_EMAIL:
		if '@' in str(emails[i]): q.put(str(emails[i]))
		i += 1

def check_mail(email):
	global dead_cnt, live_cnt
	result = validate_email(email, verify=True)
	lock.acquire()
	if result == True:
		live_cnt += 1
		write.append(email)
		df = pandas.DataFrame(write)
		writer = pandas.ExcelWriter(OUTPUT)
		df.to_excel(writer,'Sheet1',  header = False, index = False)
		writer.save()
	else:
		dead_cnt += 1
	lock.release()
	return

def work():
	while True:
		lock.acquire()
		if q.empty() == True:
			lock.release()
			break
		else:
			email = q.get()
		lock.release()
		check_mail(email)

def main(INPUT):
	init(INPUT)
	crr_time = time.time()
	# if dfc == None:
	# 	return "Can't open file named -> {}".format(INPUT)
	s_time = time.time()
	emails = dfc['Email']
	create_task(emails)
	for i in range(0, int(NUM_OF_EMAIL/10)):
		t = threading.Thread(target = work)
		t.start()
		threads.append(t)
	for thread in threads:
		thread.join()
	return "DONE, {} live, {} dead, processed data saved to file -> ".format(live_cnt, dead_cnt), OUTPUT
