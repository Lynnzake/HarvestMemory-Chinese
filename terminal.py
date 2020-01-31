__version__ = "0.1"
# Version 0.1:改编自主仓库(graphics.py)，主仓库已经更新到5.0.
# 主仓库使用了GUI，本版本采用终端窗口来作为界面。
# 一来少了tkinter的大量代码，二来本版本只是为了理解核心代码的原理。
# 故而采用终端的界面，代码更加简略。更加有助于理解整个代码的逻辑。
# 2020.01.31
import time, os, sys
# try:
#     import tkinter as tk
# except:
#     import tkinter as tk

##########################################################################
#继承一下就行
class GraphicsError(Exception):
    pass

OBJ_ALREADY_DRAWN = "对象已被描绘"
UNSUPPORTED_METHOD = "对象不支持该操作"
BAD_OPTION = "非法选项"
#
##########################################################################


#全局变量
# _root = tk.Tk()
# _root.withdraw()

# _update_lasttime = time.time()

def update(sec):
    pass
if __name__ == '__main__':
    pass
    