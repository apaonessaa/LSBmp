import sys

from src.analyzer import Analyzer
from src.embedder import Embedder
from src.strategy import Strategy, StrategyImpl

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
            ### STAGE 0. Read the images
            with open(self.src_file, "rb") as src, \
                    open(self.host_file, "rb") as host:
                a1 = Analyzer(host.read(), self.debug)
                a2 = Analyzer(src.read(), self.debug)
            
            if (self.debug):
                images_info(a1, a2)
                print("="*120)
                print("PIPELINE")
                print("-"*120)

            ### STAGE 1. Clean the layers
            a1.clean(0).clean(1).clean(2)        

            ### STAGE 2. Choose the strategies
            strategy1 = Strategy().set_accuracy(accuracy= 35).set_strategy(method= StrategyImpl.substitution)
            strategy2 = Strategy().set_accuracy(accuracy= 50).set_strategy(method= StrategyImpl.substitution2)

            ### STAGE 3. Apply the pipeline
            embedder = Embedder(self.debug)
            embedder.set_host(a1)
            
            # Set Layer (RGB) [0:B ,1:G, 2:R]
            # Embedding parameters: [src_analyzers], [src_layers], [locations], strategy

            embedder.set_host_layer(0)
            embedder.embedding([a2,a2,a2],[0,1,2],[(0,0),(100,100),(250,235)],strategy1)
            
            embedder.set_host_layer(1)
            embedder.embedding([a2,a2,a2,a2,a2],[1,0,2,0,1],[(100,220),(0,100),(800,345),(90,700),(500,900)],strategy2)
            
            embedder.set_host_layer(2)
            embedder.embedding([a2,a2],[2,2],[(345,500),(0,0)],strategy2)
                
            ### STAGE 4. Embedding
            with open(self.host_file, "wb") as host:    
                host.write(a1.get_raw_image())

            if (self.debug):
                print("="*120)
                print()

        except Exception as e:
            print(f"Error@Pipeline: {e}")
            sys.exit(1)

def images_info(a1: Analyzer, a2: Analyzer):
    print()
    print("="*120)
    print("Host")
    print("-"*120)
    print(f"Image width, height: {a1.get_size()}")
    print(f"Pixel array size: {a1.get_payload_size()}")
    print(f"Row size: {a1.get_rowsize_Bpp()}")
    print(f"Padding: {a1.get_padding()}")
    print(f"Bpp: {a1.get_Bpp()}")
    print("="*120)
    print()
    print("="*120)
    print("Source")
    print("-"*120)
    print(f"Image width, height: {a2.get_size()}")
    print(f"Pixel array size: {a2.get_payload_size()}")
    print(f"Row size: {a2.get_rowsize_Bpp()}")
    print(f"Padding: {a2.get_padding()}")
    print(f"Bpp: {a2.get_Bpp()}")
    print("="*120)
    print()