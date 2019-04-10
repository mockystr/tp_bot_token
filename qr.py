import qrcode
import datetime
import os
import time
from settings import save_path
from jinja2 import Template, Environment, PackageLoader, select_autoescape, FileSystemLoader
import imgkit


class QR:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        template_loader = FileSystemLoader(searchpath="./src")
        self.env = Environment(
            loader=template_loader,
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=50,
            border=2,
        )

    def createqr(self, text_data: str = 'default'):
        self.qr.add_data(text_data)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")
        img.new_image()
        qr_tmp_path = "{}/tmp{}_{}.jpg".format(save_path,
                                               datetime.datetime.now().strftime('%H%M%S'),
                                               text_data[:10])
        img.save(qr_tmp_path)
        template = self.env.get_template("index.html")
        print(qr_tmp_path)
        r = template.render(qr_code=qr_tmp_path)
        qr_final_path = '{}/{}_{}.png'.format(save_path,
                                              datetime.datetime.now().strftime('%H%M%S'),
                                              text_data[:10])
        config = imgkit.config(wkhtmltoimage='/usr/local/bin/wkhtmltoimage')
        imgkit.from_string(r, qr_final_path, config=config, options={'width': 420, 'height': 600})
        os.remove(qr_tmp_path)
        return qr_final_path, img


if __name__ == '__main__':
    start = time.time()
    qr = QR()
    qr.createqr('asdasd')
    print(time.time() - start)
