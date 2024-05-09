import panel as pn
import param

def viewer():
    pn.extension('texteditor')
    wysiwyg = pn.widgets.TextEditor(placeholder='Enter some text')
    return wysiwyg