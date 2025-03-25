from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime


def filling_fields(driver, common_info, filling_data, server):
    serv_of_msk = ['179', '183', '184', '139', '114', '138']
    serv_of_obl = ['109', '110', '106', '129']

    for k, v in filling_data.items():
        for options in v:
            if options == "select":
                select = Select(driver.find_element(By.ID, filling_data[k][options]))
                select.select_by_index(common_info["OPTIONS_DICT"].get(filling_data[k]["option"]))

            elif options == "set":
                set_val = driver.find_element(By.ID, filling_data[k][options])

                if "set_keys" not in v:
                    if server in serv_of_msk:
                        if "set_keys_M" in v:
                            set_val.send_keys(filling_data[k]["set_keys_M"])
                    elif server in serv_of_obl:
                        if "set_keys_MO" in v:
                            set_val.send_keys(filling_data[k]["set_keys_MO"])
                else:
                    set_val.send_keys(filling_data[k]["set_keys"])

            elif options == "set_ot":
                set_ot = driver.find_element(By.ID, filling_data[k][options])
                set_ot.send_keys(filling_data[k]["set_keys_ot"])

            elif options == "set_do":
                if "set_keys_do" in v:
                    set_do = driver.find_element(By.ID, filling_data[k]["set_do"])
                    set_do.send_keys(filling_data[k]["set_keys_do"])
                else:
                    set_do = driver.find_element(By.ID, filling_data[k]["set_do"])
                    set_do.send_keys(datetime.today().strftime('%Y-%m-%d'))

