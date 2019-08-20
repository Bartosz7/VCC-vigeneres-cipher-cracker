from math import sqrt
from statistics import stdev, mean

def divisors(n):
    """

    :param n: number n
    :return: list of divisors of n
    """
    divs = {1,n}
    for i in range(2,int(sqrt(n))+1):
        if n%i == 0:
            divs.update((i,n//i))
    return sorted(list(divs))

def GCD(list_1):
    """

    :param list_1: list of numbers
    :return: greatest common divisor gcd of numbers in the list_1
    """
    numbers_sorted = sorted(list_1)
    gcd = numbers_sorted[0]

    for i in range(1, int(len(list_1))):
        divisor = gcd
        dividend = numbers_sorted[i]
        remainder = dividend % divisor
        if remainder == 0:
            gcd = divisor
        else:
            while not remainder == 0:
                dividend_one = divisor
                divisor_one = remainder
                remainder = dividend_one % divisor_one
                gcd = divisor_one

    return gcd

def find_distance(text, el, num):
    """

    :param text: text
    :param el: name of repeating fragment
    :param num: number of appearings of such fragment
    :return: the distance between two exact fragments
    """
    list_of_distances = []
    k = 0
    for i in range(num):
        try:
            p = text.index(el, k)
            q = text.index(el, p + 1)
            distance = (q - p)                 # earlier: distance = (1-p-(len(el)))
            list_of_distances.append(distance)
            k += distance + len(el) - 1
        except ValueError:
            continue
    return list_of_distances

def transformer(list_1):
    """
    Function displaces elements of list by 1
    transformer([1,2,3,4]) --> [4,1,2,3]-->[3,4,1,2]-->[2,3,4,1]
    :param list_1: list
    :return: list transformed by 1; last element becomes first and first becomes second
    """
    end = list_1.pop()    #erase end and copy it to the beginning
    list_1.insert(0, end)
    return list_1

def normalize(list_1):
    s = stdev(list_1)
    m = mean(list_1)
    for i in range(len(list_1)):
        list_1[i] = int(((list_1[i] - m) / s)*-100)
    return list_1

def normalize_2(list_1):
    s = stdev(list_1)
    m = mean(list_1)
    list_2 = []
    for el in list_1:
        list_2.append((((el-m)/s)*-100))
    return list_2


def normalize_3(list_1):
    minimum = min(list_1)
    maximum = max(list_1)
    length = len(list_1)
    big = 0
    while length > 0:
        big += 1
        length = length // 10
    new_min = 0
    new_max = 10**(big+2)
    list_2 = []
    for i in range(len(list_1)):
        item = new_max - (int((list_1[i]- minimum)/(maximum - minimum)*(new_max-new_min)+new_min))
        list_2.append(item)
    return list_2

def new_function(list_1):
    key = list_1[0]
    for i in range(len(list_1)):
        list_1[i] = (key - list_1[i]) / key
    return list_1