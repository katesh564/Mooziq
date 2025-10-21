import json, os, re, csv
from typing import List, Tuple, Dict, Optional
months = ["January","February","March","April","May","June"]
months += ["July","August","September","October","November","December"]

def find_artist(chosen_art,artists_name_idnamegenre):    
        artist_found = False
        for key in artists_name_idnamegenre.keys():
            if key == chosen_art.lower():
                artist_found = True
                return artist_found
        return False

def print_tracks_popularity(list_track_popul):
    for track_popul in list_track_popul:
        
        track = track_popul[0]
        popularity = track_popul[1]
        
        if popularity <= 30:
            print(f"- \"{track}\" has a popularity score of {popularity}. No one knows this song.")
        elif popularity <= 50:
            print(f"- \"{track}\" has a popularity score of {popularity}. Popular song.")
        elif popularity <= 70:
            print(f"- \"{track}\" has a popularity score of {popularity}. It is quite popular now!")
        elif popularity > 70:
            print(f"- \"{track}\" has a popularity score of {popularity}. It is made for the charts!")


def safe_load_json(path: str) -> Optional[dict]:
    """Return parsed JSON or None if missing/invalid."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

def sanitize_text(text: str) -> str:
    if text is None:
        return ""
    txt = text.lower()
    txt = re.sub(r"[.,!?\"'()\/:;]", "", txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

def format_release_date(release_date: str, precision: str) -> str:
    if not release_date:
        return "Date Not Found"
    if precision == "day":
        year, month, day = release_date.split('-')
        month_name = months[int(month) - 1]
        day_int = int(day)
        if 11 <= day_int <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_int % 10, "th")
        return f"{month_name} {day_int}{suffix} {year}"
    if precision == "month":
        year, month = release_date.split('-')[:2]
        month_name = months[int(month) - 1]
        return f"{month_name} {year}"
    return release_date

def read_csv_rows(path: str) -> List[Dict[str, str]]:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, newline='', encoding="utf8") as csvfile:
        return list(csv.DictReader(csvfile))

def write_csv_rows(path: str, header: List[str], rows: List[dict]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline='', encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

def update_or_append_csv(path: str, header: List[str], row: dict, key_field: str) -> bool:
    rows = read_csv_rows(path)
    updated = False
    for r in rows:
        if r.get(key_field) == row.get(key_field):
            r.update(row)
            updated = True
            break
    if not updated:
        rows.append(row)
    write_csv_rows(path, header, rows)
    return updated

def get_top_two_tracks_for_artist(artist_id: str) -> Tuple[str, str]:
    path = os.path.join("dataset", "top_tracks", f"{artist_id}.json")
    data = safe_load_json(path)
    if not data:
        return "", ""
    tracks = data.get("tracks", [])
    tracks_sorted = sorted(tracks, key=lambda x: x.get("popularity", 0), reverse=True)
    t1 = tracks_sorted[0].get("name", "") if len(tracks_sorted) > 0 else ""
    t2 = tracks_sorted[1].get("name", "") if len(tracks_sorted) > 1 else ""
    return t1, t2

def get_song_entries() -> List[Tuple[str, str, str]]:
    out = []
    folder = os.path.join("dataset", "songs")
    for fname in sorted(os.listdir(folder)):
        full = os.path.join(folder, fname)
        data = safe_load_json(full)
        if not data:
            continue
        out.append((data.get("title", "Unknown Title"), data.get("artist", "Unknown Artist"), data.get("lyrics", "")))
    return out

def load_inverted_index(path: str) -> Dict[str, List[Tuple[str, str]]]:
    data = safe_load_json(path)
    if not data:
        return {}
    return {w: [tuple(item) for item in lst] for w, lst in data.items()}

def save_inverted_index(path: str, index: Dict[str, List[Tuple[str, str]]]) -> None:
    to_save = {w: [[t, a] for (t, a) in lst] for w, lst in index.items()}
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(to_save, f, ensure_ascii=False, indent=2)

def read_jsons(folder_path):
    list_json = sorted(os.listdir(folder_path))
    file_name_data = {}
    for file_name in list_json:
        with open(f"{folder_path}/{file_name}", 'r',encoding = "utf-8") as file:
            file_content = json.load(file)
            file_name_data[file_name] = file_content
    return file_name_data