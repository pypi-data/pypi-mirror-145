import json
import os
import re
from typing import List, Dict


class File:
    """Methods for a file."""

    def __init__(self, filepath: str):
        """
        Args:
            filepath (str): the path of file.
        """
        self.filepath = filepath

    def read(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            filedata = f.read()
        return filedata

    def write(self, filedata: str, mode: str = "w", is_print: bool = True):
        with open(self.filepath, mode, encoding="utf-8") as f:
            f.write(filedata)
        if is_print:
            print(self.filepath, f"mode:{mode} write done.")

    def readlines(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return lines

    def writelines(self, lines: List, mode: str = "w", is_print: bool = True):
        with open(self.filepath, mode, encoding="utf-8") as f:
            f.writelines(lines)
        if is_print:
            print(self.filepath, f"mode:{mode} writelines done.")

    def change_filetype(self, fromtype, totype):
        """修改文件类型，会直接覆盖原文件"""
        if self.filepath.endswith(fromtype):
            af = self.filepath[: -len(fromtype)] + totype
            os.rename(self.filepath, af)
            return af
        return print(self.filepath, f"文件类型不是 {fromtype}，无法修改")

    def copy_file_to_other_type(self, fromtype, totype, is_cover=True):
        """修改文件类型，is_cover 是否覆盖已存在的文件"""
        if self.filepath.endswith(fromtype):
            bf = self.filepath
            af = bf[: -len(fromtype)] + totype
            if os.path.exists(af):
                if not is_cover:
                    return print(af, f"文件已存在，指定 is_cover 为 False 可覆盖")
                os.remove(af)
            os.system(f'copy "{bf}" "{af}"')
            return af
        return print(self.filepath, f"文件类型不是 {fromtype}，无法修改")

    def run_batgit(self, gitclis=None):
        """把命令行文本写文件并运行"""
        if not self.filepath.endswith(".bat"):
            return print("文件类型不符")
        if gitclis == None:
            gitclis = self.readlines()
        elif type(gitclis) != list:
            return print("请提供列表形式的命令行")
        else:
            self.writelines(gitclis)
        os.system(self.filepath)

    @classmethod
    def zh_format_text(cls, data: str) -> str:
        """format for zh-text.

        a classmethod. use as: `File.zh_format_text(data)`

        Args:
            data (str): the data with zh(Chinese Words).

        Returns:
            str: the data formated.
        """

        # 中文和英文、数字之间应有空格
        data = re.sub(r"([\u4e00-\u9fa5])([\da-zA-Z])", r"\1 \2", data)
        data = re.sub(r"([\da-zA-Z])([\u4e00-\u9fa5])", r"\1 \2", data)

        # 多个换行，改为单个换行
        data = re.sub(r"\n{3,}", r"\n\n", data)

        # 文件首尾的多余换行
        data = re.sub(r"^[\n ]+", r"", data)
        data = re.sub(r"[\n ]+$", r"", data)
        return data

    def zh_format(self):
        """format for file with zh-text.

        File(filepath).zh_format()
        """
        data = self.read()
        data = self.zh_format_text(data)
        self.write(data)

    @classmethod
    def quote_json_format_text(cls, data: str) -> str:
        """format data with json-quoted. only json-quoted  was formated.

        classmethod.use as `data = File.quote_json_format_text(data)`.

        Args:
            data (str): the data with json-quoted  need to format.

        Returns:
            str: the data with json-quoted   formated.
        """

        from .jsonfile import JsonFile

        tp = r"\n```json\n+([\s\S]+?)```"
        rs = re.findall(tp, data)
        for i in rs:
            try:
                ix = json.loads(i)
                JsonFile("temp.json").write(ix, indent=4)
                ix = File("temp.json").read()
                data = data.replace(i, str(ix).replace("'", '"') + "\n")
            except Exception as e:
                print(i)
                print(e)
        return data

    def quote_json_format(self):
        """format file with json-quoted data."""

        data = self.read()
        data = self.quote_json_format_text(data)
        self.write(data)
        self.zh_format()

    def zip(self, to_zipfile=None, mode="w"):
        import zipfile

        to_zipfile = to_zipfile or os.path.join(self.filepath, "_.zip")
        zf = zipfile.ZipFile(to_zipfile, mode, zipfile.ZIP_DEFLATED)
        zf.write(self.filepath, arcname=os.path.basename(self.filepath))
        zf.close()

    def split(self, size=256):
        """split big file to small files.

        Args:
            size (int, optional): Each small file defaults to 256 Mb.
        """

        from .mydir import Dir

        file_dir, file_name = os.path.split(self.filepath)
        file_name, file_type = os.path.splitext(file_name)
        file_dir = os.path.join(file_dir, file_name)
        Dir(file_dir).check()

        file_num = 0
        stream = open(self.filepath, "rb")

        while True:
            part_file_name = os.path.join(
                file_dir, f"{file_name}_{file_num}{file_type}"
            )
            print(f"split file start {part_file_name}")
            part_stream = open(part_file_name, "wb")

            read_count = 0
            read_size = 1024 * 1024 * size

            while True:
                read_content = stream.readline()
                if not read_content:
                    print("split done")
                    return
                read_count_per = len(read_content)

                if read_count_per > 0:
                    part_stream.write(read_content)
                else:
                    break

                read_count += read_count_per
                if read_count > read_size:
                    break
            part_stream.close()
            file_num += 1
