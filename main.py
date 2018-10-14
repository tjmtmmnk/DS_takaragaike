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

    # db.clearTable()

    # sc.debugReservationList()

    for res in resv_list:
        db.insertValues(res)

    free_list = db.getFreeList()

    if (db.hasFree() != True):
        print("No Change")

    for fl in free_list:
        print(fl)
