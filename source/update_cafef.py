import pandas as pd
from icecream import ic

link = 'https://s.cafef.vn/Lich-su-giao-dich-{}-1.chn'


class Crawl:
    def __init__(self, mck):
        self.mck = mck
        self.link = link.format(self.mck)
        self.df_old, self.df_new = None, None

    def get_response(self):
        df_new = pd.read_html(self.link, encoding='utf-8')[1]

        df_new = df_new.iloc[2:, [0, 2, 5, 9, 10, 11]]
        df_new.columns = ["Date", "Close", 'Volume', "Open", "High", "Low"]
        df_new["Date"] = pd.to_datetime(df_new["Date"], format='%d/%m/%Y')

        for col in df_new.columns[1:]:
            df_new[col] = pd.to_numeric(df_new[col])
        df_new[["Close", "Open", "High", "Low"]] = df_new[["Close", "Open", "High", "Low"]] * 1000
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
        ic(len(self.df_new))
        ic(len(self.df_old))
        self.df_new.set_index('Date', inplace=True)
        self.df_old.set_index('Date', inplace=True)
        add_ = [i for i in self.df_new.index if i not in self.df_old.index]
        ic(add_)
        if add_:
            for dt in add_:
                self.df_old.loc[dt, :] = self.df_new.loc[dt, :]
        self.df_old = self.df_old.sort_index(ascending=False)
        ic("After merge ", self.df_old.head())
        return self.df_old

    def write_csv(self):
        ic(self.mck)
        df = self.merger_to_old_data()
        df.to_csv('../data/{}.csv'.format(self.mck))


if __name__ == '__main__':
    VN30 = ["ABT", "BID", "BVH", "CTD", 'CTG', 'EIB', 'FPT', 'GAS', 'HDB', 'HPG', 'MBB', 'MSN', 'MWG',
            'NVL', 'PLX', 'PNJ', 'POW', 'REE', 'ROS', 'SAB', 'SBT', 'SSI', 'STB', 'TCB', 'VCB', 'VHM',
            'VIC', 'VJC', 'VNM', 'VPB', 'VRE']

    # for ck in VN30:
    #     Crawl(ck).write_csv()
