
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (1280, 720), color=(10, 10, 10))
draw = ImageDraw.Draw(img)

# Try to draw text
try:
    font = ImageFont.truetype("arial.ttf", 100)
    draw.text((400, 300), "IDLE_STATE", fill=(100, 100, 100), font=font)
except Exception:
    draw.text((400, 300), "IDLE_STATE", fill=(100, 100, 100))

img.save('assets/memes/idle.png')
print("Created assets/memes/idle.png")
