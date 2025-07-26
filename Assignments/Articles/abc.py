import os

folder = "/photos"
for count, filename in enumerate(os.listdir(folder)):
    new_name = f"Vacation_{count+1:03}.jpg"
    os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
