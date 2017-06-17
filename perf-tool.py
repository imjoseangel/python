#!/usr/bin/env python
#
# A script that runs the commands to perform Netflix's
# "Linux Performance Analysis in 60,000 Milliseconds"
#
# (http://techblog.netflix.com/2015/11/linux-performance-analysis-in-60s.html)
#
import subprocess
import datetime
import argparse
import sys
import socket

tasks = [
  {
    "cmd": "uptime",
    "help": "View load averages (1m, 5m, 15m) and system uptime",
    "poll": False
  },
  {
    "cmd": "dmesg | tail",
    "help": "Shows the last 10 system messages - look for errors",
    "poll": False
  },
  {
    "cmd": "vmstat 1 {}",
    "help": "r - number of processes running on CPU\nfree - free memory in KB\nsi, so - swap-in and swap-out (non-zero, bad)\nus,sy,id,wa,st - breakdown of CPU time across CPUs",
    "poll": True
  },
  {
    "cmd": "mpstat -P ALL 1 {}",
    "help": "Prints CPU time breakdowns per CPU",
    "poll": True
  },
  {
    "cmd": "pidstat 1 {}",
    "help": "Per-process resource use summary",
    "poll": True
  },
  {
    "cmd": "iostat -xz 1 {}",
    "help": "r/s, w/s, rkB/s, wkB/s - delivered reads, writes, read Kbytes, and write Kbytes per second to the device\nawait - The average time for the I/O in milliseconds\navgqu-sz - average number of requests issued to the device; values > 1 -> saturation\n%util - Device utilization (busy percent)",
    "poll": True
  },
  {
    "cmd": "free -m",
    "help": "Free memory\nbuffers - buffer cache, used for block device I/O\npage cache, used by file systems",
    "poll": False
  },
  {
    "cmd": "sar -n DEV 1 {}",
    "help": "check network interface throughput: rxkB/s and txkB/s, as a measure of workload",
    "poll": True
  },
  {
    "cmd": "sar -n TCP,ETCP 1 {}",
    "help": "summarized view of some key TCP metrics\nactive/s - Number of locally-initiated TCP connections per second\npassive/s - Number of remotely-initiated TCP connections per second\nretrans/s - Number of TCP retransmits per second",
    "poll": True
  }
]

def call_task(task, count):
    cmd = task['cmd']
    if task['poll']:
        cmd = cmd.format(count)
    print
    print '-' * 50
    print '`{}`'.format(cmd)
    print '{}'.format(task['help'])
    print '-' * 50
    print
    print subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', help='Poll count for each command that waits / polls', default=3)
    args = parser.parse_args()

    print
    print 'Host is {}, time is {}'.format(socket.gethostname(), datetime.datetime.now())

    for task in tasks:
        try:
            call_task(task, args.count)
        except Exception as e:
            print e
