import cv2

# Загрузка двух последовательных изображений
prev_image_path = 'eval-data/Evergreen/frame10.png'
cur_image_path = 'eval-data/Evergreen/frame11.png'
previous_frame = cv2.imread(prev_image_path, 0)
current_frame = cv2.imread(cur_image_path, 0)

# Расчет оптического потока с использованием метода Lucas-Kanade
# Оптический поток будет представлен в виде поля скоростей (u, v)
flow = cv2.calcOpticalFlowFarneback(previous_frame, current_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)

# Визуализация поля скоростей
flow_vis = cv2.cvtColor(previous_frame, cv2.COLOR_GRAY2BGR)
step = 32  # шаг визуализации (расстояние между векторами)
for y in range(0, flow_vis.shape[0], step):
    for x in range(0, flow_vis.shape[1], step):
        fx, fy = flow[y, x]
        cv2.arrowedLine(flow_vis, (x, y), (int(x + fx), int(y + fy)), (0, 255, 0), 1)

# Отображение изображений и визуализации
cv2.imshow('Previous Frame', previous_frame)
cv2.imshow('Current Frame', current_frame)
cv2.imshow('Optical Flow', flow_vis)
cv2.waitKey(0)
cv2.destroyAllWindows()