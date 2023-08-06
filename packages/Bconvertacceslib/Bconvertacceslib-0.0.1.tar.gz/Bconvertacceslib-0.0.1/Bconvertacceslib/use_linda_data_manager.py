"""
    This submodule is the bridge between top layer manager and bit converter functionalities.
"""
import numpy as np
from Bconvertacceslib.linda_data_manager import LindaDataUnpacker, LindaDataPacker
from Bconvertacceslib.data_manager import simple_data_unpack

linda_data_packer = LindaDataPacker()
linda_data_unpacker = LindaDataUnpacker()

bit_len_config_chipreg = [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 6, 1, 1, 4, 4, 14, 14, 1, 1]
bit_len_packs_chipreg = 32  # bits
bit_len_config_pixelreg = [1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4,
                           1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4,
                           1, 1, 1, 1, 1, 4,
                           2, 2, 2, 1, 1, 1]

bit_len_packs_pixelreg = 32  # bits
bit_len_packs_acq = 32
bit_len_config_acq = [16, 16, 16, 16, 16, 16]


# Chip register functions
def use_pack_chip_reg_to_data(in_array):
    mx_data_container = np.zeros((30, 19), dtype=np.uint32)
    mx_data_out = linda_data_unpacker.pack_data_array_tdi_to_chipreg(in_array, mx_data_container,
                                                                     bit_len_packs_chipreg,
                                                                     bit_len_config_chipreg)
    # Expanding dimension for work with LabView.
    expaded_data = np.expand_dims(mx_data_out, axis=0)
    return expaded_data


def use_chip_reg_to_pack_data(in_array):
    trans_chip_reg = np.array(np.squeeze(in_array, axis=0).transpose(), dtype=np.uint32)

    mx_pack_data_out = linda_data_packer.chipreg_to_pack_data_array_tdi(trans_chip_reg, bit_len_config_chipreg,
                                                                        bit_len_packs_chipreg)
    return np.array(mx_pack_data_out, dtype=np.uint32).reshape(-1)  # Converting to dimension array to one dimension


# Pixel register functions
def use_pack_pixel_reg_to_data(in_array):
    mx_data_container = np.zeros((30, 8, 20, 44), dtype=np.uint32)
    mx_data_out = linda_data_unpacker.pack_data_array_tdi_to_pixelreg(in_array, mx_data_container,
                                                                      bit_len_packs_pixelreg,
                                                                      bit_len_config_pixelreg)

    flip_data_out = np.flip(mx_data_out, 2)
    return np.array(flip_data_out, dtype=np.uint32)


def use_pixel_reg_to_pack_data(in_array):
    trans_pixel_reg = np.array(in_array, dtype=np.uint32).transpose((1, 2, 3, 0))
    # flip_pixel_reg = np.flip(trans_pixel_reg, 2)
    mx_pack_data_out = linda_data_packer.pixelreg_to_pack_data_array_tdi(trans_pixel_reg, bit_len_config_pixelreg,
                                                                         bit_len_packs_pixelreg)
    return np.array(mx_pack_data_out, dtype=np.uint32).reshape(-1)  # Converting to dimension array to one dimension


# ACQ
def use_pack_acq_to_data(in_array, tuple_transpose, tuple_reshape):
    out = np.array(simple_data_unpack(in_array, (30, 8, 20, 6)), dtype=np.uint32)
    tr_mx = np.flip(np.transpose(out, (3, 0, 1, 2)), 3)  # 6,30,8,20
    out_mx = enlarge_mx(tr_mx, tuple_transpose, tuple_reshape)

    return out_mx


def use_pack_acq_to_data_tdi(in_array, tuple_transpose, tuple_reshape):
    out = np.array(simple_data_unpack(in_array, (8, 30, 20, 6)), dtype=np.uint32)
    flip_arr = np.flip(out, 2)
    out_mx = enlarge_mx(flip_arr, tuple_transpose, tuple_reshape)

    return out_mx


# Usefully_functions
def enlarge_mx(matrix, tuple_transpose, tuple_reshape):
    tr = matrix.transpose(tuple_transpose).reshape(tuple_reshape)
    container = np.zeros(tuple_reshape, dtype=np.uint32)
    out = np.where(container >= 0, tr, container)
    return out
