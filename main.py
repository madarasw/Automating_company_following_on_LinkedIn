from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

USERNAME = "username@gmail.com"
PASSWORD = "password"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


# open LinkedIn jobs for software test engineer with easy apply filter
url = 'https://www.linkedin.com/jobs/search/?currentJobId=3804846005&distance=100&f_AL=true&geoId=103804675&keywords=software%20test%20engineer&location=Singapore%2C%20Singapore&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'
driver.get(url)
sleep(2)

# Auto login
sign_in = driver.find_element(By.LINK_TEXT, value="Sign in")
sign_in.click()
sleep(5)

try:
    element_present = EC.presence_of_element_located((By.ID, 'username'))
    WebDriverWait(driver, 300).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
except:
    print("ERROR, Please try again")
else:
    # log in
    user_name = driver.find_element(By.ID, value="username")
    password = driver.find_element(By.ID, value="password")
    user_name.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    sign_in = driver.find_element(By.XPATH, value='//*[@id="organic-div"]/form/div[3]/button')
    sign_in.click()

try:
    # waiting for the job listing page
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'scaffold-layout__list-container'))
    WebDriverWait(driver, 300).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load.")
except:
    print("Error")
else:
    # Find all listed jobs
    job_list = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")
    for job in job_list:
        # going through each job one by one.
        job.click()
        not_found = True
        while not_found:
            try:
                # scroll down and clock the follow button if not already following
                driver.execute_script("window.scrollTo(0, 10)")
                sleep(2)
                follow_button = driver.find_element(By.XPATH, value='//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/section/section/div[1]/div[1]/button')
                should_follow = follow_button.find_element(By.TAG_NAME, value='span').text == 'Follow'
                if should_follow:
                    follow_button.click()
                    print("Followed new company")
            except:
                print("Scrolling down to follow.")
            else:
                not_found = False

# close the tab
sleep(5)
driver.close()


