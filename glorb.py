import itertools
import time

import matplotlib.pyplot as plt
import numpy as np
import sacn

color_channels = 3  # for RGB
no_pixels = 120  # number of pixels in the strip


# generate RGB data as a list with len 3 and values from 0-255 as a rainbow for a pixel given idx
def rainbow(idx, max_idx):
    # Calculate the position in the rainbow for this pixel
    position = (idx % max_idx) / max_idx

    # Calculate the values for red, green, and blue
    red = 0
    green = 0
    blue = 0

    if position < 0.2:
        red = 255
        green = int(1275 * position)
    elif position < 0.4:
        red = int(255 - 1275 * (position - 0.2))
        green = 255
    elif position < 0.6:
        green = 255
        blue = int(1275 * (position - 0.4))
    elif position < 0.8:
        green = int(255 - 1275 * (position - 0.6))
        blue = 255
    else:
        red = int(1275 * (position - 0.8))
        blue = 255

    return [red, green, blue]


def one_pixel(idx, step: int):
    if idx == step % no_pixels:
        return [255, 255, 255]
    else:
        return [0, 0, 0]


# use rgb(idx) to generate effects for each pixel
def generate_pixels(step: int, effects: list):
    pixels = []
    for idx in range(no_pixels):
        pixel = [0, 0, 0]
        for effect in effects:
            # add the rgb channels of the effect to the  rgb channels of the pixel
            effect_data = effect(idx, step)
            pixel = [sum(x) for x in zip(pixel, effect_data)]
        # make sure all values in pixel is less or equal to 255
        pixel = [min(x, 255) for x in pixel]
        pixels.append(pixel)
    return pixels


def plot_pixels(pixels):
    # reshape the pixel data into a 2D array
    # no_pixels = len(pixels) / color_channels
    pixels_2d = np.array(pixels).reshape((-1, 20, 3))
    ax.imshow(pixels_2d)
    ax.axis("off")
    plt.show(block=False)


sender = (
    sacn.sACNsender()
)  # provide an IP-Address to bind to if you want to send multicast packets from a specific interface
sender.start()  # start the sending thread
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].multicast = False
sender[1].destination = "glorb.local"

plt.ion
_, ax = plt.subplots()

effects = [
    lambda idx, step: rainbow(idx, 120),
    lambda idx, step: one_pixel(idx, step),
    # Add more functions here if desired
]

for step in range(120):
    pixel_data = generate_pixels(step, effects)
    plot_pixels(pixel_data)
    pixel_data_as_tuple = tuple(itertools.chain(*pixel_data))
    sender[1].dmx_data = pixel_data_as_tuple
    # make matplotlib render
    plt.pause(0.01)
    time.sleep(0.05)
sender.stop()  # do not forget to stop the sender
