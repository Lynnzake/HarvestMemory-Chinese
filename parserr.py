opcodes = { # Opcodes are keys, number of operands(操作数) are values.
    'harvest': 1,
    'plant': 1,
    'peek': 2,
    'poke': 2,
    'goto': 1,
    'ifequal': 3,
    'ifless': 3,
    'ifmore': 3,
    'add': 3,
    'sub': 3,
    'mult': 3,
    'div': 3,
    'mod': 3,
    'random': 3
}

class Instruction(object):
    def __init__(self, token=None, operands=None):
        self.token = token
        self.operands = operands

class Operand(object):
    def __init__(self, token=None, opType=None, prefixed=None):
        self.token = token
        self.type = opType
        self.prefixed = prefixed

class Parser(object):
    def __init__(self, name=None, code=None):
        self.input = code
        self.filename = name
        self.lineNumber = None
        self.labels = {}
        self.instructions = []
    
    def parser(self):
        #把源代码全部转小写，方便后面处理
        self.input = self.input.lower()
        #把代码按行分割好，存放在lines中(lines是个list)
        lines = self.input.split('\n')
        
        for index, line in enumerate(lines, start=1):
            #目前是第几行
            self.lineNumber = index
            #delete whitespace
            line = line.split(';')[0].lstrip()
            print("字符行流解析: {}".format(line))
            #将当前行分解成 token 存在 tokens中，tokens是个list
            #省去re匹配，而且按照原作者这里的做法‘more fast’。具体我也不知道为什么更加快
            tokens = line.replace(',', ' ').replace('\t', ' ').replace('\r', ' ').split(' ')
            print("tokens: {}".format(tokens))   
            #前半句很简单，后半句是去掉空格
            if len(tokens) == 0 or tokens[0] == ' ':
                continue
            #第一个token是标号(label)的情况
            elif ':' in tokens[0]:
                label = tokens[0].split(':')[0]
                if label not in self.labels:
                    #trick
                    self.labels[label] = len(self.instructions)
                print('标签(label)生成: {}'.format(self.labels))
            
            #第一个token是操作码的情况
            elif tokens[0] in opcodes:
                self.instructions.append(self.parserInst(tokens))
            else:
                print('无法识别的指令: {}'.format(tokens[0]))
            print('---------------------------------------------------')
         
        return

    def parserInst(self, tokens):
        inst =  tokens[0]
        expectOperdCount = opcodes[inst] #expectOperdCount ---Operand Count
        operands = []

        for i in range(1, len(tokens)): #原代码的bug，已经改正
            t = tokens[i]
            if t == '':
                continue

            addr = False
            #立即数
            if t[0] == '$':
                addr = True
                t = t[1:]
            
            #label, int, reg
            if self.isReg(t):
                operands.append(Operand(t, 'REG', addr))
            elif self.isInt(t):
                operands.append(Operand(t, 'INT', addr))
            else:
                if (inst == 'goto' or inst == 'ifequal' or inst == 'ifmore' or inst == 'ifless') and addr == False:
                    operands.append(Operand(t, "LABEL", False))
                else:
                    print('无法识别的指令或标签: {}'.format(t))

        if expectOperdCount != len(operands):
            print('指令 {} 需要 {} 个操作数, 您只写了：{}个'.format(inst, expectOperdCount, len(operands)))
            print('您已经写下的操作数为: {}'.format(operands))


        print('已经识别的指令和操作码为：{} ; {}'.format(inst,operands))
        return Instruction(inst, operands)    
        
    def isReg(self, str):
        if len(str) == 2 and str[0] == 'r':
            if str[1] == '0' or str[1] == '1' or str[1] == '2' or str[1] == '3'  or str[1] == 's' or str[1] == 'w' or str[1] == 't' or str[1] == 'f':
                 return True
        return False

    def isInt(self, str):
        if len(str) >= 2 and (str[0] == '+' or str[0] == '-'):
            return str[1:].isdigit()
        return str.isdigit()             

if __name__ == '__main__':
    pass
    