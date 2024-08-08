import os
from PIL import Image

def txt_to_image(txt_file, image_file):
    # Lecture du fichier TXT
    with open(txt_file, 'r') as f:
        lines = f.readlines()

    # Récupération des données
    size = int(lines[0].strip())
    frames = []
    for line in lines[1:]:
        if line.strip():
            row = line.strip().split()
            frames.append(row)
        else:
            if frames:
                frames.append(frames)
                frames = []

    # Création de l'image
    width = len(frames[0][0]) * size
    height = len(frames[0]) * size
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    # Remplissage de l'image
    for y, row in enumerate(frames[0]):
        for x, color in enumerate(row):
            r, g, b = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            for i in range(size):
                for j in range(size):
                    pixels[x * size + i, y * size + j] = (r, g, b)

    # Sauvegarde de l'image
    img.save(image_file)

# Exemple d'utilisation
txt_file = 'example.txt'
image_file = 'example.png'
txt_to_image(txt_file, image_file)