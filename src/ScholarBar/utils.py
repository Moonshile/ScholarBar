
import json
import re

class JsonSelectorNavigator(object):
    global _ChildPattern, _DescendantPattern, _Child, _Descendant, _ArrayPattern
    _Descendant = 1
    _Child = 2

    _DescendantPattern = r'\s+'
    _ChildPattern = r'\s*>\s*'

    _ArrayPattern = re.compile(r'(\w*)\s*\[\s*(\d+)\s*\]')

    def __init__(self, data):
        self.data = json.loads(data) if isinstance(data, (str, unicode)) else data
        self.cache = {}

    def identify_target(self, target_str):
        arr = _ArrayPattern.findall(target_str)
        if arr:
            target_name, index = arr[0]
            return (target_name.strip(), int(index))
        else:
            return target_str

    def selector_str_to_parts(self, selector):
        str_parts = re.split(r'(%s|%s)'%(_ChildPattern, _DescendantPattern), selector.strip())
        if len(str_parts) == 1 and str_parts[0] == '':
            return []
        if str_parts[0].strip() == '>':
            raise Exception('Selector should not start with \'>\'')
        result = [(_Descendant, self.identify_target(str_parts[0]))]
        for i in range(1, len(str_parts), 2):
            scope = _Child if str_parts[i].strip() == '>' else _Descendant
            target = self.identify_target(str_parts[i + 1])
            result.append((scope, target))
        return result

    def search_with_selector_parts(self, selector_parts, data):
        if not selector_parts:
            return [data]
        scope, target = selector_parts[0]
        others = selector_parts[1:]
        data_parts = []

        def search_in_children(json_data, action_on_v):
            for k, v in json_data.items():
                if k == target:
                    data_parts.append(v)
                elif isinstance(target, tuple) and\
                  k == target[0] and isinstance(v, list) and len(v) > target[1]:
                    data_parts.append(v[target[1]])
                action_on_v(v)

        if scope == _Descendant:
            def traverse(json_data):
                if isinstance(json_data, list):
                    for d in json_data:
                        traverse(d)
                elif isinstance(json_data, dict):
                    search_in_children(json_data, traverse)
            traverse(data)
        else:
            if isinstance(data, dict):
                search_in_children(data, lambda v: None)

        result = []
        # print(data_parts)
        for p in data_parts:
            result += self.search_with_selector_parts(others, p)
        return result

    def search_all(self, selector):
        selector_parts = self.selector_str_to_parts(selector)
        return self.search_with_selector_parts(selector_parts, self.data)


if __name__ == '__main__':
    test_json_str ='''
{
    "a": 1,
    "b": [1,2,3,4,5],
    "c": {"a":"hello", "e": 2},
    "f": [{"e": 100, "b": true}, {"a": { "inner": {"data": 200}}}]
}
'''
    navigator = JsonSelectorNavigator(test_json_str)
    assert navigator.search_all('aa') == []
    assert navigator.search_all('a') == [1, 'hello', { "inner": {"data": 200}}]
    assert navigator.search_all('b[3]') == [4]
    assert navigator.search_all('e') == [2, 100]
    assert navigator.search_all('c e') == [2]
    assert navigator.search_all('f[1] > a data') == [200]

