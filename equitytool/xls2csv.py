import pandas as pd
import re
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


if __name__ == '__main__':
    script, path, form_id = sys.argv
    c = Converter()
    c.set_excel(path)
    c.set_form_id(form_id)
    print c.get_csv()
