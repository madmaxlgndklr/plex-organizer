from pathlib import Path
import os, shutil, argparse, logging

SOURCE = Path("/media/madmaxlgndklr/media31/Shows/Guyver The Bioboosted Armor")
DEST   = Path("/media/madmaxlgndklr/media31/Shows/Guyver The Bioboosted Armor")

MANIFEST = [
    # ── Season 1 (26 episodes) ────────────────────────────────────────────
    ("Guyver ep01 'The Amazing Bioboosted Armor'.mp4",    DEST, 1, [1],  "The Amazing Bioboosted Armor"),
    ("Guyver ep02 'Secret Organization Cronos'.mp4",      DEST, 1, [2],  "Secret Organization Cronos"),
    ("Guyver ep03 'Inspector Lisker'.mp4",                DEST, 1, [3],  "Inspector Lisker"),
    ("Guyver ep04 'Visitor of the Dusk'.mp4",             DEST, 1, [4],  "Visitor of the Dusk"),
    ("Guyver ep05 'The Third Shadow'.mp4",                DEST, 1, [5],  "The Third Shadow"),
    ("Guyver ep06 'The End of a Deadly Battle'.mp4",      DEST, 1, [6],  "The End of a Deadly Battle"),
    ("Guyver ep07 'Miracle of Supreme Cell'.mp4",         DEST, 1, [7],  "Miracle of Supreme Cell"),
    ("Guyver ep08 'The Shaking Skyscraper'.mp4",          DEST, 1, [8],  "The Shaking Skyscraper"),
    ("Guyver ep09 'Ashes and Chasing Memories'.mp4",      DEST, 1, [9],  "Ashes and Chasing Memories"),
    ("Guyver ep10 'Prelude of the Chase'.mp4",            DEST, 1, [10], "Prelude of the Chase"),
    ("Guyver ep11 'Relic's Point'.mp4",                   DEST, 1, [11], "Relic's Point"),
    ("Guyver ep12 'Respective Decisions'.mp4",            DEST, 1, [12], "Respective Decisions"),
    ("Guyver ep13 'The Tragic Enzyme II'.mp4",            DEST, 1, [13], "The Tragic Enzyme II"),
    ("Guyver ep14 'Escape in the Rain'.mp4",              DEST, 1, [14], "Escape in the Rain"),
    ("Guyver ep15 'Guyot Strikes'.mp4",                   DEST, 1, [15], "Guyot Strikes"),
    ("Guyver ep16 'The Awakened Guyver I'.mp4",           DEST, 1, [16], "The Awakened Guyver I"),
    ("Guyver ep17 'The Nightmare Encircling Net'.mp4",    DEST, 1, [17], "The Nightmare Encircling Net"),
    ("Guyver ep18 'Vibration'.mp4",                       DEST, 1, [18], "Vibration"),
    ("Guyver ep19 'The Night Before the Strike'.mp4",     DEST, 1, [19], "The Night Before the Strike"),
    ("Guyver ep20 'The Advents' Ship'.mp4",               DEST, 1, [20], "The Advents' Ship"),
    ("Guyver ep21 'Chaos at Relic's Point'.mp4",          DEST, 1, [21], "Chaos at Relic's Point"),
    ("Guyver ep22 'Countdown of Destruction'.mp4",        DEST, 1, [22], "Countdown of Destruction"),
    ("Guyver ep23 'Beam of Annihilation'.mp4",            DEST, 1, [23], "Beam of Annihilation"),
    ("Guyver ep24 'At the Town Under Oppression'.mp4",    DEST, 1, [24], "At the Town Under Oppression"),
    ("Guyver ep25 'The Quickening Chrysalis'.mp4",        DEST, 1, [25], "The Quickening Chrysalis"),
    ("Guyver ep26 'Advent! Gigantic Bio-Boost'.mp4",      DEST, 1, [26], "Advent! Gigantic Bio-Boost"),
]


def _show_name(dest_root: Path) -> str:
    return dest_root.name


def _ep_tag(episodes: list) -> str:
    return "".join(f"E{e:02d}" for e in episodes)


def _dest_path(dest_root: Path, season: int, episodes: list, title: str, ext: str = ".mp4") -> Path:
    show = _show_name(dest_root)
    fname = f"{show} - S{season:02d}{_ep_tag(episodes)} - {title}{ext}"
    return dest_root / f"Season {season:02d}" / fname


def build_plan() -> list:
    moves = []
    for src_name, dest_root, season, episodes, title in MANIFEST:
        src = SOURCE / src_name
        dest = _dest_path(dest_root, season, episodes, title, Path(src_name).suffix)
        moves.append((src, dest))
    return moves


def execute_plan(moves: list, dry_run: bool = True) -> tuple:
    moved = skipped = errors = 0
    for src, dest in moves:
        if not src.exists():
            logging.warning(f"WARN  source missing: {src.name}")
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
    parser = argparse.ArgumentParser(description="Reorganize Guyver files for Plex")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("organize_guyver.log"),
        ],
    )

    moves = build_plan()
    logging.info(f"\nPlan: {len(moves)} file operations")
    moved, skipped, errors = execute_plan(moves, dry_run=not args.execute)
    logging.info(f"\nSummary: moved={moved}  skipped={skipped}  errors={errors}")


if __name__ == "__main__":
    main()
