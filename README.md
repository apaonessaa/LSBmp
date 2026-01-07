# LSBmp - Least Significant Bit Image Embedding

LSBmp is a advanced tool that enables image embedding using the Least Significant Bit (LSB) technique. It takes a host image and embeds a source image within it, leveraging the LSB layers of the BMP format. This project is designed for research and experimentation in steganography and image manipulation.

It works with BMP images for precise bit manipulation.

## Features

- **Image Embedding**: Embed a source image into a host image using LSB techniques.
- **Multiple Layers**: Modify different layers (Red, Green, Blue) for embedding.
- **Customizable Strategies**: Apply different embedding strategies with adjustable accuracy.

## Requirements

Before running the project, ensure you have the following tools installed:

- **Python 3.x**
- **ImageMagick** (optional, for image conversion)
- **ExifTool** (optional, for image metadata analysis)

## Installation

Clone this repository and navigate to the project directory:

```sh
git clone https://github.com/yourusername/LSBmp.git
cd LSBmp
```

## Usage with BMP convertor

Run the `run` script to embed a source image into a host image:

```sh
./run <host_image> <src_image> [-H <host_width>x<host_height>] [-S <src_width>x<src_height>]
```

**Note**: Ensure `imagemagick` is installed and properly configured.

### Example:

```sh
./run images/tiger.jpg images/cat.jpeg -H 1222x1228 -S 100x100
```

## Usage of the core script

If you want to run the main `lsbmp` script directly:

```sh
./lsbmp --host-file <host_image> --src-file <src_image> [-d, --debug]
```

**Note**: Ensure that the **host image** and the **src image** are BMP file image format.

### Project Breakdown

- **run**: Bash script that handles image validation, conversion (to BMP), and execution (It is a support scripts to simplify the watermarked image creation process).
- **lsbmp**: Python script that executes embedding.
- **pipeline.py**: Defines a custom embedding pipeline stages and can be manipulated by the user to define their own embedding strategy.
  - Which RGB layer to clean? (All pixels to zero)
  - Where to place the SRC image inside the host object? (You choose the layer and fix the coordinates of the pixels to be altered)
- **analyzer.py**: Analyzes BMP images for size, padding, and bit depth.
- **embedder.py**: Handles embedding logic with different strategies.
- **strategy.py**: Defines embedding strategies and accuracy levels.

## Output

After execution, the modified host image is saved as `out.bmp` in the same directory.

## Video Demonstration

Below is a demonstration of the embedding process and the resulting image:



https://github.com/user-attachments/assets/32d2a1ba-1c37-4ea3-a6e5-796256061c04



Note: The quality of the embedded information in the host image depends on several factors, including the embedding accuracy, the selected LSB layer, the number of altered bits, and the applied embedding strategy. These factors influence both the visibility of the embedded content and the preservation of the host image quality.

## Roadmap

- **Choose which LSB to alter**: Add for each RGB layer which bit you want to alter.
- **Add alternative to the "cleaning" of the RGB layer with only zeros to increase the imperceptibility property of the watermark**.
- **Multiple Source Images to Embedding**.
- **Simplify Pipeline Definition**: via GUI?.
- **Enhanced Error Handling**: Improve robustness in case of incorrect input parameters.

## License

This project is licensed under the MIT License.

