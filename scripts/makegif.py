import argparse
from dataclasses import dataclass
import glob
import os
from pathlib import Path

from PIL import Image


@dataclass
class Frame:
    path: Path
    duration: int


def create_gif(frames, output_path, scale_factor=3):

    mapping = {
        (255, 255, 255): (187, 215, 167),   # background
        (255, 0, 0):     (244,  94,  19),   # red
        (0, 128, 0):     ( 27, 175,  91),   # green
        (0, 0, 255):     ( 35,  75, 166),   # blue
    }
    palette_list = []
    for color in mapping.values():
        palette_list.extend(color)
    palette_list.extend([0] * (768 - len(palette_list)))
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette_list)
    
    processed_frames = []
    durations = []

    for frame in frames:
        # load
        image = Image.open(frame.path).convert("RGB")
        # resize
        new_size = (image.width * scale_factor, image.height * scale_factor)
        image = image.resize(new_size, resample=Image.NEAREST)
        # apply color mapping
        pixels = list(image.getdata())
        new_pixels = [mapping.get(pixel, pixel) for pixel in pixels]
        image.putdata(new_pixels)
        # Convert to fixed palette
        image = image.quantize(palette=palette_img, dither=0)
        processed_frames.append(image)
        durations.append(frame.duration)

    # save sequence
    if processed_frames:
        processed_frames[0].save(
            output_path,
            save_all=True,
            append_images=processed_frames[1:],
            optimize=True,
            duration=durations,
            loop=0
        )
        print(f"GIF saved as '{output_path}''")


def load_sequence(pattern, duration):
    files = glob.glob(str(pattern))
    files = sorted(files)
    assert len(files) > 0
    frames = [Frame(file,duration) for file in files]
    return frames


def build_sequence(input_folder):
    files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.bmp'))])
    patterns = {
        input_folder / '00-main.bmp' : 1000,
        input_folder / 'gif' / 'botma1' / 'botma0*.bmp' : 300,
        input_folder / 'gif' / 'botma1' / 'botma11.bmp' : 1000,
        input_folder / 'gif' / 'botma2' / 'botma1*.bmp' : 300,
        input_folder / 'gif' / 'botma2' / 'botma2*.bmp' : 300,
        input_folder / 'gif' / 'botma2' / 'botma24.bmp' : 1500,
        input_folder / 'gif' / 'fight' / 'attak0*.bmp' : 200,
        input_folder / 'gif' / 'fight' / 'attak1*.bmp' : 200,
        input_folder / 'gif' / 'fight' / 'attak20.bmp' : 1000,
        input_folder / 'gif' / 'world' / 'world0*.bmp' : 300,
        input_folder / 'gif' / 'world' / 'world1*.bmp' : 75,
        input_folder / 'gif' / 'meltingpot' / '*.bmp' : 300,
        input_folder / '99-the-end.bmp' : 2000,
    }
    sequence = list()
    for pattern, duration in patterns.items():
        sequence += load_sequence(pattern, duration)
    return sequence


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--directory', '-d')
    args = p.parse_args()
    projdir = Path(args.directory)

    input_folder = projdir / 'doc' / 'images'
    output_path = projdir / 'images' / 'tproject.gif'

    sequence = build_sequence(input_folder)
    create_gif(sequence, output_path, scale_factor=3)

if __name__ == "__main__":
    main()
