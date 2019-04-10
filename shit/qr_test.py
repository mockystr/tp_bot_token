import qrcode
import datetime
import time
from multiprocessing import Pool, Process, current_process
from jinja2 import Template
from jinja2 import Template, Environment, PackageLoader, select_autoescape
import os

# index_html = open('static/index.html')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
env = Environment(
    loader=PackageLoader('tp_token_bot', 'static'),
    autoescape=select_autoescape(['html', 'xml'])
)


def create(text):
    print('cur process name: {}; text {}'.format(current_process().name, text))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=2,
    )
    qr.add_data(str(text))
    qr.make(fit=True)
    qr_path = '../tmpqr/{}tmpqr.jpg'.format(datetime.datetime.now())
    img = qr.make_image(fill_color="black", back_color="white")
    img.new_image()
    img.save(qr_path)
    template = env.get_template('index.html')
    template.render(qr_code=qr_path)
    template.generate()
    print(template.__dict__)


if __name__ == '__main__':
    create('asdasd')
    # start = time.time()
    # p = Pool()
    # processes = []
    #
    # for i in range(5):
    #     p = Process(target=create, args=(str(i)))
    #     processes.append(p)
    #     p.start()
    #
    # [i.join() for i in processes]
    # #
    # # finish for 0.10032010078430176s
    #
    # # for num in range(500):
    # #     Process(target=create, args=(str(num),)).start()
    #
    # # range 5 finish for 0.019150733947753906s
    #
    # # with Pool(500) as p:
    # #     p.map(create, ['aasd', 'asd', 'zxcawoudha oiwhdoaiw daw', '1', 'asdasd'])
    #
    # # range 5 finish for 0.22086381912231445s
    # # range 500 finish for 2.0069198608398438s
    #
    # # [create(i) for i in range(500)]
    # # range 5 finish for 0.08029317855834961s
    # # range 500 finish for 6.8953211307525635s
    #
    # print('finish for {}s'.format(time.time() - start))
