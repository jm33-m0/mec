# massExploitConsole
a collection of tools with a cli ui


## screenshot

![](/screenshot/main.png)


## disclaimer

- please use this tool only on **authorized systems**, im not responsible for any damage caused by users who ignore my warning
- **i do not own** the code of adapted exploits or tools
- exploits are adapted from other sources, please refer to their author info
- please **note**, due to my limited programming experience (it's my first Python project), you can expect some silly bugs


## what does it do?

- an easy-to-use cli ui
- execute any adpated exploits with **process-level concurrency**
- some built-in exploits (automated)
- hide your ip addr using `proxychains4` and `ss-proxy` (built-in)
- zoomeye host scan (10 threads)
- google page crawler with gecko and firefox (not fully working)
- a simple baidu crawler (multi-threaded)
- more to come...


## getting started

```bash
git clone https://github.com/jm33-m0/massExpConsole.git
cd massExpConsole
./mec.py
```

- if you ran `mec.py` and saw missing python modules, please run `pip3 install -r requirements.txt` (if anything is not listed, please report)
- now you should be good to go
- install any dependencies
- type `proxy` command to run a pre-configured [Shadowsocks](https://github.com/shadowsocks/shadowsocks-go) socks5 proxy in the background, `vim ./data/ss.json` to edit proxy config. and, `ss-proxy` exits with `mec.py`


## requirements

- GNU/Linux or MacOS, WSL (Windows Subsystem Linux), fully tested under [Kali Linux (Rolling, 2017)](https://www.kali.org), Ubuntu Linux (16.04 LTS) and Fedora 25 (it will work on other distros too as long as you have dealt with all deps)
- Python 3.5 or later (or something might go wrong, [https://github.com/jm33-m0/massExpConsole/issues/7#issuecomment-305962655](https://github.com/jm33-m0/massExpConsole/issues/7#issuecomment-305962655))
- `proxychains4` (in `$PATH`), used by exploiter, requires a working socks5 proxy (you can modify its config in `mec.py`)
- Java is required when using Java deserialization exploits, you might want to install `openjdk-8-jre` if you haven't installed it yet
- python packages can be found in `requirements.txt` (not complete, as some third-party scripts might need other deps as well)
- **note** that you have to install all the deps of your exploits or tools as well


## usage

- just run `mec.py`, if it complains about missing modules, install them
- if you want to add your own exploit script (or binary file, whatever):
    - `cd exploits`, `mkdir <your_exploit_dir>`
    - your exploit should take the last argument passed to it as its target, dig into `mec.py` to know more
    - `chmod +x <exploit>` to make sure it can be executed by current user
    - use `attack` command then `m` to select your custom exploit
- type `help` in the console to see all available features
- `zoomeye` requires a valid user account config file `zoomeye.conf`


## how to contribute

- if you had any issues, please report them to *[https://github.com/jm33-m0/massExpConsole/issues](https://github.com/jm33-m0/massExpConsole/issues)*
- **report any unhandled exceptions** you encounter, 'coz i haven't fully tested it
- open a pull request when you have fixed any bugs or added any features
- i would appreciate you adding your own adapted exploits to this repo
- any suggestions are welcomed
