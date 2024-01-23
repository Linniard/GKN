from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import common
from datetime import datetime
import sys

# Timeout for 60 seconds
TIMEOUT = 60 

class check_content_height(object):
    def __init__(self, element):
        self.element = element
    def __call__(self, driver):
        # Javascript code to get the attributes of a Component
        # Return type: dictionary
        result = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', self.element)
        try:
            val = result['style']
        except KeyError:
            print("There ist no attribute with the [Style] key.")
        
        return 'height' in val

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def Find_Web_Component(attr, loc, name):
    element = None
    try:
        element = driver.find_element(attr, loc)
    except common.exceptions.NoSuchElementException:
        print(f"Can't locate element {name}")
        exit_program()

    return element

def LoginPage():
    # username = driver.find_element(By.ID, 'username')
    username = Find_Web_Component(By.ID, 'username', 'Username-textbox')

    password = Find_Web_Component(By.ID, 'password', 'Password-textbox')
    
    # Write username ; ToDo: Not Safe !
    username.clear()
    username.send_keys("Sepehr.khashee")
    # Write Password ; ToDo: Not Safe !
    password.clear()
    password.send_keys("Gknloh+123456")

    login_btn = Find_Web_Component(By.NAME, 'login', "Login-button")
    login_btn.click()
    return

def StartPage():
    project_btn = Find_Web_Component(By.CSS_SELECTOR, '#top-menu-container .menu-manager.menu-easy-quick-top-menu a[href^="/projects?set_filter=0"]', 'Project-button')
    project_btn.click()
    return

def ProjectPage():
    project_table = Find_Web_Component(By.CSS_SELECTOR, '#projects_table .name.has-expander a[href="/projects/1000"]', "Global-project")
    project_table.click()
    return

def GanttTab():
    gantt_tab = Find_Web_Component(By.CSS_SELECTOR, '#main-menu a[href="/projects/1000/easy_gantt"]', 'Gantt-tab')
    gantt_tab.click()
    return

def FullyLoadTheTable():
    # Wait until the attribute [height] of component [gannt_cont] be generated
    try:
        WebDriverWait(driver, 10, 1).until(check_content_height(driver.find_element(By.CSS_SELECTOR, '#gantt_cont')))
    except:
       print("There was an Error Checking the attribute [height] from the component [gantt_cont]")

    return

def CalcTime(t):
    s = t.split(":")[2]
    s = s.split(".")
    sec = s[0]
    ms = s[1][0]
    return sec, ms

def WriteOnFile(sec, ms):
    file = open("C:\\Users\\sepehr.khashee\\Desktop\\Runtime-Record.txt", "a")
    file.write(f"\n{sec}, {ms}")
    file.close()

driver = webdriver.Chrome()
driver.maximize_window()

# To calculate the runtime
timer_start = datetime.now()

# Website upload process
try:
    driver.get("https://simulation/")
    driver.set_page_load_timeout(TIMEOUT)
    LoginPage()
    StartPage()
    ProjectPage()
    GanttTab()
    FullyLoadTheTable()

    timer_stop = datetime.now()

    delta_time = timer_stop - timer_start

    # Divide the runtime into seconds and milliseconds
    sec, ms = CalcTime(str(delta_time))

    # Record it on a file
    WriteOnFile(sec, ms)

    print(f"Runtime:     {sec}.{ms}s          Time: {datetime.now()}")

except common.exceptions.TimeoutException:
    print(f"Timeout in {TIMEOUT} secnods")

print("Finished...")
