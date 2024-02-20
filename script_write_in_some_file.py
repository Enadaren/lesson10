import os
import psutil
import threading

def print_cpu_inform(func):
    def wrapper():
        result = func()
        with open("CPU_info.txt","w") as text_file:
            text_file.writelines('{:<70}'.format(result[0])+'{:>10}'.format(result[1])+"\n")
    return wrapper

@print_cpu_inform
def cpu_inform():
    value=psutil.cpu_percent(interval=1)
    if isinstance(value,float): 
        loading="CPU[" + "|"*round(value/2)
        value_str=str(round(value,1)) +"%]"
    return [loading, value_str]

def print_virtual_memory_inform(func):
    def wrapper():
        result = func()
        with open("Memory_state.txt","w") as text_file:
            text_file.writelines('{:<70}'.format("Mem[" + result[0] +result[1])+'{:>10}'.format(result[2])+"   ")
    return wrapper

@print_virtual_memory_inform
def virtual_memory_inform():
    value=psutil.virtual_memory()
    active="|"*round(value[5]/value[0]*50)
    free="|"*round(value[4]/value[0]*50)
    not_used=str(round((value[0] - value[1])/1024/1024/1024,1))
    total=str(round(value[0]/1024/1024/1024,1))
    stat_inf =not_used+"G/" + total + "G]"
    return [active, free,stat_inf]

def print_process_info(func):
    def wrapper():
        result=func()
        with open("CPU_info.txt","a") as text_file:
            text_file.writelines('{:<25}'.format(result)+"\n")
    return wrapper

@print_process_info
def process_info():
    tasks=str(len(list(psutil.process_iter())))
    threads = str(threading.active_count())
    inform = "Tasks: " + tasks +", " + threads + " thr"
    return inform


def print_load_average_info(func):
    def wrapper():
        result = func()
        with open("CPU_info.txt","a") as text_file:
            text_file.writelines('{:<25}'.format(result)+"\n")
    return wrapper 

@print_load_average_info
def load_average_info():
    value = list(map(lambda x: str(round(x,2)),psutil.getloadavg()))
    inform = "Load average: " + value[0] +" " + value[1] + " " +value[2]
    return inform

def print_svmi(func):
    def wrapper():
        result = func()
        with open("Memory_state.txt","a") as text_file:
            text_file.writelines('{:<70}'.format("Swp["+result[0]+result[1])+'{:>10}'.format(result[2])+ "   ")
    return wrapper

@print_svmi
def swap_virtual_memory_inform():
    value=psutil.swap_memory()
    active="|"*round(value[1]/value[0]*50)
    free="|"*round(value[2]/value[0]*50)
    used=str(round(value[1]/1024/1024/1024,1))
    total=str(round(value[0]/1024/1024/1024,1))
    stat_inf=used+"G/" + total + "G]"
    return [active, free,stat_inf]

def print_ui(func):
    def wrapper():
        result=func()
        with open("CPU_info.txt","a") as text_file:
            text_file.writelines('{:<20}'.format(result)+"\n")
    return wrapper

@print_ui
def uptime_info():
    value = round(float(open("/proc/uptime").read().split()[0]))
    day = str(value // 3600 // 24)
    hours = str(value // 3600 % 24)
    minutes = str(value // 60 % 60)
    seconds = str(value % 60)
    inform = "Uptime: "+ day + " days, " + hours + ":" + minutes + ":" + seconds
    return inform

def print_pls(func):
    def wrapper():
        result=func()
        with open("Process_info.txt","w") as text_file:
            text_file.writelines('{:>6} {:^20} {:^10} {:^10} {:^7} {:^7} {:^10} {:^20}'.format('PID','User','VIRT','RES','CPU%','MEM%','Time','Command')+"\n")
            for p in result:
                text_file.writelines('{:>6}'.format(p[0]))
                text_file.writelines('{:^20}'.format(p[1]))
                text_file.writelines('{:>10.1f}'.format(p[2]))
                text_file.writelines('{:>10.1f}'.format(p[3]))
                text_file.writelines('{:>8.1f}'.format(p[4]))
                text_file.writelines('{:>8.1f}'.format(p[5]))
                text_file.writelines('{:>10}'.format(p[6]))
                text_file.writelines('{:^20}'.format(p[7])+"\n")
    return wrapper


@print_pls
def process_list_info():
    process_list=[]
    for p in psutil.process_iter():
        temp_list=[]
        temp_list.append(p.pid)
        temp_list.append(p.username())
        temp_list.append(p.memory_info()[1]/1024/1024)
        temp_list.append(p.memory_info()[0]/1024/1024)
        temp_list.append(p.cpu_percent())
        temp_list.append(p.memory_percent())
        value = p.cpu_times()[0]
        minut=int(value)//60
        second=round(value - minut*60,2)
        temp_list.append(format(str(minut)+":"+str(second)))
        names=p.cmdline()
        if len(names)>0:
            temp_list.append(" " + str(names[0]))
        else:
            temp_list.append("NA")
        process_list.append(temp_list)
    return process_list

cpu_inform()
process_info()
virtual_memory_inform()
load_average_info()
swap_virtual_memory_inform()
uptime_info()
process_list_info()    