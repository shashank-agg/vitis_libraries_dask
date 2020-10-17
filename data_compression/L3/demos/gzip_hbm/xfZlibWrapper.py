from ctypes import *
import time
import os

class xfZlibWrapper:
    
    def __init__(self, xclbin_path):
        print("####", xclbin_path)
        self.lib = cdll.LoadLibrary('build/libz.so')
        xfZlib_constructor_wrapper = self.lib.xfZlib_constructor_wrapper
        xfZlib_constructor_wrapper.argtypes = [c_char_p, c_uint8, c_uint8, c_uint8, c_uint8, c_uint8]
        xfZlib_constructor_wrapper.restype = c_void_p

        self.xfZlibObject =  xfZlib_constructor_wrapper(
            c_char_p(xclbin_path),  #binaryFileName
            c_uint8(10),   #max_cr
            c_uint8(0),   #cd_flow
            c_uint8(0),   #device_id
            c_uint8(0),   #profile
            c_uint8(2)   #d_type
        )       

    def compress_file(self, inFilePath, outFilePath):
        print("$$$$$", inFilePath, outFilePath)
        inFilePath = inFilePath.encode('utf-8')
        outFilePath = outFilePath.encode('utf-8')
        compress_file_wrapper = self.lib.compress_file_wrapper
        compress_file_wrapper.argtypes = [c_void_p, c_char_p, c_char_p, c_uint64]
        return compress_file_wrapper(
            self.xfZlibObject, 
            inFilePath,
            outFilePath,
            os.path.getsize(inFilePath))
        # return 10
    
    def decompress_file(self, inFilePath, outFilePath):
        decompress_file_wrapper = self.lib.decompress_file_wrapper
        decompress_file_wrapper.argtypes = [c_void_p, c_char_p, c_char_p, c_uint64, c_int]
        return decompress_file_wrapper(
            self.xfZlibObject, 
            inFilePath,
            outFilePath,
            os.path.getsize(inFilePath),
            c_int(0))

# if __name__ == '__main__':
#     XCLBIN_PATH = b'build/xclbin_xilinx_u200_xdma_201830_2_sw_emu/compress_decompress.xclbin'
#     IN_FILE_PATH = b'Makefile'
#     OUT_FILE_PATH = b'sample.gz'
    
#     xfZlib = xfZlibWrapper(XCLBIN_PATH)

#     size = xfZlib.compress_file(IN_FILE_PATH, OUT_FILE_PATH)
#     print(f'Compressed from {os.path.getsize(IN_FILE_PATH)} to {size} bytes')

    # size = xfZlib.decompress_file(b"hello.txt.gz", b"decompressed")
    # print(f'Decompressed from {os.path.getsize("hello.txt.gz")} to {size} bytes')

