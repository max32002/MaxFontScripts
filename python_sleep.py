#!/usr/bin/env python3
#encoding=utf-8

import time
import datetime
import sys

if __name__ == "__main__":

    argument_count = 1 + 1
    if len(sys.argv)==argument_count:
        delay_time = sys.argv[1]
        if len(delay_time) > 0:
            if 'H' in delay_time:
                delay_time = delay_time.replace('H','h')
            if 'h' in delay_time:
                delay_time = delay_time.replace('h','*60M')
            if 'M' in delay_time:
                delay_time = delay_time.replace('M','m')
            if 'm' in delay_time:
                delay_time = delay_time.replace('m','*60S')
            if 'S' in delay_time:
                delay_time = delay_time.replace('S','s')
            if 's' in delay_time:
                delay_time = delay_time.replace('s','*1')

            delay_time_int = 0
            if '*' in delay_time:
                delay_time_int = eval(delay_time)
            else:
                delay_time_int = int(delay_time)
            print("Current Time:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            format_time_string = "%d seconds" % delay_time_int
            if delay_time_int > 60:
                format_time_string += ",about %d minutes" % (delay_time_int/60)
            if delay_time_int > 60*60:
                format_time_string += ",about %d hours" % (delay_time_int/(60*60))
            print("start to sleep: %s." % format_time_string)

            time.sleep(delay_time_int)
            print("end of sleep.")
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))
