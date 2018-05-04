import os
import sys

KEY = 0xA3

def decode(src_path, dest_path):
    try:
        fin = open(src_path, "rb")
    except IOError as e:
        print(str(e))
        return
    try:
        fout = open(dest_path, "wb")
    except IOError as e:
        print(str(e))
        return

    song_encode = fin.read()
    song_decode = bytearray()
    for i, byte in enumerate(song_encode):
        sys.stdout.write("\r处理进度: %d%%" % (round((i + 1) * 100 / len(song_encode))))
        sys.stdout.flush()
        if type(byte) == str: #python 2
            song_decode.append(int(byte.encode("hex"), 16) ^ KEY)
        else:                 #python 3
            song_decode.append(byte ^ KEY)
    
    print()
    fout.write(song_decode)
    fin.close()
    fout.close()

def main():
    if len(sys.argv) !=2:
       print("使用 python uc!decoder.py [source]")
    else:
        last = sys.argv[1].rfind(os.path.sep)
        src_path = sys.argv[1][:last + 1]
        dest_path = sys.argv[1][:last + sys.argv[1][last:].find(".")] + ".mp3"
        print("Source path: %s\nDestination path: %s" % (sys.argv[1], dest_path))
        decode(sys.argv[1], dest_path)
        print("如果缓存为无损歌曲，请将后缀名由mp3改为flac")

if __name__ == '__main__':
    main()
    