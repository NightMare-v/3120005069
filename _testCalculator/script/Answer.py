import functools
import re
from fractions import Fraction
import os

class Answer:
# 用于生成任何题目文件的结果到Answers.txt中的类

    def __init__(self, FileName):
        self.file = FileName
        self.OpenAFile()

    def mul_divOperation(self, s):
        sub_str = re.search('(\d+\.?\d*[*/]-?\d+\.?\d*)', s)
        while sub_str:
            sub_str = sub_str.group()
            if sub_str.count('*'):
                l_num, r_num = sub_str.split('*')
                s = s.replace(sub_str, str(int(l_num) * int(r_num)))
            else:
                break
            sub_str = re.search('(\d+\.?\d*[*/]\d+\.?\d*)', s)
        return s

    def add_minusOperation(self, s):
        s = '+' + s
        # 寻找 x/x/ 格式，即需要除法运算
        if  re.search('[+\-]\d+\.?\d*[*/]-?\d+\.?\d*[/]', s):
            add1 = 0
            if re.findall('\d+\.?\d*[+\-]',s):
                add1 = re.findall('[+\-]\d+\.?\d*',s)[0]
            sub_str = re.findall('[+\-]\d+\.?\d*[*/]-?\d+\.?\d*[*/]\d+\.?\d*[*/]\d+\.?\d*', s)  # 将触发运算的双方提取出来
            if len(sub_str) == 0:   # 若后半为整数的特例情况
                sub_str = re.findall('[+\-]\d+\.?\d*[*/]-?\d+\.?\d*[*/]\d+\.?\d*', s)[-1]
                sub_str = sub_str + '/1'
            sub_str=''.join(sub_str) # 转化为字符串
            l_num = re.match('[+\-]\d+\.?\d*[*/]-?\d+\.?\d*',sub_str).group() # 取左边的值
            if sub_str.count('*')>=2:
                return '0'
            r_num = sub_str.split('/',2)[2] # 取分割右边的值
            # 处理 l_num 的乘法
            mul2 = 0
            if re.search('\*',l_num):
                mul2=l_num.split('*')[-1]
                l_num=l_num.split('*')[0]
                l_num = int(mul2)*int(l_num)
            l_num = Fraction(l_num)
            # 处理 r_num 的乘法
            mul1 = 0
            if re.search('\*',r_num):
                mul1=r_num.split('*')[-1]
                r_num=r_num.split('*')[0]
            r_num = Fraction(r_num)
            s = str(Fraction(l_num,r_num) * int(mul1) + int(add1) )
            return s
        # 无除法无分数情况
        if not re.search('/',s):
            tmp = re.findall('[+\-]\d+\.?\d*', s)
            s = str(functools.reduce(lambda x, y: int(x) + int(y), tmp))
            if re.search('\+', s):
                s = s.replace('+', '')
            return s
        # 存在分数后的乘法计算
        if s.count('*'):
            l_num = 0
            r_num = 0
            if s.count('*')>=2:
                return '0'
            if  re.search('[*]\d+\.?\d*[*]\d+\.?\d*',s):
                mul2=re.findall('[*]\d+\.?\d*[*]\d+\.?\d*',s)
                mul2=''.join(mul2)
                mul2=mul2[1:]
                mul_l,mul_r=mul2.split('*')
                mul2=int(mul_l)*int(mul_r)
                mul2='*'+ str(mul2)
                s = re.sub(r'[*]\d+\.?\d*[*]\d+\.?\d*',mul2,s)
            l_num, r_num = s.split('*')
            if r_num.count('/')>=2:
                return '0'
            add1=0
            add2=0
            if re.search('\d+\.?\d*[+\-]',l_num):
                add2 = re.findall('[+\-]\d+\.?\d*',l_num)[0]
                l_num = re.findall('[+\-]\d+\.?\d*[/]\d+\.?\d*', l_num)[0]
            if re.search('\d+\.?\d*[+\-]',r_num):
                add1 = re.findall('[+\-]\d+\.?\d*',r_num)[0]
                r_num = re.findall('\d+\.?\d*', r_num)[0]
            s = s.replace(s, str(Fraction(l_num) * Fraction(r_num) + int(add1) + int(add2)))
            return s
        # 分数的加法
        fra1 = re.findall('[+\-]\d+\.?\d*[*/]-?\d+\.?\d*', s)
        # 在字符串中剔除检测出的分数
        for i in range(0,len(fra1)):
            s = s.replace(fra1[i],'')
        tmp = re.findall('[+\-]\d+\.?\d*', s)
        # 无分数list tmp 中求和
        total = 0
        for i in range(0,len(tmp)):
            total = int(tmp[i]) + total

        # total与分数求和
        for i in range(0,len(fra1)):
            total = Fraction(fra1[i]) + total

        # 可以化为真分数
        # total = float(total)
        s = str(total)
        return s

# 分类计算类型
    def compute(self, formula):
        formula = self.mul_divOperation(formula)
        formula = self.add_minusOperation(formula)
        return formula

    def calc(self, formula):
        """计算程序入口"""
        if (formula[0] == '(' and formula[len(formula) - 1] == ')'):
            formula = formula.replace('(', '')
            formula = formula.replace(')', '')
        formula = re.sub('[^.()/*÷\-+0-9]', "", formula)  # 清除非算式符号
        dotIndex=formula.index('.')
        print(formula)
        if (formula[dotIndex] == '.'):
            formula = formula.replace(formula[0:dotIndex+1], '')  # 计算含有题目序列号的标准算式
        has_parenthesise = formula.count('(')
        while has_parenthesise:
            sub_parenthesise = re.search('\([^()]*\)', formula)  # 匹配最内层括号
            if sub_parenthesise:
                formula = formula.replace(sub_parenthesise.group(), self.compute(sub_parenthesise.group()[1:-1]))
            else:
                has_parenthesise = False
        ret = self.compute(formula)
        return ret

    def Transfer(self, formula):
        '这是一个把小数字符串转换成分数的函数'
        i = formula.find('.')
        if (i != -1 and formula.find('-') == -1):  # 如果存在小数点，只取小数点后三位
            e = float(formula[0:i + 4])
            intE = int(e)
            term = round(e - intE, 4)  # 小数部分四舍五入
            if (term == 0): return formula[:i]
            termD = term * 1000
            Deno = 1000
            if (termD % 333 == 0): Deno = 999  # 优化小学生算术题中常出现的1/3
            while (termD != Deno):  # 求最大公约数以化简
                if (Deno > termD): Deno = Deno - termD
                if (termD > Deno): termD = termD - Deno
            term = int(term * 1000 / termD)
            Deno = int(1000 / termD)
            if (intE != 0): answers = [str(intE), '\'', str(term), '/', str(Deno)]
            if (intE == 0): answers = [str(term), '/', str(Deno)]
            answers = ''.join(answers)
            return answers
        else:
            return formula

# 读取文件的函数
    def OpenAFile(self):
        fileE = open(self.file, "r+", encoding='utf-8')
        string = fileE.read()
        fileE.close()
        string = string.replace('÷', '/')
        out = ""
        for line in string.splitlines():
            # out = out + self.compute(line) + '\n'
            out = out.replace('+', '')
            out = out + self.Transfer(self.calc(line)) + '\n'
        fileA = open("Answers.txt", "w+")
        print('生成答案结束，文件名为Answer.txt')
        print(out, file=fileA)
        fileA.close()
