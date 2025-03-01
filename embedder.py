from analyzer import Analyzer
from strategy import Strategy

class Embedder:    
    """
    The Embedder class handles embedding a source image into a host image using LSB techniques.
    It allows for setting the host image, defining the target layer for embedding, and embedding multiple images at specific locations.
    """

    host_analyzer: Analyzer = None
    host_layer: int = 0

    def set_host(self, host_analyzer: Analyzer):
        """Assigns the host image analyzer."""
        self.host_analyzer = host_analyzer
        return self

    def set_host_layer(self, host_layer: int):
        """Sets the LSB layer of the host image where the embedding will occur."""
        if not self.host_analyzer.exist_layer(host_layer):
            raise ValueError('Error: The specified embedding layer is out of bounds.')
        self.host_layer = host_layer
        return self
    
    def embedding(self, s_analyzers, s_layers, s_locations, strategy):
        """Embeds multiple source images into the host image at specified locations using a given strategy."""
        if self.host_analyzer is None:
            raise ValueError('Error: No host image has been set for embedding.')

        n = min(len(s_analyzers), len(s_layers), len(s_locations))

        print('-' * 120 + '\n')
        for i in range(n):
            ws, hs = s_locations[i]
            try:
                self._embedding(s_analyzers[i], strategy, s_layers[i], ws, hs)
                print(f'[+] Successfully embedded source {i}: Layer={s_layers[i]}, Position={s_locations[i]}, Strategy={strategy}')
                print()
            except Exception as e:
                print(f'[-] Error embedding source {i}: Layer={s_layers[i]}, Position={s_locations[i]}, Strategy={strategy}')
                print(f'    Exception: {e}')
                print(f'    Skipping task {i}...')
        print('-' * 120)

    def _embedding(self, s_analyzer: Analyzer, strategy: Strategy, s_layer=0, w_start=0, h_start=0):
        """Handles the actual embedding process at the pixel level."""
        if s_analyzer is None:
            raise ValueError('Error: The source image analyzer is null.')

        if not s_analyzer.exist_layer(s_layer):
            raise ValueError('Error: The specified source layer is out of bounds.')
    
        t_width, t_height = self.host_analyzer.get_size()
        s_width, s_height = s_analyzer.get_size()

        # Validate start positions and sizes
        if w_start < 0 or h_start < 0:
            raise ValueError(f"Error: Negative starting position ({w_start}, {h_start}) is not allowed.")

        if t_width < w_start + s_width:
            raise ValueError(f"Error: Source image width ({s_width}) exceeds the host width. Reduce image size or adjust position.")
        
        if t_height < h_start + s_height:
            raise ValueError(f"Error: Source image height ({s_height}) exceeds the host height. Reduce image size or adjust position.")
        
        # Retrieve host image properties
        t_payload = self.host_analyzer.get_payload()
        t_rowsize = self.host_analyzer.get_rowsize_Bpp()
        t_padding = self.host_analyzer.get_padding()
        t_Bpp = self.host_analyzer.get_Bpp()

        # Retrieve source image properties
        s_payload = s_analyzer.get_payload()
        s_rowsize = s_analyzer.get_rowsize_Bpp()
        s_padding = s_analyzer.get_padding()
        s_Bpp = s_analyzer.get_Bpp()

        # Embedding loop
        for h in range(s_height):
            # Calculate row offsets
            t_offset = (h + h_start) * (t_rowsize + t_padding) + w_start * t_Bpp
            s_offset = h * (s_rowsize + s_padding)
            
            # Initialize channel indices
            t_channel = t_offset + self.host_layer 
            s_channel = s_offset + s_layer 
            
            for pixel in range(s_width):
                # Apply the embedding strategy on the pixel
                t_payload[t_channel] = strategy.apply(t_payload[t_channel], s_payload[s_channel])
                # Move to the next pixel in the same channel
                t_channel += t_Bpp
                s_channel += s_Bpp
                
        self.host_analyzer.set_payload(t_payload)
        return self
    
    # Note:
    #   The following formula:
    #       (h + h_start) * (t_rowsize + t_padding) 
    #   determines the starting row (height) in the host image where the embedding begins.
    #   Similarly, w_start defines the starting column (width) in the host image.
    #
    #   Example: (w_start, h_start) = (4, 5)
    #
    #   Visual Representation:
    #
    #   Height (rows)
    #   6:      ...
    #   5:      |               |*  <-- Embedding starts here
    #   4:      ----------------------- ...
    #   3:      |                   
    #   2:      |       Pass (not modified)        
    #   1:      |                   
    #   0:      ----------------------- ...
    #           0   1   2   3   4   ...     Width (columns)
    #
    #   - `h_start = 5` means the embedding starts at row 5 of the host image.
    #   - `w_start = 4` means the embedding starts at column 4 of the host image.
    #   - The asterisk (*) marks the exact pixel where the process begins.
    #
    #   The algorithm ensures that the embedding process does not exceed 
    #   the boundaries of the host image.

