from analyzer import Analyzer

class Embedder:    
    # LSB method
    target_analyzer: Analyzer=None
    target_layer: int=0
    accuracy=25        #%

    def __init__(self, target_analyzer):
        self.target_analyzer=target_analyzer

    def set_target(self, target_analyzer):
        self.target_analyzer=target_analyzer

    def set_target_layer(self, target_layer):
        self.target_layer=target_layer

    def set_accuracy(self, accuracy: int):
        if accuracy < 0 or accuracy>100:
            raise ValueError('<Embedder> Error@set_accuracy')
        self.accuracy = accuracy

    def get_factor(self, value: int):
        # value : 255 = x : 100%
        return value * 100 // 255 if value>0 else 0
    
    # LSB layers: 3,2,1,0 - Alpha,RED,GREEN,BLUE

    def embedding(self, src_analyzers):
        if self.target_analyzer is None:
            raise ValueError('<Embedder> Error@embedding')

        for src_analyzer in src_analyzers:
            try:
                self.single_embedding(src_analyzer)
            except Exception as e:
                print(f"<Embedder> Error@embedding: @{src_analyzer}, {e}")
                pass

    # This method works fine iff target and data byte array are the same size and same Bpp.
    def single_embedding(self, src_analyzer: Analyzer):
        if self.target_analyzer is None or src_analyzer is None:
            raise ValueError('<Embedder> Error@single_embedding')

        if not self.target_analyzer.exist_layer(self.target_layer):
            raise ValueError('<Embedder> Error@single_embedding : out-of-bound layer of the target.')

        #if not src_analyzer.exist_layer(src_layer):
        #    raise ValueError('<Embedder> Error@single_embedding : out-of-bound layer of the info.')

        target_payload_size = self.target_analyzer.get_payload_size()
        steg_payload_size = src_analyzer.get_payload_size()

        if target_payload_size != steg_payload_size:
            raise ValueError('<Embedder> Error@single_embedding : different size')

        # Target 
        target_payload = self.target_analyzer.get_payload()
        _, target_height = self.target_analyzer.get_size()
        target_rowsize = self.target_analyzer.get_rowsize_Bpp()
        target_padding = self.target_analyzer.get_padding()
        target_Bpp = self.target_analyzer.get_Bpp()

        # Payload 
        src_payload = src_analyzer.get_payload()

        # Embedding
        for h in range(target_height):
            offset = h * (target_rowsize + target_padding) # h * target_rowsize + h * target_padding
            for pixel_offset in range(offset, offset + target_rowsize, target_Bpp):
                # pixel offset: [ B G R A ]
                pixel = pixel_offset + self.target_layer    # set which channel
                target_payload[pixel] = self.substitution(target_payload[pixel], src_payload[pixel]) 
        self.target_analyzer.set_payload(target_payload)

    # (1) strategy : LSB substitution if factor(src_value) > accuracy then 1 else 0
    def substitution(self, target_value, src_value):
        factor = self.get_factor(src_value)
        if factor < self.accuracy:
            target_value &= 0xFE    
        else:
            target_value |= 0x01   
        return target_value
    
    # (2) strategy : LSB substitution if factor(src_value) > accuracy then 1 else pass
    def substitution2(self, target_value, src_value):
        factor = self.get_factor(src_value)
        if factor >= self.accuracy:
            target_value |= 0x01          
        return target_value