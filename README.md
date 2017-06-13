# massExploitConsole - Windows
a collection of tools with a cli ui

## screenshot

![](/screenshot/main.png)

## known issues

- `exploits` command gives irrelevent results because of different exec permission setting in Windows
- some *nix related stuff might not work, ive fixed some, but do expect more bugs

## disclaimer

- please use this tool only on **authorized systems**, im not responsible for any damage caused by users who ignore my warning
- **i do not own** the code of adapted exploits or tools
- exploits are adapted from other sources, please refer to their author info


## what does it do?

- an easy-to-use user interface (cli)
- execute any adapted exploit with process-level concurrency
- crawler for baidu
- zoomeye api crawler
- google crawler using gecko driver
- some built-in exploits (automated)
- more to come...


## requirements

- `proxychains4` (in `$PATH`), used by exploiter, requires a working socks5 proxy (you can modify its config in `mec.py`)
- Python2.7+ and Python3.5+
- Java is required when using Java deserialization exploits
- python packages can be installed via `python3 -m pip install -r requirements.txt`(not complete, as some third-party scripts might need other deps as well)


## usage

- just run `mec.py`, if it complains about missing modules, install them
- if you want to add your own exploit script (or binary file, whatever):
    - `cd exploits`, `mkdir <dir of your exploit>`
    - your exploit should take the last argument passed to it as its target, dig into `mec.py` to know more
    - make sure your exploit can be directly executed by system, or you have to modify `mec.py` a little bit
    - if your exploits were some scripts, make sure py3 scripts have their filenames end with `-3.py`
    - use `attack` command then `m` to select your custom exploit
- type `help` in the console to see all available features
