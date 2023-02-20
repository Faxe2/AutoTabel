# imports #
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
# Constants #
XPATH_START_BUTTON = '//*[@id="1-9-1-9-true"]/a'
XPATH_MOBILE_VERSION = '//*[@id="keyboard-shift"]'
XPATH_MATH_ELEMENT = '//*[@id="active-text"]'
XPATH_ENTER_BUTTON = '//*[@id="keybksp"]'
CONFIG_FILE_PATH = ''


# Sæt den kommende global variable til None som standard
driver = None


# config funktion #
def read_config(data_value: str) -> None:
    # åben config filen med den givende config fil sti og få dens data via at bruge "conf" værdien
    with open(CONFIG_FILE_PATH) as conf:
        # få alt data i config filen
        data = json.loads(conf.read())
        # returner dataen som er valgt i vores data_value parameter
        return data[f'{data_value}']


# Selenium setup #
def setup_driver():
    """
    This function setups the selenium driver with a global variable "driver" to use over other selenium functions
    """
    global driver # global variable "driver" global variabler er en variable man kan få adgang til overalt, kort forklaret..
    # Selenium Setup
    # Lav en options constant/variable som gør at man kan tilføje muligheder til Selenium driveren
    options = webdriver.ChromeOptions()
    
    
    # Tilføj en mulighed som er god for debugging, performance osv..
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Dette if statement bruger "read_config" funktionen til at tjekke config.json filen og se hvad værdi "window_visible" har, hvis den er false så skal vinduet ikke være synligt når programmet køre
    if read_config('window_visible') == 'false':
        options.add_argument('headless') # fjern vinduet fra driveren
    # få chromedriver stien (altså hvor chromedriver.exe filen er på ens computer)
    path = read_config('chromedriver_path')
    # sæt chromedriveren op med de muligheder vi har sat op og ens chromedriver sti
    driver = webdriver.Chrome(options=options , executable_path=path)
    
    
# Selenium Funktioner    
def start_tabel():
    global driver # global variable "driver" global variabler er en variable man kan få adgang til overalt, kort forklaret..
    
    driver.get('https://gangetabel.dk/') # fortæl selenium hvilken hjemmeside vi skal bruge
    start_button = driver.find_element(By.XPATH, XPATH_START_BUTTON) # find start knappen via dens xpath
    start_button.click() # tryk på start knappen når den er fundet
    
    # SKIFT TIL MOBIL VERSIONEN - Find knappen man skifter til mobil version via dens XPATH.
    mobile_version = driver.find_element(By.XPATH, XPATH_MOBILE_VERSION)
    # Når knappen er fundet, trykker den på knappen og skifter til mobil versionen
    mobile_version.click()
    
    # start en timer for at få tiden den er færdig med tabellen på
    start_time = time.time()
    
    
    # FINDING THE MATH ANSWER
    for i in range(81): # kør koden 81 gange (så mange gange den skal igennem tabellen)
        math_div = driver.find_element(By.XPATH, XPATH_MATH_ELEMENT) # find gangestykke teksten (den grønne tekst)
        get_math_text = math_div.text # find gangestykket
        
        replaced_text = get_math_text.replace('•', '') # erstat • med ingenting(fjerner gange tegnet)
        
        get_first_number = replaced_text[0] # få det første number i gangestykket
        
        get_last_number = replaced_text[-1] # få det sidste number i gangestykket
        
        convert_first_number = int(get_first_number) # skift første number til en integer. Normalt er gangestykke teksten en string, men vi skal lave numrene til et integer (nummer) så vi kan gange dem sammen
        
        convert_last_number = int(get_last_number) #  skift sidste number til en integer. Normalt er gangestykke teksten en string, men vi skal lave numrene til et integer (nummer) så vi kan gange dem sammen
        
        final_result = convert_first_number * convert_last_number # gang de to numre og få svaret til gangestykket

        
        # tjek om resultatet af gangestykket er 9 eller under 9 (Dette gør vi fordi at hvis den er 2 cifret skal vi splitte numrene op pga mobil versionen)
        if final_result <= 9:
            final_result = str(final_result) # skift final_result (integer) til en string igen
            key_menu = driver.find_element(By.XPATH,f'//*[@id="key{final_result}"]') # find knappen for resultatet af gangestykket, så hvis svaret var 7 så vil der egentlig bare stå key7
            key_menu.click() # tryk på det givne nummers knap 
            enter_button = driver.find_element(By.XPATH, XPATH_ENTER_BUTTON) # find enter knappen
            enter_button.click() # tryk på enter knappen
            
        else: # hvis at resultatet er over 9. Split de to tal op i to knap tryk
            final_result = str(final_result) # skift final_result (integer) til en string igen
            first_num = driver.find_element(By.XPATH,f'//*[@id="key{final_result[0]}"]') # find det første tal på resultatet
            sec_num = driver.find_element(By.XPATH,f'//*[@id="key{final_result[-1]}"]')  # find det andet/sidste tal på resultatet
            first_num.click() # tryk på det første nummers knap
            sec_num.click() # tryk på det sidste nummers knap
            enter_button = driver.find_element(By.XPATH, XPATH_ENTER_BUTTON) # Find enter knappen
            enter_button.click() # tryk på enter knappen
    else:
        # hvis den har kørt 81 gange, skal den stoppe og vise tiden det tog at lave hele tabellen
        print("Finish Time: {:.2f} second(s)".format(time.time() - start_time))
  
            