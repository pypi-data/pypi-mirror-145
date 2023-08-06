import pandas as pd
import os

class ReadData():

    def __init__(self):

        self.sep_list = [',', '\t']
        self.encoding_list = ['utf8', 'gbk']
        self.replace_str = '=|"'
        self.encode = 'gbk'

    def try_read_csv(self, path, encoding, sep, col_num=100):

        try:
            if path.split('.')[1] == 'xlsx':
                df = pd.read_excel(path,header=None)
                return df
            else:
                try:
                    df = pd.read_csv(path, engine='python', encoding=encoding, sep=sep, dtype='object',
                                     skip_blank_lines=False, names=list(range(0, col_num)))
                except:
                    df = pd.read_excel(path, header=None)

                if len(df.dropna(axis=1, how='all').columns) <= 1:
                    return None
                else:
                    return df
        except:
            return None

    def handle_csv_df(self, df):

        df.dropna(axis=1, how='all', inplace=True)
        df.columns = list(df.iloc[0])
        df.reset_index(drop=True, inplace=True)
        df.drop(0, inplace=True)
        return df

    def read_csv(self, file_path, file_type):

        if not os.path.exists(file_path):
            raise Exception('文件不存在')

        df = None
        for encoding in self.encoding_list:
            self.encode = encoding
            for sep in self.sep_list:
                df = self.try_read_csv(file_path, encoding, sep)
                if df is None:
                    continue
                else:
                    break
            if df is None:
                continue
            else:
                break

        if df is None:
            raise Exception('文件读取失败')

        df = df.replace(self.replace_str, '', regex=True)
        df.dropna(axis=1, how='all', inplace=True)

        if file_type != 'position':
            df.dropna(axis=0,how='all',inplace=True)
            return pd.DataFrame(),self.handle_csv_df(df), self.encode

        df_na_count = df.isna().sum(axis=1)
        div_index = df_na_count[df_na_count == len(df.columns)]
        if len(div_index) != 0:
            div_index = div_index.index[0]
            df1 = self.handle_csv_df(df.iloc[0:div_index])
            df2 = self.handle_csv_df(df.iloc[div_index + 1:])
        else:
            df1 = pd.DataFrame()
            df2 = self.handle_csv_df(df)

        return df1, df2, self.encode