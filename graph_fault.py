import os
from decimal import Decimal
import matplotlib.pyplot as plt

path_s = "/home/pathikrit/Desktop/Spring 22/598/Assignment2/all/results_sl_50_500"
path_b = "/home/pathikrit/Desktop/Spring 22/598/Assignment2/all/results"
path_f = "/home/pathikrit/Desktop/Spring 22/598/Assignment2/all/results_fl"
path_m = "/home/pathikrit/Desktop/Spring 22/598/Assignment2/all/results_ml_5M"

write_ratio = 0.05
read_ratio = 0.95

def read(path):
	os.chdir(path)
	latency = []
	thput = []
	for file in os.listdir():
		if(file.endswith(".txt")):
			file_path = f"{path}/{file}"
			start = file_path.rfind("_") + len("_")
			end = file_path.find(".")
			clients = int(file_path[start:end])
			a,b = processFile(file_path, clients)
			latency.append(a)
			thput.append(b)
	return latency, thput

def processFile(file_path, clients):
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
	tot_latency = read_ratio*read_latency + write_ratio*write_latency
	return tot_latency, tot_thput
	

def plot(latency, thput, mylabel):
	new_latency = [x for _, x in sorted(zip(thput, latency))]
	new_thput = [x for _, x in sorted(zip(thput, thput))]
	plt.plot(new_thput, new_latency, label = mylabel, marker ='o')


			

def main():
	latency, thput = read(path_b)
	plot(latency, thput, "Baseline")

	latency, thput = read(path_s)
	plot(latency, thput, "Slow Node")

	latency, thput = read(path_f)
	plot(latency, thput, "Failed Node")

	latency, thput = read(path_m)
	plot(latency, thput, "Memory Contention")

	plt.xlabel('Throughput(ops/s)')
	plt.ylabel('Latency(us)')
	plt.title('Leader Failure Performance Graph')
	plt.legend()
	plt.show()

main()
