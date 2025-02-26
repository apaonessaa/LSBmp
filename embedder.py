from analyzer import Analyzer

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

    target_analyzer=None

    def __init__(self, target_analyzer: Analyzer):
        self.target_analyzer=target_analyzer

    # This method works fine iff target and data byte array are the same size.
    # LSB layers: 3,2,1,0 - Alpha,RED,GREEN,BLUE
    def apply(self, steg_analyzer: Analyzer, target_layer: int =0, steg_layer: int =0):
        if self.target_analyzer is None or steg_analyzer is None:
            raise ValueError('<Embedder> Error@apply')

        if not self.target_analyzer.exist_layer(target_layer):
            raise ValueError('<Embedder> Error@apply : out-of-bound layer of the target.')

        if not steg_analyzer.exist_layer(steg_layer):
            raise ValueError('<Embedder> Error@apply : out-of-bound layer of the info.')

        target_payload_size = self.target_analyzer.get_payload_size()
        steg_payload_size = steg_analyzer.get_payload_size()

        if target_payload_size != steg_payload_size:
            raise ValueError('<Embedder> Error@apply : different size')

        # Target 
        target_payload = self.target_analyzer.get_payload()
        _, target_height = self.target_analyzer.get_size()
        target_rowsize = self.target_analyzer.get_rowsize()
        target_Bpp = self.target_analyzer.get_Bpp()

        # Payload 
        steg_payload = steg_analyzer.get_payload()

        # Embedding
        for h in range(target_height):
            offset = h * target_rowsize
            for i in range(offset, offset + target_rowsize, target_Bpp):
                if steg_payload[i + steg_layer] < 128:
                    target_payload[i + target_layer] &= 0xFE     # LSB - set zero
                else:
                    target_payload[i + target_layer] |= 0x01     # LSB - set one

        self.target_analyzer.set_payload(target_payload)

        print(f"Embedding complete.")

        
