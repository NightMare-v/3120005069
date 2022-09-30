import re

class Verify:
    '这是一个用于修正有负数结果的式子，判断式子是否有重复，以及生成题目序号的类,判断/后面有没有0'

    # 筛选出等式中的符号
    def __init__(self, FileName):
        self.file = FileName
        self.VerifyAFile()

    def VerifyAFile(self):
        No = 1
        with open(self.file) as r:
            lines = r.readlines()
        with open('StandExercises.txt', 'w', encoding='utf-8') as w:
            for l in lines:
                s = l
                s = s.replace('÷', '/')
                if ((self.math_compute(s) == 1)):
                    position = re.search('\Z', l).end()
                    l = l.replace(l[position - 1], ' = \n')
                    l = str(No) + '. ' + l
                    w.write(l)
                    No += 1
        r.close()
        w.close()

    def filt_sym(self, e1_fs):
        sym_get = ""
        for sym in e1_fs:
            if sym == '+' or sym == '-' or sym == '*' or sym == '/':
                sym_get = sym_get + sym
        return sym_get

    # 筛选出等式中的数字
    def filt_num(self, e1_fn):
        num_get = []
        num_c = ""
        # print(e1_fn)
        for num in e1_fn:
            if num != '+' and num != '-' and num != '*' and num != '/':
                flag = 1
                num_c += num
            else:
                flag = 0
            if flag == 0:
                # print(num_c)
                num_get = num_get + [float(num_c)]
                num_c = ""
        num_get = num_get + [float(num_c)]
        return num_get

    # 判断优先级
    def judge_pri(self, sym_int):
        i = 0
        sym_p = []
        for sym_jp in sym_int:
            if sym_jp == '/':
                sym_p += [40 + i]
                i += 1
            elif sym_jp == '*':
                sym_p += [30 + i]
                i += 1
            else:
                i += 1
        i = 0
        for sym_jp in sym_int:
            if sym_jp == '-':
                sym_p += [20 + i]
                i += 1
            elif sym_jp == '+':
                sym_p += [10 + i]
                i += 1
            else:
                i += 1
        return sym_p

    # 等式运算计算细节实现
    def int_compute(self, num_int, sym_int):
        sym_p_int = self.judge_pri(sym_int)
        while sym_p_int != []:
            sym = int(sym_p_int[0])
            if sym >= 40:
                if num_int[sym - 40 + 1] == 0:
                    return -1
                num_int[sym - 40] /= num_int[sym - 40 + 1]
                num = num_int[sym - 40: sym - 40 + 1]
                del num_int[sym - 40 + 1: sym - 40 + 2]
                sym_int = sym_int[:sym - 40] + sym_int[sym - 40 + 1:]
            elif sym >= 30:
                num_int[sym - 30] *= num_int[sym - 30 + 1]
                num = num_int[sym - 30: sym - 30 + 1]
                del num_int[sym - 30 + 1: sym - 30 + 2]
                sym_int = sym_int[:sym - 30] + sym_int[sym - 30 + 1:]
            elif sym >= 20:
                num_int[sym - 20] -= num_int[sym - 20 + 1]
                num = num_int[sym - 20: sym - 20 + 1]
                if num[0] < 0:
                    return -1
                del num_int[sym - 20 + 1: sym - 20 + 2]
                sym_int = sym_int[:sym - 20] + sym_int[sym - 20 + 1:]
            elif sym >= 10:
                num_int[sym - 10] += num_int[sym - 10 + 1]
                num = num_int[sym - 10: sym - 10 + 1]
                del num_int[sym - 10 + 1: sym - 10 + 2]
                sym_int = sym_int[:sym - 10] + sym_int[sym - 10 + 1:]
            sym_p_int = self.judge_pri(sym_int)
        return float(num[0])

    # 等式运算
    def compute_c(self, e1):
        num_int = float()
        num_int = self.filt_num(e1)
        sym_int = self.filt_sym(e1)
        flag = self.int_compute(num_int, sym_int)
        if flag < 0:
            return 'f'
        else:
            return str(flag)

    # 将等式中括号里面的等式提取出来
    def judge_bracket(self, equ_j):
        left = equ_j.rfind('(')
        right = equ_j.find(')', left)
        e1 = equ_j[left + 1:right]
        c1 = self.compute_c(e1)
        if c1 == 'f':
            return False
        equ_j = equ_j[0:left] + str(c1) + equ_j[(left + len(c1)):]
        equ_j = equ_j[0: left + len(str(c1))] + equ_j[right + 1:]
        return equ_j

    def math_compute(self, equation):
        equ_m = equation
        while equ_m.find('(') != -1:
            if equ_m.find('(') != -1:
                equ_m = self.judge_bracket(equ_m)
                if not equ_m:
                    break;
            else:
                break
        if not equ_m:
            return 0
        elif equ_m.find('+') != -1 or equ_m.find('-') != -1 or equ_m.find('*') != -1 or equ_m.find('/') != -1:
            val = self.compute_c(equ_m)
            if val == 'f':
                return 0
            else:
                return 1
        else:
            return 1
