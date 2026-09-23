from PIL import Image
img = Image.open("frontend/static/iconeContatos.png")
img = img.resize((128, 128), Image.LANCZOS)
img.save("frontend/static/iconeContatos.png")