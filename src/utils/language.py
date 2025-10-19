
def windows_gettext(locale_win) -> list[str]:
    lang = { 
        "fr_FR": ['fr_FR.UTF-8', 'French_France', 'fr_FR']
    }
    
    if lang.get(locale_win[0]):
        return lang["fr_FR"]
    else:
        return None