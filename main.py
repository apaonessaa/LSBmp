import sys
from analyzer import Analyzer
from embedder import Embedder

def main(target_file, src_file):
    layer=0
    try:
        with open(target_file, "rb+") as target, open(src_file, "rb") as src:
            a1 = Analyzer(target.read())
            a2 = Analyzer(src.read())
            
            target_offset = a1.get_offset()
            target_width, target_height = a1.get_size()

            # print(f"target_offset: {target_offset}, target_size: {(target_width, target_height)}")

            target_Bpp = a1.get_Bpp()
            #src_Bpp = a2.get_Bpp()

            # print(f"target_Bpp: {target_Bpp}, src_Bpp: {src_Bpp}")

            _, target_height = a1.get_size()

            #print(f"target_height: {target_height}")

            target_data = a1.get_bmp()
            src_data = a2.get_bmp()

            #print(f"target_data: {target_data}")
            #print(f"src_data: {len(src_data)}")

            target_rowsize = a1.get_rowsize()

            #print(f"target_rowsize: {target_rowsize}")

            Embedder.apply(target_data, layer, src_data, target_height, target_rowsize, target_Bpp)

            target.seek(target_offset)
            target.write(target_data)
    except Exception as e:
        print(f"Error@Main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    target_file = sys.argv[1]
    src_file = sys.argv[2]
    main(target_file, src_file)
    