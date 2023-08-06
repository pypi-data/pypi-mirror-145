import csv
import logging

logging.basicConfig(level=logging.ERROR)


class OperationCSV:
    def __init__(self, path):
        self.path = path

    def get_value(self, row_num, col_num):
        """

        :param row_num:
        :param col_num:
        :return: csv_value
        """
        with open(self.path, 'r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
            return rows[row_num][col_num]

    def get_values(self, row_start, row_end, col_start, cor_end):
        """

        :param row_start: 开始行
        :param row_end: 结束行
        :param col_start: 开始列
        :param cor_end: 结束列
        :return: 查询结果
        """
        # 物理数改为索引
        row_start = row_start - 1
        row_end = row_end - 1
        col_start = col_start - 1
        cor_end = cor_end - 1
        with open(self.path, 'r') as file:
            reader = csv.reader(file)
            results = []
            for index, info in enumerate(reader):   # 获取索引和对应数据
                if row_start < row_end and col_start < cor_end:
                    if row_start <= index <= row_end:
                        results.append(info[col_start:cor_end + 1])
                elif row_start < row_end and col_start == cor_end:
                    if row_start <= index <= row_end:
                        results.append(info[col_start:col_start + 1])
                elif row_start == row_end and col_start < cor_end:
                    if row_start == index:
                        results.append(info[col_start: cor_end + 1])
                elif row_start == row_end and col_start == cor_end:
                    if row_start == index:
                        results.append(self.get_value(row_start, col_start))
                else:
                    if row_start > row_end and col_start > cor_end:
                        return logging.error('row_start>row_end and col_start > cor_end')
                    elif col_start > cor_end:
                        return logging.error('col_start>cor_end')
                    else:
                        return logging.error('row_start > row_end')
            return results

    def write_value(self, values, headers=None):
        """

        :param values: [(),()...]
        :param headers: dict
        :return:
        """
        if headers is None:
            with open(self.path, 'w', newline='') as file:
                f_write = csv.writer(file)
                f_write.writerows(values)
        elif headers is not None:
            with open(self.path, 'w', newline='') as file:
                f_write = csv.writer(file)
                f_write.writerow(headers)
                f_write.writerows(values)
