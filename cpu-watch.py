#! /usr/bin/env python3

import psutil
import argparse
import sys
import time
import logging
import os

cpu_usage = []


def print_processes():
    for proc in psutil.process_iter(["pid", "name"]):
        print(proc.info)


def monitoring_worker(pids, verbose):
    for i in pids:
        pid = i["pid"]
        p = psutil.Process(pid=pid)
        if p.is_running():
            cpu = p.cpu_percent(interval=0.1)
            if cpu > 0:
                cpu_usage.append(cpu)
            if verbose:
                logging.debug("cpu:{cpu} pid: {pid}"
                              .format(cpu=cpu, pid=p.pid))
    return


def main(process_name, command, interval, limit, dry=False, verbose=False):
    processes = [proc.info for proc in psutil.process_iter(["pid", "name"]) if
                 process_name.lower() in proc.info["name"].lower()]

    if len(processes) == 0:
        logging.warning("couldn't find any processes that matched the term '{process_name}'"
                        .format(process_name=process_name))
        return

    if verbose:
        logging.debug("found the following processes")
        for p in processes:
            logging.debug("name: {name} pid: {pid}"
                          .format(name=p["name"], pid=p["pid"]))

    for n in range(interval):
        monitoring_worker(pids=processes, verbose=verbose)
        time.sleep(1)

    if len(cpu_usage) == 0:
        cpu_average = 0
    else:
        cpu_average = round(sum(cpu_usage) / len(cpu_usage))

    if verbose:
        logging.debug("cpu average {cpu_average}%"
                      .format(cpu_average=cpu_average))

    if dry:
        if cpu_average >= limit:
            print("\n\ncpu %{cpu} hit max rule of {max}%, would have triggered command `{cmd}`"
                  .format(cpu=cpu_average,
                          max=limit,
                          cmd=command))
            return
        else:
            print("\n\ncpu %{cpu} did not hit max rule of {max}%, would have done nothing"
                  .format(cpu=cpu_average,
                          max=limit))
            return

    if cpu_average >= limit:
        logging.info("cpu average of {cpu_average}% triggering command execution"
                     .format(cpu_average=cpu_average))
        cmd = os.popen(command)
        output = cmd.read()
        if verbose:
            logging.debug("command: {command}  command_output: {output}"
                          .format(command=command, output=output))
        return

    if verbose:
        logging.debug("max cpu not reached. finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description="description:\n"
                                                 "monitors processes to see if they are above a certain cpu percentage"
                                                 "\nfor a given period of time, and if so executes a shell command")

    parser.add_argument("--list",
                        help="list processes and exit (useful for selecting process name)\n\n",
                        action="store_true")

    parser.add_argument("--process", default="passenger",
                        help="match process name (default: %(default)s)\n\n",
                        action="store")

    parser.add_argument("--command",
                        default="systemctl reload nginx",
                        help="command to execute (default: %(default)s)\n\n",
                        action="store")

    parser.add_argument("-n", type=int,
                        default=300,
                        help="time frame in seconds to monitor cpu (default: %(default)s)\n\n")

    parser.add_argument("--max", type=int,
                        default=80,
                        help="max cpu limit percentage during chosen interval to trigger command (default: %("
                             "default)s)\n\n")

    parser.add_argument("-f", "--forever",
                        default=False, action="store_true",
                        help="run forever and sleep for default sleep time (default: %("
                             "default)s)\n\n")

    parser.add_argument("-s", type=int,
                        default=300,
                        help="seconds to sleep if running forever (default: %(default)s)\n\n")

    parser.add_argument("--dry", default=False,
                        help="test with dry run without executing command (default: %(default)s)\n\n",
                        action="store_true")

    parser.add_argument("-V", "--verbose", help="verbose logging (default: %(default)s)\n\n",
                        action="store_true")

    parser.add_argument("--log", default="",
                        help="file to log output. if left blank then logs are sent to stderr (default: %(default)s)\n\n",
                        action="store")

    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                        help="show this help message and exit\n\n")

    args = parser.parse_args()

    if args.log != "":
        logging.basicConfig(level=logging.DEBUG, filename=args.log,
                            format="%(asctime)s %(levelname)s %(message)s")
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s")

    if args.list:
        print_processes()
        sys.exit(0)

    if args.forever:
        logging.info("running in infinite loop mode with {sleep} second sleep intervals"
                     .format(sleep=args.s))
        while True:
            cpu_usage.clear()
            main(process_name=args.process, command=args.command, limit=args.max,
                 interval=args.n, dry=args.dry, verbose=args.verbose)
            time.sleep(args.s)

    main(process_name=args.process, command=args.command, limit=args.max,
         interval=args.n, dry=args.dry, verbose=args.verbose)
