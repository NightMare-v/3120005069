import time
import sys
import os
pid = os.getpid()
print('pid: ', pid)

sys.path.append(os.path.realpath("."))

from script.Generate import Generate
from script.Verify import Verify
from script.Answer import Answer
from script.Judge import Judge
from optparse import OptionParser

usage = "[<-n> + 数字] 确定题目条数 [<-r> + 数字] 确定数字范围 \n 可选参数: \n [<-a> + (filename)] 回答filename文件的题目 \n [<-e> + (filename)] 批改filename文件的题目"
parser = OptionParser() # usage
# parser.print_help()
parser.add_option("-n", action='store', type='int', dest='Numbers', help="生成Numbers条无负数结果的算式,输出文件是StandExercises.txt")
parser.add_option("-r", action='store', type='int', dest='Range', help="指定数字Range范围")
parser.add_option("-a", action='store', type='string', dest='AnsFile', help="指定题目文件,并生成答案到Answers.txt")
parser.add_option("-e", action='store', type='string', dest='JudgeFile', help="指定用户答案文件,并将其和标准Answers.txt对比")
options, args = parser.parse_args() # 传入参数与命令

# 以下为测试代码块
# print(options.Numbers, options.Range)
# options.Numbers=30
# options.Range=10
# options.AnsFile='StandExercises.txt'
# options.JudgeFile='Ans.txt'

# options
if options.Numbers is not None and options.Range:
    '生成Numbers条有负数结果的算式, 再将其标准化(去除中间过程有负数结果的算式以及/后面有0的非法算式), 输出文件是StandExercises.txt'
    fileE = Generate(options.Numbers, options.Range)
    fileStand = Verify(fileE.filename)
    print("grenerated")

if options.AnsFile and not options.Numbers:
    '回答-a后面的filename题目文件,并输出结果到Answers.txt文件'
    fileA = Answer(options.AnsFile)

if options.Numbers and options.Range and not options.AnsFile:
    '生成Numbers条有负数结果的算式, 生成文件是Exercises.txt'
    fileE = Generate(options.Numbers, options.Range)

if options.JudgeFile and not options.Numbers and not options.Range:
    '-e 接一个用户的答案文件, 并将其和标准答案文件Answers.txt比较'
    FileA = Judge(options.JudgeFile, "Answers.txt")

if options.Numbers:
    print('program started')

if __name__ == '__main__':
    pass