import paddle
import paddle.nn.functional as F
import numpy as np

#paddle.device.set_device("cpu")
data = paddle.rand(shape=[1,1,6,6])
pool_out, indices = F.max_pool2d(data, kernel_size=2, stride=2, padding=0, return_mask=True)
print("indices:", indices)
print(data)
Unpool2D = paddle.nn.MaxUnPool2D(kernel_size=2, padding=0)
unpool_out = Unpool2D(pool_out, indices)
print(unpool_out.shape)
