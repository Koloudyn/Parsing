from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter
import openpyxl
# Распарсить первые две таблички в эксель файл на разные листы. Просто вот как там таблички, такие же должны быть и в экселе.
# Таблицы "функциональная валюта" и "осколки и фрагменты"

# Получение данных таблицы
def get_table_info(column_names, temp):
    columns_info = dict.fromkeys(columns_names)
    for i in range(len(columns_names)):
        columns_info[columns_names[i]] = []
    temp_td = temp.find('td')
    while (temp != None):
        for i in range(len(columns_names)):
            if (i == 0):
                columns_info[columns_names[i]].append(temp_td.find('a').get_text())
            else:
                columns_info[columns_names[i]].append(temp_td.get_text())
            temp_td = temp_td.next_sibling
        temp = temp.next_sibling
        if (temp != None):
            temp_td = temp.find('td')

    return columns_info


if __name__ == '__main__':
    # Делаем реквест на html-страницу
    url = 'https://pathofexile.fandom.com/ru/wiki/%D0%92%D0%B0%D0%BB%D1%8E%D1%82%D0%B0'
    response = requests.get(url)
    print(response)

    # Забираем все таблицы со страницы
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', 'wikitable sortable item-table')

    # Получение наименований колонок (одинаковы для обеих таблиц)
    columns_names = tables[0].find_all('th')
    temp = columns_names[0]  # Указатель на текущий тег
    columns_names = []
    columns_names.append(temp.get_text())
    while (temp.next_sibling != None):
        temp = temp.next_sibling
        columns_names.append(temp.get_text())

    # Переносим две таблички в excel
    table1 = pd.DataFrame.from_dict(get_table_info(columns_names, tables[0].find_all('tr')[1]))
    table2 = pd.DataFrame.from_dict(get_table_info(columns_names, tables[1].find_all('tr')[1]))

    sheets_names = {'Таблица1': table1, 'Таблица2': table2}
    writer = pd.ExcelWriter('./task.xlsx', engine='xlsxwriter')

    for sheet_name in sheets_names.keys():
        sheets_names[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()
