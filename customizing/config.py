IMAGE_CONFIG = {
    "favicon": {
        "sizes": {
            "favicon-96x96.png": (96, 96),
            "apple-touch-icon.png": (180, 180),
            "web-app-manifest-192x192.png": (192, 192),
            "web-app-manifest-512x512.png": (512, 512),
            "favicon.png": None,
        },
        "save_paths": {
            "favicon-96x96.png": r"static\favicon",
            "apple-touch-icon.png": r".\static\favicon",
            "web-app-manifest-192x192.png": r".\static\favicon",
            "web-app-manifest-512x512.png": r".\static\favicon",
            "favicon.png": [
                r".\static\favicon",
                r".\static\static",
                r".\backend\open_webui\static",
            ],
        },
    },
    "background": {
        "sizes": {
            "custom-background.png": None,
        },
        "save_paths": {"custom-background.png": r".\static\static"},
    },
    "splash": {
        "sizes": {
            "splash.png": None,
        },
        "save_paths": {"splash.png": [r".\backend\open_webui\static", r".\static\static"]},
    },
    "splash-dark": {
        "sizes": {
            "splash-dark.png": None,
        },
        "save_paths": {"splash-dark.png": [r".\static\static"]},
    },
}
