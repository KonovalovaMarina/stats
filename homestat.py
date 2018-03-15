#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from io import StringIO

import lxml.html


def make_stat(filename):
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """
    with open(filename, encoding='cp1251') as f:
        html = f.read()
        page = lxml.html.parse(StringIO(html))
    root = page.getroot()
    female_names = set()
    with open('russian_names.csv', encoding='utf-8') as s:
        for row in csv.reader(s, delimiter=';'):
            if row[2] == 'Ж':
                female_names.add(row[1])
    year = None
    statistic = []
    for i in root.xpath('//tr/td[2]/h3|//tr/td[2]/a'):
        if i.tag == 'h3':
            year = i.text
        else:
            surname, name = i.text.split()
            gender = 'Ж' if name in female_names else 'М'
            statistic.append((year, surname, name, gender))
    return statistic


def extract_years(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """
    list_years = set()
    for i in stat:
        list_years.add(i[0])
    return sorted(list_years)


def extract_general(stat, sex=None, year=None):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """
    count_dict = {}
    for i in stat:
        _year, _name, _sex = i[0], i[2], i[3]
        if (sex is None or _sex == sex) and (year is None or _year == year):
            if _name in count_dict:
                count_dict[_name] += 1
            else:
                count_dict[_name] = 1
    return sorted(count_dict.items(), key=lambda x: x[1], reverse=True)


def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general(stat, sex='М')


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general(stat, sex='Ж')


def extract_year(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general(stat, year=year)


def extract_year_male(stat, year):
    """
   Функция принимает на вход вычисленную статистику и год.
   Результат — список tuple'ов (имя, количество) общей статистики для всех
   имён мальчиков в указанном году.
   Список должен быть отсортирован по убыванию количества.
   """
    return extract_general(stat, sex='М', year=year)


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general(stat, sex='Ж', year=year)


if __name__ == '__main__':
    print(make_stat('home.html'))
