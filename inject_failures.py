import os 
from multiprocessing import Process
import sys

pid = 23089
tot_clients = 1
output_file = "/dcsdata/home/pathikrit/test/results_mf/output_"
process_list = []

def kill_node():
	os.system("kill -9 " + str(pid))

'''
quota = 50ms
period = 200ms
'''
def slow_node():
	quota=50000
	period=200000
	print("sudo sh -c 'sudo mkdir /sys/fs/cgroup/cpu/db'")
	print("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cpu.cfs_quota_us'".format(quota))
	print("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cpu.cfs_period_us'".format(period))
	print("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cgroup.procs'".format(pid))
	#os.system("sudo sh -c 'sudo mkdir /sys/fs/cgroup/cpu/db'")
	#os.system("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cpu.cfs_quota_us'".format(quota))
	#os.system("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cpu.cfs_period_us'".format(period))
	#os.system("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cgroup.procs'".format(pid))

def memory_contention():
	os.system("sudo sh -c 'sudo mkdir /sys/fs/cgroup/memory/db'")
	os.system("sudo sh -c 'sudo echo @(5 * 1024 * 1024) > /sys/fs/cgroup/memory/db/memory.limit_in_bytes'")
	os.system("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/memory/db/cgroup.procs'".format(pid))
	#print("sudo sh -c 'sudo mkdir /sys/fs/cgroup/memory/db'")
	#print("sudo sh -c 'sudo echo @(5 * 1024 * 1024) > /sys/fs/cgroup/memory/db/memory.limit_in_bytes'")
	#print("sudo sh -c 'sudo echo {} > /sys/fs/cgroup/cpu/db/cgroup.procs'".format(pid))

def load_data():
	os.system("./bin/ycsb load zookeeper -s -P workloads/workloadb -p zookeeper.connectString=localhost:2181 -p recordcount=10000")

def run_client():
	os.system("./bin/ycsb run zookeeper -P workloads/workloadb -p zookeeper.connectString=localhost:2181,localhost:2182,localhost:2183 >> " + output_file)

def benchmark(count):
	for x in range(count):
		t_process = Process(target = run_client)
		process_list.append(t_process)



def main():
	if len(sys.argv) < 3:
		print "Less arguments"
		return
	global pid 
	global tot_clients
	tot_clients = sys.argv[1]
	pid = sys.argv[2]
	global output_file
	output_file = output_file + tot_clients + ".txt"
	benchmark(int(tot_clients))
	fault_process = Process(target = memory_contention)
	for x in process_list:
		x.start()
	fault_process.start()
	fault_process.join()
	for x in process_list:
		x.join()

main()