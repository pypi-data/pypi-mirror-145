import os
from typing import List, Dict
from .jsonfile import JsonFile


class Dir:
    """About dir."""

    def __init__(self, dirpath):
        """

        Args:
            dirpath (str): the path of the dir.
        """
        self.dirpath = dirpath

    def check(self, tododir=None):
        """check the dirpath exists and create it if not.

        Args:
            tododir (str, optional): the dirpath to check. Defaults to self.dirpath.
        """
        dirpath = tododir or self.dirpath
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    def get_subdirs(self, tododir=None):
        """获取 dirpath 下的首层文件夹"""
        dirpath = tododir or self.dirpath

        rlt = []
        for i in os.listdir(dirpath):
            idir = os.path.join(dirpath, i)
            if os.path.isdir(idir):
                rlt.append(idir)
        return rlt

    def get_subdirs_for_livebooks(self, tododir=None):
        """get_subdirs 针对 live books 的特殊封装：本地 live books 对书籍进行了二次分组，并用 sub_ 来标记分组"""

        tododir = tododir or self.dirpath
        subdirs = []
        for i in self.get_subdirs(tododir):
            # todo: more pythonic.
            if i.split("\\")[-1].startswith("sub_"):
                subdirs.extend(self.get_subdirs(i))
            else:
                subdirs.append(i)
        return subdirs

    def search_files_by_types(self, filetypes) -> List:
        """搜索文件夹中指定类型的文件，返回文件的绝对路径构成的列表"""
        filepaths = []
        for roots, dirnames, filenames in os.walk(self.dirpath):
            for ifile in filenames:
                if ifile.endswith(filetypes):
                    xfile = os.path.join(roots, ifile)
                    filepaths.append(xfile)
        return filepaths

    def search_files_by_names(self, names: List) -> List:
        """搜索指定文件夹中名字含有某些词片段的文件，返回文件的绝对路径构成的列表；可指定多个片段"""
        filepaths = []
        for roots, dirnames, filenames in os.walk(self.dirpath):
            for ifile in filenames:
                for iname in names:
                    if ifile.find(iname) >= 0:
                        xfile = os.path.join(roots, ifile)
                        filepaths.append(xfile)
                        break
        return filepaths

    def move_dirs(self, afdir):
        """把 dirpath 作为一个整体，不改名，移动到 afdir 目录之下"""
        at = os.path.join(afdir, os.path.basename(self.dirpath))
        if os.path.exists(at):
            return print(at, "已存在该文件夹，改名自动取消")
        self.check(afdir)
        os.rename(self.dirpath, at)

    def black(self):
        """采用 black 自动对本目录所有 .py 源文件处理为 PEP8 规范"""

        for i in self.search_files_by_types(".py"):
            os.system(f"black {i}")

    def rewrite_jsonfiles(self, filetypes=(".json", ".ipynb")):
        """重新读写文件，包括ipynb文件和xue.cn.json文件"""

        for i in self.search_files_by_types(filetypes):
            if i.find("checkpoint") == -1:
                JsonFile(i).rewrite()

    def zip(self, to_zipfile, mode=None, not_dirname=None, not_filetype=None):
        """Open the ZIP file with mode read 'r', write 'w', exclusive create 'x',or append 'a'."""
        import zipfile

        not_dirname = not_dirname or [
            "__pycache__",
            ".pytest_cache",
            ".git",
        ]
        not_filetype = not_filetype or (".7z", ".db", ".zip")
        mode = mode or "a"

        zf = zipfile.ZipFile(to_zipfile, mode)
        self.__zip_add_file(self.dirpath, zf, not_dirname, not_filetype)
        zf.close()

    def __zip_add_file(self, path, zf, not_dirname, not_filetype):
        for subpath in os.listdir(path):
            if subpath in not_dirname:
                continue
            subpath = os.path.join(path, subpath)
            if os.path.isfile(subpath):
                if not subpath.endswith(not_filetype):
                    zf.write(subpath)
            elif os.path.isdir(subpath):
                zf.write(subpath)
                self.__zip_add_file(subpath, zf, not_dirname, not_filetype)
