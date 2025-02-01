# settings.py

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Edusystem Admin panel",
    "SITE_HEADER": "Edusystem Admin panel",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        # "image": lambda request: static("sample/login-bg.jpg"),
    },
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "en": "🇬🇧",
                "ru": "🇷🇺",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Admin"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:accounts_users_changelist"),
                    },
                    {
                        "title": _("Sertifikatlar"),
                        "link": reverse_lazy("admin:certificate_certificate_changelist"),
                    },
                    {
                        "title": _("Sertifikat turlari"),
                        "link": reverse_lazy("admin:education_certificatetype_changelist"),
                    },
                    {
                        "title": _("Kurslar"),
                        "link": reverse_lazy("admin:courses_courses_changelist"),
                    },
                    {
                        "title": _("O'quv markazlar"),
                        "link": reverse_lazy("admin:education_educenter_changelist"),
                    },
                    {
                        "title": _("To'lovlar"),
                        "link": reverse_lazy("admin:payments_payments_changelist"),
                    },
                    {
                        "title": _("Xonalar"),
                        "link": reverse_lazy("admin:rooms_rooms_changelist"),
                    },
                    {
                        "title": _("O'quvchilar"),
                        "link": reverse_lazy("admin:students_students_changelist"),
                    },
                    {
                        "title": _("Sozlamalar"),
                        "link": reverse_lazy("admin:settings_settings_changelist"),
                    },
                    {
                        "title": _("O'qituvchilar"),
                        "link": reverse_lazy("admin:teachers_teachers_changelist"),
                    },
                ],
            },
        ],
    },
}
