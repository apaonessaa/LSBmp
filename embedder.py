from analyzer import Analyzer

class Strategy:
    accuracy=12        #%

    @classmethod
    def set_accuracy(cls, accuracy: int):
        if accuracy < 0 or accuracy>100:
            raise ValueError('<Embedder> Error@set_accuracy')
        cls.accuracy = accuracy

    def get_factor(value: int):
        # value : 255 = x : 100%
        return value * 100 // 255 if value>0 else 0
    
    # (1) strategy : LSB substitution if factor(src_value) > accuracy then 1 else 0
    @classmethod
    def substitution(cls, tvalue, svalue):
        factor = cls.get_factor(svalue)
        if factor < cls.accuracy:
            tvalue &= 0xFE    
        else:
            tvalue |= 0x01   
        return tvalue
    
    # (2) strategy : LSB substitution if factor(src_value) > accuracy then 1 else pass
    @classmethod
    def substitution2(cls, tvalue, svalue):
        factor = cls.get_factor(svalue)
        if factor >= cls.accuracy:
            tvalue |= 0x01 
        return tvalue

class Embedder:    
    # LSB method
    target_analyzer: Analyzer=None
    target_layer: int=0

    def __init__(self, target_analyzer):
        self.target_analyzer=target_analyzer

    def set_target(self, target_analyzer):
        self.target_analyzer=target_analyzer

    def set_target_layer(self, target_layer):
        if not self.target_analyzer.exist_layer(target_layer):
            raise ValueError('<Embedder> Error@set_target_layer : out-of-bound layer.')
        self.target_layer=target_layer
    
    # LSB layers: 3,2,1,0 - Alpha,RED,GREEN,BLUE
    def embedding(self, s_analyzers, s_layers):
        if self.target_analyzer is None:
            raise ValueError('<Embedder> Error@embedding')
        
        n=min(len(s_analyzers), len(s_layers))
        for i in range(n):
            try:
                self._embedding(s_analyzers[i], s_layers[i])
            except Exception as e:
                print(f'<Embedder> Error@embedding: @{s_analyzers[i]}, @{s_layers[i]}')
                print(f'{e}')
                pass
    
    def _embedding(self, s_analyzer: Analyzer, s_layer: int =0):
        if s_analyzer is None:
            raise ValueError('<Embedder> Error@_embedding: src is null')

        if not s_analyzer.exist_layer(s_layer):
            raise ValueError('<Embedder> Error@_embedding: src out-of-bound layer.')
    
        t_width, t_height = self.target_analyzer.get_size()
        s_width, s_height = s_analyzer.get_size()

        # check size 
        #if (t_width < s_width and t_height < s_height):
        #    raise ValueError('<Embedder> Error@_embedding: incompatible size.')
        
        if (t_width < s_width):
            raise ValueError('<Embedder> Error@_embedding: incompatible width.')

        if (t_height < s_height):
            raise ValueError('<Embedder> Error@_embedding: incompatible heigth.')
        
        # Target 
        t_payload = self.target_analyzer.get_payload()
        t_rowsize = self.target_analyzer.get_rowsize_Bpp()
        t_padding = self.target_analyzer.get_padding()
        t_Bpp = self.target_analyzer.get_Bpp()

        # Source 
        s_payload = s_analyzer.get_payload()
        s_rowsize = s_analyzer.get_rowsize_Bpp()
        s_padding = s_analyzer.get_padding()
        s_Bpp = s_analyzer.get_Bpp()

        # Set to zero
        for h in range(t_height):
            t_offset = h * (t_rowsize + t_padding)
            # s_width <= t_heigth
            for t_pixel_offset in range(t_offset, t_offset + t_rowsize, t_Bpp): 
                # [ ---- raw data ---- ] [ -- padding -- ] until the padding section
                # pixel offset: [ B G R A ]
                t_channel = t_pixel_offset + self.target_layer 
                # apply substitution 
                t_payload[t_channel] &= 0xFE

        # Embedding
        for h in range(s_height): # s_height <= t_height
            s_offset = h * (s_rowsize + s_padding)
            t_offset = h * (t_rowsize + t_padding)
            t_channel = t_offset # init t_channel
            for s_pixel_offset in range(s_offset, s_offset + s_rowsize, s_Bpp): # s_width <= t_heigth
                # [ ---- raw data ---- ] [ -- padding -- ] until the padding section
                # pixel offset: [ B G R A ]
                s_channel = s_pixel_offset + s_layer
                t_channel += t_Bpp + self.target_layer 
                # apply substitution 
                t_payload[t_channel] = Strategy.substitution2(t_payload[t_channel], s_payload[s_channel]) 
        self.target_analyzer.set_payload(t_payload)
