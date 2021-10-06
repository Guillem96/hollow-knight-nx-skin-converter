import argparse
from pathlib import Path

import UnityPy

GAMEID = "0100633007D48000"
MAPPING = {
    ("resources", "atlas0", "359"): "Knight",
    ("resources", "atlas0", "301"): "Hatchling",
    ("resources", "atlas0", "397"): "Sprint",
    ("resources", "atlas0", "402"): "Hud",
    ("resources", "atlas0", "417"): "Unn",
    ("resources", "atlas0", "226"): "VS",
    ("resources", "atlas0", "311"): "Wraiths",
    ("resources", "atlas0", "384"): "VoidSpells",
    ("resources", "atlas0", "310"): "Fluke",
    ("resources", "atlas0", "356"): "Geo",
    ("resources", "atlas0", "375"): "Shield",
    ("resources", "atlas0", "367"): "Baldur",
    ("resources", "atlas0", "391"): "Weaver",
    ("resources", "atlas0", "394"): "Grimm",
    ("sharedassets339", "atlas0", "7"): "Birthplace",
    ("sharedassets242", "atlas0", "7"): "DreamArrival",
    ("sharedassets242", "atlas0", "8"): "Dreamnail",
    ("sharedassets316", "atlas0", "3"): "Hornet",
    ("sharedassets337", "atlas0", "12"): "Cloak",
    ("sharedassets345", "atlas0", "8"): "Wings",
    ("sharedassets304", "atlas0", "8"): "Webbed",
    ("sharedassets13", "atlas0", "19"): "Quirrel",
    # (): "OrbFull",
    ("sharedassets336", "atlas0", "26"): "Shriek",
}


def main():
    args = parse_args()

    skin_path = Path(args.skin)
    mod_files = {
        Path(args.dump_path, "Data", f"{o[0]}.assets")
        for o in MAPPING
    }
    output = Path(args.output, skin_path.stem, GAMEID, "romfs", "Data")
    output.mkdir(exist_ok=True, parents=True)

    for fpath in mod_files:
        modify_file(fpath, skin_path, output)

    print("*** DONE ***")
    print(f"*** Copy the '{GAMEID}' folder which is in",
          f"{Path(args.output, skin_path.stem)} to 'atmosphere/contents'***")
    print("***Don't forget to restart your Switch every time you add a",
          "new skin! ***")


def modify_file(fpath, skin_path, base_out):
    has_modification = False

    e = UnityPy.load(str(fpath))
    for obj in e.objects:
        data = obj.read()
        key = (fpath.stem, "atlas0", str(data.path_id))

        if key in MAPPING:
            skin_file = skin_path / f"{MAPPING[key]}.png"
            if skin_file.exists():
                print(f"=> Applying '{skin_file.stem}'texture...")
                data.image = str(skin_file)
                data.save()
                has_modification = True
            else:
                print(f"=> Skin '{skin_path.stem}' does not have",
                      f"'{skin_file.stem}' texture, skipping...")

    if has_modification:
        with (base_out / fpath.name).open("wb") as f:
            f.write(e.file.save())


def parse_args():
    parser = argparse.ArgumentParser("Hollow Knight Skin converter")
    parser.add_argument("--dump-path",
                        required=True,
                        help="Path to Hollow Knight dump.")
    parser.add_argument("--skin", required=True, help="Skin directory.")
    parser.add_argument("--output",
                        default=f"output",
                        help="Base output path.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
