from my_module import DataBase
from my_module import DataBaseConfig

if __name__ == '__main__':
    db_cfg = DataBaseConfig()
    db = DataBase(db_cfg)
    one = {
        "date": "9/12",
        "time": "5:10",
        "status": 1
    }

    db.insertValues(one)
    db.debugTable()

