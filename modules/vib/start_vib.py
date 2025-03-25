import json
import os
import time

from modules.vib.authentication import authentication
from modules.vib.browser_init import browser
from modules.vib.vib_routes import vib_routes


def start_vib(vib_path, server):
    err = None
    try:
        with open('C:\\soft_for_py_exe\\karman\\config\\common.json', 'r', encoding='UTF-8') as f:
            common_info = json.load(f)

        # Запуск браузера
        driver = browser(common_info['OUT_VIB_DIR'])

        # Запуск VIB в Firefox
        try:
            driver.get(common_info['NVP_SERVER_URL']["url_login"].replace('serv', server))
        except Exception as e:
            err = str(e) + "Неверный URL адрес для аутентификации"
            return err

        # Логинимся
        err = authentication(driver, common_info['ACCOUNT'])
        if err:
            return err

        # Переход на страницу выборок
        try:
            driver.get(common_info['NVP_SERVER_URL']["url_vib"].replace('serv', server))
        except Exception as e:
            err = str(e) + "Неверный URL для выборок"
            return err

        # Осуществление выборки
        vib_routes(driver, vib_path, common_info, server)

        # Ожидание завершения загрузки
        while any(file.endswith('.part') for file in os.listdir(common_info['OUT_VIB_DIR'])):
            time.sleep(1)

        # Переименование
        with open(vib_path, 'r', encoding='utf-8') as f:
            name = json.load(f)["Наименование"]
        old_name = os.path.join(common_info['OUT_VIB_DIR'], 'results.csv')
        os.rename(old_name, f"{common_info['OUT_VIB_DIR']}\\{name}-Serv-{server}.csv")

        driver.close()
        return err
    except Exception as e:
        err = str(e)
        return err

