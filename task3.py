import generator
import re
import time
from PLY.parserClass import MyParser


class RecognizerPLY(object):
    __overload_file = 'Task3\\overload.txt'
    __result_file = 'Task3\\result.txt'
    __time_file = 'Task3\\time.txt'
    __file = False
    __Over_A = dict()

    def __init__(self, from_file=False):
        self.__parser = MyParser(from_file)
        self.__file = from_file

    def check_strings_from_file(self, data):
        self.__Over_A.clear()
        f_time = open(self.__time_file, 'w')
        f_time.write('iter time' + '\n')
        start_time = time.perf_counter()

        f = open("Functions\\" + data + ".txt")
        nf = f.read()
        f.close()

        self.__parser.check_string(nf)
        self.__Over_A = self.__parser.get_A()

        f_time.write(str(time.perf_counter() - start_time) + '\n')
        f_time.close()

    def check_strings_from_console(self):
        self.__Over_A.clear()
        working = True
        print('Input your line or "exit" to exit:')

        while working:
            user_string = input()
            if user_string == "exit":
                working = False
                break

            # проверка на соответсвие РВ
            self.__parser.check_string(user_string)
            if self.__parser.get_A().keys():
                print("- yes\n")
                res = list(self.__parser.get_A().keys())[0]
                # добавляем её в массив
                if self.__Over_A.get(res) is None:
                    self.__Over_A.setdefault(res, 1)
                else:
                    self.__Over_A[res] += 1
            else:
                print("- no\n")

        print('Statistic: \n')
        for key in self.__Over_A:
            if self.__Over_A.get(key) > 1:
                print(str(key) + ' ' + str(self.__Over_A.get(key)) + '\n')

    def analyze_overload(self):
        f_overload = open(self.__overload_file, 'w')
        for key in self.__Over_A:
            if self.__Over_A.get(key) > 1:
                f_overload.write(str(key) + ' ' + str(self.__Over_A.get(key)) + '\n')
        f_overload.close()

    def get_Over(self):
        return self.__Over_A

    def get_Time(self):
        return self.__time_file


if __name__ == "__main__":

    dialog = True

    while dialog:
        dialog = False
        print('Hello, how do your want to input lines (file or console)')
        input_type = input()
        if input_type == "file":
            print("Input filename:")
            filename = input()
            generator.Generator(10000, filename)
            recognizer = RecognizerPLY(True)
            recognizer.check_strings_from_file(filename)
            recognizer.analyze_overload()
            print("Data saved to files")
            print("Show statistic (yes to show):")
            input_show = input()
            if input_show == "yes":
                Over_A = recognizer.get_Over()
                for key in Over_A:
                    if Over_A.get(key) > 1:
                        print(str(key) + ' ' + str(Over_A.get(key)) + '\n')
                try:
                    f = open(recognizer.get_Time())
                    nf = f.read()
                    print("Time:", nf.split('\n')[1])

                    f.close()
                except IOError as e:
                    print("---- Error ----")

        elif input_type == "console":
            recognizer = RecognizerPLY(True)
            recognizer.check_strings_from_console()
        else:
            print("You are wrong! Try again")
            dialog = True