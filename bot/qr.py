import qrcode
import datetime
import os


class QR:
    def __init__(self):
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
        img_path = "../tmpqr/{}_{}.jpg".format(datetime.datetime.now().strftime('%H%M%S'), text_data[:10])
        img.save(img_path)
        self.qr.clear()
        return img_path, img

    def deleteqr(self, img_path: str):
        os.remove(img_path)
        return 1
