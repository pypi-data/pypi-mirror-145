"""
    **This submodule is the bridge between top layer manager and communication functionalities.**
"""
import numpy as np
from Commacceslib.comm import Bridge
from Commacceslib.data_convert.chip_bitmap_pos import convert
from Commacceslib.data_convert.data_swap import pack_data_swap
from . import logger

logger = logger.getChild(__name__)


class UseBridge(Bridge):

    def __init__(self, ip, sync_port, async_port, dll_path):
        super().__init__(ip, sync_port, async_port, dll_path)

    def use_reset(self):
        self.camera_reset()
        self.controller_reset()
        return 0

    def use_close_communication(self):
        self.close_communication()
        return 0

    # Chip register functions
    def use_full_array_chip_register_write(self, in_array, bitmap):
        ATTEMPS = 5
        counter_error = 0

        empty_in_array = np.zeros((5,), dtype=np.uint32)

        cr_incr = 5
        chips_bitmap_list, array_subset_pos = convert(bitmap, cr_incr)

        i = 0
        for chips_bitmap in chips_bitmap_list:
            counter_error = 0
            for attemp in range(ATTEMPS):
                data_in = in_array[array_subset_pos[i]:array_subset_pos[i] + cr_incr]
                self.chip_register_write(data_in, chips_bitmap)

                error, read_data = self.chip_register_read(empty_in_array, chips_bitmap)

                if np.all(read_data == data_in) or error > 0:
                    break
                else:
                    logger.error("Error in programing chip_bitmap`: {}".format(chips_bitmap))
                    counter_error += 1
            i += 1
        if counter_error >= 4:
            return -1
        else:
            return 0

    def use_full_array_chip_register_write_all(self, in_array, chips_bitmap):
        array_subset_pos = 0  # Program to all chips the chip 0 configuration
        error = self.chip_register_write(in_array[array_subset_pos:array_subset_pos + 5], chips_bitmap)
        if error != 0:
            return error
        return 0

    def use_chip_register_write(self, in_array, chip_bitmap):
        error = self.chip_register_write(in_array, chip_bitmap)
        if error != 0:
            return error
        return 0

    def use_full_array_chip_register_read(self, chips_bitmap):
        empty_in_array = np.zeros((150,), dtype=np.uint32)
        error, out_array = self.full_array_chip_register_read(empty_in_array, chips_bitmap)
        return error, out_array

    def use_chip_register_read(self, chips_bitmap):
        empty_in_array = np.zeros((5,), dtype=np.uint32)
        error, out_array = self.chip_register_read(empty_in_array, chips_bitmap)
        return error, out_array

    # Pixel register functions

    def use_full_array_pixel_register_read(self, chips_bitmap):
        empty_in_array = np.zeros((14400,), dtype=np.uint32)
        error, out_array = self.full_array_pixel_register_read(empty_in_array, chips_bitmap)
        return error, out_array

    def use_full_array_pixel_register_write(self, in_array, bitmap):
        ATTEMPS = 5
        counter_error = 0

        empty_in_array = np.zeros((480,), dtype=np.uint32)

        px_incr = 480
        chips_bitmap_list, array_subset_pos = convert(bitmap, px_incr)

        i = 0
        for chips_bitmap in chips_bitmap_list:
            counter_error = 0
            for attemp in range(ATTEMPS):
                data_in = in_array[array_subset_pos[i]:array_subset_pos[i] + px_incr]
                self.pixel_register_write(data_in, chips_bitmap)
                error, read_data = self.pixel_register_read(empty_in_array, chips_bitmap)
                read_data = pack_data_swap(read_data)

                if np.all(read_data == data_in) or error > 0:
                    break
                else:
                    logger.error("Error in programing pixel_register: {}".format(chips_bitmap))
                    counter_error += 1
            i += 1

        if counter_error >= 4:
            return -1
        else:
            return 0

    def use_full_array_pixel_register_write_all(self, in_array, chips_bitmap):
        array_subset_pos = 0
        error = self.pixel_register_write(in_array[array_subset_pos:array_subset_pos + 480], chips_bitmap)
        if error != 0:
            return error
        return 0

    def use_pixel_register_write(self, in_array, chip_bitmap):
        error = self.pixel_register_write(in_array, chip_bitmap)
        if error != 0:
            return error
        return 0

    # ID functions

    def use_full_array_read_erica_id(self, chips_bitmap):
        empty_in_array = np.zeros((30,), dtype=np.uint32)
        error, out_array = self.full_array_read_erica_id(empty_in_array, chips_bitmap)
        return error, out_array

    # Temperature functions

    def use_full_array_read_temperature(self, chips_bitmap):
        empty_in_array = np.zeros((30,), dtype=np.uint32)
        error, temp_value = self.full_array_read_temperature(empty_in_array, chips_bitmap)
        return error, temp_value

    # ACQ functions

    def use_acq_cont(self, pulses_width, pulses, timer_reg, belt_dir, test_pulses, chips_bitmap):
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32
        tdi = False
        error = self.acq_cont(chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)
        return error

    def use_acq_cont_tdi(self, pulses_width, pulses, timer_reg, belt_dir, test_pulses, chips_bitmap):
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32
        tdi = True
        error = self.acq_cont(chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)
        return error

    def use_acq(self, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, chips_bitmap):
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32 * 30 = 14400
        tdi = False
        error = self.acq(chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi, frames)
        return error

    def use_acq_tdi(self, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, chips_bitmap):
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32 * 30 = 14400
        tdi = True
        error = self.acq(chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi, (frames * 8))
        return error

    def use_load_flood_norm_factors(self, factor_value_mx, chip_bitmap_array):
        error_array = []
        acq_out_array = []
        i = 0
        for chip_bitmap in chip_bitmap_array:
            factor_value_array = factor_value_mx[i]
            error, acq_out = self.load_flood_norm_factors(factor_value_array, chip_bitmap)
            error_array.append(error)
            acq_out_array.append(acq_out)

        return error_array, acq_out_array

    def use_pop_frame(self):
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32 * 30 = 14400
        empty_in_array = np.full((14400,), 0xff, dtype=np.uint32)
        acq_out, ret = self.pop_frame(empty_in_array)
        if ret < 0:
            return True, np.full(14400, 0xfe, dtype=np.uint32)
        return False, acq_out

    def use_read_touchdown(self):
        empty_in_array = np.zeros((1,), dtype=np.uint32)
        error, out_array = self.read_touchdown(empty_in_array)
        return error, out_array[0]

    def use_stop_acq(self):
        error = self.stop_acq()
        return error

    def use_get_write_frame(self):
        return self.get_write_frame()

    def use_get_read_frame(self):
        return self.get_read_frame()

    def use_get_element_counter(self):
        return self.get_element_counter()

    # Set hardware values
    def use_set_hv(self, hv_value):
        hv_counts = int((hv_value / 2.5) * 65535)
        return self.set_hv(hv_counts)

    def use_set_tdac(self, tdac_value):
        tdac_counts = int((tdac_value / 2.5) * 65535)
        return self.set_tdac(tdac_counts)

    def use_get_all_regs(self):
        return self.get_all_regs()

    def use_controller_reset(self):
        return self.controller_reset()

    def use_reset_buffer(self):
        return self.reset_buffer()

    def use_update_HB(self):
        return self.update_HB()
