from .myfile import File


class CsvFile(File):
    """about .csv file

    Args:
        File (class object): the file class object.
    """

    def read(self, sep=";", header=1, encoding="utf-8"):
        """读取 csv 文件，转换为列表 [{},{},]，默认参数适用于 grafana 导出的 csv 文件"""

        import pandas as pd

        if not self.filepath.endswith(".csv"):
            raise ValueError(f"{self.filepath} is not .csv file")

        df = pd.read_csv(self.filepath, sep=sep, header=header, encoding=encoding)
        rlt = []
        cols = list(df.columns)
        for ivalues in df.values:
            irlt = {}
            for j in range(len(ivalues)):
                irlt[cols[j]] = ivalues[j]
            rlt.append(irlt)
        return rlt
