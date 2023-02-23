import qrcode
from PIL import Image

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data("http://127.0.0.1:5502/PROJECT/menu.html")
qr.make(fit=True)
img= qr.make_image(fill_color="black",back_color="white")
img.save("Menu.png")