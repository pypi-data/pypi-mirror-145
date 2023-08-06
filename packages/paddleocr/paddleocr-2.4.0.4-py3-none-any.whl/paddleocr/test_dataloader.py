import numpy as np

from paddle.io import Dataset, DistributedBatchSampler

# init with dataset
class RandomDataset(Dataset):
    def __init__(self, num_samples):
        self.num_samples = num_samples

    def __getitem__(self, idx, idx_list):
        image = np.random.random([784]).astype('float32')
        label = np.random.randint(0, 9, (1, )).astype('int64')
        return image, label

    def __len__(self):
        return self.num_samples

dataset = RandomDataset(100)
for i in range(0,100, 8):
    print("i:", i)
sampler = DistributedBatchSampler(dataset, batch_size=8)

# for data in sampler:
#     print(data)
