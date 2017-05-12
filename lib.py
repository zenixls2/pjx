from metapensiero.pj.api import translates
from yattag import Doc, indent
import json
import inspect

doc, _, text, line = Doc().ttl()

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

class Html(str):
    var = {}
    local = {}
    def __new__(cls, *args, **kwargs):
        t = _Html.__new__(cls, *args, **kwargs)
        obj = str.__new__(cls, t.__str__())
        return obj
    def header(self):
        pass
    def body(self):
        pass
    def __str__(self):
        hold = {}
        for k, v in self.var.items():
            hold[k] = globals().get(k, None)
            globals()[k] = v
        for k, v in self.local.items():
            hold[k] = globals().get(k, None)
            globals()[k] = v
        with _('html'):
            with _('header'):
                with _('script'):
                    for k, v in self.var.items():
                        doc.asis('var ' + k + ' = ' + json.dumps(v) + ';')
                    for k, v in self.local.items():
                        v.add(doc)
                self.header()
            with _('body'):
                self.body()
        result = doc.getvalue()
        for k, v in hold.items():
            globals()[k] = v
        return result

class _Html(str):
    def header(self):
        pass
    def body(self):
        pass
    def __str__(self):
        hold = {}
        for k, v in self.var.items():
            hold[k] = globals().get(k, None)
            globals()[k] = v
        for k, v in self.local.items():
            hold[k] = globals().get(k, None)
            globals()[k] = v
        with _('html'):
            with _('header'):
                with _('script'):
                    for k, v in self.var.items():
                        doc.asis('var ' + k + ' = ' + json.dumps(v) + ';')
                    for k, v in self.local.items():
                        v.add(doc)
                self.header()
            with _('body'):
                self.body()
        result = doc.getvalue()
        for k, v in hold.items():
            globals()[k] = v
        return result
