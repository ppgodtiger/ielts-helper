import pandas as pd

class EnglishDict():
    def __init__(self):
        self.data_dict = None

    def load_data(self, dict_path): #加载路径
        self.data_dict = pd.read_csv(dict_path,
                    usecols=["word","translation"])

    def query(self, word): #查询单词
        row = self.data_dict.query(f"word == '{word}'")
        if len(row) == 1:
            return row.iloc[0]["translation"]
        return "FALSE! PLEASE INPUT RIGHT WORD!"

english_dict = EnglishDict()
english_dict.load_data("./mydict/stardict.csv")
print(english_dict.query('python'))