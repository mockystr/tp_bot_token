import qrcode
import datetime
import os
import time
from settings import save_path
import logging

class QR:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=50,
            border=2,
        )

    def createqr(self, text_data: str = 'default'):
        utext = str(text_data.encode('utf-8'))
        print(utext)
        self.qr.add_data(utext)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")
        img.new_image()
        img_path = "{}/{}_{}.jpg".format(save_path,
                                         datetime.datetime.now().strftime('%H%M%S'),
                                         utext[:10])
        img.save(img_path)
        return img_path, img

    def deleteqr(self, imgp: str):
        self.qr.clear()
        os.remove(imgp)
        return 1


if __name__ == '__main__':
    qr = QR()
    # img_path = '../tmpqr/220040_fuck.jpg'
    img_path, _ = qr.createqr('asd')
    # qr.deleteqr(img_path)
    logging.warning(img_path)
