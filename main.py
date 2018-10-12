from my_module import TakaragaikeConfig
from my_module import ControlBrowser
from my_module import Scraping

if __name__ == '__main__':
    cfg = TakaragaikeConfig()
    cb = ControlBrowser(cfg)

    cb.setURL(cfg.LOGIN_URL)
    cb.login()
    cb.setCarType(cfg.AT)
    cb.selectCar()

    sc = Scraping(cb.getSource(), "html.parser", cfg)
    sc.makeReservationList()
    sc.debugReservationList()

    cb.close()

# options = webdriver.chrome.options.Options()
# options.add_argument("--headless")
#
# browser = webdriver.Chrome(chrome_options=options)
#
# login_url = "http://tkr.ncors.com/ncors/login.asp"
# browser.get(login_url)
#
# user_name_field = browser.find_element_by_xpath("/html/body/form/table/tbody/tr[1]/td/input")
# user_name_field.send_keys(USERNAME)
#
# pass_word_field = browser.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[1]/input")
# pass_word_field.send_keys(PASSWORD)
#
# submit_button = browser.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td/input")
# submit_button.click()
#
# car_type_list = browser.find_element_by_name('CARTYPE')
# car_type_select = Select(car_type_list)
# car_type_select.select_by_value('02')  # AT
#
# ok_button = browser.find_element_by_xpath("/html/body/p/table[2]/tbody/tr[1]/td[2]/form/table/tbody/tr[2]/td[2]/input")
# ok_button.click()
#
# soup = BeautifulSoup(browser.page_source, "html.parser")
#
# head = soup.find_all(class_="Head")
#
# dates = []
# status = []
# times = []
#
# reservation = []
#
# for h in head:  # 日付取得
#     dates.append(h.text)
#
# for i in range(TABLE_ID_MAX):  # status取得
#     for j in range(TABLE_COLUM_MAX):
#         fmt = format(i * 100 + j, '04d') #IDの生成規則を利用
#         _id = "ID" + fmt;
#
#         status_not_format = soup.find(id=_id)
#
#         e1 = str(status_not_format).find('"')
#         status_not_format = str(status_not_format).replace('"', 'a', 1)
#         e2 = str(status_not_format).find('"')
#
#         status.append(status_not_format[e1 + 1:e2]) #format前に"に注目するとstatusを表すワードが""で囲われていて1,2番目に出現することを利用
#
# for d in range(len(dates)): #予約リストの作成
#     for t in range(len(TIME)):
#         reservation.append([dates[d], TIME[t], status[10*d+t]])
#
# for res in reservation:
#     print(res)
#
# sleep(3)
#
# browser.close()
