__version__ = "0.1"
# Version 0.1:改编自主仓库(graphics.py)，主仓库已经更新到5.0.
# 主仓库使用了GUI，本版本采用终端窗口来作为界面。
# 一来少了tkinter的大量代码，二来本版本只是为了理解核心代码的原理。
# 故而采用终端的界面，代码更加简略。更加有助于理解整个代码的逻辑。
# 2020.01.31
import time
# import os, sys
# try:
#     import tkinter as tk
# except:
#     import tkinter as tk

##########################################################################
#继承一下就行
# class GraphicsError(Exception):
#     pass

OBJ_ALREADY_UPDATE = "对象已更新"
UNSUPPORTED_METHOD = "对象不支持该操作"
BAD_OPTION = "非法选项"
#
##########################################################################


#全局变量
# _root = tk.Tk()
# _root.withdraw()

# _update_lasttime = time.time()

#以下是将原作者的GUI改为CLI
#这一改动使得代码的结构更加简单和清晰
#也使得学习代码的人一开始的难度降低许多
class Display(object):
    def __init__(self, vm:object=None, 
                players:list=None):
        #虚拟机
        self.vm = vm
        #存放玩家的list
        self.players = players
        # self.timeGap = secs
    def display(self):
        print("虚拟机已经执行了{}步".format(self.vm.ticks))
        print("各玩家水果数为: {}".format({self.player.displayName:self.player.registers['rs'] 
            for self.player in self.players}))
        return  
if __name__ == '__main__':
    pass
    