import UnityPy
import argparse
from pathlib import Path


def main():
    args = parse_args()

    base_path = Path(args.dump_path)
    out = Path(args.output)
    out.mkdir(exist_ok=True)

    for asset in base_path.rglob("*.assets"):
        print(f"=> Reading {asset}...", end="", flush=True)
        e = UnityPy.load(str(asset))

        for obj in e.objects:
            data = obj.read()
            if data.type == "Texture2D":
                try:
                    data.image.save(
                        out / f"{asset.stem}_{data.name}_{data.path_id}.png")
                except SystemError:
                    print("*", end="", flush=True)

        print("done", flush=True)


def parse_args():
    parser = argparse.ArgumentParser(
        "Retrieve all Texture2D images from Unity assets files.")
    parser.add_argument("--dump-path",
                        required=True,
                        help="Path to Hollow Knight dump.")
    parser.add_argument("--output",
                        default=f"output",
                        help="Base output path.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
