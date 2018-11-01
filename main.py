from my_module import TakaragaikeConfig
from my_module import ControlBrowser
from my_module import Scraping
from my_module import DataBase
from my_module import DataBaseConfig

if __name__ == '__main__':
    cfg = TakaragaikeConfig()
    cb = ControlBrowser(cfg)
    db_cfg = DataBaseConfig()
    db = DataBase(db_cfg)

    cb.setURL(cfg.LOGIN_URL)
    cb.login()
    cb.setCarType(cfg.AT)

    sc = Scraping(cb.getSource(), "html.parser", cfg)
    sc.makeReservationList()

    resv_list = sc.getReservationList()

    for rl in resv_list:
        db.update(rl)

    free_list = db.getFreeList()
    filled_list = db.getFilledList()

    for fl in free_list:
        print("[空きが出ました] \t" + str(fl["date"]) + " " + str(fl["time"]))

    for fil in filled_list:
        print("[埋まりました] \t" + str(fil["date"]) + " " + str(fil["time"]))
