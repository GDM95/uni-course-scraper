from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json


'''
Crawls University course catalog page scraping subject and course names
writes data json file in the form:
catalog : { subject: { 'courseID': ..., 'courseTitle': ... }, ... }

'''

chromedriver_loc = './chromedriver'
driver = webdriver.Chrome(chromedriver_loc)


url = 'http://sis.rutgers.edu/soc/#home'
driver.get(url)

items = len(driver.find_elements_by_class_name("cursortext"))
current_semester = driver.find_element_by_xpath("//div[@id='currentSemesters']/li[1]/input[1]")

locations = driver.find_element_by_xpath("//div[@id='locationsOnCampusList']")
locations = locations.find_elements_by_tag_name("li")


levels = driver.find_element_by_xpath("//ul[@id='levelsList']")
levels = levels.find_elements_by_tag_name("li")

submit = driver.find_element_by_id('continueButton')


''' BUTTON CLICKS '''
current_semester.click()
for location in locations:
    location.find_element_by_tag_name("input").click()
for level in levels:
    level.find_element_by_tag_name('input').click()
submit.click()


''' SUBJECT SEARCH PAGE '''
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#filteringSelectDiv .dijitArrowButtonInner"))).click()
courses = driver.execute_script('return [...arguments[0]].map(e=>e.textContent)',
                                    wait.until(EC.presence_of_all_elements_located(
                                        (By.CSS_SELECTOR, ".dijitComboBoxMenuPopup .dijitMenuItem[item]"))))
# key=subject: value=list of courses:
catalog = {}

# for every course in the subject
for course in courses:
    # for firestore push - key can't have slashes
    parsedCourse = course
    if '/' in course:
        parsedCourse = course.replace('/', ' AND ')


    catalog[parsedCourse] = []

    print(parsedCourse)
    driver.find_element_by_css_selector(".dijitInputInner").clear()
    driver.find_element_by_css_selector(".dijitInputInner").send_keys(course, Keys.TAB)
    wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))


    # course list div
    courseDiv = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="courseDataParent"]'))
    )
    courseList = courseDiv.find_elements_by_class_name('subject')

    for course in courseList:
        courseInfo = course.find_element_by_xpath('.//div[@class="courseInfo"]')
        id = courseInfo.find_element_by_xpath('./span[3]/span[1]/span[1]').text
        courseTitle = courseInfo.find_element_by_xpath('./span[4]/span[1]/span[1]').text

        catalog[parsedCourse].append({'courseID': id, 'courseTitle': courseTitle})
        # print(id, courseTitle)



#print(catalog)
json = json.dumps(catalog)
f = open("catalog.json","w")
f.write(json)
f.close()


driver.close()
