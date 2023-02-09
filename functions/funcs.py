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

# Global Variables
driver = None


# config stuff #
def read_config(data_value: str) -> None:
    """
    This Function Reads specific values from  the config.json file
    """
    with open(CONFIG_FILE_PATH) as conf:
        data = json.loads(conf.read())
        return data[f'{data_value}']


# Selenium setup #
def setup_driver():
    """
    This function setups the selenium driver with a global variable "driver" to use over other selenium functions
    """
    global driver # global driver variable
    # Selenium Setup
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if read_config('window_visible') == 'false':
        options.add_argument('headless')

    path = read_config('chromedriver_path')
    driver = webdriver.Chrome(options=options , executable_path=path)
    
    
# Selenium Functions    
def start_tabel():
    global driver # global driver variable
    driver.get('https://gangetabel.dk/') # set driver on site
    start_button = driver.find_element(By.XPATH, XPATH_START_BUTTON) # find the start button
    start_button.click() # click the start button
    # SWITCHING TO MOBILE VERSION KEYBOARD
    mobile_version = driver.find_element(By.XPATH, XPATH_MOBILE_VERSION)
    mobile_version.click()
    
    # TIMER
    start_time = time.time()
    
    
    # FINDING THE MATH ANSWER
    for i in range(81): # "repeat" code 81 times
        math_div = driver.find_element(By.XPATH, XPATH_MATH_ELEMENT) # find the active math calculation text
        get_math_text = math_div.text # get the div text of the active-text element
        replaced_text = get_math_text.replace('•', '') # replace the • in the div text with nothing
        get_first_number = replaced_text[0] # get the first math number of div text
        get_last_number = replaced_text[-1] # get the last math number of div text
        convert_first_number = int(get_first_number) # convert the first math number to integer
        convert_last_number = int(get_last_number) # convert the last math number to integer
        final_result = convert_first_number * convert_last_number # finally multiply the two numbers together

        
        # CHECK THE ANSWERS NUMBER (Needed because if 2 digit number it gets split up in two parts because of mobile keyboard menu)
        if final_result <= 9: # if the math answer is equal or less than 9 (Max number on the keyboard menu)
            final_result = str(final_result) # convert final_result (integer) to string
            key_menu = driver.find_element(By.XPATH,f'//*[@id="key{final_result}"]') # find the keyboard button for example: key1, key5 etc..
            key_menu.click() # click the number button
            enter_button = driver.find_element(By.XPATH, XPATH_ENTER_BUTTON) # Find the enter button
            enter_button.click() # click the enter button
            
        else:    
            # if not, get the answers first and last number to split it up in two keyboard presses
            final_result = str(final_result) # convert final_result (integer) to string
            first_num = driver.find_element(By.XPATH,f'//*[@id="key{final_result[0]}"]')
            sec_num = driver.find_element(By.XPATH,f'//*[@id="key{final_result[-1]}"]') 
            first_num.click() # click the first number of the solved multiply calculation
            sec_num.click() # click the second number of the solved multiply calculation
            # finally, click the enter button
            enter_button = driver.find_element(By.XPATH, XPATH_ENTER_BUTTON) # find enter button
            enter_button.click() # click enter button
    else:
        
        print("Finish Time: {:.2f} second(s)".format(time.time() - start_time))
  
            