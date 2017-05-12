from yattag import indent
from lib import Html, Container, jsfy, domfy

class MyHtml(Html):
    pass

@domfy(MyHtml)
def ohoh(doc, tag, text, line):
    with tag('div'):
        text("ohoh")

class MyContainer(Container):
    def render(self, doc, _, text, line):
        with _('div'):
            text('ohoh')

@jsfy(MyHtml)
def click_handler(event):
    document.getElementById('xdd').innerHTML = ohoh

class MyHtml(Html):
    def body(self, doc, _, text, line):
        line('h3', 'Hello World!')
        with _('form', action=""):
            doc.input(name='name', type='text', onkeypress=click_handler)
            doc.stag('br')
            with _('div', id='xdd'):
                text('xddd')
            doc.asis(ohoh)
            doc.asis(MyContainer())
            doc.textarea(name='msg')
            doc.stag('input', type='submit', value='Leave comments...')


if __name__ == '__main__':
    print(indent(MyHtml()))
