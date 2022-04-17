import os
from decimal import Decimal
import matplotlib.pyplot as plt

path = "/home/pathikrit/Desktop/Spring 22/598/Assignment2/all/results_sl_50_200"
latency = []
thput = []
readlatency = []
writelatency = []

write_ratio = 0.05
read_ratio = 0.95

def read(path):
	os.chdir(path)
	for file in os.listdir():
		if(file.endswith(".txt")):
			file_path = f"{path}/{file}"
			start = file_path.rfind("_") + len("_")
			end = file_path.find(".")
			clients = int(file_path[start:end])
			processFile(file_path, clients)

def processFile(file_path, clients):
	#print(file_path)
	with open(file_path) as f:
		lines = f.readlines();
	write_latency = 0
	read_latency = 0
	tot_latency = 0
	tot_thput = 0
	for line in lines:
		if(line.find("OVERALL") != -1 and line.find("Throughput") != -1) :
			start = line.rfind(" ") + 1
			tot_thput += float(line[start:])
			#print(tot_thput)
		if(line.find("READ") != -1 and line.find("AverageLatency") != -1) :
			start = line.rfind(" ") + 1
			read_latency += float(line[start:])
		if(line.find("UPDATE") != -1 and line.find("AverageLatency") != -1) :
			start = line.rfind(" ") + 1
			write_latency += float(line[start:])
	read_latency = read_latency/clients
	write_latency = write_latency/clients
	tot_latency = read_ratio*read_latency + write_ratio*write_latency
	#print(tot_thput)
	#print(read_latency)
	#print(write_latency)
	#print(tot_latency)
	latency.append(tot_latency)
	thput.append(tot_thput)
	readlatency.append(read_latency)
	writelatency.append(write_latency)

def plot():
	new_latency = [x for _, x in sorted(zip(thput, latency))]
	new_readlatency = [x for _, x in sorted(zip(thput, readlatency))]
	new_writelatency = [x for _, x in sorted(zip(thput, writelatency))]
	new_thput = [x for _, x in sorted(zip(thput, thput))]
	plt.plot(new_thput, new_latency, label = "Average Latency", marker ='o')
	plt.plot(new_thput, new_readlatency, label = "Average Read Latency", marker = 'o')
	plt.plot(new_thput, new_writelatency, label = "Average Write Latency", marker = 'o')
	plt.xlabel('Throughput(ops/s)')
	plt.ylabel('Latency(us)')
	plt.title('Slow Leader Performance Graph')
	plt.legend()
	plt.show()


			

def main():
	read(path)
	plot()
	#print(latency)
	#print(thput)

main()
