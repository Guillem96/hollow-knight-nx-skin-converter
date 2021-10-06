import argparse
from pathlib import Path

import UnityPy
from PIL import Image

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
    ("sharedassets336", "atlas0", "26"): "Shriek",
    ("resources", "atlas0", "278"): "Liquid",
    ("resources", "moth_feather_particle", "423"): "DoubleJFeather",
    ("resources", "mines_floating_crystals", "386"): "SDCrystalBurst",
    ("resources", "atlas0", "306"): "Shade",
    ("resources", "charm_sprite_02", "2285"): "Charm_1",
    ("resources", "charm_sprite_03", "1702"): "Charm_2",
    ("resources", "charm_grub_mid", "1566"): "Charm_3",
    ("resources", "_0006_charm_stalwart_shell", "2173"): "Charm_4",
    ("resources", "charm_blocker", "2372"): "Charm_5",
    ("resources", "_0005_charm_fury", "1606"): "Charm_6",
    ("resources", "_0005_charm_fast_focus", "2423"): "Charm_7",
    ("resources", "_0010_charm_bluehealth", "2793"): "Charm_8",
    ("resources", "_0007_charm_blue_health_large", "1494"): "Charm_9",
    ("resources", "charm_dung_def", "2241"): "Charm_10",
    ("resources", "charm_fluke", "1421"): "Charm_11",
    ("resources", "_0000_charm_thorn_counter", "2243"): "Charm_12",
    ("resources", "char_mantis", "2073"): "Charm_13",
    ("resources", "_0006_charm_no_recoil", "2756"): "Charm_14",
    ("resources", "_0008_charm_nail_damage_up", "2144"): "Charm_15",
    ("resources", "charm_shade_impact", "2272"): "Charm_16",
    ("resources", "charm_fungus", "2696"): "Charm_17",
    ("resources", "_0007_charm_greed", "2499"): "Charm_18",
    ("resources", "_0002_charm_spell_damage_up", "2690"): "Charm_19",
    ("resources", "_0001_charm_more_soul", "1880"): "Charm_20",
    ("resources", "charm_soul_up_large", "2109"): "Charm_21",
    ("resources", "_0009_charm_Hatchling", "2594"): "Charm_22",
    ("resources", "_0002_charm_glass_heal_broken", "1813"): "Charm_23_Broken",
    ("resources", "_0002_charm_glass_heal", "2066"): "Charm_23_Fragile",
    ("resources", "_0002_charm_glass_heal_full", "1569"):
    "Charm_23_Unbreakable",
    ("resources", "_0003_charm_glass_geo_broken", "1577"): "Charm_24_Broken",
    ("resources", "_0003_charm_glass_geo", "1690"): "Charm_24_Fragile",
    ("resources", "_0003_charm_glass_geo_full", "2009"):
    "Charm_24_Unbreakable",
    ("resources", "_0002_charm_glass_attack_up_broken", "1479"):
    "Charm_25_Broken",
    ("resources", "_0002_charm_glass_attack_up", "2330"): "Charm_25_Fragile",
    ("resources", "_0002_charm_glass_attack_up_full", "1533"):
    "Charm_25_Unbreakable",
    ("resources", "_0004_charm_charge_time_up", "1518"): "Charm_26",
    ("resources", "charm_blue_health_convert", "2478"): "Charm_27",
    ("resources", "charm_slug", "1585"): "Charm_28",
    ("resources", "charm_hive", "1506"): "Charm_29",
    ("resources", "inv_dream_charm", "2219"): "Charm_30",
    ("resources", "_0011_charm_generic_03", "1612"): "Charm_31",
    ("resources", "_0003_charm_nail_slash_speed_up", "2465"): "Charm_32",
    ("resources", "charm_magic_cost_down", "2382"): "Charm_33",
    ("resources", "charm_crystal", "2758"): "Charm_34",
    ("resources", "charm_grub_blade", "1562"): "Charm_35",
    ("resources", "charm_black", "1899"): "Charm_36_Black",
    ("resources", "charm_white_full", "2500"): "Charm_36_Full",
    ("resources", "charm_white_left", "1580"): "Charm_36_Left",
    ("resources", "charm_white_right", "2124"): "Charm_36_Right",
    ("resources", "charm_grimm_sprint_master", "1767"): "Charm_37",
    ("resources", "charm_grimm_markoth_shield", "1498"): "Charm_38",
    ("resources", "charm_grimm_silkweaver", "1773"): "Charm_39",
    ("resources", "charm_grimmkin_01", "2049"): "Charm_40_1",
    ("resources", "charm_grimmkin_02", "2378"): "Charm_40_2",
    ("resources", "charm_grimmkin_03", "1950"): "Charm_40_3",
    ("resources", "charm_grimmkin_04", "2814"): "Charm_40_4",
    ("resources", "charm_grimmkin_05", "1802"): "Charm_40_5",
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

    skin_files = {p.name for p in skin_path.glob("*.png")}
    used_files = set()
    for fpath in mod_files:
        used_files.update(modify_file(fpath, skin_path, output))

    skin_files.difference_update(used_files)

    print(f".. WARNING following skin files has not been used: {skin_files}")

    print("*** DONE ***")
    print(f"*** Copy the '{GAMEID}' folder which is in",
          f"{Path(args.output, skin_path.stem)} to 'atmosphere/contents'***")
    print("***Don't forget to restart your Switch every time you add a",
          "new skin! ***")


def modify_file(fpath, skin_path, base_out):
    used_files = set()

    e = UnityPy.load(str(fpath))
    for obj in e.objects:
        data = obj.read()
        key = (fpath.stem, getattr(data, "name", None), str(data.path_id))
        if key in MAPPING:
            skin_file = skin_path / f"{MAPPING[key]}.png"
            if skin_file.exists() and obj.type == "Texture2D":
                update_texture(data, skin_file)
                used_files.add(skin_file.name)
            elif skin_file.exists() and obj.type == "Sprite":
                update_sprite(data, skin_file)
                used_files.add(skin_file.name)
            else:
                print(f"=> Skin '{skin_path.stem}' does not have",
                      f"'{skin_file.stem}' texture, skipping...")

    if used_files:
        with (base_out / fpath.name).open("wb") as f:
            f.write(e.file.save())

    return used_files


def update_texture(data, skin_file):
    print(f"=> Applying '{skin_file.stem}' texture...")
    data.image = str(skin_file)
    data.save()


def update_sprite(data, skin_file):
    print(f"=> Applying '{skin_file.stem}' sprite...")
    new_sprite = Image.open(skin_file)
    atlas = None
    if data.m_SpriteAtlas:
        atlas = data.m_SpriteAtlas.read()
    elif data.m_AtlasTags:
        # looks like the direct pointer is empty, let's try to find the Atlas
        # via its name
        for obj in data.assets_file.objects.values():
            if obj.type == "SpriteAtlas":
                atlas = obj.read()
                if atlas.name == data.m_AtlasTags[0]:
                    break
                atlas = None

    if atlas:
        sprite_atlas_data = atlas.m_RenderDataMap[data.m_RenderDataKey]
    else:
        sprite_atlas_data = data.m_RD

    pptr_texture2d = sprite_atlas_data.texture
    alpha_texture = sprite_atlas_data.alphaTexture
    texture_rect = sprite_atlas_data.textureRect

    new_sprite = new_sprite.resize(
        (int(texture_rect.width), int(texture_rect.height)))

    new_sprite = new_sprite.transpose(Image.FLIP_TOP_BOTTOM)
    original_image = UnityPy.export.SpriteHelper.get_image(
        data, pptr_texture2d, alpha_texture)
    original_image.paste(new_sprite,
                         (int(texture_rect.x), int(texture_rect.y)))

    texture2d = pptr_texture2d.read()
    texture2d.image = original_image.transpose(Image.FLIP_TOP_BOTTOM)
    texture2d.save()
    data.save()


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
