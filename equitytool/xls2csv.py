import pandas as pd
import sys


class Converter(object):

    def set_excel(self, io):
        self.sheets = pd.read_excel(io, sheetname=None)

    def set_form_id(self, form_id):
        settings = self.sheets['settings']
        settings['form_id'][0] = form_id

    def get_csv(self):
        result = ''
        for name, sheet in self.sheets.items():
            result += name + '\n'
            csv = sheet.to_csv(index=False)
            lines = csv.strip().split('\n')
            shifted = '\n'.join([',' + line for line in lines])
            result += shifted + '\n'
        return result


def xls2csv(io, form_id=None):
    c = Converter()
    c.set_excel(io)
    if form_id:
        c.set_form_id(form_id)
    return c.get_csv()


if __name__ == '__main__':
    args = sys.argv[1:]
    print xls2csv(*args)
