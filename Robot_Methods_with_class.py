from Library.Robot_definition import run, run_many, log, log_color, log_hyperlink, skip, fail, use_globals_update_keywords
from random import randint
from Library.BaseFunctions import BaseFunction
from robot.api.deco import keyword


class My_methods(BaseFunction):
    def for_loop_print_keyowrds(self, nums):
        for num in range(nums):
            log(f'Keyword {num}')

    def print_fruit(self):
        for fruit in ['Apple', 'Banana', 'Strawberry', 'Pineapple', 'Watermelon']:
            color = self.Ramdom_color()
            log('<h3 style="font-weight: bold; color: '+ color +'">'+fruit+'</h3>', html=True)

    def cars(self):
        for car in ['Toyota', 'Volkswagen', 'Ford', 'Honda', 'Hyundai', 'General Motors', 'Nissan', 'KIA', 'BMW', 'Benz']:
            color = self.Ramdom_color()
            log_color(car, color)

    def skip_on_even_max(self, a, b):
        Summ = a*b
        blue_text = log_color(Summ, 'blue', print=False)
        red_text = log_color(Summ, 'red', print=False)
        if Summ % 2 == 0 and Summ > 100:
            log(f'Answer {blue_text} <b>is even</b> and <b style="color: blue;">{Summ}</b> > 100', level='WARN', html=True)
            skip(f'Answer {Summ} is even and {Summ} > 100')
        elif Summ % 2 != 0 and Summ > 100:
            log(f'Answer {red_text} is <b>NOT</b> even and <b style="color: red;">{Summ}</b> > 100', level='ERROR', html=True)
            fail(f'Answer {Summ} is NOT even and {Summ} > 100')
        else: log(Summ)
    
    def type_error_with_try_except(self):
        try:
            err_add_type = '1' + 2
            log(err_add_type)
        except Exception as e:
            log(f"str(1) + int(2) triggers <b>{e}</b> Exception")
    
    def type_error_test(self):
        err_add_type = '1' + 2
        log(err_add_type)

    def loop_error(self):
        List = ['1', 2]
        log(List[2])

    def loop_error_with_try_except(self):
        try:
            List = ['1', 2]
            log(List[2])
        except Exception as e:
            log(f"List[2] on ['1', 2] triggers <b>{e}</b> Exception")

    def genator_error(self):
        test_tuple = (num for num in range(5))
        for i in test_tuple:
            if i%2 == 0: log(i)
        next(test_tuple)
    
    def genator_error_with_try_except(self):
        try:
            test_tuple = (num for num in range(5))
            for i in test_tuple:
                if i%2 == 0: log(i)
            next(test_tuple)
        except StopIteration as e:
            log(f"Generator exhausted, <b>next(test_tuple)</b> iterate empty!")

    def test_run(self):
        log('Run Robot keywords in Python')
        run('for_loop_print_keyowrds', 10)
        run('log_color', 'Google', self.Ramdom_color())
        log_hyperlink('Google link', 'http://www.google.com', print=True)
    
    def test_errors(self):
        try:
            run('type_error_test')
        except:
            run('type_error_with_try_except')
        try:
            run('loop_error')
        except:
            run('loop_error_with_try_except')
        try:
            run('genator_error')
        except:
            run('genator_error_with_try_except')
    
    def test_even_max(self):
        run('skip_on_even_max', randint(1, 20), randint(1, 20))
        
    def test_run_many(self):
        run_many('print fruit', 'cars')

    def gen_loop_list(self):
        return self.Gen_Random_List(2, 50)


    def print_func_name(self, func):
        def warp_1():
            print("Now use function '{}'".format(func.__name__))
            func()
        return warp_1

    def print_time(self):
        import time
        Time = time.localtime()
        year = Time.tm_year
        month = Time.tm_mon
        day = Time.tm_mday
        hour = Time.tm_hour
        min = Time.tm_min
        sec = Time.tm_sec
        print("Use print()\nNow the Unix time is asctime {}".format(time.asctime()) + '\n' + 
            "Now the Unix time is localtime: {}".format(f"{year}/{month}/{day} {hour}:{min}:{sec}"))
        log("<H1 style='color: grey'>Use log()</H1>\n\n\nNow the Unix time is asctime {}".format('<b>'+time.asctime()+'</b>') + '\n' + 
            "Now the Unix time is localtime: {}".format(f'<b style="color: orange">{year}/{month}/{day} {hour}:{min}:{sec}</b>'), html=True)
        log_color("Use log_color()\nNow the Unix time is asctime {}".format(time.asctime()) + '\n' + 
            "Now the Unix time is localtime: {}".format(f"{year}/{month}/{day} {hour}:{min}:{sec}"), self.Ramdom_color())
    
    def test_zip_performance(self, list_length):
        keys = self.generate_random_list(list_length)
        values = self.generate_random_list(list_length)
                                           
        def Func_A(keys, values):
            return {keys[i]: values[i] for i in range(len(keys))}

        def Func_B(keys, values):
            return {k: v for k, v in zip(keys, values)}

        def Func_C(keys, values):
            return dict(zip(keys, values))

        result_a, time_a = self.timeit(Func_A, keys, values)
        result_b, time_b = self.timeit(Func_B, keys, values)
        result_c, time_c = self.timeit(Func_C, keys, values)

        # 確保結果正確性
        assert result_a == result_b == result_c

        # 打印執行時間，用於比較
        log(f"List length: {list_length}\nFunc_A: {time_a:.6f} seconds\nFunc_B: {time_b:.6f} seconds\nFunc_C: {time_c:.6f} seconds")
        log("-" * 25)

    def zip_performance_comparison(self):
        for times in [50000, 100000, 500000, 1000000]:
            run('test_zip_performance', times)

    @keyword('Move files to ${Folder} folder')
    def Move_files_to_report(self, Folder):
        log(f'Utilize variable <b>{Folder}</b> to call Move files to {Folder} folder function!')
        pass

    def Call_keyword_contains_variable(self):
        folder_name = 'Test Report 0228'
        folder_name2 = 'Test Report 0229'
        log_color('Not use Variable', color='blue')
        run('Move files to Report folder', folder_name)
        log_color('Use Variable folder_name', color='blue')
        run(f'Move files to {folder_name2} folder')

    def Move_files_to_report_folder(self, Folder):
        import subprocess, os
        output = subprocess.run('cd', shell=True, capture_output=True, universal_newlines=True)
        directory = output.stdout.splitlines()[0]
        # Folder_loc = Folder_loc = os.path.join(directory[0], Folder)
        Folder_loc = f'"{directory}\\{Folder}"' # "folder name" Handle folder name contains space
        if not os.path.isdir(Folder_loc):
            os.mkdir(Folder)
        else: print(f"{Folder} already existed")

        files = os.listdir(directory)
        # Move files to folder
        for file in files:
            try:
                if any(file.endswith(typ) for typ in ['png', 'html', 'xml', 'txt']):
                    file = f'"{file}"'
                    print(f'move {file} {Folder_loc}')
                    subprocess.run(f'move {file} {Folder_loc}', shell=True, capture_output=True, universal_newlines=True)
            except FileNotFoundError as e:
                print(f'FileNotFoundError: {e}')
                continue

use_globals_update_keywords(My_methods(), globals())

    
    