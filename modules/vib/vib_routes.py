import json
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.vib.filling_fields import filling_fields
from modules.vib.select_DB import select_database
from modules.vib.select_fields import select_fields
from modules.vib.select_table import select_table


def vib_routes(driver, vib_path, common_info, server):
    try:
        with open(vib_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            print(config_data)

        useful_btn = common_info['USEFUL-BTN']
        vib_fields = config_data["Выборки"]
        filling_data = config_data["Уточнения"]

        # Выбор БД - 1й шаг
        select_database(driver, vib_fields['База данных'], useful_btn)

        # Выбор таблиц БД - 2й шаг
        select_table(driver, vib_fields['Таблица'], useful_btn)

        # Выбор полей таблиц - 3й шаг
        select_fields(driver, vib_fields['Поля'], useful_btn)

         # Заполнение полей - 4й шаг
        filling_fields(driver, common_info, filling_data, server)

        # Выполнение запроса
        run_query_btn = driver.find_element(By.ID, useful_btn["run_query_btn"])
        run_query_btn.click()

        # Сохранение запроса
        WebDriverWait(driver, 580).until(EC.presence_of_element_located((By.ID, 'form1:text1')))

        WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.ID, useful_btn["save_btn"])))

        if driver.find_element(By.ID, 'form1:text1').text in ('-1', '0'):
            raise AssertionError('Проблемы с сервером, получено строк: -1 ')

        save_btn = driver.find_element(By.ID, useful_btn["save_btn"])
        save_btn.click()

    except Exception as e:
        err = 'Ошибка осуществления выборки: ', e
        return err
