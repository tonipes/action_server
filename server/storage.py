import falcon
import uuid

class ModuleStorage(object):

    def __init__(self, pages):
        pages = self._build_tree(pages)
        self.tree = pages

    def _build_tree(self, tree):
        new_tree = {}
        if type(tree) is list:
            new_tree = {self.get_item_key(i): self._build_tree(i) for i in tree}
        elif type(tree) is dict:
            for k, v in tree.items():
                if type(v) is list:
                    new_tree[k] = {self.get_item_key(i): self._build_tree(i) for i in v}
                else:
                    new_tree[k] = self._build_tree(v)
        else:
            new_tree = tree
        return new_tree


    def get_from(self, levels):
        cur_tree = self.tree
        for level in levels:
            if level in cur_tree:
                cur_tree = cur_tree[level]
            else:
                return None
        return cur_tree

    def get_item_key(self, item):
        if 'name' in item:
            return self.slugify(item['name'])
        else:
            return str(uuid.uuid4())[:8]

    def slugify(seld, name):
        return name.lower().replace(' ', '_')

class EngineStorage(object):
    def __init__(self, engines):
        self.engines = engines

    def get(self, id):
        try:
            engine = self.engines[id]
        except KeyError:
            return None
        return engine
