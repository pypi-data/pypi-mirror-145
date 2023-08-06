"""
    This submodule  contain the DataPacke and DataUnpacker class and bits_to_max_decimal function used in both class.
"""
import numpy as np
from struct import unpack


def bits_to_max_decimal(bits_in):
    """
    This function convert bit lenght integer to the correspond max decimal number.
    :param bits_in: (int) Bit length.
    :return: (int) Returns the maximum decimal number for a bit length.
    """
    str_array_out = []
    for i in range(bits_in):
        str_array_out.append("1")

    join_str_out = "".join(str_array_out)
    max_decimla = int(join_str_out, 2)
    return max_decimla


class DataPacker:
    """
    The function of this object is to pass python data to C format data.
    """

    def array_to_pack_data(self, data_array_in, bitlen_array_in):
        """
        This method converts a 1D data array to a representive packed decimal number.
        :param data_array_in: (list) n lenght 1d array of data.
        :param bitlen_array_in: (list) same lenght array as 'data_array_in', represent the bit len distribution for each position.
        :return: (int) Decimal packed data.
        """
        data_out = 0
        sum_bit_len = 0

        if len(data_array_in) == len(bitlen_array_in):
            for pos in range(len(data_array_in)):
                if pos == 0:
                    data_out = (int(data_array_in[pos] & bits_to_max_decimal(bitlen_array_in[pos])) << 0)

                else:
                    sum_bit_len += bitlen_array_in[pos - 1]
                    data_out |= int(data_array_in[pos] & bits_to_max_decimal(bitlen_array_in[pos])) << sum_bit_len

            sum_bit_len += bitlen_array_in[-1]
            return data_out, sum_bit_len

        else:
            print("Data array and bit len array must have the same length")
            return 1, 1

    def split_pack_data(self, decimal_packed_data, bit_len_data, split_len):
        """
        Split packed data to separet bit len packed data.
        :param decimal_packed_data: (int) Decimal packed data.
        :param bit_len_data: (int) How many bits does 'decimal_packed_data' occupy.
        :param split_len: (int) Bit size of packets.
        return: (list) Packed splited data array.
        """
        sum_bit_len = 0
        pack_array_out = []
        packs = int(np.ceil(bit_len_data / split_len))  # Round up float value
        max_decimal = bits_to_max_decimal(split_len)

        for pack in range(packs):
            pack_array_out.append((decimal_packed_data >> sum_bit_len) & max_decimal)
            sum_bit_len += split_len

        return pack_array_out


class DataUnpacker:
    """
    The function of this object is to convert C  data fromat to python fromat.
    """

    def __init__(self):
        pass

    def pack_data_to_array(self, decimal_packdata, bitlen_array_in):
        """
        This method converts packed decimal number to a data array.
        :param decimal_packdata: (int) Decimal packed data in.
        :param bitlen_array_in: (list) Bit length distribution for the array out.
        :return: (list) Data array out.
        """
        array_data_out = []
        sum_bit_len = 0

        for bit_length in bitlen_array_in:
            array_data_out.append((decimal_packdata >> sum_bit_len) & bits_to_max_decimal(bit_length))
            sum_bit_len += bit_length

        return array_data_out

    def merge_pack_data(self, pack_array_in, bits_data_packs):
        """
        Merge separet bit len packed data to single packed data.
        :param pack_array_in: (list) Packed data array in.
        :param bits_data_packs: (int) Bit size to unpack.
        :return: (int) Single decimal data value out
        """
        data_out = 0
        sum_bit_len = 0
        for pos in range(len(pack_array_in)):
            if pos == 0:
                data_out = (int(pack_array_in[pos] & bits_to_max_decimal(bits_data_packs)) << 0)

            else:
                sum_bit_len += bits_data_packs
                data_out |= int(pack_array_in[pos] & bits_to_max_decimal(bits_data_packs)) << sum_bit_len

        sum_bit_len += bits_data_packs

        return data_out, sum_bit_len


def simple_data_unpack(list_in, reshape_format):
    unpack_data = unpack("H" * ((len(list_in)) * 2), list_in)
    try:
        data_reshape = np.reshape(unpack_data, reshape_format)
        return data_reshape
    except ValueError:
        return None
