
import json
import re

import lxml.html

def dict2html(data, indent=0):
    indent_str = '  '*indent
    if isinstance(data, dict):
        res = ''
        for k, v in data.items():
            v_html = dict2html(v, indent + 1)
            res += u'{0}<div class="{1}">\n{2}{0}</div>\n'.format(indent_str, k, v_html)
        return res
    elif isinstance(data, list):
        res = ''
        for item in data:
            item_html = dict2html(item, indent + 1)
            res += u'{0}<div>\n{1}{0}</div>\n'.format(indent_str, item_html)
        return res
    else:
        return u'{0}{1}\n'.format(indent_str, unicode(data))

def html_text(html_str):
    data = lxml.html.fromstring(html_str)
    return data.text_content().strip()

class JsonSelectorNavigator:
    _Descendant = 1
    _Child = 2

    _DescendantPattern = r'\s+'
    _ChildPattern = r'\s*>\s*'
    _Separator = re.compile(r'(%s|%s)'%(_ChildPattern, _DescendantPattern))

    _ArrayPattern = re.compile(r'(\w*)\s*\[\s*(\d+)\s*\]')

    def __init__(self, data):
        self.data = data
        self.is_leaf = not isinstance(data, dict)

    def identify_target(self, target_str):
        arr = JsonSelectorNavigator._ArrayPattern.findall(target_str)
        if arr:
            target_name, index = arr[0]
            return (target_name.strip(), int(index))
        else:
            return target_str

    def selector_str_to_parts(self, selector):
        str_parts = re.split(JsonSelectorNavigator._Separator, selector.strip())
        if len(str_parts) == 1 and str_parts[0] == '':
            return []
        if str_parts[0].strip() == '>':
            raise Exception('Selector should not start with \'>\'')
        result = [(JsonSelectorNavigator._Descendant, self.identify_target(str_parts[0]))]
        for i in range(1, len(str_parts), 2):
            if str_parts[i].strip() == '>':
                scope = JsonSelectorNavigator._Child
            else:
                scope = JsonSelectorNavigator._Descendant
            target = self.identify_target(str_parts[i + 1])
            result.append((scope, target))
        return result

    def search_with_selector_parts(self, selector_parts, data_navigator):
        #print(selector_parts, data_navigator.data)
        if not selector_parts:
            return [data_navigator]
        if data_navigator.is_leaf:
            return []
        scope, target = selector_parts[0]
        others = selector_parts[1:]

        data = data_navigator.data
        data_parts = []

        def search_in_children(json_data, action_on_v):
            for k, v in json_data.items():
                if k == target:
                    data_parts.append(JsonSelectorNavigator(v))
                elif isinstance(target, tuple) and\
                  k == target[0] and isinstance(v, list) and len(v) > target[1]:
                    data_parts.append(JsonSelectorNavigator(v[target[1]]))
                action_on_v(v)

        if scope == JsonSelectorNavigator._Descendant:
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
        #print(data_parts)
        for p in data_parts:
            result += self.search_with_selector_parts(others, p)
        return result

    def search_all(self, selector):
        selector_parts = self.selector_str_to_parts(selector)
        return self.search_with_selector_parts(selector_parts, self)

    def css(self, selector):
        return self.search_all(selector)

    def extract(self):
        return str(self.data)

    def xpath(self, selector = 'text()'):
        """
        Only support text() for now.
        """
        return JsonSelectorNavigator(str(self.data))


if __name__ == '__main__':
    test_json_str ='''
{
    "a": 1,
    "b": [1,2,3,4,5],
    "c": {"a":"hello", "e": 2},
    "f": [{"e": 100, "b": true}, {"a": { "inner": {"data": 200}}}]
}
'''
    navigator = JsonSelectorNavigator(json.loads(test_json_str))
    assert map(lambda x: x.data, navigator.search_all('aa')) == []
    assert map(lambda x: x.data, navigator.search_all('a')) == [1, 'hello', { "inner": {"data": 200}}]
    #print(map(lambda x: x.data, navigator.search_all('b')))
    assert map(lambda x: x.data, navigator.search_all('b')) == [[1, 2, 3, 4, 5], True]
    assert map(lambda x: x.data, navigator.search_all('b[3]')) == [4]
    assert map(lambda x: x.data, navigator.search_all('e')) == [2, 100]
    assert map(lambda x: x.data, navigator.search_all('c e')) == [2]
    assert map(lambda x: x.data, navigator.search_all('f[1] > a data')) == [200]

