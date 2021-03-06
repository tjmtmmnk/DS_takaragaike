from bs4 import BeautifulSoup


class Scraping():
    FREE = 1
    FILLED = 0

    def __init__(self, source, parser, cfg):
        self.soup = BeautifulSoup(source, parser)
        self.dates = []
        self.status = []
        self.reservation = []
        self.cfg = cfg

    def getDates(self):
        head = self.soup.find_all(class_="Head")
        for h in head:  # 日付取得
            month, day, date = self.separateDateTuple(str(h.text))
            self.dates.append(
                {
                    "month": month,
                    "day": day,
                    "date": date
                }
            )

    # @input : 11/05(月)のような形式
    def separateDateTuple(self, raw_date: str):
        slash = raw_date.find('/')
        left = raw_date.find('(')
        right = raw_date.find(')')
        return int(raw_date[0:slash]), int(raw_date[slash + 1:left]), raw_date[left + 1:right]

    def getStatus(self):
        for i in range(self.cfg.TABLE_ID_MAX):  # status取得
            for j in range(self.cfg.TABLE_COLUM_MAX):
                fmt = format(i * 100 + j, '04d')  # IDの生成規則を利用
                _id = "ID" + fmt;

                status_not_format = self.soup.find(id=_id)

                e1 = str(status_not_format).find('"')
                status_not_format = str(status_not_format).replace('"', 'a', 1)
                e2 = str(status_not_format).find('"')
                # format前に"に注目するとstatusを表すワードが""で囲われていて1,2番目に出現することを利用
                self.status.append(status_not_format[e1 + 1:e2])

    #   @param (status) :　空いているときに1, それ以外は0
    def makeReservationList(self):
        self.getDates()
        self.getStatus()

        for d in range(len(self.dates)):  # 予約リストの作成
            for t in range(len(self.cfg.TIME)):
                status = 0
                if (self.status[10 * d + t] == self.cfg.FREE):
                    status = self.FREE
                else:
                    status = self.FILLED
                self.reservation.append(
                    {
                        "month": self.dates[d]["month"],
                        "day": self.dates[d]["day"],
                        "date": self.dates[d]["date"],
                        "time": self.cfg.TIME[t],
                        "status": status
                    }
                )

    def getReservationList(self):
        return self.reservation

    def debugReservationList(self):
        for res in self.reservation:
            print(res)

    def debugDatesList(self):
        for d in self.dates:
            print(d)

    def debugStatusList(self):
        for s in self.status:
            print(s)
