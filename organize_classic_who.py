from pathlib import Path
import os, shutil, re, argparse, logging

COLLECTION   = Path("/media/madmaxlgndklr/classic_who1/Doctor Who - The Complete Classic 26 Seasons Collection + Extras")
SHOW_DEST    = Path("/media/madmaxlgndklr/classic_who1/Doctor Who (1963)")
MOVIE_DEST   = Path("/media/madmaxlgndklr/classic_who1/Movies")
SEASON1_FLAT = COLLECTION / "Doctor Who Season 1"
TV_MOVIE_DIR = COLLECTION / "Doctor Who - SXXEXX (156) - Television Movie"

SERIALS = []   # populated in subsequent tasks
SPECIALS = []  # Season 00 entries


def _ep_dest(season: int, ep: int, title: str, recon: bool) -> Path:
    suffix = " (Recon)" if recon else ""
    fname = f"Doctor Who (1963) - S{season:02d}E{ep:02d} - {title}{suffix}.avi"
    return SHOW_DEST / f"Season {season:02d}" / fname


def _extras_dest(season: int, filename: str) -> Path:
    return SHOW_DEST / f"Season {season:02d}" / "extras" / filename


def _find_serial_eps(folder: Path) -> list:
    files = sorted([
        f for f in folder.iterdir()
        if f.suffix == ".avi"
        and "Bonus" not in f.name
        and "Special Edition" not in f.name
        and not re.search(r"\(0\)", f.name)
    ])
    return files


def _find_extras(folder: Path) -> list:
    result = []
    for f in folder.iterdir():
        if f.suffix == ".pdf":
            result.append(f)
        elif f.suffix == ".avi" and (
            "Bonus" in f.name or re.search(r"\(0\)", f.name)
        ):
            result.append(f)
    return result


def _find_season1_flat(ep_num: int) -> Path | None:
    for f in SEASON1_FLAT.iterdir():
        if f.suffix != ".avi":
            continue
        for pat in [f"S01E{ep_num:02d}", f"S01E0{ep_num:02d}"]:
            if pat in f.name:
                return f
    return None


def build_plan(serials: list, specials: list) -> list:
    moves = []

    for entry in specials:
        moves.extend(_plan_special(entry))

    for entry in serials:
        moves.extend(_plan_serial(entry))

    return moves


def _plan_special(entry: dict) -> list:
    moves = []
    if entry["episode_source"] == "loose":
        src = COLLECTION / entry["folder"]
        s, e, title, recon = entry["episodes"][0]
        moves.append((src, _ep_dest(s, e, title, recon)))
    elif entry["episode_source"] == "serial":
        folder = COLLECTION / entry["folder"]
        eps = _find_serial_eps(folder)
        for i, (s, e, title, recon) in enumerate(entry["episodes"]):
            if i < len(eps):
                moves.append((eps[i], _ep_dest(s, e, title, recon)))
            else:
                logging.warning(f"WARN missing part {i+1} for {entry['title']}")
    return moves


def _plan_serial(entry: dict) -> list:
    moves = []
    folder = COLLECTION / entry["folder"] if entry["folder"] else None
    season = entry["episodes"][0][0] if entry["episodes"] else 0

    if entry["episode_source"] == "serial" and folder:
        eps = _find_serial_eps(folder)
        for i, (s, e, title, recon) in enumerate(entry["episodes"]):
            if i < len(eps):
                moves.append((eps[i], _ep_dest(s, e, title, recon)))
            else:
                logging.warning(f"WARN missing part {i+1} for {entry['title']}")
        for f in eps[len(entry["episodes"]):]:
            moves.append((f, _extras_dest(season, f.name)))
        for f in _find_extras(folder):
            moves.append((f, _extras_dest(season, f.name)))

    elif entry["episode_source"] == "season1_flat":
        for (s, e, title, recon) in entry["episodes"]:
            src = _find_season1_flat(e)
            if src:
                moves.append((src, _ep_dest(s, e, title, recon)))
            else:
                logging.warning(f"WARN S01E{e:02d} not found in flat folder")
        if folder and folder.exists():
            for f in _find_extras(folder):
                moves.append((f, _extras_dest(season, f.name)))
            for f in _find_serial_eps(folder):
                moves.append((f, _extras_dest(season, f.name)))

    elif entry["episode_source"] == "tv_movie":
        avs = [f for f in TV_MOVIE_DIR.iterdir() if f.suffix == ".avi"]
        if avs:
            _, _, title, _ = entry["episodes"][0]
            dest = MOVIE_DEST / title / f"{title}.avi"
            moves.append((avs[0], dest))

    for se in entry.get("se_entries", []):
        se_folder = COLLECTION / se["folder"]
        if not se_folder.exists():
            logging.warning(f"WARN SE folder not found: {se['folder']}")
            continue
        eps = _find_serial_eps(se_folder)
        for i, (s, e, title, recon) in enumerate(se["episodes"]):
            if i < len(eps):
                moves.append((eps[i], _ep_dest(s, e, title, recon)))
        if se.get("include_extras"):
            for f in _find_extras(se_folder):
                moves.append((f, _extras_dest(se["episodes"][0][0], f.name)))

    return moves


def execute_plan(moves: list, dry_run: bool = True) -> tuple:
    moved = skipped = errors = 0
    for src, dest in moves:
        if not src.exists():
            logging.warning(f"WARN  source missing: {src}")
            errors += 1
            continue
        if dest.exists():
            logging.info(f"SKIP  {dest.name}")
            skipped += 1
            continue
        if dry_run:
            logging.info(f"DRY   {src.name}\n   -> {dest}")
            moved += 1
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.rename(src, dest)
            except OSError:
                shutil.move(str(src), str(dest))
            logging.info(f"MOVE  {src.name}\n   -> {dest}")
            moved += 1
    return moved, skipped, errors


def main():
    parser = argparse.ArgumentParser(description="Reorganize Classic Doctor Who for Plex")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("organize_classic_who.log"),
        ],
    )

    moves = build_plan(SERIALS, SPECIALS)
    logging.info(f"\nPlan: {len(moves)} file operations")
    moved, skipped, errors = execute_plan(moves, dry_run=not args.execute)
    logging.info(f"\nSummary: moved={moved}  skipped={skipped}  errors={errors}")


if __name__ == "__main__":
    main()
