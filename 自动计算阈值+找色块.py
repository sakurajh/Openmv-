import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)

Range = (0, 0, 160, 120)  # 感兴趣区域的坐标范围

for i in range(200):
    img = sensor.snapshot()
    img.draw_rectangle((75, 55, 10, 10), color=(255, 0, 0))
    statistics = img.get_statistics(roi=(75, 55, 10, 10))
    thresholds = [statistics.l_min(),statistics.l_max(),
                  statistics.a_min(),statistics.a_max(),
                  statistics.b_min(), statistics.b_max()]
    print("Thresholds:", thresholds)

while True:
    img = sensor.snapshot()
    blobs = img.find_blobs([((87, 4, 88, 15, 81, 6)))], roi=Range, pixels_threshold=100,are_threshold=100,merge=True,margin=10)

    for blob in blobs:
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        print("Blob center:", blob.cx(), blob.cy())
