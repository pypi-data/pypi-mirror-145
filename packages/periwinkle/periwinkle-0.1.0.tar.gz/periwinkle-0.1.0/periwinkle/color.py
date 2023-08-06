#Laksh Patel ©2022


def Hex_to_RGB(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)

def RGB_to_Hex(rgb):
    return '%02x%02x%02x' % rgb