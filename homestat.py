#!/usr/bin/env python3
from io import StringIO
from urllib.request import urlopen
import io
import lxml.html
import csv


def make_stat(filename):
    f = urlopen(filename)
    html = f.read().decode('cp1251')
    page = lxml.html.parse(StringIO(html))
    root = page.getroot()
    female_names = set()
    with io.open('russian_names.csv', encoding='utf-8') as s:
        for row in csv.reader(s, delimiter=';'):
            if row[2] == 'Ж':
                female_names.add(row[1])
    year = None
    statistic = []  
    for i in root.xpath('//tr/td[2]/h3|//tr/td[2]/a'):
        if i.tag == 'h3':
            year = i.text
        else:
            surname, name = i.text.split(' ')
            gender = 'Ж' if female_names.__contains__(name) else 'М'
            statistic.append((year, surname, name, gender))
    return statistic
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """


stat = make_stat('ftp://shannon.usu.edu.ru/python/hw2/home.html')


def extract_years(stat):
    list_years = []
    for i in stat:
        if i[0] not in list_years:
        #if not list_years.__contains__(i[0]):
            list_years.append(i[0])
    list_years.sort()
    return list_years
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """


def extract_general(stat):
    dict = {}
    for i in stat:
        dict[i[2]] = 0
    for i in stat:
        dict[i[2]] += 1
    res_list = tuple([(k, v) for k, v in dict.items()])
    return sorted(res_list, key=lambda x: x[1], reverse=True)
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """


def extract_general_male(stat):
    dict = {}
    for i in stat:
        if i[3] == 'М':
            dict[i[2]] = 0
    for i in stat:
        if i[3] == 'М':
            dict[i[2]] += 1
    res_list = tuple([(k, v) for k, v in dict.items()])
    return sorted(res_list, key=lambda x: x[1], reverse=True)
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """


def extract_general_female(stat):
    dict = {}
    for i in stat:
        if i[3] == 'Ж':
            dict[i[2]] = 0
    for i in stat:
        if i[3] == 'Ж':
            dict[i[2]] += 1
    res_list = tuple([(k, v) for k, v in dict.items()])
    return sorted(res_list, key=lambda x: x[1], reverse=True)
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """


def extract_year(stat, year):
    dict = {}
    for i in stat:
        if i[0] == year:
            dict[i[2]] = 0
    for i in stat:
        if i[0] == year:
            dict[i[2]] += 1
    res_list = tuple([(k, v) for k, v in dict.items()])
    return sorted(res_list, key=lambda x: x[1], reverse=True)


    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """


def extract_year_male(stat, year):
    dict = {}
    for i in stat:
        if i[0] == year:
                if i[3] == 'М':
                    dict[i[2]] = 0
    for i in stat:
        if i[0] == year:
                if i[3] == 'М':
                    dict[i[2]] += 1
    res_list = tuple([(k, v) for k, v in dict.items()])
    return sorted(res_list, key=lambda x: x[1], reverse=True)
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """


def extract_year_female(stat, year):
    dict = {}
    for i in stat:
        if i[0] == year:
                if i[3] == 'Ж':
                    dict[i[2]] = 0
    for i in stat:
        if i[0] == year:
            if i[3] == 'Ж':
                dict[i[2]] += 1
    res_list = tuple([(k, v) for k, v in dict.items()])
    return sorted(res_list, key=lambda x: x[1], reverse=True)
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """


if __name__ == '__main__':
    print(make_stat('ftp://shannon.usu.edu.ru/python/hw2/home.html'))
    print(extract_years(stat))
   # print(extract_general(stat))
   # print(extract_general_male(stat))
   # print(extract_general_female(stat))
   # print(extract_year(stat, '2009'))
   # print(extract_year_male(stat, '2009'))
   # print(extract_year_female(stat, '2009'))

