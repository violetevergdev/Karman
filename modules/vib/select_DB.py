from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def select_database(driver, vib_fields, useful_btn):
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'form1:table1')))

    rows = driver.find_elements(By.CLASS_NAME, 'table-row')
    ind = 0

    start_iteration = True

    while start_iteration:
        for el in vib_fields:
            for _ in rows:
                db_val = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text2')

                if db_val.text == el:
                    db = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':rowSelect1__input_sel')
                    db.click()
                    break

                ind += 1
        start_iteration = False


    next_btn = driver.find_element(By.ID, useful_btn["next_btn"])
    next_btn.click()
