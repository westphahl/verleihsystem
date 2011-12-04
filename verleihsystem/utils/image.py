import math


def entropy(image):
    """
    Calculates the entropy of a given image.

    Entropy is a measure of the average information density of a symbol system.
    In this case the symbols are pixels.

    See: http://en.wikipedia.org/wiki/Entropy_(information_theory)
    
        "The entropy of a image uses a structure in image processing known as a
        histogram. You can think of a histogram as a graph where the x-axis
        represents the range of all color intensities and the y-axis
        represents the frequency each intensity occurs in the image. The
        function returns a high value if there are a lot of different color
        intensities in the image, and a low value if there are a lot of
        similar color intensities."

    Source: http://www.reddit.com/r/pics/comments/j1q8q/for_science/c28fpb7
    """

    # Get the distribution of colors in the image.
    # 
    # That's the number of pixels that have colors in each of a fixed list of
    # color ranges, that span the image's color space.
    # (color space = the set of all possible colors).
    histogram = image.histogram()

    # Calculate the scope of the histogram
    #
    # Example:
    # Image with a size of 200 x 200 pixel
    #
    # a) Color space: RGBA (Red Green Blue Alpha) 4 Channels
    #    Scope: 200 * 200 * 4 = 160000
    #
    # b) Color space: Grayscale
    #    Scope: 200 * 200 * 1 = 40000
    histogram_scope = float(sum(histogram))
    
    # Calculate relative frequencies for non-zero bins
    #
    # A bin holds the number of pixels for a intensity range of a color
    # channel. Python's PIL divides a color channel into 256 intensity ranges.
    relative_frequencies = [c / histogram_scope for c in histogram if c != 0]

    # Return the entropy of the image.
    return -sum([f * math.log(f, 2) for f in relative_frequencies])


def scale_image(image_path, max_width, max_height, crop=True):
    """
    Scale image, optionally cropping it to the specified width and height.

    The function takes a path to an image as it's first argument and returns
    a PIL Image file.
    If crop is set to false the aspect ratio of the source image is preserved 
    and the result contains a image not larger than the given width and height.
    """
    from PIL import Image

    img = Image.open(image_path)
    width, height = img.size
    src_aspect_ratio = float(width) / height
    dst_aspect_ratio = float(max_width) / max_height

    # Crop the source image to match the desired aspect ratio.
    if crop:
        if src_aspect_ratio > dst_aspect_ratio: 
            # Cut the sides off.
            x, y = img.size
            crop_width = width - int(dst_aspect_ratio * height)

            while (crop_width > 0):
                x, y = img.size
                slice_width = min(crop_width, 10)
                left = img.crop((0, 0, slice_width, y))
                right = img.crop((x - slice_width, 0, x, y))

                # Remove the slice with the least entropy
                if entropy(left) < entropy(right):
                    img = img.crop((slice_width, 0, x, y))
                else:
                    img = img.crop((0, 0, x - slice_width, y))

                crop_width = crop_width - 10
        else:
            # Cut top and bottom off.
            x, y = img.size
            crop_height = height - int(dst_aspect_ratio * width)

            while (crop_height > 0):
                x, y = img.size
                slice_height = min(crop_height, 10)
                top = img.crop((0, 0, x, slice_height))
                bottom = img.crop((0, y - slice_height, x, y))

                # Remove the slice with the least entropy
                if entropy(top) < entropy(bottom):
                    img = img.crop((0, slice_height, x, y))
                else:
                    img = img.crop((0, 0, x, y - slice_height))

                crop_height = crop_height - 10

    # Do the actual scaling of the image
    if width < height:
        img.thumbnail((max_height, max_width), Image.ANTIALIAS)
    else:
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)

    return img
