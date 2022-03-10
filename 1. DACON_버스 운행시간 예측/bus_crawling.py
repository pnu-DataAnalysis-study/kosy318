from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome('C:/Users/kkosy/Downloads/chromedriver.exe')
driver.get(
    'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%A3%BC%ED%8A%B9%EB%B3%84%EC%9E%90%EC%B9%98%EB%8F%84%EC%9D%98_%EC%8B%9C%EB%82%B4%EB%B2%84%EC%8A%A4_%EB%85%B8%EC%84%A0_%EB%AA%A9%EB%A1%9D')
driver.implicitly_wait(10)

train_df = pd.read_csv('train.csv')

bus_nm = train_df['route_nm'].unique()

bus_nm_unique = []
for bus in bus_nm:
    bus_nm_unique.append(bus[0:3])

bus_nm_unique = list(set(bus_nm_unique))

table = 1
row = 2
how_often = []
found = 0
while True:
    try:
        text = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div[1]/table[{table}]/tbody/tr[{row}]/th').text
        # print(text)
        if text in bus_nm_unique:
            # print(text)
            value = driver.find_element_by_xpath(
                                  f'//*[@id="mw-content-text"]/div[1]/table[{table}]/tbody/tr[{row}]/td[6]').text
            print(text, value)
            print(value[:2], value[-3:-1])
            value = (int(value[:2])+int(value[-3:-1]))/2
            how_often.append([text, value])
            found += 1
        # print(found, len(bus_nm_unique))
        if found == len(bus_nm_unique):
            break
        row += 1
    except:
        table += 1
        row = 2

driver.close()

print(how_often)

how_often = pd.DataFrame(how_often, columns=['bus', 'how_often'])
how_often.to_csv("bus.csv")
