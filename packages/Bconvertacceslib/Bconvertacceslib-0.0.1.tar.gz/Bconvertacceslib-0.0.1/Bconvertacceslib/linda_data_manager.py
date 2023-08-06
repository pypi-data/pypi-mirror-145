"""
    This submodule inheritance DataPacker, DataUnpacker and specialize for LINDA
"""
import numpy as np
from Bconvertacceslib.data_manager import DataPacker, DataUnpacker


class LindaDataPacker(DataPacker):
    """
    This object is a specialization of DataPacker designed to work with LINDA.
    """

    def pixelreg_to_pack_data_array_tdi(self, data_matrix_in, bit_len_config_in, bit_len_packs_in):
        """
        Use DataPacker.array_to_pack_data and DataPacker.split_pack_data to convert the pixel_register matrix to dll format.
        :param data_matrix_in: (matrix) Pixel register matrix, usual shape = (30, 8, 20, 44)
        :param bit_len_config_in: (array) Pixel register bit len configuration, usual shape = (44,)
        :param bit_len_packs_in: (int) The pack bits value, usual 32 bits.
        :return: (array) Data packed used in dll.
        """
        mx_pack_data_out = []

        for chip_pos in range(len(data_matrix_in)):
            for rows_pos in range(len(data_matrix_in[0])):
                for column_pos in range(len(data_matrix_in[0][0])):
                    decimal_packdata_out, bit_len_data_out = self.array_to_pack_data(data_matrix_in[chip_pos]
                                                                                     [rows_pos]
                                                                                     [column_pos], bit_len_config_in)
                    mx_pack_data_out.append(self.split_pack_data(decimal_packdata_out,
                                                                 bit_len_data_out, bit_len_packs_in))

        return mx_pack_data_out

    def chipreg_to_pack_data_array_tdi(self, data_matrix_in, bit_len_config_in, bit_len_packs_in):
        """
        Use DataPacker.array_to_pack_data and DataPacker.split_pack_data to convert the chip_register matrix to dll format.
        :param data_matrix_in: (matrix) Chip register matrix, usual shape = (19,)
        :param bit_len_config_in: (array) Chip register bit len configuration, usual shape = (19,)
        :param bit_len_packs_in: (int) The pack bits value, usual 32 bits.
        :return: (array) Data packed used in dll.
        """
        mx_pack_data_out = []
        for chip_pos in range(len(data_matrix_in)):
            # We flip the uint32 pack beacuse the info is inverted.
            decimal_packdata_out, bit_len_data_out = self.array_to_pack_data(data_matrix_in[chip_pos],
                                                                             bit_len_config_in)

            mx_pack_data_out.append(np.flip(self.split_pack_data(decimal_packdata_out, bit_len_data_out,
                                                                 bit_len_packs_in)))

        return mx_pack_data_out


class LindaDataUnpacker(DataUnpacker):
    """
    This object is a specialization of DataUnpacker designed to work with LINDA.
    """

    def pack_data_array_tdi_to_pixelreg(self, dll_packed_data_array, mx_data_container_in,
                                        bit_len_packs_in, bit_len_config_in):
        """
        Use DataUnpacker.merge_pack_data and DataUnpacker.pack_data_to_array to convert the dll format to pixel_register matrix.
        :param dll_packed_data_array: (array) Data packed data read from dll
        :param mx_data_container_in: (matrix) Empty matrix where the data will be save.
        :param bit_len_config_in: (array) Pixel register bit len configuration, usual shape = (19,)
        :param bit_len_packs_in: (int) The pack bits value, usual 32 bits.
        :return: (array) mx_data_container_in
        """

        packs_len = int(np.ceil(np.sum(bit_len_config_in) / bit_len_packs_in))
        packs_pos = packs_len
        pos = 0
        for chip_pos in range(len(mx_data_container_in)):
            for rows_pos in range(len(mx_data_container_in[0])):
                for column_pos in range(len(mx_data_container_in[0][0])):
                    decimal_data, bit_len_sum = self.merge_pack_data(dll_packed_data_array[pos:packs_pos],
                                                                     bit_len_packs_in)
                    pos += packs_len
                    packs_pos += packs_len
                    mx_data_container_in[chip_pos][rows_pos][column_pos] = self.pack_data_to_array(decimal_data,
                                                                                                   bit_len_config_in)

        return mx_data_container_in

    def pack_data_array_tdi_to_chipreg(self, dll_packed_data_array, mx_data_container_in,
                                       bit_len_packs_in, bit_len_config_in):
        """
        Use DataUnpacker.merge_pack_data and DataUnpacker.pack_data_to_array to convert the dll format to chip_register matrix.
        :param dll_packed_data_array: (array) Data packed data read from dll
        :param mx_data_container_in: (matrix) Empty matrix where the data will be save.
        :param bit_len_config_in: (array) Chip register bit len configuration, usual shape = (19,)
        :param bit_len_packs_in: (int) The pack bits value, usual 32 bits.
        :return: (array) mx_data_container_in
        """

        packs_len = int(np.ceil(np.sum(bit_len_config_in) / bit_len_packs_in))
        packs_pos = packs_len
        pos = 0
        for chip_pos in range(len(mx_data_container_in)):
            # We flip the uint32 pack beacuse the info is inverted.
            decimal_data, bit_len_sum = self.merge_pack_data(np.flip(dll_packed_data_array[pos:packs_pos])
                                                             , bit_len_packs_in)
            pos += packs_len
            packs_pos += packs_len
            mx_data_container_in[chip_pos] = self.pack_data_to_array(decimal_data, bit_len_config_in)

        return mx_data_container_in

    def pack_data_array_to_acq(self, dll_packed_data_array, mx_data_container_in,
                               bit_len_packs_in, bit_len_config_in):
        """
        Use DataUnpacker.merge_pack_data and DataUnpacker.pack_data_to_array to convert the dll format to acq.
        :param dll_packed_data_array: (array) Data packed data read from dll
        :param mx_data_container_in: (matrix) Empty matrix where the data will be save.
        :param bit_len_config_in: (array) ACQ  bit len configuration, usual shape = (30, 8, 8, 20)
        :param bit_len_packs_in: (int) The pack bits value, usual 32 bits.
        :return: (array) mx_data_container_in
        """

        # packs_len = int(np.ceil(np.sum(bit_len_config_in) / bit_len_packs_in))
        pos = 0

        for chip_pos in range(len(mx_data_container_in)):
            for pix in range(len(mx_data_container_in[0])):
                decimal_data, bit_len_sum = self.merge_pack_data(dll_packed_data_array[pos:pos + 3],
                                                                 bit_len_packs_in)
                pos += 3
                pix_dac_data = self.pack_data_to_array(decimal_data, bit_len_config_in)
                mx_data_container_in[chip_pos][pix] = np.array(pix_dac_data, dtype=np.uint32)

        return mx_data_container_in


