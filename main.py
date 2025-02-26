#!/usr/bin/python3
import sys
from analyzer import Analyzer
from embedder import Embedder

def main(target_file, src_file):
    try:
        with open(target_file, "rb+") as target, open(src_file, "rb") as src:
            a1 = Analyzer(target.read())
            a2 = Analyzer(src.read())
            embedder = Embedder(a1)
            embedder.set_accuracy(35)
            embedder.apply(a2)
            target.seek(a1.get_offset())
            target.write(a1.get_payload())
    except Exception as e:
        print(f"Error@Main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    target_file = sys.argv[1]
    src_file = sys.argv[2]
    main(target_file, src_file)