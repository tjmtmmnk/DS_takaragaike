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