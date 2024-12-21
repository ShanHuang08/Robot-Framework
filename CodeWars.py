from Library.Robot_definition import run, log, log_color, log_hyperlink, use_globals_update_keywords
from Library.BaseFunctions import BaseFunction

class My_CodeWars(BaseFunction):

    def Text_transitionBy_String(self, Text):
        Alstr='abcdefghijklmnopqrstuvwxyz'
        answer=''
        color = self.Ramdom_color()
        log('Test ' + log_color(Text, color, print=False))
        for i in range(len(Text)):
            for j in range(len(Alstr)):
                if i == len(Text)-1 and Text[i].lower() == Alstr[j]:
                    answer+=str(j+1)
                elif Text[i].lower() == Alstr[j]:
                    answer+=str(j+1)+',' 
        log_color(answer, color) 
        return answer

    def smash(self, words):
        # Begin here
        result = ""
        log(f"Test {words}")
        if isinstance(words, list):
            for i in range(len(words)):
                if i != len(words)-1: #如果不是最後一位
                    result = result + words[i] + " "
                else:
                    result = result + words[i]
            log(result)
        else: log_color(f"{type(words)}\nArg data type is not list", "red")
        return result

    def count_by(self, x,n):
        List=[]
        z=x
        for i in range(n):
            List.append(int(x))
            x+=z
        log(List)
        return List


    def String_Transition(self):
        for _ in range(5):
            data = self.Gen_Random_Alstr()
            run('Text_transitionBy_String', data)

    def SmashRun(self):
        datas = [('Test empty', []), ('Test one world', ["hello"]), ('Test two words', ["hello", "world"]), 
                 ('Test String', 'hello'), ('Test int', 123), ('Test bool', True), ('Test None', None)]
        for data in datas:
            log(f"{data[0]}: {data}")
            run('smash', data[1])

    def Count_Average(self, numbers:list):
        print(f"First line in Python  {numbers}")
        if len(numbers)>0:
            Sum=0
            for i in range(len(numbers)):
                Sum=Sum+int(numbers[i])
            log_color(f"Average={Sum/len(numbers)}", self.Ramdom_color())
            return Sum/len(numbers)
        else:
            return 0
    
    def count_by_five_times(self):
        for _ in range(5):
            run('count_by', self.Gen_digit(5), self.Gen_digit(10))


    def sum_array(self, arr):
        if arr == None or len(arr) < 3:
            # run('skip', f"length array {len(arr)} is too short.")
            log_color(f"length array {len(arr)} is too short.", "red")
            return 0
        log("%s\nMax: %s\nMin: %s" % (arr, max(arr), min(arr)))
        arr = [int(i) for i in arr]
        color = self.Ramdom_color()
        log_color("Sum: %s" % (sum(arr) - max(arr) - min(arr)), color)
        return sum(arr) - max(arr) - min(arr)
    
    def sum_array_run_three_times(self):
        for _ in range(3):
            run('sum_array', self.Gen_Random_List(1, 100))


    # 定義波峰波谷再切割 再比
    def pick_peaks(self, arr):
        pos = []
        peaks = []
        min_pos = []
        min_num = ''
        max_pos = []
        max_num = ''
        
        if len(arr) == 0 or max(arr) == min(arr):
            return {'pos':[], 'peaks':[]}
        else:
            # 跟左邊右邊比就好 所以左右邊都要有數字, 波谷會有兩個一樣的數字, 這兩個數字都比左右邊數字小
            for i in range(len(arr)):
                min_count = 0
                max_count = 0
                if i-1 >= 0 and i+1 != len(arr): #邊角不算
                    # 波谷一個數字, 需要做if arr[i] == arr[j]
                    for j in range(i-1, i+2, 2):
                        if j-1 >= 0 and j+1 != len(arr):
                            if arr[i] < arr[j]: min_count+=1
                            if arr[i] > arr[j]: max_count+=1
                            if j+1 < len(arr):
                                if arr[i] == arr[j] and arr[i] and arr[i] < arr[i-1] and arr[j] < arr[j+1]: min_count+=1
                            if i+1 < len(arr):
                                if arr[i] == arr[j] and arr[i] and arr[i] < arr[i+1] and arr[j] < arr[j-1]: min_count+=1
                    if min_count == 2:
                        min_pos.append(i)
                        min_num += str(arr[i]) + ', '   
                    if max_count == 2: 
                        max_pos.append(i)
                        max_num += str(arr[i]) + ', '

            print(f'波谷位置= {min_pos}\n波谷: {min_num}') #波谷定義: 這個數字比兩邊數字都小
            print(f'波峰位置= {max_pos}\n波峰: {max_num}') #波峰定義: 這個數字比兩邊數字都大

            # 分割Lists
            Lists = []
            for i in range(len(min_pos)):
                if len(min_pos) == 1:
                    Lists.append(arr[0:min_pos[i]+1])
                    Lists.append(arr[min_pos[i]:])
                else:
                    if i == 0:
                        Lists.append(arr[0:min_pos[i]+1])
                        Lists.append(arr[min_pos[i]:min_pos[i+1]+1])
                    elif i == len(min_pos)-1:
                        Lists.append(arr[min_pos[i]:])
                    else:
                        Lists.append(arr[min_pos[i]:min_pos[i+1]+1])  
            if len(Lists) == 0 : Lists = [arr]
            print(f'Lists: {Lists}')
            
            List_Pos = 0
            for i in range(len(Lists)):
                count = len(Lists[i])
                #處理無效Lists
                for j in range(len(Lists[i])):
                    if len(Lists[i]) > 2:
                        if Lists[i][0] == max(Lists[i]): Lists[i].pop(0)
                        if Lists[i][-1] == max(Lists[i]): Lists[i].pop(-1)
                #比大小
                if len(Lists[i]) > 2:
                    non_added = True
                    for k in range(len(Lists[i])):
                        if Lists[i][k] == max(Lists[i]) and non_added:
                            pos.append(List_Pos + k - i) #5 + 1 - 1
                            non_added = False
                    peaks.append(max(Lists[i]))
                List_Pos+=count
        log_color({'pos':pos, 'peaks':peaks}, self.Ramdom_color())
        return {'pos':pos, 'peaks':peaks}
    
    def pick_peaks_best(self, arr):
        pos = []
        prob_peak = False
        for i in range(1, len(arr)):
            if arr[i] > arr[i-1]:
                prob_peak = i
                print(f'prob_peak = {prob_peak}\n{arr[i]}')
            elif arr[i] < arr[i-1] and prob_peak:
                pos.append(prob_peak)
                prob_peak = False
        log_color({'pos':pos, 'peaks':[arr[i] for i in pos]}, self.Ramdom_color())
        return {'pos':pos, 'peaks':[arr[i] for i in pos]}

    def peak_best(self):
        test_list = self.Gen_Random_List_for_pick_peaks(1, 50)
        log(f"List1: {test_list}")
        run('pick_peaks', test_list)
        test_list2 = self.Gen_Random_List_for_pick_peaks(1, 50)
        log(f"List2: {test_list2}", level='INFO')
        run('pick_peaks_best', test_list2)
    
use_globals_update_keywords(My_CodeWars(), globals())