from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time
from icecream import ic
import random
# pd.set_option('display.max_columns', None)

chrome_drive = "../chromedriver"
os.environ['webdrive.chrome.drive'] = chrome_drive
chrome_options = Options()

raw_name = ['Ngày', 'Giá đóng cửa', 'GD khớp lệnh', 'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']
new_name = ["Date", "Close", 'Volume', 'Value', "Open", "High", "Low"]


class CafeF:
    def __init__(self, mck):
        self.mck = mck
        self.drive = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_drive)
        self.drive.get('https://s.cafef.vn/Lich-su-giao-dich-{}-1.chn'.format(self.mck))
        ic(self.mck)

    @staticmethod
    def clean(df):
        # ic(df.iloc[0, :].values)
        # if df.shape[1] == 14:
        #     df = df.iloc[2:, [0, 2, 6, 11, 12, 13]]
        # if df.shape[1] == 13:
        #     df = df.iloc[2:, [0, 2, 5, 9, 10, 11]]
        df.columns = df.iloc[0, :].values
        df = df.loc[2:, :][raw_name]
        df.columns = new_name
        df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y')
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col])
        df[["Close", "Open", "High", "Low"]] = df[["Close", "Open", "High", "Low"]] * 1000
        return df

    def get_response(self):
        time.sleep(2)
        entry, page = [], 1
        df = pd.read_html(self.drive.page_source)[1]
        if len(df) <= 2:
            ic("Invalidate!")
            return
        ic(df.head())
        while len(df) >= 5 and page != 50:
            self.drive.execute_script("""__doPostBack('ctl00$ContentPlaceHolder1$ctl03$pager1','{}')""".format(page))
            time.sleep(random.uniform(0.5, 0.9))
            df = pd.read_html(self.drive.page_source, encoding='utf-8')[1]
            df = self.clean(df)
            page += 1
            entry.append(df)
            ic('Page: ', len(entry))
        df = pd.concat(entry).reset_index(drop=True)
        df.to_csv('../data/{}.csv'.format(self.mck), header=True)


class Crawl:
    def __init__(self, mcks):
        self.mcks = mcks

    @staticmethod
    def get_exist_mck():
        return pd.read_csv('../mck.csv')['c'].values

    def run(self):
        exists = self.get_exist_mck()
        if isinstance(self.mcks, list):
            for mck in self.mcks:
                if mck in exists:
                    CafeF(mck).get_response()
                    ic("Completed with ", mck)
                else:
                    ic('Invalidate')
        if isinstance(self.mcks, str) and self.mcks in exists:
            CafeF(self.mcks).get_response()
            ic("Completed with ", self.mcks)
        else:
            ic('Invalidate')


if __name__ == '__main__':
    Crawl(['VNM']).run()
    ic("Crawled!")
