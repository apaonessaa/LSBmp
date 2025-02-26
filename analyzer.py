import math

class Analyzer:
    data=None
    def __init__(self, data):
        self.data=data
            
    def get_offset(self):
        # bitmap image data (pixel array) offset
        # [+] start offset:     10 bytes
        # [+] size:             4 bytes
        return int.from_bytes(self.data[10:14], byteorder='little')

    def get_size(self):
        # bitmap image width & height (signed integer)
        # [+] start offset:     18 bytes
        # [+] size:             4 bytes
        width = int.from_bytes(self.data[18:22], byteorder='little')
        height = int.from_bytes(self.data[22:26], byteorder='little')
        return width, height

    def get_bpp(self):
        # bitmap image bpp (bits per pixel)
        # [+] start offset:     28 bytes
        # [+] size:             2 bytes
        bpp = int.from_bytes(self.data[28:30], byteorder='little')
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
    
    def get_bmp_size(self):
        # bitmap image size in pixel, pixel array size
        rowsize = self.get_rowsize() 
        _, heigth = self.get_size()
        return heigth * rowsize
    
    def get_bmp(self):
        # bitmap image data (pixel array), bytearray format
        # [+] start offset:     10 bytes
        # [+] size:             4 bytes
        start = self.get_offset()
        bmp_size = self.get_bmp_size()
        return bytearray(self.data[start:start+bmp_size])