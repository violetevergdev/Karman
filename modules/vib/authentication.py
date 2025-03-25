from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def authentication(driver, account_data):
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.NAME, 'j_username')))

        user_field = driver.find_element(By.NAME, 'j_username')
        user_field.send_keys(account_data["login"])

        pass_field = driver.find_element(By.NAME, 'j_password')
        pass_field.send_keys(account_data["password"])

        action_button = driver.find_element(By.NAME, 'action')
        action_button.click()
    except Exception as e:
        err = 'Ошибка аутентификации: ', e
        return err