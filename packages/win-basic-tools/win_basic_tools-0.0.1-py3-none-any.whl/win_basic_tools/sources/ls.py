import sys
import os
import stat
import time
from colorama import Fore, Style, init, deinit

class Ls:
    '''Docstring for Ls. This is a simple Python class for listing the content of a directory.
    The sole purpose is giving portability to the common ls command to Windows systens'''
    
    just = 6

    def __init__(self, opt='', path='.') -> None:
        
        if not opt:
            self.opt, self.path = opt, path
        elif opt.startswith('-'):
            self.opt, self.path = opt, path
        else:
            self.opt, self.path = '', opt

    def echo(self) -> None:  
        try:
            with os.scandir(self.path) as dir:
                dir = sorted(dir, key=lambda x: (x.stat().st_mode, x.name))

                if 'l' in self.opt:
                    for i in dir:
                        if i.name.startswith('.') and 'a' not in self.opt: continue
                        print(
                            self.colorful_permissions(stat.filemode(i.stat().st_mode), 'c' in self.opt),
                            time.strftime('%d %b %y %H:%M', time.localtime(i.stat().st_ctime)),
                            self.human_color(self.humanize(i), 'c' in self.opt).rjust(self.just),
                            self.type_color(i, 'c' in self.opt), sep='   ')
          
                else:
                    print(*[self.type_color(i, 'c' in self.opt) for i in dir \
                        if not i.name.startswith('.') or 'a' in self.opt], sep='   ') 
            
        except PermissionError:
            print(Fore.RED + "This process doesn't have the permissions to list this directory" + Style.RESET_ALL)
            
        finally:
            deinit() ; quit()


    def type_color(self, i: os.DirEntry, colors: bool) -> str:
        if not colors:
            return i.name

        if i.is_symlink():
            return Fore.CYAN + i.name + Fore.LIGHTBLACK_EX + ' --> ' + os.path.realpath(i.path) + Style.RESET_ALL
        elif i.is_dir():
            return Fore.LIGHTBLUE_EX + i.name + Style.RESET_ALL
        else:
            if i.name.endswith(('.zip', '.exe', '.msi', '.dll', '.bat', '.sys', '.log')):
                return Fore.YELLOW + i.name + Style.RESET_ALL
            if i.name.endswith(('.py', 'pyx', 'pyd')):
                return Fore.GREEN + i.name + Style.RESET_ALL
            if i.name.endswith(('.tmp')):
                return Fore.LIGHTBLACK_EX + i.name + Style.RESET_ALL
            return i.name

    def humanize(self, i: os.DirEntry):
        if i.is_dir():
            return '-'

        entry = i.stat().st_size 
        units = ('k', 'M', 'G')
        final = ''
        
        for unit in units:
            if entry >= 1024:
                entry /= 1024
                final = unit
            else:
                break
        
        if entry:
            if final:
                return f'{entry:.1f}{final}'
            return str(entry)
        return '-'
    
    def human_color(self, data: str, colors: bool) -> str:
        if not colors: return data
        
        self.just = 15

        if 'G' in data:
            return Fore.RED + data + Style.RESET_ALL
        elif 'M' in data:
            return Fore.LIGHTRED_EX + data + Style.RESET_ALL
        elif 'k' in data:
            return Fore.LIGHTYELLOW_EX + data + Style.RESET_ALL
        else:    
            return Fore.WHITE + data + Style.RESET_ALL

    
    def colorful_permissions(self, data: os.stat_result.st_mode, colors: bool) -> str:
        if not colors:
            return data
        
        lis = list(data)
        lis.insert(-3, Fore.LIGHTRED_EX)
        lis.insert(4, Fore.LIGHTYELLOW_EX)
        lis.insert(1, Fore.LIGHTGREEN_EX)
        if lis[0] == 'd': lis.insert(0, Fore.LIGHTBLUE_EX)
        lis.append(Style.RESET_ALL)

        return ''.join(lis)


def main():
    init()

    args = sys.argv[1:]

    #verificar caso haja portabilidade para unix
    if len(args) > 2: args = args[:2] ; print(f'Ignored {sys.argv[3:]} parameters') 

    if args: obj = Ls(*args)
    else: obj = Ls()
    
    obj.echo()
    deinit()  


if __name__ == '__main__':
    main()