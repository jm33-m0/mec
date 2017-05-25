# massExploitConsole - Windows
a collection of tools with a cli ui

## screenshot

![](/screenshot/main.png)

## known issues

- `proxychains4` is currently not available, you can compile your own if you want
- some *nix related stuff might not work, ive fixed some, but do expect more bugs
- <s>**NOTE** that `readline` doesn't work on Windows. thus this branch will not work unless you put it into WSL</s> 
- problem solved by using `pyreadline`, <s>but it's nearly **unusable** due to **slowness**</s>
- found the problem with `pyreadline`: `.python_history` is malformed somehow, causing `pyreadline`'s slowness
- windows console doesn't support `colors.UNDERLINE` and `input()` method can't display any colors
- to avoid that, i replaced all `input()` prompt with `print()`, not a perfect solution, though

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

- `proxychains4` (in `$PATH`), used by exploiter, requires a working socks5 proxy (you can modify its config in `mec.py`)
- Java is required when using Java deserialization exploits
- python packages (not complete, as some third-party scripts might need other deps as well):
    - `pyreadline`
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
    - make sure your exploit can be directly executed by system, or you have to modify `mec.py` a little bit
    - use `attack` command then `m` to select your custom exploit
- type `help` in the console to see all available features
