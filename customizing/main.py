from utils import customize_images

# TODO opacity hierüber setzen
# TODO Tabnamen hierüber setzen
# TODO: Functions hierüber setzen

RUN_SCRIPTS = {"customize_images": True}


def main():
    """Führt die aktivierten Skripte aus."""
    for script in RUN_SCRIPTS.keys():
        if RUN_SCRIPTS[script]:
            print(f"\nStarte {script}...\n")
            for category in customize_images.IMAGE_CONFIG.keys():
                customize_images.process_image(category)

    print("Alle aktivierten Prozesse abgeschlossen.")


if __name__ == "__main__":
    main()
