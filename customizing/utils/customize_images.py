import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from config import IMAGE_CONFIG  # Importiere die Konfiguration


def select_image():
    """Öffnet einen Dialog zum Auswählen eines Bildes."""
    tk.Tk().withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    return file_path if file_path else None


def resize_image(image_path, sizes):
    """Skaliert ein Bild auf verschiedene Größen oder behält die Originalgröße, wenn size=None."""
    img = Image.open(image_path)
    return {name: img.resize(size, Image.LANCZOS) if size else img.copy() for name, size in sizes.items()}


def save_images(images, save_locations):
    """Speichert die generierten Bilder und überschreibt sie, falls sie bereits existieren."""
    for filename, image in images.items():
        paths = save_locations[filename]

        # Falls nur ein einzelner Speicherpfad angegeben ist, mache es zu einer Liste
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            save_path = os.path.join(path, filename)
            image.save(save_path, format="PNG")
            print(f"✅ Gespeichert (überschrieben falls vorhanden): {save_path}")


def process_image(category):
    """Fragt den Nutzer nach einem Bild für die gewählte Kategorie und speichert es."""
    print(f"Wähle eine Bilddatei für '{category}' aus.")
    image_path = select_image()

    if not image_path:
        print(f"Kein Bild für '{category}' ausgewählt. Überspringe...")
        return

    print(f"Verarbeite {category}...")
    resized_images = resize_image(image_path, IMAGE_CONFIG[category]["sizes"])
    save_images(resized_images, IMAGE_CONFIG[category]["save_paths"])
    print(f"{category.capitalize()}-Bilder erfolgreich gespeichert.\n")
