from PIL import Image, ImageDraw

# Open image or create a blank one
img = Image.new("RGB", (300, 300), color="black")
draw = ImageDraw.Draw(img)

# Draw a rectangle (x0, y0, x1, y1)
draw.rectangle([50, 50, 250, 250], outline="red", width=5)

# Draw a filled ellipse
draw.ellipse([100, 100, 200, 200], fill="blue")

# Draw a line
draw.line([0, 0, 300, 300], fill="green", width=3)

# Save or show
img.save("image_with_shapes.jpg")
img.show()




