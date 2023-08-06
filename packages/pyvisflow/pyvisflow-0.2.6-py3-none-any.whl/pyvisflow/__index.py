from .app import App

app = App()

__all__ = [
    'box',
    'fns',
    'add_srcipt',
    'to_html',
    'dataTable',
    'input',
    'echart',
    'inputNumber',
    'markdown',
    'plotly',
    'select',
    'cols',
    'tabs',
    'to_html',
    'config2file',
    'text',
    'icon',
    'icon_fromfile',
    'row',
    'file',
    'app',
    'image_from_mpl',
    'image_from_file',
    'image_from_url',
    'button',
]

image_from_mpl= app.image_from_mpl
image_from_file = app.image_from_file
image_from_url = app.image_from_url

button = app.button

box = app.box
add_srcipt = app.add_srcipt
dataTable = app.dataTable
input = app.input
echart = app.echart
inputNumber = app.inputNumber
markdown = app.markdown
select = app.select
cols = app.cols
tabs = app.tabs
text = app.text
plotly = app.plotly
fns = app.Fns
icon_fromfile = app.icon_fromfile
icon = app.icon
row=app.row
file=app.file

# v = FnContext()

config2file = app.config2file
to_html = app.to_html
