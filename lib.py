from metapensiero.pj.api import translates
from yattag import Doc, indent
import json
import inspect

class FuncObj(str):
    def __new__(cls, func, *args, **kwargs):
        name = func.__name__ + '()'
        obj = str.__new__(cls, name)
        obj.source = translates(
            inspect.getsource(func).split('\n', 1)[1],
            enable_es6=True)[0]
        return obj
    def add(self, _doc=None):
        if not _doc:
            global doc
            _doc = doc
        _doc.asis(self.source)

def jsfy(klass):
    def wrapper(func):
        value = FuncObj(func)
        klass.local[func.__name__] = value
        return value
    return wrapper

def domfy(klass):
    def wrapper(func):
        _doc, _tag, _text, _line = Doc().ttl()
        func(_doc, _tag, _text, _line)
        value = _doc.getvalue()
        klass.var[func.__name__] = value
        return value
    return wrapper

class Container(str):
    var = {}
    local = {}
    def __new__(cls, *args, **kwargs):
        t = str.__new__(cls, *args, **kwargs)
        obj = str.__new__(cls, t.__str__())
        return obj
    def render(self, doc, _, text, line):
        pass
    def __str__(self):
        doc, _, text, line = Doc().ttl()
        hold = {}
        if len(self.var) + len(self.local) > 0:
            with _('script'):
                for k, v in self.var.items():
                    doc.asis('var ' + k + ' = ' + json.dumps(v) + ';')
                for k, v in self.local.items():
                    v.add(doc)
        self.render(doc, _, text, line)
        result = doc.getvalue()
        for k, v in hold.items():
            globals()[k] = v
        return result

class Html(str):
    var = {}
    local = {}
    def __new__(cls, *args, **kwargs):
        t = str.__new__(cls, *args, **kwargs)
        obj = str.__new__(cls, t.__str__())
        return obj
    def header(self, doc, _, text, line):
        pass
    def body(self, doc, _, text, line):
        pass
    def __str__(self):
        hold = {}
        doc, _, text, line = Doc().ttl()
        with _('html'):
            with _('header'):
                if len(self.var) + len(self.local) > 0:
                    with _('script'):
                        for k, v in self.var.items():
                            doc.asis('var ' + k + ' = ' + json.dumps(v) + ';')
                        for k, v in self.local.items():
                            v.add(doc)
                self.header(doc, _, text, line)
            with _('body'):
                self.body(doc, _, text, line)
        result = doc.getvalue()
        for k, v in hold.items():
            globals()[k] = v
        return result
