# massExploitConsole
a collection of tools with a cli ui

> check out [Windows version](https://github.com/jm33-m0/massExpConsole/tree/win) if you are using Windows

## screenshot

![](/screenshot/main.png)


## disclaimer

- please use this tool only on **authorized systems**, im not responsible for any damage caused by users who ignore my warning
- **i do not own** the code of adapted exploits or tools
- exploits are adapted from other sources, please refer to their author info


## what does it do?

- an easy-to-use user interface (cli)
- execute any adapted exploit with process-level concurrency
- crawler for baidu and zoomeye
- a simple webshell manager
- some built-in exploits (automated)
- more to come...


## requirements

- GNU/Linux or MacOS, WSL (Windows Subsystem Linux), fully tested under [Kali Linux (Rolling, 2017)](https://www.kali.org), Ubuntu Linux (16.04 LTS) and Fedora 25 (it will work on other distros too as long as you have dealt with all deps)
- `proxychains4` (in `$PATH`), used by exploiter, requires a working socks5 proxy (you can modify its config in `mec.py`)
- Java is required when using Java deserialization exploits, you might want to install `openjdk-8-jre` if you haven't installed it yet
- python packages (not complete, as some third-party scripts might need other deps as well):
    - `requests`
    - `bs4`
    - `beautifulsoup4`
    - `html5lib`
    - `docopt`
    - `pip3 install` on the go
- **note** that you have to install all the deps of your exploits or tools as well


## usage

- just run `mec.py`, if it complains about missing modules, install them
- if you want to add your own exploit script (or binary file, whatever):
    - `cd exploits`, `mkdir <yourExploitDir>`
    - your exploit should take the last argument passed to it as its target, dig into `mec.py` to know more
    - `chmod 755 <exploitBin>` to make sure it can be executed by current user
    - use `attack` command then `m` to select your custom exploit
- type `help` in the console to see all available features
