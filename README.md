# LSBmp - Least Significant Bit Image Embedding

LSBmp is a tool that enables image embedding using the Least Significant Bit (LSB) technique. It takes a host image and embeds a source image within it, leveraging the LSB layers of the BMP format. This project is designed for research and experimentation in steganography and image manipulation.

## Features

- **Image Embedding**: Embed a source image into a host image using LSB techniques.
- **Multiple Layers**: Modify different layers (Alpha, Red, Green, Blue) for embedding.
- **Customizable Strategies**: Apply different embedding strategies with adjustable accuracy.
- **BMP Format Support**: Works with BMP images for precise bit manipulation.
- **Automatic Image Conversion**: Uses ImageMagick to convert images to the required BMP format.
- **Upcoming Enhancements**:
  - Define embedding layers via command-line arguments.
  - Allow selection of embedding strategies dynamically.
  - Support multiple strategies per execution.
  - Improve the embedding pipeline for better flexibility.

## Requirements

Before running the project, ensure you have the following tools installed:

- **Python 3.x**
- **ImageMagick** (for image conversion)
- **ExifTool** (optional, for image metadata analysis)

## Installation

Clone this repository and navigate to the project directory:

```sh
git clone https://github.com/yourusername/LSBmp.git
cd LSBmp
```

Ensure `imagemagick` is installed and properly configured.

## Usage

Run the `run` script to embed a source image into a host image:

```sh
./run <host_image> <src_image> [-H <host_width>x<host_height>] [-S <src_width>x<src_height>]
```

### Example:

```sh
./run images/tiger.jpg images/cat.jpeg -H 1222x1228 -S 100x100
```

### Script Breakdown

- **run**: Bash script that handles image validation, conversion, and execution.
- **main.py**: Core Python script that executes the embedding pipeline.
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

- **Command-line Strategy Selection**: Users will be able to specify which embedding strategy to use.
- **Layer Customization**: Allow users to define which LSB layer to modify from the command line.
- **Multiple Strategies in a Single Execution**: Users will be able to define multiple strategies to enhance flexibility.
- **Enhanced Error Handling**: Improve robustness in case of incorrect input parameters.

## License

This project is licensed under the MIT License.
