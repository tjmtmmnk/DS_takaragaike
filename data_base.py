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
            " values(" + str(values["month"]) + "," + str(values["day"]) + ",'" + values["time"] +
            "'," + str(values["status"]) + ");"
        )

    def update(self, resv_list):
        db_free_list = []

        for rl in resv_list:  # スクレイピング結果からFREEリストを作る
            if rl["status"] == self.FREE:
                value = \
                    {
                        "month": rl["month"],
                        "day": rl["day"],
                        "time": rl["time"]
                    }
                self.free_list.append(value)

        self.execSql("select * from reservation where status = 1;")  # 更新前のDBのFREEリストを作る
        for f in self.cursor.fetchall():
            value = \
                {
                    "month": f[0],
                    "day": f[1],
                    "time": f[2]
                }
            db_free_list.append(value)

        for rfl in self.free_list:  # 更新前のDBのFREE要素がスクレイピング結果の中になければ埋まった
            for dfl in db_free_list:
                if not (rfl["month"] == dfl["month"] and rfl["day"] == dfl["day"] and rfl["time"] == dfl["time"]):
                    self.filled_list.append(dfl)
                    self.updateStatus(dfl, self.FILLED)

            self.updateStatus(rfl, self.FREE)

    # @return : DB内に存在するときはDB内のstatus
    # @return : DB内に存在しないときはNone
    def getStatus(self, values):
        self.execSql(
            "select status from " + self.db_cfg.TABLE_NAME + \
            " where month=" + str(values["month"]) + " and day=" + str(values["day"]) + \
            " and " + "time=" + "'" + values["time"] + "'" + ";"
        )
        return self.cursor.fetchone()[0]

    def updateStatus(self, values, status):
        self.execSql(
            "update " + self.db_cfg.TABLE_NAME + " set status=" + str(status) + \
            " where month=" + str(values["month"]) + " and day=" + str(values["day"]) +
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
