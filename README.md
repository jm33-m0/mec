# massExploitConsole
a collection of hacking tools with a cli ui

 [![Bless](https://cdn.rawgit.com/LunaGao/BlessYourCodeTag/master/tags/bacon.svg)](http://lunagao.github.io/BlessYourCodeTag/)

> take a look at [mec-ng](https://github.com/jm33-m0/mec-ng "new mec, written in Go")

## screenshot

![attack](/screenshot/main.jpg)
![zoomeye](/screenshot/zoomeye.jpg)


## disclaimer

- please use this tool only on **authorized systems**, im not responsible for any damage caused by users who ignore my warning
- exploits are adapted from other sources, please refer to their author info
- please note, due to my limited programming experience (it's my first Python project), you can expect some silly bugs


## features

- [x] an easy-to-use cli ui
- [x] execute any adpated exploits with **process-level concurrency**
- [x] some built-in exploits (automated)
- [x] hide your ip addr using `proxychains4` and `ss-proxy` (built-in)
- [x] zoomeye host scan (10 threads)
- [x] a simple baidu crawler (multi-threaded)
- [x] censys host scan
- [x] built-in ssh bruteforcer

## getting started

```bash
git clone --depth=1 https://github.com/jm33-m0/massExpConsole.git && \
cd massExpConsole && \
python3 ./install.py
```

- mec is installed under `~/.mec`
- [register an account](https://www.zoomeye.org) for zoomeye
- type `proxy` command to run a pre-configured [Shadowsocks](https://github.com/shadowsocks/go-shadowsocks2) socks5 proxy in the background (socks5 on port 1099), `vim ~/.mec/data/ss.json` to edit proxy config. and, `ss-proxy` exits with `mec.py`


## requirements

- `install.py` supports Ubuntu, Debian, Kali, Linux Mint, Fedora, CentOS, RHEL, Arch. for CentOS/RHEL, you might need to manually configure python3 environment before installing
- Python 3.6 or later
- `proxychains4` (in `$PATH`)
- Java is required when using Java deserialization exploits
- **note** that you have to install all the deps of your exploits or tools as well


## usage

- just run `mec` after having it installed
- if you want to add your own exploit script (or binary file, whatever):
    - `cd exploits`, `mkdir <your_exploit_dir>`
    - your exploit should take the last argument (`sys.argv[-1]`) passed to it as its target, dig into `mec.py` to know more
    - `chmod +x <exploit>` to make sure it can be executed by current user
    - use `attack` command then `m` to select your custom exploit
- type `help` in the console to see all available features
- `zoomeye` requires a valid user account config file `zoomeye.conf`


## how to contribute

- if you had any issues, please report them to *[https://github.com/jm33-m0/massExpConsole/issues](https://github.com/jm33-m0/massExpConsole/issues)*
- open a pull request when you have fixed any bugs or added any features
- i would appreciate you adding your own adapted exploits to this repo
