import os
import json
import datetime
from .jsonlist import JsonList


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np

        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.datetime):
            return obj.__str__()
        elif isinstance(obj, datetime.date):
            return obj.__str__()
        else:
            return super(NpEncoder, self).default(obj)


class JsonFile:
    """About .json file."""

    def __init__(self, filepath):
        self.filepath = filepath

    @property
    def data(self):
        return self.read()

    def read(self, nulldata=[]):
        if not os.path.exists(self.filepath):
            return nulldata

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"{self.filepath} {e}")

    def write(self, data, indent=1, is_cover=True):
        from .mydir import Dir

        filepath = self.filepath
        if os.path.exists(self.filepath) and is_cover == False:
            filepath += f"_{datetime.date.today()}_temp.json"

        # check the dirpath exists and makedirs.
        Dir(os.path.dirname(os.path.abspath(filepath))).check()

        with open(filepath, "w", encoding="utf-8") as f:
            try:
                json.dump(data, f, indent=indent, sort_keys=False, ensure_ascii=False)
            except:
                json.dump(
                    data,
                    f,
                    indent=indent,
                    sort_keys=False,
                    ensure_ascii=False,
                    cls=MyEncoder,
                )

    def rewrite(self, nulldata=[]):
        self.write(self.read(nulldata=nulldata))

    def merge_jsonlist(self, key, jsonlist):
        """把新数据融入到json数据文件中，item 的唯一标记符为参数 key；如果key值item不存在则添加，存在则不作任何处理"""
        old = self.read()
        oc = JsonList(old).check_key(key)
        nc = JsonList(jsonlist).check_key(key)
        if oc != 1 or nc != 1:
            return print(f"{key} 并不存在于所有的item")

        oldkeys = [i[key] for i in old]
        for j in jsonlist:
            if j[key] not in oldkeys:
                old.append(j)
        JsonFile(self.filepath).write(old)

    def merge_jsondata_of_dict(self, dictdata):  # 没被调用过
        data = self.read(nulldata={})
        data.update(dictdata)
        JsonFile(self.filepath).write(data)
