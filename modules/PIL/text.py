from PIL import Image, ImageDraw, ImageFont

img = Image.open("example.jpg")  # Open an image
draw = ImageDraw.Draw(img)
text = "Hello, World!"        # draw.text((100,100),"helllo world",font=font)
position = (100, 100)

try:
    font = ImageFont.truetype("arial.ttf", 36)  #optional but need
except IOError:
    font = ImageFont.load_default()

draw.text(position, text, fill="white",font=font)   ## Add text to the image

img.save("image_with_text.jpg")
img.show()


# https://www.google.com/search?sca_esv=a69cbbbda68ed245&q=lord+shiva+images&udm=2&fbs=AIIjpHxU7SXXniUZfeShr2fp4giZ1Y6MJ25_tmWITc7uy4KIemkjk18Cn72Gp24fGkjjh6xc8y8oU3IJovU34XDyOFvEl9PQhCX-bXyx8AzQGU_JUmd7tO0Sp0t0qHqXwx4ZXWZ46FMJ_5qOlBWL317zdnko09c3cS91eOWyqKC8pqNi-T4DhtjV8zWXL8UGIxO7yEoZ63L3KD6mXO4QEFSbHyfGyMpJqQ&sa=X&ved=2ahUKEwj2r8us7p6OAxWyh1YBHUlGMWMQtKgLKAF6BAgQEAE&biw=1280&bih=585&dpr=1.5#vhid=QQt-Q1GTuKDXeM&vssid=mosaic

# Long text   import textwraps
#text = "This is a long piece of text that will automatically wrap across multiple lines."

# Wrap text to fit a certain width
#wrapped_text = textwrap.fill(text, width=40)

# Get text size
# text = "Centered Text"
# text_width, text_height = draw.textsize(text, font=font)

# # Calculate center position
# x = (img.width - text_width) // 2
# y = (img.height - text_height) // 2

# draw.text((x, y), text, font=font, fill="yellow")
# img.save("centered_text.jpg")
