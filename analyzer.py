import math

class Analyzer:
    raw_image=None
    def __init__(self, raw_image):
        self.raw_image=bytearray(raw_image)
            
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
        bpp = self.get_bpp()
        return bpp // 8
    
    def get_rowsize(self):
        width, _ = self.get_size()
        bpp = self.get_bpp()
        # bitmap image row size in pixel
        # [+] width, image width expressed in pixels
        # [+] bpp, bits per pixel
        return math.ceil(bpp * width / 32) * 4
    
    def get_payload_size(self):
        # bitmap image size in pixel, pixel array size
        rowsize = self.get_rowsize() 
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
        print(f"Bpp: {Bpp}, layer: {layer}")
        return layer < Bpp