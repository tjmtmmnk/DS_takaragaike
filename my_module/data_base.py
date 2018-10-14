import psycopg2 as ps


class DataBase():
    def __init__(self, db_cfg):
        self.db_cfg = db_cfg
        self.connect = ps.connect(self.db_cfg.URL)
        self.connect.autocommit = True
        self.cursor = self.connect.cursor()
        self.free_list = []
        self.has_free = False

    def __del__(self):
        self.connect.close()
        self.cursor.close()

    def execSql(self, sql):
        self.cursor.execute(sql)

    # debug用 通常時はprivate関数
    def __insertValues(self, values):
        self.execSql(
            "insert into " + self.db_cfg.TABLE_NAME +
            " values('" + values["date"] + "', '" + values["time"] + "', " + str(values["status"]) + ");"
        )

    def insertValues(self, values):
        status = self.getStatus(values)
        if status is None:
            self.__insertValues(values)
        else:
            if (status != values["status"]):
                self.free_list.append(values)
                self.updateTable(values)
                self.has_free = True

    def getStatus(self, values):
        self.execSql(
            "select status from " + self.db_cfg.TABLE_NAME + \
            " where date=" + "'" + values["date"] + "'" + \
            " and " + "time=" + "'" + values["time"] + "'" + ";"
        )
        return self.cursor.fetchone()[0]

    def updateTable(self, values):
        self.execSql(
            "update " + self.db_cfg.TABLE_NAME + " set status=" + str(values["status"]) + \
            " where date=" + "'" + values["date"] + "'" + \
            " and " + "time=" + "'" + values["time"] + "'" + ";"
        )

    def clearTable(self):
        self.execSql("delete from " + self.db_cfg.TABLE_NAME)

    def debugTable(self):
        self.execSql("select * from " + self.db_cfg.TABLE_NAME + ";")
        result = self.cursor.fetchall()
        for res in result:
            print(res)

    def hasFree(self):
        return self.has_free

    def getFreeList(self):
        return self.free_list
