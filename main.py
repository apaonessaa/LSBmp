#!/usr/bin/python3
import sys
from analyzer import Analyzer
from embedder import Embedder

def routine(target_file, out_file, src_file):
    embedder = Embedder(None)
    try:
        with open(src_file, "rb") as src, \
                open(target_file, "rb") as target:
            a1 = Analyzer(target.read())
            a2 = Analyzer(src.read())

        embedder.set_target(a1)
        embedder.set_accuracy(35)

        print()
        print("===================================")
        print("Target")
        print("-----------------------------------")
        print(f"Image width, height: {a1.get_size()}")
        print(f"Pixel array size: {a1.get_payload_size()}")
        print(f"Row size: {a1.get_rowsize_Bpp()}")
        print(f"Padding: {a1.get_padding()}")
        print(f"Bpp: {a1.get_Bpp()}")
        print("===================================")
        print()
        print("===================================")
        print("Src")
        print("-----------------------------------")
        print(f"Image width, height: {a2.get_size()}")
        print(f"Pixel array size: {a2.get_payload_size()}")
        print(f"Row size: {a2.get_rowsize_Bpp()}")
        print(f"Padding: {a2.get_padding()}")
        print(f"Bpp: {a2.get_Bpp()}")
        print("===================================")
        print()

        embedder.set_target_layer(0)
        embedder.embedding([a2])
        embedder.set_target_layer(1)
        embedder.embedding([a2])
        embedder.set_target_layer(2)
        embedder.embedding([a2])

        with open(out_file, "wb") as out: 
            out.write(a1.get_raw_image())

    except Exception as e:
        print(f"Error@Main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    target_file = sys.argv[1]
    out_file = sys.argv[2]
    src_file = sys.argv[3]
    routine(target_file, out_file, src_file)