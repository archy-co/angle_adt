'''
AngleADT module
'''
import ctypes

Array = ctypes.py_object

def heximize(message):
    '''
    This function transforms message into array of hex values
    '''
    ArrayType = ctypes.py_object * len(message)
    hex_arr = ArrayType()

    i = 0
    for sym in message:
        hex_arr[i] = hex(ord(sym))[2:]
        i += 1

    return hex_arr

def get_actual_arr_len(message):
    '''
    This function returns actual array length
    '''
    for i in range(len(message)):
        try:
            message[i]
        except ValueError:
            break
    return i

def optimize_array(array):
    '''
    This funciton optimizes array so that it is exactly of the size of number of elements
    '''
    opt_size = get_actual_arr_len(array)
    ArrayType = ctypes.py_object * opt_size
    opt_array = ArrayType()
    for i in range(opt_size):
        opt_array[i] = array[i]

    return list(opt_array)



class AngleADT:
    '''
    Class that helps represent message as sequence of angles
    '''
    def __init__(self, message):
        self.message = message
        self.hex_message = heximize(self.message)

    def encode_message(self):
        '''
        This method encodes message (returns array with relative angles of camera)
        '''
        angle_count = len(self.hex_message)*3 + 1
        ArrayType = ctypes.py_object * angle_count
        angle_arr_abs = ArrayType()
        angle_arr_rel = ArrayType()
        k = 0
        for i in range(len(self.hex_message)):
            for j in range(len(self.hex_message[i])):
                angle_arr_abs[k] = 360/16 * int(self.hex_message[i][j], 16)
                angle_arr_rel[k] = angle_arr_abs[k]
                if k > 0:
                    angle_arr_rel[k] = angle_arr_abs[k] - angle_arr_abs[k-1]
                if angle_arr_rel[k] == 0:
                    angle_arr_rel[k] = 360
                k += 1
        return optimize_array(angle_arr_rel)

if __name__ == '__main__':
    a = AngleADT('hello')
    a_r = [135.0, 45.0, -45.0, -22.5, 22.5, 135.0, -135.0, 135.0, -135.0, 202.5]
    print(a_r == a.encode_message())
