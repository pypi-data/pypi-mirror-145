import time
import re

def calculator_information():
    print("Hello :)")
    time.sleep(1)
    print("This calculator has the following actions: (+, -, /, *, %, //)")
    time.sleep(2)
    print("On it you can create a large series of numbers, with different signs, "
          "without having to process each pair one by one!")
    time.sleep(2)
    print("I recommend trying it with different examples.\n")
    time.sleep(2)
    print("Number examples:\n200 * 5 / 3 + 8 * 10 // 3 == 1137\n"
          "10000 + 5000 / 2 * 4 // 2.7 == 11111\n"
          "800 * 3 // 24 - 50 * 5 // 3 == 83\nEtc...\n")
    time.sleep(6)
    print("Also installed here is another module of my production called: 'floatdeldot'.")
    time.sleep(3)
    print("Its role is to clear unnecessary numbers after the dot.\n")
    time.sleep(3)
    print("Here are a couple of examples:\n"
          "15.0 --> 15\n"
          "18.01 -- > 18.01\n"
          "18.001 --> 18\n"
          "19.67384 --> 19.67\n"
          "And much more.\n\n")
    time.sleep(4)
    print("You can use it by installing the module via PIP\n\n"
          "---------------------------------\n"
          "Download: pip install floatdeldot\n"
          "---------------------------------\n")
    time.sleep(6)
    print("Good luck friend :)")

def calculator(write_example_here=""):
    res = str(write_example_here)
    # nums = str(write_example_here)
    def func(nums):
        ii = ""
        nums_list = []
        for i in nums:
            if nums.count("//") != 0:
                if i == "/":
                    ii += i
                    nums_list.append(ii)
                    if len(ii) == 2:
                        nums_list.pop()
                        nums_list.pop()
                        nums_list.append(ii)
                        ii = ""

                else:
                    ii = ""
                    nums_list.append(i)
            else:
                nums_list.append(i)
        return nums_list

    def calculatorA(nums_list, nums_new):
        try:
            p, m, um, de = nums_list.count("+"), nums_list.count("-"), nums_list.count("*"), nums_list.count("/")
            pr, du = nums_list.count("%"), nums_list.count("//")
            pmumdeprdu = "{}{}{}{}{}{}".format(p, m, um, de, pr, du)

            res_pmumdeprdu = 0
            for j in pmumdeprdu:
                if int(j) > 1:
                    j = 1
                res_pmumdeprdu += int(j)

            if res_pmumdeprdu > 1:
                for i in nums_list:
                    try:
                        nums_list.insert(nums_list.index("+"), "SUM")
                        nums_list.pop(nums_list.index("+"))
                    except:
                        pass

                    try:
                        nums_list.insert(nums_list.index("-"), "MINUS")
                        nums_list.pop(nums_list.index("-"))
                    except:
                        pass

                    try:
                        nums_list.insert(nums_list.index("*"), "UMN")
                        nums_list.pop(nums_list.index("*"))
                    except:
                        pass

                    try:
                        nums_list.insert(nums_list.index("/"), "DEL")
                        nums_list.pop(nums_list.index("/"))
                    except:
                        pass

                    try:
                        nums_list.insert(nums_list.index("%"), "PROC")
                        nums_list.pop(nums_list.index("%"))
                    except:
                        pass

                    try:
                        nums_list.insert(nums_list.index("//"), "DUB")
                        nums_list.pop(nums_list.index("//"))
                    except:
                        pass

                nums_list_split = "".join(nums_list).split(" ")
                res = float(nums_list_split[0].replace("MINUS", "-").replace("SUM", "+"))

                for i in range(1, len(nums_list_split), 1):
                    if nums_list_split[i].count("MINUS"):
                        if nums_list_split[i] == "MINUS":

                            if float(res) <= 0 and float(nums_list_split[i+1]) <= 0:
                                res += abs(float(nums_list_split[i+1].replace("MINUS", "-").replace("SUM", "+")))

                            elif float(res) == 0 and float(nums_list_split[i+1]) <= 0:
                                res -= abs(float(nums_list_split[i+1].replace("MINUS", "-").replace("SUM", "+")))

                            elif float(res) >= 0 and float(nums_list_split[i+1]) <= 0:

                                kkkx = 0
                                for kkx in nums_new[i]:
                                    if kkx == "-":
                                        continue
                                    else:
                                        kkkx += int(kkx)
                                        break

                                indx = nums_list.index(str(kkkx))
                                if nums_list[indx:0:-3].count("-") >= 1:
                                    res += abs(float(nums_list_split[i+1].replace("MINUS", "-").replace("SUM", "+")))

                                else:
                                    res -= abs(float(nums_list_split[i+1].replace("MINUS", "-").replace("SUM", "+")))

                            elif float(res) <= 0 and float(nums_list_split[i+1]) >= 0:
                                res -= float(nums_list_split[i+1].replace("MINUS", "-").replace("SUM", "+"))

                            elif float(res) >= 0 and float(nums_list_split[i+1]) >= 0:
                                res -= float(nums_list_split[i+1].replace("MINUS", "-").replace("SUM", "+"))

                        else:
                            if float(res) <= 0 and float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")) <= 0:
                                res += abs(float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")))

                            elif float(res) == 0 and float(nums_list_split[i]) <= 0:
                                res -= abs(float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")))

                            elif float(res) >= 0 and float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")) <= 0:
                                kkkx = 0
                                for kkx in nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"):
                                    if kkx == "-":
                                        continue
                                    else:
                                        kkkx += int(kkx)
                                        break

                                indx = nums_list.index(str(kkkx))
                                if nums_list[indx:0:-3].count("-") >= 1:
                                    res += abs(float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")))

                                else:
                                    res -= abs(float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")))


                            elif float(res) <= 0 and float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")) >= 0:
                                res -= float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))

                            elif float(res) >= 0 and float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+")) >= 0:
                                res -= float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))

                    elif nums_list_split[i].count("SUM"):
                        if nums_list_split[i] == "SUM":
                            res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                        else:
                            res += float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))

                    elif nums_list_split[i].count("UMN"):
                        if nums_list_split[i] == "UMN":
                            res *= float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                        else:
                            res *= float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))


                    elif nums_list_split[i].count("DEL"):
                        if nums_list_split[i] == "DEL":
                            res /= float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                        else:
                            res /= float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))

                    elif nums_list_split[i].count("PROC"):
                        if nums_list_split[i] == "PROC":
                            res %= float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                        else:
                            res %= float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))

                    elif nums_list_split[i].count("DUB"):
                        if nums_list_split[i] == "DUB":
                            res //= float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))
                        else:
                            res //= float(nums_list_split[i].replace("MINUS", "-").replace("SUM", "+"))
                            if float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+")) < 0:
                                res += float(nums_list_split[i + 1].replace("MINUS", "-").replace("SUM", "+"))


            elif p == 0 and um == 0 and de == 0 and pr == 0 and du == 0:
                res = float(nums_new[0])
                for i in range(1, len(nums_new)):
                    if float(res) < 0 and float(nums_new[i]) <= 0:
                        print("Be careful if you didn't press the spacebar and it turned out:\n"
                              "'X -Y' instead of 'X - Y', one of the options will be an error.")
                        res += abs(float(nums_new[i]))

                    elif float(res) == 0 and float(nums_new[i]) <= 0:
                        res -= abs(float(nums_new[i]))

                    elif float(res) >= 0 and float(nums_new[i]) <= 0:
                        kkk = 0
                        for kk in nums_new[i]:
                            if kk == "-":
                                continue
                            else:
                                kkk += int(kk)
                                break

                        indx = nums_list.index(str(kkk))
                        if nums_list[indx:0:-3].count("-") >= 1:
                            res += abs(float(nums_new[i]))

                        else:
                            res -= abs(float(nums_new[i]))

                    elif float(res) <= 0 and float(nums_new[i]) >= 0:
                        res -= float(nums_new[i])

                    elif float(res) >= 0 and float(nums_new[i]) >= 0:
                        res -= float(nums_new[i])

            elif m == 0 and um == 0 and de == 0 and pr == 0 and du == 0:
                res = 0
                for i in nums_new:
                    res += float(i)

            elif p == 0 and m == 0 and um == 0 and pr == 0 and du == 0:
                res = float(nums_new[0])
                for i in nums_new[1::]:
                    res /= float(i)

            elif p == 0 and m == 0 and de == 0 and pr == 0 and du == 0:
                res = float(nums_new[0])
                for i in nums_new[1::]:
                    res *= float(i)

            elif p == 0 and m == 0 and um == 0 and de == 0 and du == 0:
                res = float(nums_new[0])
                for i in nums_new[1::]:
                    res %= float(i)

            elif p == 0 and m == 0 and um == 0 and de == 0 and pr == 0:
                res = float(nums_new[0])
                for i in nums_new[1::]:
                    res //= float(i)

            print("\nResult = ", float(res), "\n", sep="")

            return float(res)

        except:
            try:
                return float(res)
            except:
                return float(res)

    print("\nTo end an iteration, write S and press Enter.\n")
    time.sleep(1)

    while True:
        try:

            print(f"Write an example: {res} ", end='')
            nums = input()
            if nums == "":
                nums = "+ 0"
            if nums == "S" or nums == "s" or nums == "S " or nums == "s ":
                False
                print("\nEnd result: ", res, '\n')
                return res

            nums_list = func(nums)

            if nums_list[0] == " " or nums_list[0] == "-" or nums_list[0] == "+" or nums_list[0] == "*" or nums_list[0] == "/" \
                    or nums_list[0] == "%" or nums_list[0] == "//":
                # if
                nums_list.insert(0, " ")
                nums_l = list(str(res))
                nums_l.reverse()

                for i in nums_l:
                    nums_list.insert(0, str(i))
                resul = str(str(res) + " ; X" + nums).replace("X", " ")

                nums_new = re.split(" \+ | \* | / | - | % | // | ; | ", resul)
                if nums_new.count(""):
                    nums_new.remove("")

            else:
                nums_new = re.split(" \+ | \* | / | - | % | // | ", nums)

            res = calculatorA(nums_list, nums_new)

        except:
            print("\nSome error has occurred. You may have entered letters instead of numbers.\n"
                  "Or they didn't put a space between the action and the number.\n")
            try:
                print("Result: ", float(res), '\n')
            except:
                res = 0
                print("Result: ", res, '\n')
                return res