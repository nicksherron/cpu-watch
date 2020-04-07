# cpu-watch
cpu-watch monitors processes to see if they are above a certain cpu percentage
for a given period of time, and if so executes a shell command.

### Install
clone the git repository
```
git clone https://github.com/nicksherron/cpu-watch
cd cpu-watch 
python3 setup.py install
```

### Usage

Using the list then dry flags is recommended to verify that the settings are correct

```
$ ./cpu-watch.py --list

{'name': 'kernel_task', 'pid': 0}
{'name': 'suricata', 'pid': 120}
....

```
dry run examples

```
$ sudo ./cpu-watch.py -n 10 --max 80 --process "suricata" --verbose --dry
2020-04-07 08:07:25,951 DEBUG found the following processes
2020-04-07 08:07:25,951 DEBUG name: suricata pid: 120
2020-04-07 08:07:26,053 DEBUG cpu:0.0 pid: 120
...
2020-04-07 08:07:36,014 DEBUG cpu:0.1 pid: 120
2020-04-07 08:07:37,015 DEBUG cpu average 4%

cpu %4 did not hit max rule of 80%, would have done nothing
```
dry run  example showing if max of 1 percent cpu is hit
```
$ sudo ./cpu-watch.py -n 10 --max 1  --process "suricata" --command 'echo command executed' --verbose --dry
2020-04-07 08:11:13,913 DEBUG found the following processes
2020-04-07 08:11:13,913 DEBUG name: suricata pid: 120
2020-04-07 08:11:23,979 DEBUG cpu:20.9 pid: 120

....
2020-04-07 08:11:23,979 DEBUG cpu:2.9 pid: 120
2020-04-07 08:11:24,983 DEBUG cpu average 10%

cpu %10 hit max rule of 1%, would have triggered command `echo command executed`

```


Or run a harmless echo test

```
$ ./cpu-watch.py -n 10 --max 0 --process "bash" --verbose  --command='echo running echo command' 
```

this checks cpu average over a 10 second time frame for each process  and if any  bash processes are greater than 0 percent then run the command `echo running echo command`


#### options   

```
$ ./cpu-watch.py --help

usage: cpu-watch.py [--list] [--process PROCESS] [--command COMMAND] [-n N]
                    [--max MAX] [-f] [-s S] [--dry] [-V] [--log LOG] [-h]

description:
monitors processes to see if they are above a certain cpu
percentage for a given period of time, and if so executes a shell
command

optional arguments:
  --list             list processes and exit (useful for selecting process name)
                     
  --process PROCESS  match process name (default: passenger)
                     
  --command COMMAND  command to execute (default: systemctl reload nginx)
                     
  -n N               time frame in seconds to monitor cpu (default: 300)
                     
  --max MAX          max cpu limit percentage during chosen interval to trigger command (default: 80)
                     
  -f, --forever      run forever and sleep for default sleep time (default: False)
                     
  -s S               seconds to sleep if running forever (default: 300)
                     
  --dry              test with dry run without executing command (default: False)
                     
  -V, --verbose      verbose logging (default: False)
                     
  --log LOG          file to log output. if left blank then logs are sent to stderr (default: )
                     
  -h, --help         show this help message and exit
                     
```

### Setting up as a systemd service

make file excuteable and cp to a bin path 

```
chmod +x cpu-watch.py && cp cpu-watch.py /usr/local/bin
```
edit example cpu-watch.service file and save to /etc/systemd/system

```
sudo cp cpu-watch.service /etc/systemd/system
```

auto start on boot

```
sudo systemctl enable cpu-watch.service
```
start service
```
sudo systemctl start cpu-watch.service
```
view logs (if didn't set log file in script flags)
```
sudo journalctl -xfu cpu-watch.service
```

