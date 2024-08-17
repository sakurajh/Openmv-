import sensor, image, time, math, pyb
from pyb import UART, LED
import json
import ustruct  # Import the ustruct module for packing/unpacking data

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # Must be turned off for color tracking
sensor.set_auto_whitebal(False)  # Must be turned off for color tracking

red_threshold_01 = (67, 9, 115, 6, 81, -1)
#red_threshold_01 = (10, 100, 127, 32, -43, 67)
clock = time.clock()

uart = UART(3, 115200)  # Define UART3 with 115200 baud rate
uart.init(115200, bits=8, parity=None, stop=1)  # Initialize UART with given parameters

def find_max(blobs):
    """Find the largest blob from the list of blobs."""
    max_blob = None
    max_size = 0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob = blob
            max_size = blob.pixels()
    return max_blob

def sending_data(cx, cy, cw, ch):
    """Send the data via UART."""
    data = ustruct.pack("<bbhhhhb",
                        0x2C,
                        0x12,
                        int(cx),
                        int(cy),
                        int(cw),
                        int(ch),
                        0x5B)
    uart.write(data)

while True:
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([red_threshold_01])

    if blobs:
        max_b = find_max(blobs)
        if max_b:
            cx = max_b.cx()
            cy = max_b.cy()
            cw = max_b.w()
            ch = max_b.h()

            img.draw_rectangle(max_b.rect())
            img.draw_cross(cx, cy)

            sending_data(cx, cy, cw, ch)
            print(cx, cy, cw, ch)



