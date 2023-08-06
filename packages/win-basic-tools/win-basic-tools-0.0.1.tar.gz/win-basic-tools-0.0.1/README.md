# win-basic-tools

Description:
This repository intends to give some simple commands to Windows cmd.exe and Powershell(not yet) for better interoperability to WSL users.

## Installation

It is intended for the global Python Env.
Use the package manager [pip](https://pip.pypa.io/en/stablw/) to install win-basic-tools

~~~bash
$ pip install win-basic-tools
~~~

## Usage

### Windows

~~~bash
$ win-basic-tools
~~~

Run for setting the macros file for your cmd.exe. It will create the `.macros.doskey` at your home directory and add it to the Registry.
This will create the alias to the `win_basic_tools/sources/` resources and to some of the CLI commands present on Windows as the most commom Unix commands. Especially useful for WSL users that need an single command syntax between systems.

After refreshing your prompt, you can use `ls`, `ll`, `which`. See `$HOME/.macros.doskey` for the list of aliases.

### Unix

Although this package is mainly intended for Windows, the resources in `win_basic_tools/sources` can be used in any system that runs Python3.8+


## License

[MIT](https://choosealicense.com/licenses/mit/)
