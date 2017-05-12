from yattag import Doc, indent
from lib import Html, jsfy, domfy, doc, _, text, line

class MyHtml(Html):
    pass

@domfy(MyHtml)
def ohoh(doc, tag, text, line):
    with tag('div'):
        text("ohoh")

@jsfy(MyHtml)
def click_handler(event):
    document.getElementById('xdd').innerHTML = ohoh

class MyHtml(Html):
    def __str__(self):
        return super().__str__()
    def body(self):
        line('h3', 'Hello World!')
        with _('form', action=""):
            doc.input(name='name', type='text', onkeypress=click_handler)
            doc.stag('br')
            with _('div', id='xdd'):
                text('xddd')
            doc.asis(ohoh)
            doc.textarea(name='msg')
            doc.stag('input', type='submit', value='Leave comments...')


if __name__ == '__main__':
    print(indent(MyHtml()))
