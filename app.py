from flask import Flask, request, render_template
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('url-input.html')


@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['url']
    hours_total = ''
    mins_left = ''
    secs_left = ''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"/workspace/.wdm/drivers/chromedriver/linux64/108.0.5359/chromedriver.exe")
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Reject all']").click()
    driver.switch_to.default_content()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    company_content_elements = soup.find_all(
        class_='ytd-thumbnail-overlay-time-status-renderer')
    html_list = []
    for element in company_content_elements:
        if element.get_text() != '':
            html_list.append((element.get_text().replace(
                '\n', '').replace(' ', '')).split(':'))

    new_list = [sum(int(row[i]) for row in html_list)
                for i in range(len(html_list[0]))]

    mins_from_secs = round(new_list[1] / 60)
    mins_total = mins_from_secs + new_list[0]

    secs_left = new_list[1] - (mins_from_secs * 60)

    hours_total = round(mins_total / 60)

    mins_left = mins_total - (hours_total * 60)

    driver.quit()

    return render_template('time-output.html', hours_total=hours_total, mins_left=mins_left, secs_left=secs_left)
