# Создайте файл create_icon.py и запустите его для генерации иконки
from PIL import Image, ImageDraw, ImageFont

# Создаем изображение
img = Image.new('RGB', (256, 256), color='#0071e3')
draw = ImageDraw.Draw(img)

# Рисуем замок (простой символ криптографии)
draw.rectangle([78, 128, 178, 208], fill='white', outline=None)
draw.rectangle([108, 98, 148, 128], fill='white', outline=None)
draw.ellipse([118, 78, 138, 98], fill='white')

# Добавляем текст
try:
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((88, 168), "CL", fill='#0071e3', font=font)
except:
    draw.text((88, 168), "CL", fill='#0071e3')

# Сохраняем как ICO
img.save('icon.ico', format='ICO', sizes=[(256, 256)])

print("Иконка создана: icon.ico")