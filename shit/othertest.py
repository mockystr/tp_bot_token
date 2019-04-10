import pdfcrowd
import sys
from jinja2 import Template, Environment, PackageLoader, select_autoescape, FileSystemLoader

import time
import imgkit
from jinja2 import Template, Environment, PackageLoader, select_autoescape, FileSystemLoader
from settings import save_path
import datetime

start = time.time()
template_loader = FileSystemLoader(searchpath="./src")
env = Environment(
    loader=template_loader,
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template("try.html")
r = template.render()

qr_final_path = '{}/{}_{}.png'.format(save_path,
                                      datetime.datetime.now().strftime('%H%M%S'),
                                      '221233')

try:
    client = pdfcrowd.HtmlToImageClient('mockingbird321', '91c13b0721f0100ad8266d912e825a4c')
    client.setOutputFormat('png')
    client.convertStringToFile(r, qr_final_path)
except pdfcrowd.Error as why:
    sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
    raise
print('finish {}s'.format(time.time() - start))
