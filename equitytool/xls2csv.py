import pandas as pd
import sys


class Converter(object):

    def set_excel(self, io):
        # "Specify None to get all sheets"
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
        self.sheets = pd.read_excel(io, sheet_name=None)

    def set_settings(self, **kwargs):
        """
        Add settings from kwargs to the XLSForm settings sheet, overwriting
        any existing settings with the same names
        """

        try:
            settings = self.sheets['settings']
        except KeyError:
            # No settings sheet exists yet; make a new one
            self.sheets['settings'] = pd.DataFrame.from_dict(
                {k: [v] for k, v in kwargs.items()}
            )
        else:
            # Update existing settings sheet
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
