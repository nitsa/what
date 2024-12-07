import os
import time
import datetime
from colorama import Fore, Back, Style, init
import sys
import shutil
import webbrowser


def search_disk(pattern, disk, unit_size, area_size, mountpoint, bypass_unit):
    with open(disk, "rb") as fp:

        # unit counter
        i = 0

        # end of disk
        done = 0

        # start from unit > 0
        bypass_done = 0

        # get drive size
        total, used, free = shutil.disk_usage(mountpoint)
        still_size = total

        # iterate through units
        while (True):

            # start from unit > 0 check
            if (bypass_unit > 0) and (bypass_done == 0):
                bypass_done = 1
                bypass_size = bypass_unit * unit_size
                unit = fp.seek(bypass_size)
                while (i < bypass_unit):
                    i = i + 1

            # end of disk check
            if (still_size >= unit_size):
                unit = fp.read(unit_size)
            else:
                done = 1
                unit = fp.read(still_size)

            print(Style.BRIGHT + Fore.MAGENTA + Back.BLACK)
            print(str(datetime.datetime.now()) + " : scanning unit #" + str(i))
            print("\n" , file = open("out.txt", "a"))
            print(str(datetime.datetime.now()) + " : scanning unit #" + str(i), file = open("out.txt", "a"))
            print(Style.RESET_ALL)

            # absolute offset within unit
            abs_offset = 0

            # search for more patterns within same unit
            repeat = 1
            subunit = 0

            # slide though same unit
            prev_found = 0

            # iterate through same unit after a pattern is found
            while (repeat == 1):

                # take into account data to dump around found offset
                if (subunit == 0):
                    found = unit.find(pattern)
                else:
                    found = unit[prev_found + 1 : unit_len].find(pattern)

                # pattern found
                if (found > 0):

                    # absolute offset within unit, start of unit is absolute offset 0 for the unit
                    abs_offset = abs_offset + found

                    print(Style.BRIGHT + Fore.MAGENTA + Back.BLACK)
                    print(str(datetime.datetime.now()) + " : pattern found in unit #" + str(i) + " offset " + str(abs_offset))
                    print("\n" , file = open("out.txt", "a"))
                    print(str(datetime.datetime.now()) + " : pattern found in unit #" + str(i) + " offset " + str(abs_offset), file = open("out.txt", "a"))
                    print(Style.RESET_ALL)

                    # show data before found
                    offset = found - area_size

                    # show data between abs_found - area_size, abs_found + area_size
                    data = unit[prev_found + 1 + offset : prev_found + 1 + offset + 2 * area_size]

                    print(Fore.BLACK + Back.GREEN)
                    print(data)
                    print("\n" , file = open("out.txt", "a"))
                    print(data, file = open("out.txt", "a"))
                    print(Style.RESET_ALL)
                    subunit = 1
                    unit_len = len(unit)
                    prev_found = prev_found + 1 + found

                else:
                    # pattern not found
                    repeat = 0

            # end of disk
            if (done == 1):
                return -2

            # goto next unit
            i = i + 1
            still_size = still_size - unit_size


def logo():
    print (Fore.WHITE + Back.MAGENTA + Style.BRIGHT)
    print ("                                                                                                          ")
    print ("                                                                                                          ")
    print ("                                        What.Really.Was v0.1                                              ")
    print ("                                                                                                          ")
    print ("                                A forensics tool for uncovering secrets                                   ")
    print ("                                                                                                          ")
    print ("                                                                                                          ")
    print ("                                                                                                          ")
    print ("                                                                                                          ")
    print (" - Place search pattern in pattern.txt, can be binary or string                                           ")
    print (" - Output is written in out.txt (overwrite)                                                               ")
    print (" - Unit size is size of data in bytes for a single read allocated in RAM                                  ")
    print (" - Area size is the number of bytes to show around found pattern                                          ")
    print (r" - Mountpoint is where OS mounts the device like C:\ or /                                                 ")
    print (r" - Device is the actual disk like \\.\PHYSICALDRIVE0 or /dev/sda                                          ")
    print (" - Provide unit to start reading from that particulat unit                                                ")
    print (" - Supports Windows and Linux like OS                                                                     ")
    print (" - Units are sequential                                                                                   ")
    print (" - Please run as admin                                                                                    ")
    print ("                                                                                                          ")
    print(Style.RESET_ALL)


def main():

    # initialize colours
    init()

    # display start logo with help
    logo()

    # create out file
    file = open("out.txt", "w")
    file.close()

    try:
        operation = int(input("Enter operation (1=search pattern, 2=list drives, 3=listen to music) : "))

    # input error handling
    except:
        print(Fore.RED + Back.BLACK)
        print("Error : operation should be integer")
        print(Style.RESET_ALL)
        sys.exit(0)

    # input error handling
    if operation not in (1, 2, 3):
        print(Fore.RED + Back.BLACK)
        print("Error : operation should be 1 or 2")
        print(Style.RESET_ALL)
        sys.exit(0)

    # search for pattern
    if (operation == 1):
        unit_size  = input("Enter unit size in bytes or press Enter (default 1073741824 for 1 GB) : ")
        area_size  = input("Enter area size in bytes or press Enter (default 100) : ")
        mountpoint = input("Enter mountpoint/disk drive letter or press Enter (default C:) : ")
        device     = input(r"Enter device or press Enter (default \\.\PHYSICALDRIVE0) : ")
        bypass_unit = input("Enter unit to jump or press Enter (default 0) : ")

        # input error handling
        if len(str(unit_size)) == 0:
            unit_size = 1073741824
        else:
            try:
                unit_size = int(unit_size)
            except:
                print(Fore.RED + Back.BLACK)
                print("Error : unit size should be integer")
                print(Style.RESET_ALL)
                sys.exit(0)

        # input error handling
        if len(str(area_size)) == 0:
            area_size = 100
        else:
            try:
                area_size = int(area_size)
            except:
                print(Fore.RED + Back.BLACK)
                print("Error : area size should be integer")
                print(Style.RESET_ALL)
                sys.exit(0)

        # input error handling
        if len(mountpoint) == 0:
            mountpoint = "C:"

        # input error handling
        if len(device) == 0:
            device = r"\\.\physicaldrive0"

        # input error handling
        if len(str(bypass_unit)) == 0:
            bypass_unit = 0
        else:
            try:
                bypass_unit = int(bypass_unit)
            except:
                print(Fore.RED + Back.BLACK)
                print("Error : a unit should be integer")
                print(Style.RESET_ALL)
                sys.exit(0)

        # read pattern to search for
        fp = open("pattern.txt", "rb")
        pattern = fp.read()
        fp.close()

        print(Style.BRIGHT + Fore.MAGENTA + Back.BLACK)
        print(str(datetime.datetime.now()) + " : starting")
        print("\n" , file = open("out.txt", "a"))
        print(str(datetime.datetime.now()) + " : starting", file = open("out.txt", "a"))
        print(Style.RESET_ALL)

        # OS is Win
        if os.name == "nt":
            # start searching
            operation = search_disk(pattern, device, unit_size, area_size, mountpoint, bypass_unit)

            # end of disk
            if (operation == -2):
                print(Style.BRIGHT + Fore.MAGENTA + Back.BLACK)
                print(str(datetime.datetime.now()) + " : finished")
                print("\n" , file = open("out.txt", "a"))
                print(str(datetime.datetime.now()) + " : finished", file=open("out.txt", "a"))
                print(Style.RESET_ALL)
        # OS is Linux like
        if os.name == "posix":
            # start searching
            operation = search_disk(pattern, device, unit_size, area_size, mountpoint, bypass_unit)

            # end of disk
            if (operation == -2):
                print(Style.BRIGHT + Fore.MAGENTA + Back.BLACK)
                print(str(datetime.datetime.now()) + " : finished")
                print("\n" , file = open("out.txt", "a"))
                print(str(datetime.datetime.now()) + " : finished", file=open("out.txt", "a"))
                print(Style.RESET_ALL)

    # show drives
    if (operation == 2):
        print(Fore.YELLOW + Back.BLACK)

        # OS is Win
        if os.name == "nt":
            os.system("wmic diskdrive get size, description, deviceid, mediatype")
            os.system("wmic logicaldisk get size, description, name")

        # OS is Linux like
        if os.name == "posix":
            os.system("cfdisk")

        print(Style.RESET_ALL)

    # load some music
    if (operation == 3):
        print(Style.BRIGHT + Fore.MAGENTA + Back.BLACK)
        print(str(datetime.datetime.now()) + " : loading some music for you...")
        print(Style.RESET_ALL)
        music = webbrowser.open("https://www.youtube.com/watch?v=p5pHyjJB5DU")


if __name__ == "__main__":
    main()
