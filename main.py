#!/usr/bin/python3
import sys
from analyzer import Analyzer
from embedder import Embedder
from strategy import Strategy, StrategyImpl

def routine(host_file, src_file):
    try:
        with open(src_file, "rb") as src, \
                open(host_file, "rb") as host:
            a1 = Analyzer(host.read())
            a2 = Analyzer(src.read())

        print()
        print("===================================")
        print("Host")
        print("-----------------------------------")
        print(f"Image width, height: {a1.get_size()}")
        print(f"Pixel array size: {a1.get_payload_size()}")
        print(f"Row size: {a1.get_rowsize_Bpp()}")
        print(f"Padding: {a1.get_padding()}")
        print(f"Bpp: {a1.get_Bpp()}")
        print("===================================")
        print()
        print("===================================")
        print("Source")
        print("-----------------------------------")
        print(f"Image width, height: {a2.get_size()}")
        print(f"Pixel array size: {a2.get_payload_size()}")
        print(f"Row size: {a2.get_rowsize_Bpp()}")
        print(f"Padding: {a2.get_padding()}")
        print(f"Bpp: {a2.get_Bpp()}")
        print("===================================")
        print()

        strategy1 = Strategy().set_accuracy(accuracy= 45).set_strategy(method= StrategyImpl.substitution)
        strategy2 = Strategy().set_accuracy(accuracy= 27).set_strategy(method= StrategyImpl.substitution2)

        a1.clean(0).clean(1).clean(2)

        embedder = Embedder()
        embedder.set_host(a1).set_host_layer(0)
        embedder.embedding([a2,a2,a2],[0,1,2],[(0,0),(100,100),(250,235)],strategy1)

        embedder.set_host_layer(1)
        embedder.embedding([a2,a2,a2,a2,a2],[1,0,2,0,1],[(100,220),(0,100),(800,345),(90,700),(500,900)],strategy2)

        embedder.set_host_layer(2)
        embedder.embedding([a2,a2],[2,2],[(345,500),(0,0)],strategy2)

        with open(host_file, "wb") as host:    
            host.write(a1.get_raw_image())
            
    except Exception as e:
        print(f"Error@Main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    host_file = sys.argv[1]
    src_file = sys.argv[2]
    routine(host_file, src_file)