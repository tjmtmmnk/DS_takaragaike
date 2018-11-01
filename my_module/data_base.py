import psycopg2 as ps


class DataBase():
    FREE = 1
    FILLED = 0

    def __init__(self, db_cfg):
        self.db_cfg = db_cfg
        self.connect = ps.connect(self.db_cfg.URL)
        self.connect.autocommit = True
        self.cursor = self.connect.cursor()
        self.free_list = []
        self.filled_list = []

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

    def update(self, values):
        status = self.getStatus(values)
        if status is None:
            self.__insertValues(values)
            if (values["status"] == self.FREE):
                self.free_list.append(values)
        else:
            if (status == self.FILLED and values["status"] == self.FREE):  # 埋まっていたところがFREEになったとき
                self.free_list.append(values)
            elif (status == self.FREE and values["status"] == self.FILLED):  # FREEだったところが埋まったとき
                self.filled_list.append(values)
            self.updateTable(values)

    # @return : DB内に存在するときはDB内のstatus
    # @return : DB内に存在しないときはNone
    def getStatus(self, values):
        self.execSql(
            "select exists(select status from " + self.db_cfg.TABLE_NAME + \
            " where date=" + "'" + values["date"] + "'" + \
            " and " + "time=" + "'" + values["time"] + "'" + ");"
        )
        is_exist = self.cursor.fetchone()[0]
        if is_exist:
            self.execSql(
                "select status from " + self.db_cfg.TABLE_NAME + \
                " where date=" + "'" + values["date"] + "'" + \
                " and " + "time=" + "'" + values["time"] + "'" + ";"
            )
            return self.cursor.fetchone()[0]
        else:
            return None

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

    def getFreeList(self):
        return self.free_list

    def getFilledList(self):
        return self.filled_list
