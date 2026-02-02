import sys

from BMPstat.bmpstat import BMPstat

from src.embedder import Embedder

class Pipeline:
    host_file: str=""
    src_file: str=""
    debug: bool=False

    def __init__(self, host_file, src_file, debug):
        self.host_file = host_file
        self.src_file = src_file
        self.debug = debug

    def apply(self):
        try:
            """
            STAGE 0. Read the images
            """
            with open(self.src_file, "rb") as f1, \
                    open(self.host_file, "rb") as f2:
                host = BMPstat(f2.read())
                src_img = BMPstat(f1.read())
            
            if (self.debug):
                images_info(host, src_img)
                print("="*120)
                print("PIPELINE")
                print("-"*120)

            """
                Embedding parameters: 
                    layer, sublayer, [src], [src_layers], [locations]
            """
            embedder = Embedder(host, self.debug)

            embedder.clean(0,0)
            embedder.embedding(0,0,[src_img],[0],[2],[(0,0)])

            embedder.set_accuracy(0)
            embedder.clean(1,1)
            embedder.embedding(1,1,[src_img],[1],[1],[(0,0)])

            embedder.set_accuracy(65)
            embedder.clean(2,5)
            embedder.embedding(2,6,[src_img],[2],[0],[(0,0)])
            
            with open(self.host_file, "wb") as f:    
                f.write(host.get_raw_image())

            if (self.debug):
                print("="*120)
                print()

        except Exception as e:
            print(f"Error@Pipeline: {e}")
            sys.exit(1)

def images_info(host: BMPstat, src_img: BMPstat):
    print()
    print("="*120)
    print("Host")
    print("-"*120)
    print(f"Image width, height: {host.get_size()}")
    print(f"Pixel array size: {host.get_payload_size()}")
    print(f"Row size: {host.get_rowsize()}")
    print(f"Padding: {host.get_padding()}")
    print(f"Bpp: {host.get_Bpp()}")
    print("="*120)
    print()
    print("="*120)
    print("Source")
    print("-"*120)
    print(f"Image width, height: {src_img.get_size()}")
    print(f"Pixel array size: {src_img.get_payload_size()}")
    print(f"Row size: {src_img.get_rowsize()}")
    print(f"Padding: {src_img.get_padding()}")
    print(f"Bpp: {src_img.get_Bpp()}")
    print("="*120)
    print()