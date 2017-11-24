import psutil
import time


def ExecName(processpath):
    Backslashpos = len(processpath)
    if(Backslashpos != 0):
        substr = ""
        while(substr != '\\'):
            substr = processpath[Backslashpos-1]
            Backslashpos -= 1
    return (processpath[Backslashpos+1:len(processpath)])
            
def getInf(ProcessList):   
    processExec = ""
    for proc in ProcessList:
        try:
            processID = proc.pid
            try: 
                processExec = proc.exe()
                processCPUs = proc.cpu_percent(interval=0.01)
                processFisMem = proc.info['memory_info'].rss
                processVirMem = proc.info['memory_info'].vms
            except psutil.AccessDenied:
                pass
        except psutil.NoSuchProcess:
            pass
        else:
            print("Identificador del proceso :",processID)
            if(processExec == ""):
                print("Acceso no permitido")
            else:    
                print("Nombre del ejecutable :",ExecName(processExec))
                print("Utilizacion de CPU :",processCPUs)
                print("Utilizacion de memoria fisica :",processFisMem)
                print("Utilizacion de memoria virtual :",processVirMem)
    return

print(time.strftime("%I:%M:%S"))
ProcessList = psutil.process_iter(attrs=['name', 'memory_info'])
getInf(ProcessList)
            
            
            
            
 
            
            




        
        
        