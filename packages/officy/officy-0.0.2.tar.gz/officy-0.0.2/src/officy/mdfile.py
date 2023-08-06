import os
import re
import copy
from .myfile import File
from .jsonfile import JsonFile


class MdFile(File):
    """纯文本处理方法"""

    def __init__(self, filepath):
        super().__init__(filepath)
        self.filedata = self.read()

    ####################### 获得纯文本（.md）文件 #######################

    def html2md(self):
        """将一个 html 文件转为 md 文件"""
        import html2text

        data = html2text.html2text(self.filedata)
        self.filepath = self.filepath.rsplit(".", 1)[0] + ".md"
        self.write(data)

    def rst2md(self):
        os.system(f'pandoc -o {self.filepath.rsplit(".",1)[0]+".md"} {self.filepath}')

    ############################ 文本预处理 #############################

    def link_to_inline(self, data=None):
        """文件中超链接参考式替换为行内式，避免拆开后失效"""
        if data == None:
            data = self.filedata
        title = re.findall(r"(\[[^\]]+?\])(\[[^\]]+?\])", data)
        link = re.findall(r"(\[[^\]]+?\])(:[ \n]{0,1})(http.+)", data)
        for t in title:
            for l in link:
                if l[0] == t[1]:
                    data = data.replace(
                        t[0] + t[1], t[0] + f"({l[2].strip()})"
                    ).replace("".join(l), "")

        # title1 = re.findall(r"(\[[^\]]+?\])[^:\(]", data)
        # link1 = re.findall(r"(\[[^\]]+?\])(:[ \n]{0,1})(http.+)", data)
        # for t in title1:
        #     for l in link1:
        #         if l[0] == t:
        #             data = data.replace("".join(l), "").replace(t, t + f"({l[2].strip()})")
        return data

    def pretreatment(self):
        """文件内容中存在的简单又必须提前处理的问题综合处理"""
        data = self.filedata
        # ``` 标记的行内代码改为 ` 标记
        data = re.sub(r"```(.+?)```", r"`\1`", data)
        # \t 统一替换为 4 个空格
        data = data.expandtabs(4)
        # 参考式转行内式
        data = self.link_to_inline(data)
        # --- 或 === 标记的标题换成 #（可能有遗漏或特殊情况，需检查）
        data = re.sub(r"\n\n([^ #\n].*)\n----+\n\n", r"\n\n## \1\n\n", data)
        data = re.sub(r"([^ #\n].*)\n====+\n\n", r"# \1\n\n", data)
        # 待添加
        pass

        self.write(data)

    def split_md_chapters(self, flag="## "):
        """拆分 md 文件章节，更便于处理目录及知识结构，flag 至少两个 #，避免拆开code"""
        data_list = self.filedata.split(f"\n{flag}")
        n = 1
        for i in data_list:
            newfile = self.filepath.rsplit(".", 1)[0] + f"_{n}.md"
            if i != data_list[0]:
                i = flag + i
            File(newfile).write(i)
            n += 1

    ############################## 转换为 ipynb #############################

    def group_md(self):
        """将一个 md 文件内容分组，code 分到一组一个 cell，文本按空行拆成多个cell"""
        data = self.filedata
        if data.strip() == "":
            return print(self.filepath, "是空文件")

        matches = re.finditer(r" *```| *> *```", data, re.M)
        indices = [match.span()[0] for match in matches]
        if len(indices) % 2 != 0:
            return print(self.filepath, "```不成对，请修改")

        indices.append(len(data))
        if indices[0] != 0:
            indices.insert(0, 0)
        else:
            return print(self.filepath, "以```开始，请修改再分组")

        groups = [data[indices[i] : indices[i + 1]] for i in range(len(indices) - 1)]
        cells = []
        for i in range(len(groups)):
            # markdown 文本
            if i % 2 == 0:
                if groups[i].strip("> ").startswith("```"):
                    cells.extend(
                        [
                            i
                            for i in groups[i].strip("> ")[3:].split("\n\n")
                            if i.strip() != ""
                        ]
                    )
                else:
                    cells.extend(
                        [i for i in groups[i].split("\n\n") if i.strip() != ""]
                    )
            # code 文本
            else:
                ind = re.findall(r"([> ]+?)```", groups[i])
                if ind:
                    # code 统一缩进
                    lines = groups[i].rstrip().split("\n")
                    for l in range(len(lines)):
                        lines[l] = lines[l][len(ind[0]) :]
                    groups[i] = "\n".join(lines + ["```"])
                    cells.append(groups[i])
                else:
                    cells.append(groups[i].strip() + "\n```")
        return cells

    def md2ipynb(self, language="python", time=1):
        """将一个 md 文件转换为 ipynb 文件，根据语言环境，能运行的语言转换为 code cell"""
        data = {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 2}
        cells = {"cell_type": "markdown", "metadata": {}, "source": []}

        if self.group_md():
            for i in self.group_md():
                lan = re.findall(r"```(\w+)", i)
                if lan:
                    lan = lan[0].lower()
                    code_source = i.splitlines(True)[1:-1]
                    if lan == "html":
                        cd = copy.deepcopy(cells)
                        cd["metadata"]["language"] = "markdown"
                        cd["cell_type"] = "code"
                        cd["source"] = code_source
                        data["cells"].append(cd)
                    elif lan in CODE_SIGENAL[language]:
                        cd = copy.deepcopy(cells)
                        cd["cell_type"] = "code"
                        cd["source"] = code_source
                        data["cells"].append(cd)
                    else:
                        cd = copy.deepcopy(cells)
                        cd["source"] = i.splitlines(True)
                        data["cells"].append(cd)
                else:
                    cd = copy.deepcopy(cells)
                    cd["source"] = i.splitlines(True)
                    data["cells"].append(cd)

        data["metadata"] = IPYNB_METAINFO[language]
        if "." in self.filepath.split("\\")[-1]:
            filepath = self.filepath.rsplit(".", 1)[0] + ".ipynb"
        else:
            filepath = self.filepath + ".ipynb"
        # 第一次转换要判断是否重名
        if os.path.exists(filepath) and time == 1:
            print(filepath, "已经存在，请修改再转换。")
        else:
            JsonFile(filepath).write(data)

    def code2ipynb(self, filetypes=(".py", ".go", ".js", ".html"), n=1):
        """将一个脚本文件整体转换为 ipynb 文件，并将 文件名 作为标题，可运行的脚本转换为 code"""
        # n 控制文件标题, n=1 表示文件名作为标题名
        title = "/".join(self.filepath.rsplit("\\", n)[-n:])
        path_structure = self.filepath.split(DIR_INFO["books"]["dev"] + "\\")[
            -1
        ].replace("\\", "/")
        _, filetype = os.path.splitext(self.filepath)
        source = self.filedata.expandtabs(4)
        data = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"# {title}\n", f"文件目录结构：{path_structure}"],
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": source.strip().splitlines(True),
                },
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 2,
        }
        if data["cells"][1]["source"] == []:
            print(self.filepath, "是空文件")
        else:
            if filetype in (".html", ".htm"):
                data["cells"][1]["metadata"]["language"] = "markdown"
                data["metadata"] = IPYNB_METAINFO["python"]
            elif filetype == ".js":
                data["metadata"] = IPYNB_METAINFO["javascript"]
            elif filetype == ".go":
                data["metadata"] = IPYNB_METAINFO["go"]
            elif filetype == ".py":
                data["metadata"] = IPYNB_METAINFO["python"]
            else:
                data["cells"][1]["cell_type"] = "markdown"
                data["cells"][1]["source"] = (
                    ["```" + filetype.strip(".") + "\n"]
                    + data["cells"][1]["source"][:-1]
                    + [data["cells"][1]["source"][-1] + "\n", "```"]
                )
                data["metadata"] = IPYNB_METAINFO["python"]

            if "." in self.filepath.split("\\")[-1]:
                filepath = self.filepath.rsplit(".", 1)[0] + ".ipynb"
            else:
                filepath = self.filepath + ".ipynb"
            if os.path.exists(filepath):
                print(filepath, "已经存在，已修改并转换，注意修改调用")
                filepath = "_".join(self.filepath.rsplit(".", 1)) + ".ipynb"
            JsonFile(filepath).write(data)
