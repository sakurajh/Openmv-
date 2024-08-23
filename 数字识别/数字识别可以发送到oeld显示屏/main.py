import sensor, image, time, os, tf, pyb

sensor.reset()                         # 重置并初始化传感器
sensor.set_pixformat(sensor.GRAYSCALE) # 设置像素格式为 GRAYSCALE
sensor.set_framesize(sensor.QVGA)      # 设置帧大小为 QVGA (320x240)
sensor.set_windowing((240, 240))       # 设置 240x240 窗口
sensor.skip_frames(time=2000)          # 让相机调整

uart = pyb.UART(3, 9600)               # 初始化 UART3，波特率为 9600

clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot().binary([(0,64)])
    for obj in tf.classify("trained.tflite", img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
        output = obj.output()
        number = output.index(max(output))
        uart.write("@%d\r\n" % number)    # 发送识别到的数字，格式为 "@number\r\n"
    uart.write("%f fps\n" % clock.fps())  # 可选：发送 FPS 信息通过 UART