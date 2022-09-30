# 生成题目文件的类
import random

class Generate:
    # 将参量代入类中
    def __init__(self, numbers, range):
        'self.numbers 是生成题目总个数, self.range 是数值的范围'
        self.numbers = numbers
        self.range = range
        self.filename = 'Exercises.txt'
        self.Fomulas()

    def GeneralOneFormula(self):
        Range = self.range
        # OperateNumbers = random.randint(1, 3)
        # 用随机数产生随机生成的数
        X1 = int(random.random() * 10000)
        X2 = int(random.random() * 10000)
        # 对生成的数进行一定的处理得到操作数
        OperateNumbers = X1 % 3 + 1
        CountNUmbers = OperateNumbers + 1
        # 录入符号
        Ostyle = ['+', '-', '*', '÷']
        # 生成符号list
        Operates = []
        a = 0
        # 进行一些算法，对生成的数进行处理后得到运算符
        while (a <= OperateNumbers):
            # Operates.append(random.choice(Ostyle))
            if (a == 0):
                Operates.append(Ostyle[X1 % 4])
            if (a == 1):
                Operates.append(Ostyle[X2 % 4])
            if (a == 2):
                Operates.append(Ostyle[(X1 + X2) % 4])
            a += 1
        # 生成数字list与括号list
        Counts = []
        i = CountNUmbers
        while (i > 0):
            X = int(random.random() * 10000) % Range + 1
            if (X % 10 != 1):
                term = str(X)
                Counts.append(term)
            else:
                term = [str(X), '/', str(int(random.random() * 10000) % Range + 1)]
                termT = ''.join(term)
                # 此处插入分数化简
                Counts.append(termT)
            i -= 1
        if ((Operates.count('-') != 0) and (Operates.count('+') != 0) and (
                int(random.random() * 10000) % 7 == 1)):  # 假定1/7的括号生成概率
            leftPosition = int(random.random() * 10000) % OperateNumbers
            rightPosition = random.randint(leftPosition + 2, OperateNumbers + 1) - 1
            # rightPosition = int(random.random() * 10000) % OperateNumbers + 1
            term = '(' + str(Counts[leftPosition])
            Counts[leftPosition] = term
            term = str(Counts[rightPosition]) + ')'
            Counts[rightPosition] = term
        # 合并符号list 数字括号list
        FinalList = []
        j = 0
        k = 0
        i = OperateNumbers + CountNUmbers - 1
        while (i >= 0):
            if (i % 2 != 1):
                FinalList.append(Counts[j])
                j += 1
            else:
                FinalList.append(Operates[k])
                k += 1
            i -= 1
        FinalList = ''.join(FinalList)
        return FinalList

# 写入公式到文档中
    def Fomulas(self):
        Range = self.range
        Numbers = self.numbers
        out = ''
        ' 生成多个Formula并写入文档 '
        with open("Exercises.txt", 'w+') as f :
            for i in range(1, Numbers + 1):
                out = out + self.GeneralOneFormula() + '\n'
            f.write(out)