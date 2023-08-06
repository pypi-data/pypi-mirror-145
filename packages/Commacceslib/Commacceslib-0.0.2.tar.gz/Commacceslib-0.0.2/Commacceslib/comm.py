import ctypes
import numpy as np
from . import logger

logger = logger.getChild(__name__)


class Bridge:
    """
    The function of this object is to interact with the backend.
    """

    def __init__(self, ip, sync_port, async_port, dll_path):
        # cdll.LoadLibrary
        self.my_dll = None
        self.init_communication(ip, sync_port, async_port, dll_path)

    def init_communication(self, ip, sync_port, async_port, dll_path):
        # const char* str, int sync_port, int async_port
        try:
            self.my_dll = ctypes.CDLL(dll_path)
        except OSError:
            logger.error(f"Impossible to find dll/so with the following path: {dll_path}")
            raise OSError
        error = self.my_dll.InitCommunication(ctypes.c_char_p(f"{ip}".encode("utf-8")), sync_port, async_port, True)
        if error < 0:
            logger.error("Impossible to communicate with server.")
            raise ConnectionError

    def camera_reset(self):
        self.my_dll.CameraReset()

    def controller_reset(self):
        self.my_dll.ControllerReset()

    def close_communication(self):
        self.my_dll.CloseCommunication()

    def chip_register_write(self, in_array, chips_bitmap):
        # const unsigned in[5], int chips_bitmap
        np_in = np.array(in_array, dtype=np.uint32)
        c_p_out = np_in.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))  # This method works with numpy interaction
        error = self.my_dll.ChipRegisterWrite(c_p_out, ctypes.c_uint32(chips_bitmap))

        return error

    def chip_register_read(self, np_out, chips_bitmap):
        # unsigned out[5], int chips_bitmap
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))  # This method works with numpy interaction
        error = self.my_dll.ChipRegisterRead(c_p_out, ctypes.c_uint32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)

        return error, out

    def full_array_chip_register_read(self, np_out, chips_bitmap):
        # unsigned out[150], int chips_bitmap
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))  # This method works with numpy interaction
        error = self.my_dll.FullArrayChipRegisterRead(c_p_out, ctypes.c_uint32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)

        return error, out

    def pixel_register_write(self, np_in, chips_bitmap):
        # const unsigned in[480], int chips_bitmap
        c_p_out = np_in.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))  # This method works with numpy interaction
        error = self.my_dll.PixelRegisterWrite(c_p_out, ctypes.c_uint32(chips_bitmap))

        return error

    def full_array_pixel_register_read(self, np_out, chips_bitmap):
        # unsigned out[14400], int chips_bitmap
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        error = self.my_dll.FullArrayPixelRegisterRead(c_p_out, ctypes.c_int32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)
        return error, out

    def pixel_register_read(self, np_out, chips_bitmap):
        # unsigned out[14400], int chips_bitmap
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        error = self.my_dll.PixelRegisterRead(c_p_out, ctypes.c_int32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)
        return error, out

    def full_array_read_erica_id(self, np_out, chips_bitmap):
        # unsigned id[30], int chips_bitmap
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        error = self.my_dll.FullArrayReadEricaID(c_p_out, ctypes.c_int32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)

        return error, out

    def full_array_read_temperature(self, np_out, chips_bitmap):
        # unsigned *temp[30], int chips_bitmap
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        error = self.my_dll.FullArrayReadReadTemperature(c_p_out, ctypes.c_int32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)

        return error, out

    def full_array_acquisition_tdi(self, np_params, chips_bitmap):
        # const unsigned params[5], unsigned* data, int chips_bitmap
        c_p_params = np_params.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        initp = ctypes.POINTER(ctypes.c_uint32)  # Init pointer type uint32
        data = ctypes.c_uint32(0)  # Creating value instance
        addr = ctypes.addressof(data)  # Saving adress of the value instance
        ptr_data = ctypes.cast(addr, initp)  # Pointer

        error = self.my_dll.FullArrayACQuisitionTDI(c_p_params, ptr_data, ctypes.c_int32(chips_bitmap))

        params_out = np.ctypeslib.as_array(c_p_params, np_params.shape)

        return error, params_out, ptr_data[0]

    def full_array_acquisition_non_tdi(self, np_params, chips_bitmap):
        # const unsigned params[5], unsigned* data, int chips_bitmap
        c_p_params = np_params.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        initp = ctypes.POINTER(ctypes.c_uint32)  # Init pointer type uint32
        data = ctypes.c_uint32(0)  # Creating value instance
        addr = ctypes.addressof(data)  # Saving adress of the value instance
        ptr_data = ctypes.cast(addr, initp)  # Pointer

        error = self.my_dll.FullArrayACQuisitionNonTDI(c_p_params, ptr_data, ctypes.c_int32(chips_bitmap))

        params_out = np.ctypeslib.as_array(c_p_params, np_params.shape)

        return error, params_out, ptr_data[0]

    def acq_cont(self, chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi):
        # unsigned id[30], int chips_bitmap

        class AcqInfo(ctypes.Structure):
            _fields_ = [("pulses_width", ctypes.c_uint32),
                        ("pulses", ctypes.c_uint32),
                        ("timer_reg", ctypes.c_uint16),
                        ("belt_dir", ctypes.c_bool),
                        ("test_pulses", ctypes.c_bool),
                        ("tdi", ctypes.c_bool)]

        acq_info_struct = AcqInfo(pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)

        error = self.my_dll.ACQuisitionCont(acq_info_struct, ctypes.c_int32(chips_bitmap))

        return error

    def acq(self, chips_bitmap, pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi, frames):
        # unsigned id[30], int chips_bitmap

        class AcqInfo(ctypes.Structure):
            _fields_ = [("pulses_width", ctypes.c_uint32),
                        ("pulses", ctypes.c_uint32),
                        ("timer_reg", ctypes.c_uint16),
                        ("belt_dir", ctypes.c_bool),
                        ("test_pulses", ctypes.c_bool),
                        ("tdi", ctypes.c_bool)]

        acq_info_struct = AcqInfo(pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)

        error = self.my_dll.ACQuisition(acq_info_struct, ctypes.c_uint32(frames), ctypes.c_int32(chips_bitmap))

        return error

    def load_flood_norm_factors(self, factor_value_mx, chips_bitmap):
        new_value_mx = to_fixed(factor_value_mx)

        np_out = np.array(new_value_mx, dtype=np.uint16)
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        error = self.my_dll.LoadFloodNormFactors(c_p_out, ctypes.c_int32(chips_bitmap))
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)

        return error, out

    def pop_frame(self, np_out):
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        ret = self.my_dll.PopDataWithTimeout(c_p_out, 600)  # , ctypes.c_int32(chips_bitmap)
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)
        return out, ret

    def stop_acq(self):
        error = self.my_dll.ACQuisitionStop()
        return error

    def get_write_frame(self):
        return self.my_dll.GetWriteIdx()

    def get_read_frame(self):
        return self.my_dll.GetReadIdx()

    def get_element_counter(self):
        return self.my_dll.GetElemCounter()

    def get_all_regs(self):
        return self.my_dll.PrintAllRegs()

    def update_HB(self):
        return self.my_dll.UpdateHB()

    ########################################################################################

    def set_hv(self, counts):
        # unsigned counts
        return self.my_dll.SetHV(ctypes.c_uint32(counts))

    def set_tdac(self, counts):
        # unsigned counts
        return self.my_dll.SetTPDAC(ctypes.c_uint32(counts))

    def reset_buffer(self):
        return self.my_dll.ResetBuffer()

    def full_array_disc_charac_f(self, np_params, np_reg, np_px_reg, size, chips_bitmap):
        # const unsigned params[32], const unsigned reg[20], const unsigned px_reg[14400],
        # long int size, unsigned *counts, int chips_bitmap
        c_p_params = np_params.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_p_reg = np_reg.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_p_px_reg = np_px_reg.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        initp = ctypes.POINTER(ctypes.c_uint32)  # Init pointer type uint32
        counts = ctypes.c_uint32(0)  # Creating value instance
        addr = ctypes.addressof(counts)  # Saving adress of the value instance
        ptr_counts = ctypes.cast(addr, initp)  # Pointer

        error = self.my_dll.FullArrayDiscCharacF(c_p_params, c_p_reg, c_p_px_reg, ctypes.c_int32(size),
                                                 ptr_counts, ctypes.c_int32(chips_bitmap))

        params_out = np.ctypeslib.as_array(c_p_params, np_params.shape)
        reg_out = np.ctypeslib.as_array(c_p_reg, np_reg.shape)
        px_reg_out = np.ctypeslib.as_array(c_p_px_reg, np_px_reg.shape)

        return error, params_out, reg_out, px_reg_out, ptr_counts[0]

    def read_temperature(self, chips_bitmap):
        initp = ctypes.POINTER(ctypes.c_uint32)  # Init pointer type uint32
        num = ctypes.c_uint32(0)  # Creating value instance
        addr = ctypes.addressof(num)  # Saving adress of the value instance
        # It returns a new instance of type which points to the same memory block as obj.type
        ptr = ctypes.cast(addr, initp)  # Pointer

        error = self.my_dll.ReadTemperature(ptr, ctypes.c_int32(chips_bitmap))

        return error, ptr[0]  # ptr.contents.value

    def read_touchdown(self, np_out):
        c_p_out = np_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        error = self.my_dll.ReadTouchdown(c_p_out)
        out = np.ctypeslib.as_array(c_p_out, np_out.shape)

        return error, out


def to_fixed(f_mx, e=12):
    out = []
    for f in f_mx:
        a = f * (2 ** e)
        b = int(round(a))
        if a < 0:
            # next three lines turns b into it's 2's complement.
            b = abs(b)
            b = ~b
            b += 1
            out.append(b)
        else:
            out.append(b)
    return out
