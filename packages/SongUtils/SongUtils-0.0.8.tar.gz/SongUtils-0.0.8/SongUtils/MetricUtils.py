import torch

class AverageMeter(object):
    '''
    Computes and stores the average and current value
    '''

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def accuracy(output, target, topk=(1, )):       
    # params: output.shape (bs, num_classes), target.shape (bs, )
    # returns: res: list
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return [acc.item() for acc in res]


if __name__ == "__main__":
    output = torch.rand(4, 10)
    label = torch.Tensor([2, 1, 8, 5]).unsqueeze(dim=1)
    print(output)
    print('*'*100)
    values, indices = torch.topk(output, k=2, dim=1, largest=True, sorted=True)
    print("values: ", values)
    print("indices: ", indices)
    print('*'*100)

    acc = accuracy(output, label, topk=(1, 2))
    print(acc)
