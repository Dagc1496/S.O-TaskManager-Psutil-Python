import psutil
import time,sched
import csv


def ExecName(processpath):
    Backslashpos = len(processpath)
    if(Backslashpos != 0):
        substr = ""
        while(substr != '\\'):
            print(processpath[Backslashpos-1])
            substr = processpath[Backslashpos-1]
            Backslashpos -= 1
    return (processpath[Backslashpos+1:len(processpath)])

def getInf(ProcessList):
    processExec = ""
    processRead = 0
    processWrite = 0
    with open('taskManagerInfo.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for proc in ProcessList:
            try:
                processID = proc.pid
                try:
                    processExec = proc.exe()
                    processCPUs = proc.cpu_percent(interval=None)
                    processFisMem = proc.info['memory_info'].rss
                    processVirMem = proc.info['memory_info'].vms
                    #processShared = proc.info['memory_info'].shared
                    processUser = proc.info['username']
                    processRead = proc.io_counters().read_count
                    processWrite = proc.io_counters().write_count
                except psutil.AccessDenied:
                    pass
            except psutil.NoSuchProcess:
                pass
            else:
                if(processExec == ""):
                    print("Acceso no permitido")
                else:
                    writer.writerow([time.strftime("%I:%M:%S"), processID, processUser, processCPUs, processFisMem, processVirMem, processRead, processWrite, processExec])
        return

s = sched.scheduler(time.time, time.sleep)
with open('taskManagerInfo.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    writer.writerow(['TIME', 'PID', 'USER','CPU', 'MEM', 'VMEM', 'SHARED MEM', 'READ', 'WRITE', 'NAME'])
while True:
    ProcessList = psutil.process_iter(attrs=['username', 'nice', 'memory_info', 'memory_percent', 'cpu_percent', 'cpu_times', 'name', 'status', 'io_counters'])
    getInf(ProcessList)
    time.sleep(1)
