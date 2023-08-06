class CellLines:
    """适用于 ipynb 文件的 lines"""

    def __init__(self, lines=[]):
        self.lines = lines

    def lines2text(self, lines=None):
        if lines == None:
            lines = self.lines
        flag = True
        while flag:
            if len(lines) > 0:
                if lines[-1][-1] == "\n":
                    lines[-1] = lines[-1][:-1]
            else:
                flag = False
        text = "".join(lines)
        return text

    def text2lines(self, text):
        flag = True
        while flag:
            if text[-1] == "\n":
                text = text[:-1]
            else:
                flag = False
        lines = [i + "\n" for i in text.split("\n")]
        if lines[-1][-1] == "\n":
            lines[-1] = lines[-1][:-1]
        return lines
