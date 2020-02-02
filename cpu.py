import random
opcodes = {
    #操作码和对应的步长
    'harvest': 5,
    'plant': 4,
    'peek': 4,
    'poke': 3,
    'goto': 1,
    'ifequal': 2,
    'ifless': 2,
    'ifmore': 2,
    'add': 3,
    'sub': 3,
    'mult': 5,
    'div': 8,
    'mod': 7,
    'random': 6    
}

indirectTicks = 2 # 立即数的步长
harvestError = 15 # 指令错误的步长

valLimit = 2**16 # 寄存器和内存的值都是32bit的

class CPU(object):
    def __init__(self, memory=None, fruit=None, players=None):
        self.memory = memory
        self.players = players
        self.fruit = fruit
        self.ticks = 0
        self.next = 0
        self.registers = {'rw': 0, 'rt': 0}
    
    #主要函数，每一个指令其实是调用了self.run()函数
    def execute(self):
        nextPlayer = self.players[self.next] #players是list，里面放着所有的player
        if nextPlayer.delay == 0:
            try:
                self.run(nextPlayer)
            except Exception as e:
                print("由于用户: {},导致了{}".format(nextPlayer.displayName, e))
        else:
            nextPlayer.delay -= 1

        self.next += 1 
        if self.next == len(self.players):
            self.next = 0
        
        for f in self.fruit:
            self.memory[f] -= 1
            if self.memory[f] < -100:
                self.memory[f] = -100 
        
        self.registers['rt'] = self.ticks
        self.registers['rw'] = max(p.registers['rs'] for p in self.players)

    def getMemValue(self, player, addr):
        if addr < 0 or addr > len(self.memory): #越界检查
            player.registers['rf'] = 5
            return 0
        return self.memory[addr]
    
    def plantMem(self, player, addr):
        if addr < 0 or addr > len(self.memory): #越界检查
            player.registers['rf'] = 5
            return 
        if self.getMemValue(player, addr) < 0:
            self.fruit.remove(addr)

        self.memory[addr] = -1
        self.fruit.add(addr)

    def setMemValue(self, player, addr, val):
        if addr < 0 or addr > len(self.memory): #越界检查
            player.registers['rf'] = 5
            return 
        #fruit状态更新
        if self.getMemValue(player, addr) < 0:
            self.fruit.remove(addr)
        
        if val >= 0 and val <= valLimit:
            self.memory[addr] = val
        elif val < 0:
            self.memory[addr] = val % (valLimit - 1)
            player.registers['rf'] = 3
        elif val > valLimit:
            self.memory[addr] = val % (valLimit - 1)
            player.registers['rf'] = 4
    
    def getReg(self, player, reg):
        val = 0 
        if reg in player.registers:
            val = player.registers[reg]
        elif reg in self.registers:
            val = self.registers[reg]
        return val

    def setReg(self, player, reg, val):
        if reg == 'r0' or reg == 'r1' or reg == 'r2' or reg == 'r3':
            if val > -valLimit and val < valLimit:
                player.registers[reg] = val
            elif val < -valLimit:
                player.registers[reg] = val % (valLimit - 1)
                player.registers['rf'] = 1
            elif val > valLimit:
                player.registers[reg] = val % (valLimit - 1)
                player.registers['rf'] = 2
        else:
            player.registers['rf'] = 10
    
    def getAddr(self, player, op):
        addr = -1
        if op.type == "INT":
            addr = int(op.token)
        elif op.type == "REG":
            addr = self.getReg(player, op.token)
        return addr
    
    def getValue(self, player, op):
        val = -1
        if op.type == "INT":
            val = int(op.token)
        elif op.type == "REG":
            val = self.getReg(player, op.token)
        
        if op.prefixed:
            val =  self.getMemValue(player, val)
        
        return val
    
    def gotoLabel(self, player, label):
        if label in player.labels:
            player.next = player.labels[label]  - 1
        else:
            player.registers['rf'] = 7
            print('{} failer goto {}'.format(player.displayname, label))
        
    
    def run(self, player):
        #检查player的程序是否完结
        if player.next >= len(player.instructions):
            return
        #得到一行源程序，比如：harvest r0
        inst = player.instructions[player.next]
        #操作码，就是harvest
        op = inst.token
        #操作数，就是r0
        operands = inst.operands
        #获取当前指令的步长
        dTicks = opcodes[op]
        #重置错误寄存器
        player.registers['rf'] = 0


        if op == 'harvest':
            addr = self.getAddr(player, operands[0])
            if self.getMemValue(player, addr) == -100:
                self.setMemValue(player, addr, 0)
                player.registers['rs'] += 5
            else:
                dTicks += harvestError
                player.registers['rf'] = 9
            
        elif op == "plant":
            #print(player.displayName + " is planting!")

            if player.registers['rs'] > 0:
                addr = self.getAddr(player, operands[0])
                #self.setMemoryValue(player, addr, -1)
                self.plantMem(player, addr)
                player.registers['rs'] = player.registers['rs'] - 1
            else:
                player.registers['rf'] = 8

        elif op == "peek":
            addr = self.getAddr(player, operands[1])
            self.setRegister(player, operands[0].token, addr)

        elif op == "poke":
            val = self.getValue(player, operands[1])
            addr = self.getAddr(player, operands[0])
            self.setMemValue(player, addr, val)

        elif op == "goto":
            self.gotoLabel(player, operands[0].token)

        elif op == "ifequal":
            val1 = self.getValue(player, operands[0])
            val2 = self.getValue(player, operands[1])
            if val1 == val2:
                self.gotoLabel(player, operands[2].token)
                
        elif op == "ifless":
            val1 = self.getValue(player, operands[0])
            val2 = self.getValue(player, operands[1])
            if val1 < val2:
                self.gotoLabel(player, operands[2].token)

        elif op == "ifmore":
            val1 = self.getValue(player, operands[0])
            val2 = self.getValue(player, operands[1])
            if val1 > val2:
                self.gotoLabel(player, operands[2].token)

        elif op == "add":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setReg(player, operands[0].token, val1+val2)

        elif op == "sub":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setReg(player, operands[0].token, val1-val2)

        elif op == "mult":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setReg(player, operands[0].token, val1*val2)

        elif op == "div":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            if val2 == 0:
                player.registers['rf'] = 10
            else:
                self.setReg(player, operands[0].token, val1//val2)

        elif op == "mod":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setReg(player, operands[0].token, val1%val2)

        elif op == "random":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setReg(player, operands[0].token, random.randint(val1, val2+1)) 

        else: # Should never happen.
            pass

        for o in operands:
                if o.prefixed:
                    dTicks += indirectTicks
        
        #步长(ticks)的作用就是用于这里
        self.ticks += dTicks
        player.delay = dTicks
        #执行完该条指令，将next加1以执行下一条指令
        player.next += 1