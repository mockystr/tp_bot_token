import qrcode
import datetime
import os
import time
from settings import save_path
from jinja2 import Template, Environment, PackageLoader, select_autoescape, FileSystemLoader
import imgkit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(searchpath="./src"),
    # autoescape=select_autoescape(['html', 'xml'])
)


def createqr(text_data: str):
    img = qrcode.make(text_data)
    qr_tmp_path = "{}/tmp{}_{}.jpg".format(save_path,
                                           datetime.datetime.now().strftime('%H%M%S'),
                                           text_data[:10])
    img.save(qr_tmp_path)

    template = env.get_template("index.html")
    print(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         qr_tmp_path)).replace(os.sep, '/')
    print('PATH', path)
    r = template.render(qr_code=path)
    print(r)
    qr_final_path = '{}/{}_{}.png'.format(save_path,
                                          datetime.datetime.now().strftime('%H%M%S'),
                                          text_data[:10])
    config = imgkit.config(wkhtmltoimage='C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe')
    imgkit.from_string(r, qr_final_path, config=config, options={'width': 420, 'height': 600})
    # os.remove(qr_tmp_path)
    return qr_final_path, img


if __name__ == '__main__':
    start = time.time()
    url, _ = createqr('asdasd')
    # os.remove(url)
    print(time.time() - start)
