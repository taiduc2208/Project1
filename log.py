from datetime import datetime
# Get current time in pretty format
def pretty_time():
    now = datetime.now()
    pretty_time_format = now.strftime("%H:%M:%S %d-%m-%Y")
    return pretty_time_format




def write_log(code, name, description):
    time = pretty_time()
    file = open( "./result/log.txt","a", encoding="utf-8")
    log = code + ", " + name + ", " + time + ", " + description
    file.writelines(log + "\n")
    file.close()
    
