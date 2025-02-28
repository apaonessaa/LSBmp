from analyzer import Analyzer
from strategy import Strategy

class Embedder:    
    host_analyzer: Analyzer=None
    host_layer: int=0

    def set_host(self, host_analyzer):
        self.host_analyzer=host_analyzer
        return self

    def set_host_layer(self, host_layer):
        if not self.host_analyzer.exist_layer(host_layer):
            raise ValueError('<Embedder> Error@set_host_layer : out-of-bound layer.')
        self.host_layer=host_layer
        return self
    
    # Embedding more source in host layer at specific locations
    def embedding(self, s_analyzers, s_layers, s_locations, strategy):
        if self.host_analyzer is None:
            raise ValueError('<Embedder> Error@embedding')

        nsrc = len(s_analyzers)
        nlayers = len(s_layers)
        nlocs = len(s_locations)
        n = min(nsrc, nlayers, nlocs)

        for i in range(n):
            ws, hs = s_locations[i]
            try:
                self._embedding(s_analyzers[i], strategy, s_layers[i], ws, hs)
            except Exception as e:
                print(f'<Embedder> Error@embedding: @{s_analyzers[i]}, @{s_layers[i]}')
                print(f'{e}')
                pass

    # LSB layers: 3,2,1,0 - Alpha,RED,GREEN,BLUE
    def _embedding(self, s_analyzer: Analyzer, strategy: Strategy, s_layer=0, w_start=0, h_start=0):
        if s_analyzer is None:
            raise ValueError('<Embedder> Error@_embedding: src is null')

        if not s_analyzer.exist_layer(s_layer):
            raise ValueError('<Embedder> Error@_embedding: src out-of-bound layer.')
    
        t_width, t_height = self.host_analyzer.get_size()
        s_width, s_height = s_analyzer.get_size()

        ## Check start and size
        if w_start<0 or h_start<0:
            raise ValueError(f"<Embedder> Error@_embedding: negative start ({w_start},{h_start}).")

        if t_width < w_start + s_width:
            raise ValueError(f"<Embedder> Error@_embedding: incompatible width ({s_width}). Reduce the image size or assign new start.")
        
        if t_height < h_start + s_height:
            raise ValueError(f"<Embedder> Error@_embedding: incompatible height ({s_height}). Reduce the image size or assign new start.")
        
        # Host 
        t_payload = self.host_analyzer.get_payload()
        t_rowsize = self.host_analyzer.get_rowsize_Bpp()
        t_padding = self.host_analyzer.get_padding()
        t_Bpp = self.host_analyzer.get_Bpp()

        # Source 
        s_payload = s_analyzer.get_payload()
        s_rowsize = s_analyzer.get_rowsize_Bpp()
        s_padding = s_analyzer.get_padding()
        s_Bpp = s_analyzer.get_Bpp()

        # Embedding
        for h in range(s_height): # s_height <= t_height, and h_start < t_height
            # Note
            #   The following component:
            #       (h+h_start) * (t_rowsize + t_padding) 
            #   define at which host height (ROW) start (default is 0).
            #   While, the w_start at which host width (COLUMN) start the embedding (default is 0).
            #
            #   Example, (w_start,h_start)=(4,5)
            #
            #   @height
            #   6:      ...
            #   5:      |               |* <-- here
            #   4:      ----------------------- ...
            #   3:      |                   
            #   2:      |       Pass         
            #   1:      |                   
            #   0:      ----------------------- ...
            #           0   1   2   3   4   ...     @width
            #   
            #
            t_offset = (h + h_start) * (t_rowsize + t_padding) + w_start * t_Bpp
            s_offset = h * (s_rowsize + s_padding)
            # init t_channel and s_channel
            t_channel = t_offset + self.host_layer 
            s_channel = s_offset + s_layer 
            for pixel in range(s_width): # s_width <= t_heigth
                # pixel: [ B G R A ]
                # apply substitution 
                t_payload[t_channel] = strategy.apply(t_payload[t_channel], s_payload[s_channel]) 
                # switch to next pixel and same channel
                t_channel += t_Bpp
                s_channel += s_Bpp
                
        self.host_analyzer.set_payload(t_payload)
        return self