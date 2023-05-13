import numpy as np
import cv2


def horn_schunck(image1, image2, alpha=1.0, num_iterations=100, epsilon=1e-5):
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

    flow = np.zeros((image1.shape[0], image1.shape[1], 2), dtype=np.float32)
    prev_flow = np.zeros((image1.shape[0], image1.shape[1], 2), dtype=np.float32)

    fx, fy = np.gradient(image1)
    ft = image2 - image1

    for _ in range(num_iterations):
        flow_div = fx * fx + fy * fy + epsilon
        flow = np.zeros((image1.shape[0], image1.shape[1], 2), dtype=np.float32)
        flow[:, :, 0] = prev_flow[:, :, 0] - fx * ((fx * prev_flow[:, :, 0] + fy * prev_flow[:, :, 1] + ft)) / flow_div
        flow[:, :, 1] = prev_flow[:, :, 1] - fy * ((fx * prev_flow[:, :, 0] + fy * prev_flow[:, :, 1] + ft)) / flow_div
        prev_flow = flow
    return flow


def multi_scale_horn_schunck(image1, image2, alpha=1, num_iterations=3, num_scales=3, scale_factor=0.65):
    pyramid1 = [image1]
    pyramid2 = [image2]
    for _ in range(num_scales - 1):
        image1 = cv2.resize(image1, None, fx=scale_factor, fy=scale_factor)
        image2 = cv2.resize(image2, None, fx=scale_factor, fy=scale_factor)
        pyramid1.append(image1)
        pyramid2.append(image2)

    flow_sum = np.zeros((pyramid1[-1].shape[0], pyramid1[-1].shape[1], 2), dtype=np.float32)

    for i in range(num_scales - 1, -1, -1):

        flow = horn_schunck(pyramid1[i], pyramid2[i], alpha, num_iterations)

        if i > 0:
            flow_sum = cv2.resize(flow_sum, (pyramid1[i - 1].shape[1], pyramid1[i - 1].shape[0])) / scale_factor
            flow = cv2.resize(flow, (pyramid1[i - 1].shape[1], pyramid1[i - 1].shape[0])) / scale_factor
        flow_sum = sum_flows(flow_sum, flow)
    return flow_sum


def sum_flows(flow1, flow2):
    assert flow1.shape == flow2.shape, "Flow fields must have the same shape"
    summed_flow = flow1 + flow2
    return summed_flow

image1 = 'eval-data/Evergreen/frame10.png'
image1 = cv2.imread(image1)
image2 = 'eval-data/Evergreen/frame11.png'
image2 = cv2.imread(image2)

flow = multi_scale_horn_schunck(image1, image2, alpha=1.0, num_iterations=100, num_scales=2, scale_factor=0.65)


# Визуализация поля скоростей
image_final = 'eval-data/Evergreen/frame10.png'
image_final = cv2.imread(image_final, 0)

flow_vis = cv2.cvtColor(image_final, cv2.COLOR_GRAY2BGR)
step = 16  # шаг визуализации (расстояние между векторами)
for y in range(0, flow_vis.shape[0], step):
    for x in range(0, flow_vis.shape[1], step):
        fx, fy = flow[y, x]
        cv2.arrowedLine(flow_vis, (x, y), (int(x + fx), int(y + fy)), (0, 255, 0), 1)

cv2.imshow('Optical Flow', flow_vis)
cv2.waitKey(0)
cv2.destroyAllWindows()
