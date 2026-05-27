from pathlib import Path
import os, shutil, argparse, logging

SOURCE = Path("/media/madmaxlgndklr/media32/Shows/Little Einsteins")
DEST   = Path("/media/madmaxlgndklr/media32/Shows/Little Einsteins (2005)")

# Each row: (source_path_relative_to_SOURCE, season, [episode_numbers], display_title, extension)
MANIFEST = [
    # ── Season 1 — Italian-dubbed episodes ───────────────────────────────────
    (
        "Little Einsteins s01e37-40/Little Einsteins - 1x37 - Lui parla con la musica.avi",
        1, [37], "Lui parla con la musica", ".avi",
    ),
    (
        "Little Einsteins s01e37-40/Little Einsteins - 1x38 - Ciao violoncello.avi",
        1, [38], "Ciao violoncello", ".avi",
    ),
    (
        "Little Einsteins s01e37-40/Little Einsteins - 1x40 - Carmine al Gran Premio..avi",
        1, [40], "Carmine al Gran Premio", ".avi",
    ),

    # ── Season 00 — Go to America DVD specials ────────────────────────────────
    (
        "DISNEYS-LITTLE EINSTEINS[GO TO AMERICA-2009] AAC MP4-MULTI AUDIO BY WINKER@KIDZCORNER/a tall totem tale.mp4",
        0, [1], "A Tall Totem Tale", ".mp4",
    ),
    (
        "DISNEYS-LITTLE EINSTEINS[GO TO AMERICA-2009] AAC MP4-MULTI AUDIO BY WINKER@KIDZCORNER/knock on wood.mp4",
        0, [2], "Knock on Wood", ".mp4",
    ),
    (
        "DISNEYS-LITTLE EINSTEINS[GO TO AMERICA-2009] AAC MP4-MULTI AUDIO BY WINKER@KIDZCORNER/melody and me.mp4",
        0, [3], "Melody and Me", ".mp4",
    ),
    (
        "DISNEYS-LITTLE EINSTEINS[GO TO AMERICA-2009] AAC MP4-MULTI AUDIO BY WINKER@KIDZCORNER/bonus episode-handy manny.mp4",
        0, [4], "Bonus Episode - Handy Manny", ".mp4",
    ),
]


def _ep_tag(episodes: list) -> str:
    return "".join(f"E{e:02d}" for e in episodes)


def _dest_path(season: int, episodes: list, title: str, ext: str) -> Path:
    show = DEST.name
    season_folder = "Season 00" if season == 0 else f"Season {season:02d}"
    fname = f"{show} - S{season:02d}{_ep_tag(episodes)} - {title}{ext}"
    return DEST / season_folder / fname


def build_plan() -> list:
    moves = []
    for src_rel, season, episodes, title, ext in MANIFEST:
        src = SOURCE / src_rel
        dest = _dest_path(season, episodes, title, ext)
        moves.append((src, dest))
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
    parser = argparse.ArgumentParser(description="Reorganize Little Einsteins for Plex")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("organize_little_einsteins.log"),
        ],
    )

    moves = build_plan()
    logging.info(f"\nPlan: {len(moves)} file operations")
    moved, skipped, errors = execute_plan(moves, dry_run=not args.execute)
    logging.info(f"\nSummary: moved={moved}  skipped={skipped}  errors={errors}")


if __name__ == "__main__":
    main()
