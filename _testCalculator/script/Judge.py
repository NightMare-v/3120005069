
class Judge:
    '判断Exercises 和 Answers.txt ，并返回处理结果'

    def __init__(self, FileName, FilenameAns):
        self.user_file = FileName
        self.standAns_file = FilenameAns
        self.judge_ans(self.user_file, self.standAns_file)

    def judge_ans(self, user_ans, stand_ans):
        user_a = open(user_ans, 'r')
        std_a = open(stand_ans, 'r')
        i = 0
        c_sum = []
        e_sum = []
        while 1:
            equa_u = user_a.readline()
            equa_s = std_a.readline()
            if not equa_u:
                break
            ind = equa_u.rfind('=')
            if equa_u[ind + 1:].strip() == equa_s.strip():
                i += 1
                c_sum += [i]
            else:
                i += 1
                e_sum += [i]
        print("Correct: ", len(c_sum), c_sum)
        print("Wrong: ", len(e_sum), e_sum)

