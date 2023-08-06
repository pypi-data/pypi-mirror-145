import os
import platform

def main():
    assert platform.platform().startswith('Windows')

    py_version = platform.python_version()
    py_version = py_version[:py_version.rindex('.')].replace('.','') # '39','310'...
    
    sources_path = os.path.expanduser(f'~/AppData/Local/Programs/Python/Python{py_version}/Lib/site-packages/win_basic_tools/sources')
    home_path = os.path.expanduser('~')

    with open(f'{home_path}\\.macros.doskey', 'w') as file:
        file.write(
            f'''ls=python {sources_path}\\ls.py $1 $2\n
            ll=python {sources_path}\\ls.py -lac\n
            which=python {sources_path}\\which.py $1\n
            cat=type $1\n
            pwd=cd\n
            mv=move $1 $2\n
            rm=del $*\n''')
        
        
    os.system(f'reg add "HKCU\\Software\\Microsoft\\Command Processor" /v Autorun /d "doskey /macrofile=\\"{home_path}\\.macros.doskey\"" /f')

if __name__ == '__main__':
    main()