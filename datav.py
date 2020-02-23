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
            'http://datav.njupt.edu.cn:8080/feiyan_api/h5/html/auth.html',
            'http://datav.njupt.edu.cn:8080/feiyan_api/h5/html/daka/daka-multi.html',
        ]

        self.driver.get(url[0])
        self.driver.find_element_by_name('username').send_keys(self.conf[0])
        # for i in range(len(conf[1])):
        self.driver.find_element_by_name("password").send_keys(self.conf[1])
        # print(self.conf[1][i])
        # sleep(0.5)
        self.click_xpath('//*[@id="dl"]')

        sleep(1)
        self.driver.get(url[1])
        ind = int(
            self.driver.page_source.index('style="background: #FFFFFF;" id="'))
        print(self.driver.page_source[ind + 33:ind + 51])

        self.driver.find_element_by_name('acct').send_keys(self.conf[2])
        self.driver.find_element_by_name("password").send_keys(self.conf[3])
        sleep(0.1)
        self.click_xpath('//*[@id="' +
                         self.driver.page_source[ind + 33:ind + 51] +
                         '"]/div/div[4]/a')

        sleep(1)
        self.driver.get(url[2])
        sleep(1)

    def fucktheplace(self, num):
        sleep(0.2)
        for i in range(1, 4):
            for j in range(4, self.conf[num][i - 1], 3):
                sleep(0.3)
                self.click_xpath('/html/body/div[2]/div/div[' + str(i) +
                                 ']/div/div[' + str(j) + ']')
            sleep(0.3)
            self.click_xpath('/html/body/div[2]/div/div[' + str(i) +
                             ']/div/div[' + str(self.conf[num][i - 1]) + ']')

        # confirm
        sleep(0.3)
        self.click_xpath('/html/body/div[2]/header/button[2]')
        sleep(0.3)

    def fucktheform(self):
        xp = [
            '',
            # 1今日城市
            '//*[@id="question-form"]/ul/li[1]/div[2]/div/div/input',
            # 2家庭所在地
            '//*[@id="question-form"]/ul/li[2]/div[2]/div/div/input',
            # 3上学校区
            '//*[@id="question-form"]/ul/li[3]/div[2]/div/div/li[1]/label/div[1]/i',
            # 4健康情况
            '//*[@id="question-form"]/ul/li[4]/div[2]/div/div/li[1]/label/div[1]/i',
            # 5过去14天路过湖北或温州或正在两地
            '//*[@id="question-form"]/ul/li[5]/div[2]/div/div/li[2]/label/div[1]/i',
            # 6具体路过或现在所在的地方
            '',
            # 7最后一次路过具体时间(填空)
            '',
            # 8没到访疫情严重地区但与疫情严重地区人员或确诊病例有接触史
            '//*[@id="question-form"]/ul/li[8]/div[2]/div/div/li[2]/label/div[1]/i',
            # 9最后一次接触时间(填空)
            '',
            # 10是否有任何与疫情相关，值得注意的情况
            '//*[@id="question-form"]/ul/li[10]/div[2]/div/div/li[2]/label/div[1]/i'
        ]

        for i in [1, 2]:
            sleep(0.3)
            self.click_xpath(xp[i])
            self.fucktheplace(i + 3)

        for i in [3, 4, 5, 8, 10]:
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

        xp = '//*[@id="' + self.driver.page_source[
            ind + 35:ind + 53] + '"]/div/div[4]/div[2]/a'
        self.click_xpath(xp)
        print('successed')
        with open('rec.txt', 'a') as fi:
            fi.write(strftime("%Y-%m-%d %H:%M:%S\n", localtime()))

        sleep(1)
        self.driver.close()


try:
    flag=0
    print('需要chrome或edge浏览器')
    with open('rec.txt','r') as fi:
        con=fi.read().split('\n')
        if con[-2].split(' ')[0]==strftime("%Y-%m-%d", localtime()):
            flag=1
            exit(0)
    with open('config.txt', 'r', encoding='utf-8') as f:
        conf = f.read().split('\n')[0:8]
    conf[4] = list(map(int, conf[4].split(',')))
    conf[5] = list(map(int, conf[5].split(',')))
    conf[6], conf[7] = int(conf[6]), int(conf[7])
    a = datav(conf)
    a.login()
    a.fucktheform()
    a.submit()
except:
    if flag:
        print('finished')
    else:
        print('failed')
