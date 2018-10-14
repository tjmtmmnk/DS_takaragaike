import psycopg2 as ps

class DataBase():
    def __init__(self, db_cfg):
        self.db_cfg = db_cfg
        self.connect = ps.connect(self.db_cfg.URL)
        self.connect.autocommit = True
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()
        self.cursor.close()

    def execSql(self, sql):
        self.cursor.execute(sql)

    def insertValues(self, values):
        self.execSql(
            "insert into " + self.db_cfg.TABLE_NAME +
            " values('" + values["date"] + "', '" + values["time"] + "', " + str(values["status"]) + ");")

    def debugTable(self):
        self.execSql("select * from " + self.db_cfg.TABLE_NAME + ";")
        result = self.cursor.fetchall()
        for res in result:
            print(res)

