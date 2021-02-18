#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

class RLEPair:
    """This is a templated class, so you can use
    any type of data you want with the RLE
    compressor and decompressor."""
    def __init__(self, m_data, m_length):
        self.m_data = m_data
        self.m_length = m_length

class RLE:
    """The constructor just initializes
    the RLE array and
    clears the other variables."""
    def __init__(self):
        self.m_RLE = []
        self.m_runs = 0
        self.m_size = 0

    def CreateRLE(self, p_array):
        currentrun = 0
        self.m_RLE.append(RLEPair(p_array[0], chr(1)))
        self.m_size = len(p_array) # the size of the uncompressed array is recorded to make decompression easier later on
        for index in range(1, self.m_size): # loops through each item in the uncompressed array.
            if p_array[index] != self.m_RLE[currentrun].m_data:
                currentrun+=1
                if self.m_size == currentrun:
                    self.m_size = currentrun * 2
                self.m_RLE.append(RLEPair(p_array[index], chr(1)))
            else:
                if self.m_RLE[currentrun].m_length == 255:
                    currentrun+=1
                    if self.m_size == currentrun:
                        self.m_size = currentrun * 2
                    self.m_RLE.append(RLEPair(p_array[index], 1))
                else:
                    self.m_RLE[currentrun].m_length = chr(ord(self.m_RLE[currentrun].m_length) + 1)
        self.m_runs = currentrun + 1


    def FillArray(self, p_array):
        for currentrun in range(0, self.m_runs):
            for index in range(0, ord(self.m_RLE[currentrun].m_length)):
                p_array.append(self.m_RLE[currentrun].m_data)


    def SaveData(self, p_name):
        file = open(p_name, "wb")
        file.write(struct.pack('i', self.m_size))
        file.write(struct.pack('i', self.m_runs))
        for elem in self.m_RLE:
            file.write(elem.m_length.encode())
            file.write(elem.m_data.encode())
        file.close()

    def LoadData(self, p_name):
        file = open(p_name, "rb")
        self.m_size = int(struct.unpack('i', file.read(struct.calcsize('i')))[0])
        self.m_runs = int(struct.unpack('i', file.read(struct.calcsize('i')))[0])
        length = file.read(1)
        while length:
            data = file.read(1)
            self.m_RLE.append(RLEPair(data, length))
            length = file.read(1)
        file.close()


# EXAMPLE 21-1 :
# loads a file, compresses it, writes it out to disk,
# uncompresses the file into a new array, and compares 
# the contents with the original array.

def example211():
    uncompressed = []
    compressed = RLE()
    filename = input("Enter file name: ")
    original = open(filename, "r").read()
    compressed.CreateRLE(original)
    new_filename = filename + '.rle'
    compressed.SaveData(new_filename) # the data is saved to disk using file name + .rle
    print("Original File Size: %d" % compressed.m_size)
    print("Compressed File Size: %d" % (compressed.m_runs*2))
    print("Compression Ratio: %d" % (compressed.m_size/(compressed.m_runs*2)))
    compressed.FillArray(uncompressed)
    print("Checking Array Integrity...")
    for index in range(0, compressed.m_size):
        if original[index] != uncompressed[index]:
            exit("ERROR, DECOMPRESSION UNSUCCESSFUL!!")
    print("Arrays match!")


# EXAMPLE 21-2 :
# loads in a compressed RLE, decompresses it into an array,
# and then saves the uncompressed data into a new file.
# Basically, you’re supposed to use Example 21-1 to compress data and then use this
# example to decompress data back into its original form.

def example212():
    uncompressed = []
    compressed = RLE()
    dataname = input("Enter data file name: ")
    compressed.LoadData(dataname)
    compressed.FillArray(uncompressed)
    new_dataname = dataname[:-4]
    f = open(new_dataname, "w")
    f.write("".join(x.decode() for x in uncompressed))
    print("Decompressed to %s" % new_dataname)


example211() # to compress
#example212() # to decompress
