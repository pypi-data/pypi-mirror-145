import xlrd
import xlwt
from xlwt import Pattern, Style, XFStyle


class OperationExcel:
    def __init__(self, file_name, sheet_name):
        """

        :param file_name: 路径+文件名
        :param sheet_name: 工作表名
        """
        self.workbook = xlrd.open_workbook(file_name)
        self.sheet = self.workbook.sheet_by_name(sheet_name)

    def get_value(self, row, col):
        sheet_value = self.sheet.cell_value(row-1, col-1)
        return sheet_value

    def get_values(self, start_row, end_row, start_col, end_col):
        results = []
        if start_row < end_row and start_col < end_col:
            for item in range(start_row-1, end_row):
                results.append(self.sheet.row_values(item, start_col-1, end_col))
        elif start_row < end_row and start_col == end_col:
            results.append(self.sheet.col_values(start_col-1, start_row-1, end_row))
        elif start_row == end_row and start_col < end_col:
            results.append(self.sheet.row_values(start_row-1, start_col-1, end_col))
        elif start_row == end_row and start_col == end_col:
            results = self.get_value(start_row, start_col)
        else:
            raise ValueError(f'start_row must ≤ end_row and start_col must  ≤ end_col ')
        return results


class TestExcel:
    def __init__(self, file_name, sheet_name):
        """

        :param file_name: 文件地址+文件名
        :param sheet_name: 工作表名
        """
        self.file_name = file_name
        self.book = xlwt.Workbook()  # 新建工作簿
        self.sheet = self.book.add_sheet(sheet_name)  # 新建sheet

    @staticmethod
    def set_cell_style(color, font_name='宋体', font_bold=False, font_italic=False, font_underline=False):
        # 颜色处理
        new_pattern = Pattern()
        new_pattern.pattern = Pattern.SOLID_PATTERN
        new_pattern.pattern_fore_colour = Style.colour_map[color]
        new_style = XFStyle()
        new_style.pattern = new_pattern
        # 字体处理
        font = xlwt.Font()
        font.name = font_name  # 字体名称
        font.bold = font_bold  # 加粗
        font.italic = font_italic  # 斜体
        font.underline = font_underline  # 下划线
        new_style.font = font
        return new_style

    def set_value(self, row, col, body, color='white', font_name='宋体', font_bold=False, font_italic=False,
                  font_underline=False):
        style = self.set_cell_style(color, font_name, font_bold, font_italic, font_underline)
        self.sheet.write(row - 1, col - 1, body, style)
        self.book.save(self.file_name)

    def set_values(self, row, col, values, headers='', color='red',
                   font_name='宋体', font_bold=False, font_italic=False, font_underline=False):
        """

        :param row:
        :param col:
        :param values: [(),()...]
        :param headers: {}
        :param color:
        :param font_name: 字体名称
        :param font_bold: 加粗
        :param font_italic: 斜体
        :param font_underline: 下划线
        :return:
        """
        row, col = row - 1, col - 1
        style = self.set_cell_style(color, font_name, font_bold, font_italic, font_underline)
        if headers == '':
            for index, item in enumerate(values):
                for index_col, item_col in enumerate(item):
                    self.sheet.write(row + index, col + index_col, item_col, style)
                    self.book.save(self.file_name)
        else:
            for index_h, item_h in enumerate(headers):
                self.sheet.write(0, index_h, item_h)
            for index_v, item_v in enumerate(values):
                for index_col, item_col in enumerate(item_v):
                    self.sheet.write(row + index_v, col + index_col, item_col, style)
                    self.book.save(self.file_name)
