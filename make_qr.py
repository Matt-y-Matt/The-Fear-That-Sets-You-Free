"""Make print-ready QR codes for the live page.
Usage: python make_qr.py https://your-live-address.vercel.app
Needs: pip install "qrcode[pil]"
"""
import sys, qrcode, qrcode.image.svg

url = sys.argv[1]
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=4)
qr.add_data(url); qr.make(fit=True)
qr.make_image(fill_color="#1B2532", back_color="white").save("qr-fear-that-sets-you-free.png")
qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage,
            error_correction=qrcode.constants.ERROR_CORRECT_H, border=4).save("qr-fear-that-sets-you-free.svg")
print("Saved qr-fear-that-sets-you-free.png and .svg for", url)
