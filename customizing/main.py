from utils import customize_images, word_template


# TODO opacity hierüber setzen
# TODO Tabnamen hierüber setzen
# TODO: Functions hierüber setzen

# * Functions vermutlich am besten über Endpunkt integrieren?

RUN_SCRIPTS = {"customize_images": False, "word_template": True}


def main():
    """Führt die aktivierten Skripte aus."""
    for script in RUN_SCRIPTS.keys():
        if RUN_SCRIPTS[script]:
            print(f"\nStarte {script}...\n")
            word_template.render()
            # for category in customize_images.IMAGE_CONFIG.keys():
            #     customize_images.process_image(category)

    print("Alle aktivierten Prozesse abgeschlossen.")


if __name__ == "__main__":
    main()
