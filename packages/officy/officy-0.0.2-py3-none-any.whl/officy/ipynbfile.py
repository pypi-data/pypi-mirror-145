import os
import re
import copy
from .celllines import CellLines
from .myfile import File
from .jsonfile import JsonFile


class IpynbFile(JsonFile):

    """About .ipynb file. A filetype like .json for jupyter notebook.

    Args:
        JsonFile (class obj): class of .json file.
    """

    def __init__(self, filepath, language=None):
        self.filepath = filepath
        if language == None:
            self.language = self.get_language()
        else:
            self.language = language

    def get_language(self):
        filedata = self.read()
        try:
            return filedata["metadata"]["kernelspec"]["language"].lower()
        except:
            return

    def check_language(self):
        filedata = self.read()
        try:
            self.language = filedata["metadata"]["kernelspec"]["language"].lower()
        except:
            self.language = "python"
            print(self.filepath, "没有配置kernel，默认值为 python")
        return self.language

    #########################【ipynb文件的整体方法】#########################################

    def init_ipynbfile(self, cells, dontcover=True, dontzero=True):
        """初始化生成 ipynb 文件，cells 数据类型需要符合 cell 规范"""

        if os.path.exists(self.filepath) and dontcover:
            return print(f"无法执行：文件已存在")
        if not self.filepath.endswith(".ipynb"):
            return print(f"无法执行：文件类型不合法")
        if len(cells) == 0 and dontzero:
            return print(f"无法执行：cells 数据为空")
        ipynbdata = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 2}
        self.write(ipynbdata)

    def check_title(self, n):
        """期望被自动识别为toc的title不应包含某些特别的语法，否则将导致无法点击响应"""
        data = self.read()
        flag = False
        __newcells = []
        for c in data["cells"]:
            if c["cell_type"] == "markdown":
                newlines = []
                for line in c["source"]:
                    # 存在标题，即符合条件
                    if line.startswith("#" * n + " "):
                        newline = re.sub("`", "'", line)
                        if line != newline:
                            flag = True
                            line = newline
                    newlines.append(line)
                c["source"] = newlines
            __newcells.append(c)

        data["cells"] = __newcells
        if flag:
            self.write(data)

    def update_metadata(self, language="python", is_cover=True):
        """给 ipynb 文件更新 metatada；"""
        # 已有语言和指定语言对比
        l = language.lower()
        if l not in IPYNB_METAINFO:
            l = "python"
        if not is_cover:
            l = self.check_language()

        filedata = self.read()
        filedata["metadata"] = IPYNB_METAINFO[l]
        self.write(filedata)

    def remove_end_null(self, __ipynb_data=None, is_print=False):
        """移除空 cell，或者 cell 首、尾多余的空换行"""
        if __ipynb_data == None:
            __ipynb_data = self.read()
        __newcells = []
        for c in __ipynb_data["cells"]:
            # 移除空 cell
            lst = [i.strip() for i in c["source"]]
            if set(lst) == {""} or lst == []:
                continue
            # 移除前面的空行
            for i in lst:
                if i == "":
                    c["source"] = c["source"][1:]
                else:
                    break
            # 移除后面的空行
            for i in lst[::-1]:
                if i == "":
                    c["source"] = c["source"][:-1]
                else:
                    break
            # 移除最后的换行符
            if c["source"][-1][-1] == "\n":
                c["source"][-1] = c["source"][-1][:-1]
            __newcells.append(c)
        __ipynb_data["cells"] = __newcells
        self.write(__ipynb_data, is_print=is_print)
        return __ipynb_data

    def split_markdown_cells(self, __ipynb_data=None, ignore_quote=True):
        """拆分 markdown cell;ignore_quote 参数是否忽略 ```符号，如果内容中包含```就忽略"""
        print(self.filepath)
        if __ipynb_data == None:
            __ipynb_data = self.read()
        __newcells = []

        for __cell in __ipynb_data["cells"]:
            if len(__cell["source"]) == 0:
                print(self.filepath, "丢弃了一个空cell...")
            elif __cell["cell_type"] == "code":
                __newcells.append(__cell)
            elif __cell["source"][0].find("```") >= 0 and ignore_quote == True:
                __newcells.append(__cell)
            elif __cell["source"][0].find("> ") >= 0 and ignore_quote == True:
                __newcells.append(__cell)
            elif __cell["cell_type"] == "markdown":
                __lines = __cell["source"]
                __icell = {"cell_type": "markdown", "metadata": {}, "source": []}
                __ilines = []
                for l in __lines:
                    if l.replace(" ", "") == "\n" and len(__ilines) > 0:
                        __icell["source"] = __ilines
                        __newcells.append(__icell)
                        __icell = {
                            "cell_type": "markdown",
                            "metadata": {},
                            "source": [],
                        }
                        __ilines = []
                    if l.replace(" ", "") != "\n":
                        __ilines.append(l)
                if len(__ilines) > 0:
                    __icell["source"] = __ilines
                    __newcells.append(__icell)

        __ipynb_data["cells"] = __newcells
        self.write(__ipynb_data)
        __ipynb_data = self.remove_end_null()
        return __ipynb_data

    def change_cellstype_md2code(self, *sths):
        """把markdown cell 的代码转换为 code cell"""
        print(self.filepath, "change_cellstype_md2code...")
        filedata = self.read()
        data = self.remove_end_null(filedata)
        newcells = []
        for cell in data["cells"]:
            if cell["cell_type"] != "markdown":
                newcells.append(cell)
                continue
            if len(cell["source"]) < 2:
                newcells.append(cell)
                continue
            # 达标的类型：尾行和首行都带有```符号
            if cell["source"][-1].find(f"```") >= 0:
                firstline = cell["source"][0].lower()
                # html和markdown的code text 可处理为code cell
                if firstline.find(f"```html") >= 0:
                    cell["cell_type"] = "code"
                    cell["metadata"] = {"language": "html"}
                    cell["source"] = cell["source"][1:-1]
                elif (
                    firstline.find(f"```markdown") >= 0 or firstline.find(f"```md") >= 0
                ):
                    cell["cell_type"] = "code"
                    cell["metadata"] = {"language": "markdown"}
                    cell["source"] = cell["source"][1:-1]
                else:
                    for sth in sths:
                        if firstline.find(f"```{sth}") >= 0:
                            cell["cell_type"] = "code"
                            cell["source"] = cell["source"][1:-1]

            newcells.append(cell)

        data["cells"] = newcells
        data = self.remove_end_null(data)
        self.write(data)

    def change_cells_for_indent(self, sth, celltypes, indent=" ", lenth=2):
        "处理cell的缩进"
        print(self.filepath)
        data = self.read()
        newcells = []
        for cell in data["cells"]:
            # 达标的类型
            if (
                cell["cell_type"] in celltypes
                and len(cell["source"]) >= lenth
                and cell["source"][0].lower().find(sth) >= 0
            ):

                # 计算多少缩进是合适的
                n = 0
                flag = True
                while flag:
                    n += 1
                    for line in cell["source"]:
                        if line.replace(" ", "") != "\n" and not line.startswith(
                            indent * n
                        ):
                            flag = False
                            print(n)
                            break
                # 处理缩进
                n -= 1
                if n > 0:
                    newlines = []
                    for line in cell["source"]:
                        if line.replace(" ", "") != "\n" and line.startswith(
                            indent * n
                        ):
                            line = line[n:]
                        elif line.replace(" ", "") == "\n":
                            line = "\n"
                        newlines.append(line)
                    cell["source"] = newlines

            newcells.append(cell)

        data["cells"] = newcells
        data = self.remove_end_null(data)
        self.write(data)

    def update_content_by_cells(self, rules_update_content_by_cells=None):
        """以 cell 为单位处理数据"""

        if rules_update_content_by_cells == None:
            from _info_rules import rules_update_content_by_cells as rules
        else:
            rules = rules_update_content_by_cells

        print(self.filepath)
        __ipynb_data = self.read()

        # cell类型，单行或全检索，替换前，替换后，
        # 元组，字符串，表达式，表达式
        for rule in rules:
            __newcells = []
            for c in __ipynb_data["cells"]:
                if c["cell_type"] not in rule[0]:
                    __newcells.append(c)
                    continue
                if rule[1] == "line":
                    _lines = [re.sub(rule[2], rule[3], l) for l in c["source"]]
                elif rule[1] == "cell":
                    d = CellLines(c["source"])
                    data = re.sub(rule[2], rule[3], d.lines2text())
                    _lines = d.text2lines(data)
                c["source"] = _lines
                __newcells.append(c)
            __ipynb_data["cells"] = __newcells

        self.write(__ipynb_data)

    #########################【编辑任务常用方法】#########################################

    def transfile_text2ipynb(self):
        """把一个文本文件，转换为 ipynb 文件。"""

        textfile = self.filepath[:]
        __filename, __filetype = os.path.splitext(textfile)
        ipynbfile = textfile.replace(__filetype, ".ipynb")

        flag = True
        while flag:
            source = File(textfile).read()
            n = re.findall("```", source)
            if len(n) > 0 and len(n) % 2 != 0:  # 不能被整除
                asku = input(f"{textfile}源文件没有成对的 ``` 请前往修改>>")
                continue
            else:
                flag = False

        sources = [i for i in File(textfile).read().split("```") if len(i) > 0]
        n = 0
        __cells = []
        for source in sources:
            n += 1
            if n % 2 == 0:
                source = "```" + source + "```"

            __cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [i + "\n" for i in source.split("\n")],
                }
            )

        __ipynbdata = {
            "cells": __cells,
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 2,
        }
        JsonFile(ipynbfile).write(__ipynbdata)
        return ipynbfile

    def split_chapters(self, flag="## "):
        """拆分章节：单个章节过大，拆分为多个章节读取cells，挨个识别cell的起始是否为flag标记，如果是，则前面的cells为一个独立章节"""
        filedata = self.read()

        # 新章节模板
        newcopy = filedata.copy()
        newcopy["cells"] = []

        # 拆分章节
        cells = filedata["cells"]
        n = 0
        newcells = []
        for icell in cells:
            newcells.append(icell)
            if icell["cell_type"] == "markdown" and icell["source"][0].find(flag) == 0:
                # cell写入文件
                newfile = self.filepath.replace(".ipynb", f"_{n}.ipynb").replace(
                    " ", "_"
                )
                n += 1
                newcopy["cells"] = newcells[:-1]
                JsonFile(newfile).write(newcopy)
                newcells = [icell]
        else:
            # 最后的部分
            newfile = self.filepath.replace(".ipynb", f"_{n}.ipynb")
            newcopy["cells"] = newcells
            JsonFile(newfile).write(newcopy)

    def add_tags_to_cell(self, language, tags):
        """
        给章节按cell添加知识点tags
        只对markdown类型有效，code不添加
        """
        d = self.read()
        if self.language != language.lower():
            return
        cells = []
        for cell in d["cells"]:
            if cell["cell_type"] != "markdown":
                cells.append(cell)
                continue
            if "tags" not in cell["metadata"]:
                xtags = []
            else:
                xtags = cell["metadata"]["tags"]
            sdata = "".join(cell["source"])
            for tag in tags:
                print(tag)
                if tag not in xtags and sdata.find(tag) >= 0:
                    xtags.append(tag)
            if len(xtags) > 0:
                cell["metadata"]["tags"] = xtags
            cells.append(cell)
        d["cells"] = cells
        self.write(d)

    def add_metadata_to_mdcell_for_inserted(self):
        """
        检查章节中已经存在的内嵌习题和测验，并生成相应的metadata
        """

        data = self.read()
        cells = []
        for cell in data["cells"]:
            # 只处理 md cell
            if cell["cell_type"] != "markdown":
                cells.append(cell)
                continue
            # 获取已有的metadata
            if cell["metadata"] == {}:
                metadata = {}
            else:
                metadata = cell["metadata"]

            # 只对source做文本匹配，output不考虑
            sdata = "".join(cell["source"])

            # 检查习题
            qttn = r"\[.*?\]\(https://xue.cn/hub/app/exercise/(\d{1,4})\)"
            tagrlt = re.findall(qttn, sdata)
            if len(tagrlt) > 0:
                if "quesitons" not in metadata:
                    metadata["quesitons"] = [int(ix) for ix in tagrlt]
                else:
                    for ix in [int(ix) for ix in tagrlt]:
                        if ix not in metadata["quesitons"]:
                            metadata["quesitons"].append(ix)
            # 检查测验
            qttn = r"\[.*?\]\(https://xue.cn/hub/app/quiz/exam\?id=(\d{1,4})\)"
            tagrlt = re.findall(qttn, sdata)
            if len(tagrlt) > 0:
                if "quizset" not in metadata:
                    metadata["quizset"] = [int(ix) for ix in tagrlt]
                else:
                    for ix in [int(ix) for ix in tagrlt]:
                        if ix not in metadata["quizset"]:
                            metadata["quizset"].append(ix)

            if len(metadata) > 0:
                if "notes" not in metadata:
                    metadata["notes"] = "之前已有的内嵌习题及测验"
                cell["metadata"] = metadata
            cells.append(cell)
        data["cells"] = cells
        self.write(data)

    def add_tags_to_mdcell(self, tags_pttn):
        """
        对章节文件，按cell逐个添加知识点tags
        只对markdown类型有效，code不添加
        对于该章节是否应该做这个处理，另外封装方法判断；本方法内部不包含
        tags_pttn为字典，key为tag，值为该tags所满足的pttn
        """
        data = self.read()
        cells = []
        for cell in data["cells"]:
            # 只处理 md cell
            if cell["cell_type"] != "markdown":
                cells.append(cell)
                continue
            # 获取已有的tags
            if "tags" not in cell["metadata"]:
                xtags = []
            else:
                xtags = cell["metadata"]["tags"]
            # 只对source做文本匹配，output不考虑
            sdata = "".join(cell["source"])
            # 逐个匹配并变价tags
            for tag in tags_pttn:
                if tag in xtags:
                    continue
                tagrlt = re.findall(tags_pttn[tag], sdata)
                if len(tagrlt) > 0:
                    xtags.append(tag)
            if len(xtags) > 0:
                cell["metadata"]["tags"] = xtags
            cells.append(cell)
        data["cells"] = cells
        self.write(data)

    def remove_mdcell_for_inserted(self):
        """
        对章节文件，按cell检查是否仅有内嵌习题。并做拆分处理。
        """
        data = self.read()
        cells = []
        for cell in data["cells"]:
            # 只处理 md cell
            if cell["cell_type"] != "markdown":
                cells.append(cell)
                continue
            # 仅处理之前已经检查出来的cell
            if "notes" not in cell["metadata"]:
                cells.append(cell)
                continue

            # 逐行处理
            lines = []
            for line in cell["source"]:
                a = line.find("https://xue.cn/hub/app/exercise") >= 0
                b = line.find("https://xue.cn/hub/app/quiz/exam") >= 0
                if a or b:
                    pass
                else:
                    lines.append(line)

            if len(lines) > 0:
                cell["source"] = lines
            cells.append(cell)
        data["cells"] = cells
        data = self.remove_end_null(data)
        self.write(data)

    def go_book_add_code_cell_for_main(self):
        """
        为了支持 go 代码 repl 模式，可在线运行：
        检查 go 的 code cell 是否有定义 main 函数，
        如果有定义，检查是否有调用，
        如果没有调用，则添加相应的调用语句
        """
        filedata = self.read()
        newcells = []
        for i in filedata["cells"]:
            if i["cell_type"] == "code":
                flag = False
                for l in i["source"]:
                    if l.find("func main() {") >= 0:
                        flag = True
                    # 调用语句在下，所以该方法可以保证，如果已有调用语句，flag会重新变成 False
                    elif l.find("main()") >= 0:
                        flag = False
                if flag:
                    i["source"][-1] += "\n"
                    i["source"].extend(
                        ["\n", "//小编增加下方一行代码以支持 xue.cn 在线运行\n", "\n", "main()"]
                    )
            newcells.append(i)
        filedata["cells"] = newcells
        self.write(filedata)

    def go_book_add_import_fmt(self):
        """
        为了支持 go 代码 repl 模式，可在线运行：
        检查 go 的 code cell 是否有调用 fmt. 包
        如果有调用，检查是否有导入语句
        如果没有导入语句，则添加相应的导入语句
        """
        filedata = self.read()
        newcells = []
        for i in filedata["cells"]:
            if i["cell_type"] == "code":
                flag = False
                for l in i["source"]:
                    if l.find("fmt.") >= 0:
                        flag = True
                    elif l.find("import ") >= 0:
                        flag = False
                        break
                if flag:
                    text = "".join(i["source"])
                    if text.find("package") >= 0:
                        i["source"].insert(2, 'import "fmt"\n')
                        i["source"].insert(3, "\n")
                    else:
                        i["source"].insert(0, 'import "fmt"\n')
                        i["source"].insert(1, "\n")

            newcells.append(i)
        filedata["cells"] = newcells
        self.write(filedata)

    def to_md(self, markdown_filepath=None, is_output=False):
        """
        output ipynbfile to markdown file
        is_output: 是否导出输出信息
        """

        if not self.filepath.endswith(".ipynb"):
            raise ValueError(f"{filepath}\n not .ipynb file")

        data = self.read({})
        try:
            language = data["metadata"]["language_info"]["name"]
        except:
            language = "text"

        datastr = ""
        for cell in data.get("cells") or []:
            if cell["cell_type"] == "code":
                datastr += f"```{language}\n" + "".join(cell["source"]) + "\n```\n\n"
                if is_output:  # 运行结果导出不够全面完整
                    if len(cell["outputs"]) > 0:
                        outputs = "**Returns**:\n\n"
                        for j in cell["outputs"]:
                            if j["output_type"] == "execute_result":
                                outputs += "".join(j["data"]["text/plain"]) + "\n\n"
                            elif j["output_type"] == "error":
                                outputs += "**Error**: " + j["evalue"] + "\n\n"
                            else:
                                print(j["output_type"])
                        datastr += outputs
            else:
                datastr += "".join(cell["source"]) + "\n\n"

        markdown_filepath = markdown_filepath or self.filepath.replace(".ipynb", ".md")
        File(markdown_filepath).write(datastr)
