import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

uart = pyb.UART(3, 9600)  # 初始化 UART3，波特率为 9600

while(True):
    clock.tick()
    img = sensor.snapshot()

    for r in img.find_rects(threshold = 10000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners():
            img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
    
        # 发送矩形角点坐标，格式为 "@x0,y0;x1,y1;x2,y2;x3,y3\r\n"
        corners = r.corners()
        uart.write("@%d,%d;%d,%d;%d,%d;%d,%d\r\n" % (corners[0][0], corners[0][1], corners[1][0], corners[1][1], corners[2][0], corners[2][1], corners[3][0], corners[3][1]))
    
    print("FPS %f" % clock.fps())