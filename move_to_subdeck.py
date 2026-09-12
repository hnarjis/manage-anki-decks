"""
Move Anki cards matching specific word-entry IDs into a subdeck, using AnkiConnect.

Requirements:
- Anki must be open
- AnkiConnect add-on installed (code: 2055492159)

Usage:
    python move_to_subdeck.py

Edit the CONFIG section below before running.
"""

import json
import urllib.request

# ---------- CONFIG ----------
ANKI_CONNECT_URL = "http://localhost:8765"

# The parent deck that currently holds all your cards
SOURCE_DECK = "Teckenspråkslexikon"

# The subdeck you want to move matching cards into
# (AnkiConnect will create it automatically if it doesn't exist)
TARGET_SUBDECK = "Teckenspråkslexikon::2-Teckenlista"

# The name of the note field that holds the video URL
ANSWER_FIELD = "Video"

# The IDs extracted from the lexicon list
WORD_IDS = [
    "02711", "10169", "05569", "02336", "02777",
    "00389", "02433", "00041", "04378", "01803",
    "02269", "01676", "11145", "08853", "06045",
    "05572", "10603", "05598", "08252", "08253",
    "03507", "03672", "04346", "06933", "05660",
    "07288", "02585", "02025", "03983", "10547",
    "00523", "02606", "03018", "04127", "02488",
    "05086", "02842", "05183", "00631", "03589",
    "02839", "08766", "07766", "00774", "00496",
    "02173", "03108", "07265", "04457", "01061",
    "01654", "09121", "02302", "03954", "09131",
    "07357", "09955", "09968", "01302", "01729",
    "03319", "05138", "04008", "01018", "00469",
    "01145", "01720", "08602", "03375", "02354",
    "04123", "04152", "00894", "00676", "01432",
    "00887", "00666", "02963", "00521", "07128",
    "02238", "02204", "04348", "05061", "02989",
    "02521", "01984", "00147", "03399", "03573",
    "01416", "05369", "05382", "00998", "05388",
    "03455", "04101", "03454", "00593", "03212",
    "01867", "01985", "02584", "02522", "03320",
    "07943", "00561", "01585", "00588", "12284",
]
# -----------------------------


def invoke(action, **params):
    payload = {"action": action, "version": 6, "params": params}
    request = urllib.request.Request(
        ANKI_CONNECT_URL, json.dumps(payload).encode("utf-8")
    )
    response = json.load(urllib.request.urlopen(request))
    if response.get("error") is not None:
        raise Exception(response["error"])
    return response["result"]


def main():
    all_matched_card_ids = set()
    not_found = []

    for word_id in WORD_IDS:
        # Search within the source deck for a card whose Video field
        # contains a video URL ending in "-{word_id}-tecken.mp4"
        query = f'deck:"{SOURCE_DECK}" "{ANSWER_FIELD}:*-{word_id}-tecken.mp4"'
        card_ids = invoke("findCards", query=query)

        if not card_ids:
            not_found.append(word_id)
            continue

        all_matched_card_ids.update(card_ids)
        print(f"ID {word_id}: found {len(card_ids)} card(s)")

    if not all_matched_card_ids:
        print("No matching cards found at all. Check SOURCE_DECK name and field content.")
        return

    invoke("changeDeck", cards=list(all_matched_card_ids), deck=TARGET_SUBDECK)
    print(f"\nMoved {len(all_matched_card_ids)} card(s) to '{TARGET_SUBDECK}'.")

    if not_found:
        print(f"\nNo match found for these IDs (check manually): {', '.join(not_found)}")


if __name__ == "__main__":
    main()
