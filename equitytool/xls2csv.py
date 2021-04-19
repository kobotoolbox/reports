import pandas as pd
import sys


class Converter(object):

    def set_excel(self, io):
        self.sheets = pd.read_excel(io, sheetname=None)

    def set_settings(self, **kwargs):
        settings = self.sheets['settings']
        for k, v in kwargs.items():
            settings[k][0] = v

    def get_csv(self):
        result = ''
        for name, sheet in self.sheets.items():
            result += str(name) + '\n'
            csv = sheet.to_csv(index=False, encoding='utf-8')
            lines = csv.strip().split('\n')
            shifted = '\n'.join([',' + line for line in lines])
            print(type(result), type(shifted))
            result += shifted + '\n'
        return result


def xls2csv(io, **kwargs):
    c = Converter()
    c.set_excel(io)
    c.set_settings(**kwargs)
    return c.get_csv()


if __name__ == '__main__':
    args = sys.argv[1:]
    print(xls2csv(*args))
