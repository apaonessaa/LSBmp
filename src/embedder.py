from BMPstat.bmpstat import BMPstat

class Embedder:    
    """
    The Embedder class handles embedding a source image into a host image using LSB techniques.

    Strategy:
    * Embedding with accuracy factor
    * RAW Embedding

    """
    host: BMPstat=None
    accuracy: int=35
    debug: bool=False
    _RGB = ["R", "G", "B"]

    def __init__(self, host: BMPstat, debug):
        self.host = host
        self.debug = debug

    def set_accuracy(self, value:int):
        """
            Embedding strategy accuracy in [0,100].

            if accuracy > 0:
                * Embedding with accuracy factor
                if factor(src_img[i,j]) > accuracy
                    set_one
                else
                    set_zero
            else
                * RAW embedding
        """
        if value < 0 or value > 100:
            raise ValueError('Error@Accuracy: the value is not valid. Set value in [0,100]')
        self.accuracy = value

    def get_factor(self, value: int):
        # value : 255 = x : 100%
        if not 0 <= value <= 255:
            raise ValueError('Error@Factor: the value is not valid. Accepted value in [0,255]')
        return value * 100 // 255 if value>0 else 0

    def _debug(self, message: str):
        if (self.debug):
            print(message)

    def check_not_null(self):
        if self.host is None:
            raise ValueError('Error: No host image has been set for embedding.')

    def check_not_null_src(self, img: BMPstat):
        if img is None:
            raise ValueError('Error: No source image has been set for embedding.')

    # set LSB raw image to zero
    def clean(self, layer: int, sublayer: int):
        self.check_not_null()
        """
            Clean a layer by setting LSB to zero:
            - Layer:    [ R G B ]
            - Sublayer: [ 0 1 2 3 4 5 6 7 ]
        """
        width, height = self.host.get_size()
        
        for i in range(width):
            for j in range(height):
                self.host.set_zero(i, j, layer, sublayer)
        
        self._debug(f"The layer [{self._RGB[layer]},{sublayer}] is cleaned.")
        
        return self
    
    def embedding(self, layer, sublayer, src_img, src_layers, src_sublayers, pos):
        """
            The layer and sublayer of the host image.

            Embeds multiple source images into the host image:
            - Layers    [R,G,B]
            - Sublayer  [0,1,2]
            - positions [(x,y)] 

            Note: If embedding fails, move on.
        """
        self.check_not_null()

        self._debug('\n' + '-' * 120)

        for i in range( min(len(src_img), len(src_layers), len(src_sublayers), len(pos)) ):
            x, y = pos[i]
            try:
                self._embedding(layer, sublayer, src_img[i], src_layers[i], src_sublayers[i], x, y)
            
                self._debug(f'[+] Successfully embedded source {i}: Layer={self._RGB[src_layers[i]]}, Sublayer: {src_sublayers[i]}, Position={pos[i]}')
            
            except Exception as e:
                print(f'[-] Error embedding source {i}: Layer={self._RGB[src_layers[i]]}, Sublayer: {src_sublayers[i]}, Position={pos[i]}')
                print(f'    Exception: {e}')
                print(f'    Skipping task {i}...')
    
        self._debug('-' * 120 + '\n')

    def _embedding(self, layer: int, sublayer: int, src_img: BMPstat, s_layer=0, s_sublayer=0, w_start=0, h_start=0):
        """
            Handles the actual embedding process at the pixel level.
        """
        self.check_not_null()
        self.check_not_null_src(src_img)
        self.host.check_layer(layer)
        self.host.check_sublayer(sublayer)
        src_img.check_layer(s_layer)
        src_img.check_sublayer(s_sublayer)

        h_width, h_height = self.host.get_size()
        s_width, s_height = src_img.get_size()

        if w_start < 0 or h_start < 0:
            raise ValueError(f"Error: Negative starting position ({w_start}, {h_start}) is not allowed.")

        if h_width < w_start + s_width:
            raise ValueError(f"Error: Source image width ({s_width}) exceeds the host width. Reduce image size or adjust position.")
        
        if h_height < h_start + s_height:
            raise ValueError(f"Error: Source image height ({s_height}) exceeds the host height. Reduce image size or adjust position.")
 
        """
            Strategies:
                - Embedding with accuracy (default) (more perceptible)
                - Embedding raw bit
        """
        strategy = self._accuracy_embedding
        if self.accuracy == 0:
            strategy = self._raw_embedding
        
        strategy(layer, sublayer, src_img, s_layer, s_sublayer, w_start, h_start)

    def _accuracy_embedding(self, layer: int, sublayer: int, src_img: BMPstat, s_layer=0, s_sublayer=0, w_start=0, h_start=0):
        """
            Embedding strategy:
                Get value of src_img[x,y] pixel.
                Get layer value of src_img[x,y] pixel.
                
                src_value = src_img[x,y][s_layer]
                
                If the factor of the src_value > accuracy value
                    then
                        set one to host[i,j][layer] to LSB[sublayer] bit.
                else
                    set zero to host[i,j][layer] to LSB[sublayer] bit.
        """
        s_width, s_height = src_img.get_size()
        for i in range(s_width):
            for j in range(s_height):
                s_pixel = src_img.get_pixel_offset(i, j)
                value = src_img.raw_image[s_pixel + s_sublayer]
                if self.get_factor(value) < self.accuracy:
                    self.host.set_zero(i + w_start, j + h_start, layer, sublayer)
                else:
                    self.host.set_one(i + w_start, j + h_start, layer, sublayer)
        return self

    def _raw_embedding(self, layer: int, sublayer: int, src_img: BMPstat, s_layer=0, s_sublayer=0, w_start=0, h_start=0):
        """
            Embedding strategy:
                Get value of src_img[x,y] pixel.
                Get layer value of src_img[x,y] pixel.
                
                src_value = src_img[x,y][s_layer]

                Get sublayer of src_value.

                src_lsb = src_img[x,y][s_layer][sub_layer]
                
                If src_lsb is 1
                    then
                        set one to host[i,j][layer] to LSB[sublayer] bit.
                else
                    set zero to host[i,j][layer] to LSB[sublayer] bit.
        """
        s_width, s_height = src_img.get_size()
        for i in range(s_width):
            for j in range(s_height):
                s_pixel = src_img.get_pixel_offset(i, j)
                value = src_img.raw_image[s_pixel + s_sublayer]
                if value & 0X1:
                    self.host.set_one(i + w_start, j + h_start, layer, sublayer)
                else:
                    self.host.set_zero(i + w_start, j + h_start, layer, sublayer)
        return self
