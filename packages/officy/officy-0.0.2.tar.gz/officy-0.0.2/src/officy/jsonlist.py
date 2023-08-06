class JsonList:
    """自定义数据类型，由字典 item 构成 的列表"""

    def __init__(self, data):
        if not self.is_jsonlist(data):
            print("JsonList 初始化时检查失败，并不是合法的jsonlist数据类型")
        self.jsonlist = data

    def is_jsonlist(self, data):
        """检查数据是否形如 [{},{}]这类json data"""
        if data in ([], {}):
            return True
        if len(data) == 0:
            return print("数据为空，无法检测")
        if type(data) != list or type(data[0]) != dict:
            return print("参数类型不符，需要是形如 [{},{}] 的列表数据")
        return True

    def find_values_for_list(self, idkey):
        """从jsonlist中，读取idkey的值，构成列表"""
        rlt = {}
        for i in self.jsonlist:
            if idkey in i:
                if type(i[idkey]) == list:
                    for j in i[idkey]:
                        if j not in rlt:
                            rlt[j] = 1
                        else:
                            rlt[j] += 1
        return rlt

    def find_values_by_idkey(self, idkey, jsonlist=None):
        """从jsonlist中，读取idkey的值，构成列表"""
        import pandas as pd

        if jsonlist == None:
            jsonlist = self.jsonlist
        try:
            df = pd.DataFrame(jsonlist)
            return list(df[idkey].values)
        except:
            return []

    def check_key(self, key, jsonlist=None):
        """检查形如 [{},{}]中每个item是否包含指定的key，检查结果有3类：0全不包含，1全包含，2部分包含"""
        if jsonlist == None:
            jsonlist = self.jsonlist

        n = 0
        for item in jsonlist:
            if key in item:
                n += 1
        if n == len(jsonlist):
            print(f"所有 item 都包含 {key} 字段")
            return 1
        elif n == 0:
            print(f"所有 item 都不包含 {key} 字段")
            return 0
        else:
            print(f"{n} 个 item 包含 {key} 字段，{len(jsonlist)-n} 个不包含")
            return 2

    def find_items_without_key(self, key):
        """从jsonlist中寻找不存在key的items"""
        rlt = []
        for item in self.jsonlist:
            if key not in item:
                rlt.append(item)
        return rlt

    def find_item_by_unique_value(self, key, value):
        """检查 key 的值 等于 value 的 item，且仅有一个"""
        rlt = self.find_items_by_value(key, value)
        if len(rlt) != 1:
            return print(key, value, f"结果数量不符，共有{len(rlt)}个")
        return rlt[0]

    def find_ids_by_unique(self, key, idkey):
        """找到某个item（根据key为辨识）是否重复，如果存在重复则返回该item；比如 id 只能全局唯一"""
        info = self.count_value_by_key(key)
        values = [k for i, k in enumerate(info) if info[k] > 1]

        rlt = {}
        for value in values:
            irlt = self.find_items_by_value(key, value)
            rlt[value] = self.find_values_by_idkey(idkey, irlt)
        return rlt

    def find_ids_without_key(self, key, idkey):
        """从jsonlist中寻找不存在key的items，返回idkey构成的列表"""
        items = self.find_items_without_key(key)
        ids = self.find_values_by_idkey(idkey, items)
        if len(ids) > 0:
            print(f"{idkey} 为 {ids} 的 {key} 字段不存在")
        return ids

    def find_items_with_null(self, key):
        """从jsonlist中寻找key的值为空的items"""
        rlt = []
        for item in self.jsonlist:
            if item[key] in ["", {}, [], set(), tuple()]:
                rlt.append(item)
        return rlt

    def find_ids_with_null(self, key, idkey):
        """从jsonlist中寻找不存在key的items，返回idkey构成的列表"""
        items = self.find_items_with_null(key)
        ids = self.find_values_by_idkey(idkey, items)
        if len(ids) > 0:
            print(f"{idkey} 为 {ids} 的 {key} 字段为空")
        return ids

    def find_items_by_value(self, key, value):
        """检查 key 的值 等于 value 的 items"""
        rlt = []
        for item in self.jsonlist:
            if item[key] == value:
                rlt.append(item)
        return rlt

    def find_ids_by_value(self, key, value, idkey):
        """从jsonlist中寻找不存在key的items，返回idkey构成的列表"""
        items = self.find_items_by_value(key, value)
        ids = self.find_values_by_idkey(idkey, items)
        if len(ids) > 0:
            print(f"{idkey} 为 {ids} 的 {key} 字段 == {value} 值")
        return ids

    def find_items_by_value_in(self, key, value):
        """检查 key 的值 包含 value 的 items"""
        rlt = []
        for item in self.jsonlist:
            if value in item[key]:
                rlt.append(item)
        return rlt

    def find_ids_by_value_in(self, key, value, idkey):
        """检查 key 的值 包含 value 的items,返回id的值的列表"""
        items = self.find_items_by_value_in(key, value)
        ids = self.find_values_by_idkey(idkey, items)
        print(f"{idkey} 为 {ids} 的 {key} 字段的值 包含 {value}")
        return ids

    def find_items_by_value_for_check_unique(self, key):
        """找到某个key的取值是否存在重复值，如果存在重复则返回该item；比如 quizset 的习题id 字段的值需要唯一"""
        rlt = []
        for item in self.jsonlist:
            if len(item[key]) > len(set(item[key])):
                rlt.append(item)
        return rlt

    def find_ids_by_value_for_check_unique(self, key, idkey):
        """找到某个key的取值是否存在重复值，如果存在重复则返回该item的idkey构成的列表"""
        items = self.find_items_by_value_for_check_unique(key)
        ids = self.find_values_by_idkey(idkey, items)
        if len(ids) > 0:
            print(f"{idkey} 为 {ids} 的 {key} 字段存在重复值")
        return ids

    def find_items_by_diff_lenth_for_keys(self, *keys):
        """找到两个字段的值长度不一致的item"""
        rlt = []
        for item in self.jsonlist:
            l = [len(item[key]) for key in keys]
            if len(set(l)) > 1:
                rlt.append(item)
        return rlt

    def find_ids_by_diff_lenth_for_keys(self, idkey, key1, key2):
        """找到两个字段的值长度不一致的item，返回它们的idkey的值"""
        items = self.find_items_by_diff_lenth_for_keys(key1, key2)
        ids = self.find_values_by_idkey(idkey, items)
        if len(ids) > 0:
            print(f"{idkey} 为 {ids} 的 {key1} {key2} 字段长度不一致")
        return ids

    def count_value_by_key(self, key, jsonlist=None):
        """统计某个字段 key 的所有取值及每个取值的数量，key值不是列表"""
        if jsonlist == None:
            jsonlist = self.jsonlist

        rlt = {"without_key": 0}
        for item in jsonlist:
            if key not in item:
                rlt["without_key"] += 1
            elif item[key] in rlt:
                rlt[item[key]] += 1
            else:
                rlt[item[key]] = 1
        return rlt

    def count_values_for_each_by_key(self, key, jsonlist=None):
        """统计某个字段 key 的所有取值及每个取值的数量，key值是列表"""
        if jsonlist == None:
            jsonlist = self.jsonlist

        rlt = {"without_key": 0}
        for item in jsonlist:
            if key not in item:
                rlt["without_key"] += 1
            else:
                for k in item[key]:
                    if k in rlt:
                        rlt[k] += 1
                    else:
                        rlt[k] = 1
        return rlt

    def update_by_add_key_value(self, idkey, ids, key, keyvalue, data=None):
        """给特定的items 的 指定key 添加一个新的值 keyvalue"""
        if data == None:
            data = self.jsonlist
        rlt = {"done": [], "todo": []}
        for i in data:
            if i[idkey] in ids:
                if type(i[key]) == list:
                    if keyvalue not in i[key]:
                        i[key].append(keyvalue)
                        rlt["done"].append(i[idkey])
                    else:
                        rlt["todo"].append(i[idkey])
        return data, rlt

    def update_by_replace_key_value(self, idkey, key, keyvalue, newkeyvalue, data=None):
        """给特定的items 的 指定key 的值更新为一个新值"""
        if data == None:
            data = self.jsonlist
        for i in data:
            if type(i[key]) == list and keyvalue in i[key]:
                i[key].remove(keyvalue)
                i[key].append(newkeyvalue)
            if type(i[key]) == str and keyvalue == i[key]:
                i[key] = newkeyvalue
        return data

    def update_by_remove_value_in(self, key, keyvalue, idvalues, idkey="id", data=None):
        """移除指定字段中的某个值"""
        if data == None:
            data = self.jsonlist
        for i in data:
            if i["id"] in idvalues and keyvalue in i[key]:
                i[key].remove(keyvalue)
        return data

    def update_by_relpace_from_ids(self, idkey, ids, key, newvalue, data=None):
        """idkey的值在ids里的数据，它的key值替换为 newvalue"""
        if data == None:
            data = self.jsonlist
        for i in data:
            if i[idkey] in ids:
                i[key] = newvalue
        return data

    def check_value_in_values(self, key, values, idkey, data=None):
        """ "检查某个字段 key 的取值是否都存在于 values 之中"""
        if data == None:
            data = self.jsonlist
        rlt = {}
        for i in data:
            for ivalue in i[key]:
                if ivalue not in values:
                    if ivalue not in rlt:
                        rlt[ivalue] = [i[idkey]]
                    else:
                        rlt[ivalue].append(i[idkey])
        # 打印结果
        for i, k in enumerate(rlt):
            print(f"字段 {key} 的值【{k}】不在合法的取值范围，{idkey}：{rlt[k]} 请注意修改")
        print("check_value_in_values is done.")
        return rlt
