import sys, easygui

if __name__ == '__main__':
    path = easygui.diropenbox(default=f"C:\\")
    sys.stdout.write(path)