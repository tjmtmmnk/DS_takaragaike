from bs4 import BeautifulSoup


class Scraping():
    def __init__(self, source, parser, cfg):
        self.soup = BeautifulSoup(source, parser)
        self.dates = []
        self.status = []
        self.times = []
        self.reservation = []
        self.cfg = cfg

    def getDatesbyClass(self):
        head = self.soup.find_all(class_="Head")
        for h in head:  # 日付取得
            self.dates.append(h.text)

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

    #   @param (status) :　空いているときに1, それ以外は-1
    def makeReservationList(self):
        self.getDatesbyClass()
        self.getStatus()

        for d in range(len(self.dates)):  # 予約リストの作成
            for t in range(len(self.cfg.TIME)):
                status = -1
                if (self.status[10 * d + t] == self.cfg.FREE):
                    status = 1
                else:
                    status = -1
                self.reservation.append(
                    {"date": self.dates[d], "time": self.cfg.TIME[t], "status": status}
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
