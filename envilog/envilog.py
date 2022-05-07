import argparse
import os
from time import sleep
from datetime import datetime
from envirohat import EnviroHAT

QUANTS = ["temperature", "humidity", "pressure", "altitude", "lux", "proximity", "gas_oxidising", "gas_reducing", "gas_nh3", "noise_profile", "all"]

def get_datestamp():
    return datetime.now().strftime("%d-%m-%Y")


def get_timestamp():
        now = datetime.now()
        return now.strftime("%H:%M:%S")

def now_after_midnight(date):
    return datetime.now().date() > date


def mk_log_dir(parent):
    path = os.path.join(parent, get_datestamp()) 
    dp("Creating directory: " + path)
    os.makedirs(path, exist_ok=True)


def open_log_files(parent, quants):
    arr =  QUANTS[0:-1] if quants == "all" else quants.split(",")

    files = list()
    datestamp = get_datestamp()
    for name in arr:
        if not name in QUANTS:
            raise Exception("Unsupported quantity \"" + name + "\"!")

        path = os.path.join(parent, datestamp, name)
        dp("Creating file: " + path)
        files.append(open(path, "w"))
        files[-1].write("# hour:minute:second:value\n")

    return files, arr


def close_files(arr):
    for f in arr:
        dp("Closing file: " + f.name)
        f.close()


def dp(msg):
    if do_dp:
        print(msg)


parser = argparse.ArgumentParser(description="Log values from Enviro+ HAT.", epilog="Allowed quantities: " + str(QUANTS))
parser.add_argument("-p", "--period", dest="period", type=int, default=1, help="Time in seconds between measurements, default: 1.")
parser.add_argument("-q", "--quantities", dest="quant", type=str, default="all", help="Comma separated list of quantities that shold be logged, default: all.")
parser.add_argument("path", metavar="path", type=str, help="Path to directory where logs are saved.")
parser.add_argument("-v", "--verbose", dest="verb", action="store_true", default=False, help="Print debug informations.")

args = parser.parse_args()
hat = EnviroHAT()

do_dp = args.verb

start_date = datetime.now().date()
mk_log_dir(args.path)
files, names = open_log_files(args.path, args.quant)

while True:
    if now_after_midnight(start_date):
        dp("It is after midnight!")
        close_files(files)
        mk_log_dir(args.path)
        files, names = open_log_files(args.path, args.quant)
        start_date = datetime.now().date()

    for (i, name) in enumerate(names):
        if "gas" in name:
            cmd = name.replace("_", "_read_")
        else:
            cmd = "get_" + name
        
        dp("Reading: " + name + "; Command: " + cmd)
        value = eval("hat." + cmd + "()")
        files[i].write(get_timestamp() + ":" + str(value) + "\n")
        files[i].flush()

    sleep(args.period)

close_files(files)

