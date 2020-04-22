from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime, localtime


class datav:
    def __init__(self, conf):
        self.conf = conf
        if conf[7] == 1:
            self.driver = webdriver.Chrome(executable_path='chromedriver')
        elif conf[7] == 2:
            self.driver = webdriver.Edge(executable_path='msedgedriver')
        elif conf[7] == 3:
            self.driver = webdriver.Edge(executable_path='MicrosoftWebDriver')

    def click_xpath(self, xpath):
        self.driver.find_element_by_xpath(xpath=xpath).click()

    def login(self):
        url = [
            'http://rzfw.njupt.edu.cn/cas/login',
            'http://datav.njupt.edu.cn/feiyan_api/h5/html/index/yqIndex.html',
            'http://datav.njupt.edu.cn/feiyan_api/h5/html/daka/daka-multi.html',
        ]

        self.driver.get(url[0])
        self.driver.find_element_by_name('username').send_keys(self.conf[0])
        self.driver.find_element_by_name("password").send_keys(self.conf[1])
        # sleep(0.5)
        self.click_xpath('//*[@id="dl"]')

        self.driver.get(url[1])
        ind = self.driver.page_source.index('iv class="page page-current" id="')
        # print(self.driver.page_source.index('iv class="page page-current" id="'))
        print(self.driver.page_source[ind + 33:ind + 51])
        sleep(0.2)
        self.click_xpath('//*[@id="' + self.driver.page_source[ind + 33:ind + 51] + '"]/div/div[3]/a[1]')

        sleep(1)
        self.driver.get(url[2])
        sleep(1)

    def fucktheform(self):
        xp = [
            '',
            '',
            # 2今日所在校区
            '//*[@id="question-form"]/ul/li[2]/div[2]/div/div/li[4]/label/div[1]/i',
            # 3不在校原因
            '//*[@id="question-form"]/ul/li[3]/div[2]/div/div/li[4]/label/div[1]/i',
            # 4当前体温
            '//*[@id="question-form"]/ul/li[4]/div[2]/div/div/input',
            # 5今日健康状况
            '//*[@id="question-form"]/ul/li[5]/div[2]/div/div/li[1]/label/div[1]/i',
            # 6你今日的苏康码颜色
            '//*[@id="question-form"]/ul/li[6]/div[2]/div/div/li[1]/label/div[1]/i',
        ]
        sleep(0.3)
        self.driver.find_element_by_xpath(xp[4]).send_keys('正常')
        for i in [2, 3, 5, 6]:
            sleep(0.3)
            self.click_xpath(xp[i])

    def submit(self):
        ind = int(
            self.driver.page_source.index(
                '<div class="page page-current" id="'))
        print(self.driver.page_source[ind + 35:ind + 53])

        sleep(0.3)
        for i in range(self.conf[6], 0, -1):
            print(str(i) + '秒后提交')
            sleep(1)

        xp = '//*[@id="' + self.driver.page_source[ind + 35:ind + 53] + '"]/div/div[4]/div[2]/a'
        self.click_xpath(xp)
        with open('rec.txt', 'a') as fi:
            fi.write(strftime("%Y-%m-%d %H:%M:%S\n", localtime()))
        sleep(1)
        self.driver.switch_to_alert().accept()
        print('done')
        sleep(1)
        self.driver.close()


def main():
    flag = 0
    print('需要chrome或edge浏览器')
    try:
        with open('rec.txt', 'r') as fi:
            con = fi.read().split('\n')
            if con[-2].split(' ')[0] == strftime("%Y-%m-%d", localtime()):
                flag = 1
                print('finished')
                exit(0)
    except FileNotFoundError:
        print('Creating rec.txt.')
        with open('rec.txt', 'w') as fi:
            fi.write('This file is used to record the time when the questionnaire was done.\n')
    except IndexError:
        print('The format of rec.txt may be wrong.')

    try:
        with open('config.txt', 'r', encoding='utf-8') as f:
            conf = f.read().split('\n')[0:8]
        conf[4] = list(map(int, conf[4].split(',')))
        conf[5] = list(map(int, conf[5].split(',')))
        conf[6], conf[7] = int(conf[6]), int(conf[7])
    except Exception as e:
        print(e)
        print('failed')
        exit(0)
    a = datav(conf)
    a.login()
    a.fucktheform()
    a.submit()


if __name__ == '__main__':
    main()
