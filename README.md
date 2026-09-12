# Move Anki Cards to a Subdeck (via AnkiConnect)

This script finds cards in an Anki collection whose `Video` field contains a
video URL ending in `-tecken.mp4` for a specific list of word IDs, and moves
those cards into a target subdeck.

## Requirements

- Anki (desktop app) installed and open
- The AnkiConnect add-on installed
- Python 3 installed

## 1. Install AnkiConnect

1. Open Anki.
2. Go to **Tools > Add-ons > Get Add-ons**.
3. Paste in the code: `2055492159`
4. Restart Anki.
5. Keep Anki open while running the script (AnkiConnect runs a local server
   at `http://localhost:8765` that only works while Anki is running).

## 2. Set up the script

Open it in any text editor and check these config values near the top:

- `SOURCE_DECK`: the deck (or deck tree) your cards currently live in.
  Anki's search automatically includes all subdecks of this deck, so you
  don't need to list them individually.
- `TARGET_SUBDECK`: the subdeck you want matching cards moved into. It
  will be created automatically if it doesn't already exist.
- `ANSWER_FIELD`: the exact name of the note field containing the video
  URL (case-sensitive, check your note type in Anki if unsure).
- `WORD_IDS`: the list of word IDs to match and move.

## 3. Run it

Run:

```bash
python move_to_subdeck.py
```

(use `python3` instead of `python` if the first one isn't recognized)

## 4. Check the output

The script prints, for each ID, how many card(s) matched. At the end it
reports the total number of cards moved, plus a list of any IDs it couldn't
find a match for (worth checking those by hand).

## Troubleshooting

- **`ConnectionRefusedError`**: Anki isn't open, or AnkiConnect isn't
  installed. Open Anki and confirm the add-on is active.
- **An ID matches 0 cards**: double check `ANSWER_FIELD` is spelled exactly
  as in your note type, and that the field really contains a URL ending in
  `-{id}-tecken.mp4`. You can test a single search manually in Anki's Browse
  window, e.g. `Answer:*08454*` (no deck filter), to confirm the field name
  and content format.
- **An ID matches more than one card**: this can happen if multiple notes
  reference the same word ID for different reasons; review those manually
  before trusting a bulk move.
