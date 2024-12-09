from random import randint, choice, randrange
from Ronot_definition import log_color
import time

class BaseFunction():
    def Gen_Random_List_for_pick_peaks(self, low_num, high_num):
        return [str(randint(low_num, high_num)) for _ in range(randint(2, 10))]
    
    def Gen_Random_List(self, low_num:int, high_num:int):
        start_num = int
        if high_num < 10: start_num = high_num/2
        elif 10 < high_num < 50: start_num = high_num/5
        elif 50 < high_num < 100: start_num = high_num/10
        else: start_num = high_num/50
        return [str(randint(low_num, high_num)) for _ in range(randint(start_num, high_num))]
    
    def generate_random_list(self, length):
        return [randint(0, 1000) for _ in range(length)]
    
    def timeit(self, func, *args):
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        return result, end_time - start_time

    def Gen_Random_Alstr(self):
        Alstr='abcdefghijklmnopqrstuvwxyz'
        data = ''.join(choice(Alstr) for _ in range(randint(5, 15)))
        color = self.Ramdom_color()
        log_color(data, color)
        return data
    
    def Gen_digit(self, a, b=None):
        """Return random integer in range [a, b], including both end points.
        """
        a = int(a)
        if b is not None: b = int(b)
        return randrange(a, b)

    def Ramdom_color(self):
        """
        Randomly select below colors :
        - Black`: #000000` - Red`: #FF0000` - Green`: #00FF00`
        - Blue`:  #0000FF` - Yello`: #FFFF00` - Grey`: #808080`
        - Orange`: #FFA500` - Purple`: #800080` - Cyan`: #00FFFF`
        - IndianRed`: #CD5C5C` - LightCoral`: #F08080` - Navy`: #000080`
        - Teal`: #008080` - Darkgreen`: #006400` - Fuchsia`: #ff00ff`
        """
        colors = ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#808080', '#FFA500', '#800080', '#00FFFF', '#CD5C5C', '#F08080', '#000080',
                  '#008080', '#006400', '#ff00ff']
        return choice(colors)
    


    
