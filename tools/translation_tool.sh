#!/usr/bin/env bash
## Original script https://github.com/Jeffser/Alpaca/
set -euo pipefail
cd "$(dirname "$0")/.."

# Always regenerate the template first
xgettext --output=po/inspira.pot --files-from=po/POTFILES --from-code=UTF-8 --add-comments --keyword=_ --keyword=C_:1c,2

echo -e "\n--- Inspira Translation Alpaca ---\n"
echo "Available languages:"
ls po/*.po 2>/dev/null | sed -E 's|po/([^.]+)\.po|\1|' | tr '\n' ' '
echo

read -rp "Enter your language code (e.g., es, ru, pt_BR): " lang
po_file="po/${lang}.po"

if [[ -f "$po_file" ]]; then
    echo -e "\nUpdating $lang..."
    msgmerge --no-fuzzy-matching --update --backup=none "$po_file" po/inspira.pot
    echo "✅ $lang updated successfully."
else
    echo -e "\n❌ No translation found for '$lang'."
    read -rp "Would you like to create a new translation for '$lang'? (y/n): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
    	echo ""
        msginit --locale="$lang" --input=po/inspira.pot --output-file="$po_file"
        echo -e "\n✅ New translation created at $po_file."
    else
        echo -e "\n❌ Operation cancelled."
        exit 1
    fi
fi
