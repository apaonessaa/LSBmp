import math

class Analyzer:
    raw_image: bytes=None
    
    def __init__(self, raw_image):
        self.raw_image = bytearray(raw_image)

    def set_raw_image(self, raw_image):
        self.raw_image = bytearray(raw_image)
            
    def get_raw_image(self):
        return bytes(self.raw_image)

    def get_offset(self):
        # bitmap image data (pixel array) offset
        # [+] start offset:     10 bytes
        # [+] size:             4 bytes
        return int.from_bytes(self.raw_image[10:14], byteorder='little')

    def get_size(self):
        # bitmap image width & height (signed integer)
        # [+] start offset:     18 bytes
        # [+] size:             4 bytes
        width = int.from_bytes(self.raw_image[18:22], byteorder='little')
        height = int.from_bytes(self.raw_image[22:26], byteorder='little')
        return width, height

    def get_bpp(self):
        # bitmap image bpp (bits per pixel)
        # [+] start offset:     28 bytes
        # [+] size:             2 bytes
        bpp = int.from_bytes(self.raw_image[28:30], byteorder='little')
        return bpp
    
    def get_Bpp(self):
        # bitmap image Bpp (Bytes per pixel)
        # Note: 1, 4 o 8 bits per pixel
        bpp = self.get_bpp()
        return max(1, bpp // 8)
    
    def get_rowsize_bpp(self):
        # bitmap image row size in pixel
        # [+] width, image width expressed in pixels
        # [+] bpp, bits per pixel
        width, _ = self.get_size()
        bpp = self.get_bpp()
        return bpp * width
    
    def get_rowsize_Bpp(self):
        # bitmap image row size in pixel
        row_size_bpp = self.get_rowsize_bpp()
        return math.ceil(row_size_bpp / 8)

    def get_payload_size(self):
        # bitmap image size in pixel, pixel array size
        # rawdata + padding
        rowsize = self.get_rowsize_Bpp() + self.get_padding()
        _, height = self.get_size()
        return height * rowsize
    
    def get_payload(self):
        # bitmap image data (pixel array), bytearray format
        # [+] start offset:     10 bytes
        # [+] size:             4 bytes
        start = self.get_offset()
        payload_size = self.get_payload_size()
        return self.raw_image[start:start+payload_size]
    
    def set_payload(self, payload: bytearray):
        # bitmap image data (pixel array), bytearray format
        # [+] start offset:     10 bytes
        # [+] size:             4 bytes
        start = self.get_offset()
        payload_size = self.get_payload_size()
        if len(payload) != payload_size:
            raise ValueError('Error')
        self.raw_image[start:start+payload_size] = payload
    
    def exist_layer(self, layer: int):
        Bpp = self.get_Bpp()
        return layer < Bpp
    
    # Padding
    # Bitmap pixel data is stored in rows (also known as strides or scan lines).
    # Each row's size must be a multiple of 4 bytes (a 32-bit DWORD).
    # If the row's raw data is not already a multiple of 4 bytes, padding bytes are added at the end.
    def get_padding(self):  
        # Maximum padding size: 3 bytes (since a full 4-byte padding block is unnecessary).
        #
        # Example: 
        #   - 24-bit BMP (Bpp = 3 bytes per pixel), Width = 1 pixel
        #   - Raw row size = 1 * 3 = 3 bytes (not a multiple of 4)
        #   - (1) Compute remainder: 3 bytes % 4 = 3
        #   - (2) Compute padding: 4 - 3 = 1
        #   - (3) Apply final mod 4 to ensure padding is never 4: (4 - 3) % 4 = 1
        #   - Final row structure: [3 bytes pixel data] + [1 byte padding]
        #
        # General steps:
        #   (1) Compute raw row size: width * Bpp
        #   (2) Compute required padding: 4 - (raw row size % 4)
        #   (3) Apply mod 4 to prevent a full 4-byte padding block (unnecessary)
        #
        # If the row size is already a multiple of 4, the formula ensures padding = 0.
        width, _ = self.get_size()
        Bpp = self.get_Bpp()
        row_padding = (4 - (width * Bpp) % 4)  
        return row_padding % 4  

