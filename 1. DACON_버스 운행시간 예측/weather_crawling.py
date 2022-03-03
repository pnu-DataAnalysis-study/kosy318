from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome('C:/Users/kkosy/Downloads/chromedriver.exe')
month = 10
driver.get(f'https://www.weather.go.kr/w/obs-climate/land/past-obs/obs-by-day.do?stn=184&yy=2019&mm={month}&obs=1')
driver.implicitly_wait(10)

precipitation = []

row = 1
weekday = 3

weather_df = []
date = 1
while True:
    if weekday == 8:
        row += 1
        weekday = 1
    # print(row, weekday)
    precipitation.append(driver.find_element_by_xpath(
        f'/html/body/div[2]/section/div/div[2]/div[2]/div[3]/div/table/tbody/tr[{2 * row}]/td[{weekday}]/span[13]').text)
    weekday += 1

    if month == 10 and row == 5 and weekday == 6:
        print(month, precipitation)
        for p in precipitation:
            temp = p[5:]
            if temp == ' -':
                weather_df.append([f'2019-{month}-{date}', 0])
            else :
                weather_df.append([f'2019-{month}-{date}', float(p[5:-2])])
            date += 1
        precipitation = []
        month += 1
        date = 1
        row = 1
        weekday = 6
        driver.get(f'https://www.weather.go.kr/w/obs-climate/land/past-obs/obs-by-day.do?stn=184&yy=2019&mm={month}&obs=1')
        driver.implicitly_wait(10)
    if month == 11 and row == 5 and weekday == 8:
        print(month, precipitation)
        for p in precipitation:
            temp = p[5:]
            if temp == ' -':
                weather_df.append([f'2019-{month}-{date}', 0])
            else :
                weather_df.append([f'2019-{month}-{date}', float(p[5:-2])])
            date += 1
        break

driver.close()

weather_df = pd.DataFrame(weather_df, columns = ['date', 'precipitation'])

print(weather_df)
weather_df.to_csv("weather.csv")