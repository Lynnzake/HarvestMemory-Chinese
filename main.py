import player
import parserr
import cpu
import terminal
import os, random

memorySize = 2**12 #4096
memory = [0] * memorySize #4096
fruit = set() #水果，是一个集合
decay = 0.7 #蔓延系数
initialSeeds = 20 #初始种子值

def initMemory():
    #随机挑选开始的点
    seeds = [] #seed中存放的是随机的内存地址值，一共20个(initialSeeds)
    for i in range(initialSeeds):
        seeds.append(random.randrange(0, memorySize, 1))

    #在内存里添加水果，添加点为随机的点(点的意思其实就是地址)
    #使用一个蔓延机制，0.75^x，从而得到更多的水果(我不明白，为什么不直接加大初始值呢)
    for seed in seeds:
        memory[seed] = -100
        fruit.add(seed)
        chance = decay
        i = 1
        while chance > 0.01:
            #
            rLeft = random.random()
            rRight = random.random()
            if rLeft <= chance:
                if seed-i > 0:
                    memory[seed-i] = -100
                    fruit.add(seed-i)
            if rRight <= chance:
                if seed+i < len(memory)-1:
                    memory[seed+i] = -100
                    fruit.add(seed+i)
            i += 1
            chance = decay**i

    for index, i in enumerate(fruit):
            print('内存初始化{:0>3d}：in addres {:0>12b}'.format(index, i))
    print("一共初始化了{}个水果".format(len(fruit)))
    print('***************************************************')   
    return memory

def createPlayers():
    players = []
    #玩家编写的代码放在./code目录下
    path = os.path.join(os.getcwd(),'code')
    if not os.path.isdir(path):
        print("没有找到代码目录: {}".format(path))
        return None
    #code目录下，一个源程序代表一个player
    for fileName in os.listdir(path):
        
        try:
            with open(os.path.join(path,fileName), 'r') as f:
                code = f.read() #读入所有代码交给parser
                p = parserr.Parser(fileName, code)
                p.parser() #此时已经对源代码处理过了
                players.append(player.Player(fileName.split('.')[0], p.instructions, p.labels))
        except Exception as e:
            print("创建玩家时发生错误: {}".format(e))
        
    random.shuffle(players)
    return players


def updateMemTeminal(vmFruit):
    for i in vmFruit:
        if memory[i] == -100:
            print("找到一个内存水果：{}".format(i))

def updatePlayers(players):
    for i in range(len(players)):
        out = players[i].displayName + ':' + str(players[i].registers['rs'])
        print(out)     

def main():
    initMemory()
    players = createPlayers()
    #打印出所有玩家的名字
    print('当前玩家有: {}'.format([player.displayName for player in players]))
       
    if players == None:
        return
    
    vm = cpu.CPU(memory, fruit, players)
    tty = terminal.Display(vm,players)
    timer = 0
    for i in range(0,12000):
        if vm.ticks < 1000000:
            vm.execute()    
        else:
            break
        timer += 1

        if timer % 1000 == 0: # 定时更新状态
            tty.display()
    tty.display()    
    

if __name__ == '__main__':
    main()
    