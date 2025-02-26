class Embedder:    
    # LSB bitmap image bpp (bits per pixel)
    # [+] target, bitmap data.
    # [+] src, bitmap data source of data to insert in target.
    # [+] layer, which layer to apply.
    # [+] twidth & theight, size of target.
    # [+] trsize, target row size
    # [+] drsize, data row size
    # [+] tBpp, target Bpp
    # [+] dBpp, data Bpp

    # This method works fine iff target and data byte array are the same
    # size. 
    # length = height * rowsize
    @staticmethod
    def apply(target, layer, data, theight, trsize, tBpp):
        if layer<0 or layer>3:
            raise ValueError('Error@Embedder: AlphaRGB layer.')
        length = theight * trsize
        if length != len(target) or length != len(data):
            raise ValueError(f'Error@Embedder: size does not match. {length}, {len(target)}, {len(data)}')
        for h in range(theight):
            start = h * trsize
            end = h * trsize + trsize
            for i in range(start, end, tBpp):
                # LSB layers: 3,2,1,0 - Alpha,RED,GREE,BLUE 
                if data[i + layer] < 128:
                    target[i + layer] &= 0xFE     # LSB - set zero
                else:
                    target[i + layer] |= 0x01     # LSB - set one
            #print(f"start: {start}, end: {end}")