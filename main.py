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
        embedder.apply(a2)

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