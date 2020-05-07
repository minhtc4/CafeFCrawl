import logging

import pandas as pd
from icecream import ic

LOG_FILENAME = '../log/ckk.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

LINK = 'https://s.cafef.vn/Lich-su-giao-dich-{}-1.chn'
RAW_NAME = ['Ngày', 'Giá đóng cửa', 'GD khớp lệnh', 'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']
NEW_NAME = ["Date", "Close", 'Volume', 'Value', "Open", "High", "Low"]
ORDERED = ['Date', 'Close', 'Open', 'High', 'Low', 'Volume']


class Crawl:
    def __init__(self, mck):
        self.mck = mck
        self.link = LINK.format(self.mck)
        self.df_old, self.df_new = None, None

    @staticmethod
    def clean(df):
        df.columns = df.iloc[0, :].values
        df = df.loc[2:, :][RAW_NAME]
        df.columns = NEW_NAME
        df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y')
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col])
        df[["Close", "Open", "High", "Low"]] = df[["Close", "Open", "High", "Low"]] * 1000
        df = df[ORDERED]
        return df

    def get_response(self):
        df_new = pd.read_html(self.link, encoding='utf-8')[1]
        df_new = self.clean(df_new)
        return df_new

    def process_old_data(self):
        df_old = pd.read_csv("../data/{}.csv".format(self.mck)).iloc[:, :-1]
        df_old.columns = ["Date", "Close", "Open", "High", "Low", "Volume"]

        df_old["Date"] = pd.to_datetime(df_old["Date"], format='%d/%m/%Y')
        df_old["Volume"] = (df_old['Volume'].replace(r'[KM]+$', '', regex=True).replace("-", 0).astype(float) * \
                            df_old['Volume'].str.extract(r'[\d\.]+([KM]+)', expand=False) \
                            .fillna(1).replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

        for col in df_old.columns[1:]:
            df_old[col] = df_old[col].astype('str').str.replace(',', "").astype('float')
        return df_old

    def merger_to_old_data(self):
        self.df_new = self.get_response()
        self.df_old = self.process_old_data()
        self.df_new.set_index('Date', inplace=True)
        self.df_old.set_index('Date', inplace=True)
        add_ = [i for i in self.df_new.index if i not in self.df_old.index]
        logging.info(add_)
        if add_:
            for dt in add_:
                self.df_old.loc[dt, :] = self.df_new.loc[dt, :]
        self.df_old = self.df_old.sort_index(ascending=False)
        return self.df_old

    def run(self):
        df = self.merger_to_old_data()
        df.to_csv('../data/{}.csv'.format(self.mck))


if __name__ == '__main__':
    stocks = pd.read_csv('../stock.csv')
    stocks = stocks.values
    for index, stock in stocks:
        try:
            ic(index, stock)
            logging.info((index, stock))
            Crawl(stock).run()
        except Exception as e:
            logging.error(e)
