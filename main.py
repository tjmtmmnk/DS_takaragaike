from takaragaike_config import TakaragaikeConfig
from control_browser import ControlBrowser
from scraping import Scraping
from data_base import DataBase
from data_base_config import DataBaseConfig
from tweet_config import TweetConfig
from tweet import Tweet
from datetime import datetime

if __name__ == '__main__':
    now_time = datetime.now()
    is_run = (9 <= now_time.hour and now_time.hour <= 24)  # 9時~24時の間運用
    
    if is_run:
        cfg = TakaragaikeConfig()
        cb = ControlBrowser(cfg, True, False)
        db_cfg = DataBaseConfig()
        db = DataBase(db_cfg)
        tw_cfg = TweetConfig()
        tw_api = Tweet(tw_cfg)
        
        cb.setURL(cfg.LOGIN_URL)
        cb.login()
        cb.setCarType(cfg.AT)
        
        sc = Scraping(cb.getSource(), "html.parser", cfg)
        cb.close()
        
        sc.makeReservationList()
        
        resv_list = sc.getReservationList()
        
        db.update(resv_list)
        
        free_list = db.getFreeList()
        filled_list = db.getFilledList()
        
        file = open('log1.txt', 'w')
        
        exist_free_list = len(free_list) > 0
        exist_filled_list = len(filled_list) > 0
        
        if exist_free_list:
            file.write("[空いてます]\n|")
            
            fl_date = ""
            for fl in free_list:
                for rl in resv_list:
                    if rl["month"] == fl["month"] and rl["day"] == fl["day"] and rl["time"] == fl["time"]:
                        fl_date = rl["date"]
                        break
        
            file.write(str(fl["month"]) + "/" + str(fl["day"]) + "(" + fl_date + ") " + str(fl["time"]) + "| ")
    
        file.write("\n")
        
        if exist_filled_list:
            file.write("[埋まりました]\n|")
            
            fil_date = ""
            for fil in filled_list:
                _week = ["月", "火", "水", "木", "金", "土", "日"]
                temp = str(datetime.now().year) + "/" + str(fil["month"]) + "/" + str(fil["day"])
                data_format = datetime.strptime(temp, '%Y/%m/%d')
                fil_date = _week[data_format.weekday()]
                
                file.write(str(fil["month"]) + "/" + str(fil["day"]) + "(" + fil_date + ") " + str(fil["time"]) + "| ")
            
            file.write("\n")
    
        file.close()
        
        if exist_free_list or exist_filled_list:
            tw_file = open('log1.txt', 'r')
            tw_str = '*' + now_time.strftime('%H:%M') + '更新*\n'
            tw_str += tw_file.read()
            
            # tw_api.tweet(tw_str)
            print(tw_str)
            tw_file.close()
