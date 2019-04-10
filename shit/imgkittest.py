# import time
# import imgkit
# from jinja2 import Template, Environment, PackageLoader, select_autoescape, FileSystemLoader
# from settings import save_path
# import datetime
#
# start = time.time()
# template_loader = FileSystemLoader(searchpath="./src")
# env = Environment(
#     loader=template_loader,
#     autoescape=select_autoescape(['html', 'xml'])
# )
#
# template = env.get_template("try.html")
# r = template.render()
#
# qr_final_path = '{}/{}_{}.png'.format(save_path,
#                                       datetime.datetime.now().strftime('%H%M%S'),
#                                       '221233')
# config = imgkit.config(wkhtmltoimage='/usr/local/bin/wkhtmltoimage')
# imgkit.from_string(r, qr_final_path, config=config)
# print('finish {}s'.format(time.time() - start))
# finish 1.3671209812164307s