import os
import sys

import cv2
import numpy as np

from screens import AspectRatio, Screen, ScreenDimension


def get_screen_scale_factor(image_res, screen_res) -> float:
    # calculate ratio of pixels of an image relative to a screens resolution
    return image_res / screen_res


def crop_to_aspect_ratio(image: np.ndarray, aspect_ratio: AspectRatio):
    # find the ratio of width [1] to height [0]
    height = image.shape[0]
    width = image.shape[1]
    ratio = width / height

    # if less than desired ratio, remove pixels from height [0]
    # calculate by dividing width by desired aspect width then mult by desired aspect height to find new height required
    if ratio < aspect_ratio.ratio:
        new_height = (width / aspect_ratio.width) * aspect_ratio.height
        if new_height > height:
            raise Exception("new height should be smaller")
        diff = int((height - new_height) / 2)
        image = image[diff:-diff]

    # if greater than desired ratio, remove pixels from width [1]
    # divide height by desired aspect height then mult by desired aspect width to find new width.
    elif ratio < aspect_ratio.ratio:
        new_width = (height / aspect_ratio.height) * aspect_ratio.width
        if new_width > width:
            raise Exception("new width should be smaller")
        diff = int((width - new_width) / 2)
        image = image[:, diff:-diff]
    return image


def add_black_top_bar(image: np.ndarray, screen: ScreenDimension):
    # add black pixels to top.
    # calculate ratio to retina res then apply menu_height x res ratio.
    height = image.shape[0]
    top_bar_height = round(
        screen.menubar_height
        * get_screen_scale_factor(image_res=height, screen_res=screen.corrected_height)
    )
    top_bar_dims = [top_bar_height, *image.shape[1:]]

    top_bar = np.zeros(top_bar_dims)
    image = np.concatenate([top_bar, image], axis=0)
    return image


def change_directory(
    source_dir,
    sink_dir=None,
    aspect_ratio: AspectRatio = AspectRatio(width=16, height=10),
    screen: ScreenDimension = Screen.MacBookPro_16_2021_BigSur,
) -> None:
    """
    Method to convert all images in a directory to be 16:10 aspect ratio (by default) and adds a black bar to hide
    the notch.
    """
    if sink_dir is not None:
        os.makedirs(sink_dir, exist_ok=True)
    else:
        sink_dir = source_dir
    for file in os.listdir(source_dir):
        if not file == ".DS_Store":  # TODO need to exclude non-image files better
            im = cv2.imread(f"{source_dir}/{file}")
            cropped = crop_to_aspect_ratio(image=im, aspect_ratio=aspect_ratio)
            top_bar = add_black_top_bar(image=cropped, screen=screen)
            cv2.imwrite(f"{sink_dir}/{file}", top_bar)


if __name__ == "__main__":
    # converts pictures in the first argument folder for a MacBook Pro 16" screen running MacOS BigSur
    # and stores in the second argument TODO make a better CLI for this.
    change_directory(
        source_dir=os.path.join(sys.argv[1]),
        sink_dir=os.path.join(sys.argv[2]),
    )
