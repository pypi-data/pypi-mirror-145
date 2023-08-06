import re

try:
    import xlrd
except ImportError:
    raise 'pip install ninjatools[excel] or ninjatools[all] to use excel functions!'


class Excel:
    def __init__(self, workbook_path):
        self.wb = xlrd.open_workbook(workbook_path)
        self.sheet_name = None

    # Excel functions
    @staticmethod
    def get_cell(cell):
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        m = r.match(cell)
        col = m.group(1).upper()
        number_row = int(m.group(2)) - 1

        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
               "J", "K", "L", "M", "N", "O", "P", "Q", "R",
               "S", "T", "U", "V", "W", "X", "Y", "Z"]

        number_col = 0

        for char in col:
            number_col += abc.index(char)

        return number_row, number_col

    def get_sheets(self):
        return [_ for _ in self.wb.sheet_names()]

    # Reads the cell
    def cell(self, cell, sheet_name=None):
        sheet_name = sheet_name if sheet_name else self.sheet_name
        ws = self.wb.sheet_by_name(sheet_name)
        return str(ws.cell(*self.get_cell(cell)).value)

    def read_range(self, cell_1, cell_2, sheet_name=None):
        sheet_name = sheet_name if sheet_name else self.sheet_name

        var = self.get_cell(cell_1)
        var2 = self.get_cell(cell_2)

        ws = self.wb.sheet_by_name(sheet_name)

        data = []
        for _ in range(var[0], var2[0] + 1):
            temp = []
            for __ in range(var[1], var2[1] + 1):
                temp.append(ws.cell(_, __).value)

            data.append(temp)

        return data

    # TODO: Cell write values/formulas
