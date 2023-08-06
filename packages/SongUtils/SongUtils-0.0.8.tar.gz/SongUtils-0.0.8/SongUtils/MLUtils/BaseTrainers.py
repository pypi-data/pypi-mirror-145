import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.optim import SGD, Adam
from torch.optim.lr_scheduler import LambdaLR
from tensorboardX import SummaryWriter
import os
import os.path as osp
import logging

import sys
from SongUtils.MetricUtils import AverageMeter, accuracy

class BaseTrainer(object):
    def __init__(self, cfg, model, dataset_list, metrics_list):
        self.cfg = cfg
        self.init_logger()
        self.init_device()
        self.init_writer()
        self.init_loss_func()
        self.init_model(model)
        self.init_optimizer()
        self.init_lr_scheduler()

        train_set, val_set = dataset_list
        self.init_dataloader(train_set, val_set)

        self.metrics_list = metrics_list
    
    def init_logger(self):
        logging.basicConfig(level=eval(f"logging.{self.cfg.log_level}"), format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def init_writer(self):
        self.writer = SummaryWriter(self.cfg.summary_path)

    def init_device(self):
        self.device = torch.device(self.cfg.device)

    def init_model(self, model):
        self.model = model.to(self.device)

    def init_dataloader(self, train_set, val_set):
        self.train_loader = DataLoader(train_set, batch_size=self.cfg.batchSize, shuffle=True)
        self.val_loader = DataLoader(val_set, batch_size=self.cfg.batchSize, shuffle=False)
    
    def print_configs(self):
        print('*'*21, " - Configs - ", '*'*21)
        for k, v in vars(self.cfg).items():
            if v is None:
                v = "None"
            print(k, ':', v)
        print('*'*56)
    
    def write_configs_to_txt(self):
        with open(self.summary_path, 'w') as f:
            f.writelines('*'*21, " - Configs - ", '*'*21+'\n')
            for k, v in vars(self.cfg).items():
                if v is None:
                    v = "None"
                f.writelines(k, ':', v+'\n')
            f.writelines('*'*56 + '\n')

    def init_lr_scheduler(self):
        if self.cfg.lr_scheduler_type is None:
            self.lr_scheduler = None
        if self.cfg.lr_scheduler_type == "lambdalr":
            self.lr_scheduler = LambdaLR(self.optimizer, lr_lambda=lambda epoch: 1 / (epoch+1))

    def init_optimizer(self):
        if self.cfg.optimizer_type == "sgd":
            self.optimizer = SGD(self.model.parameters(), lr=self.cfg.lr, momentum=0.9, weight_decay=self.cfg.weight_decay)
        elif self.cfg.optimizer_type == "adam":
            self.optimizer = Adam(self.model.parameters(), lr=self.cfg.lr)
    
    def init_loss_func(self): 
        self.loss_func = torch.nn.CrossEntropyLoss()
    
    def resume(self):
        ckpt = torch.load(self.cfg.resume, map_location=self.device)
        self.model.load_state_dict(ckpt["state_dict"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        return ckpt["epoch"]
    
    def epoch_forward(self, isTrain, epoch):
        # for metric in self.metrics_list:
        #     exec(f"_{metric} = AverageMeter()")
        _loss = AverageMeter()
        _acc = AverageMeter()

        if isTrain:
            self.model.train()
            loader = self.train_loader
        else:
            self.model.eval()
            loader = self.val_loader
        
        for epoch_step, data in enumerate(loader):
            image = data[0].to(self.device)
            label = data[1].to(self.device)
            if isTrain:
                self.optimizer.zero_grad()
            output = self.model(image)
            loss = self.loss_func(output, label)
            acc = accuracy(output, label, [1, ])[0]
            if isTrain:
                loss.backward()
                self.optimizer.step()
            
            _loss.update(loss.item())
            _acc.update(acc)
            if (epoch_step + 1) % self.cfg.log_freq == 0:
                self.logger.debug(f"Epoch: {epoch}/{self.cfg.epochs}, Step: {epoch_step}/{len(loader)}")
                for metric in self.metrics_list:
                    self.logger.debug(f"\t {metric}: {eval(f'_{metric}.avg')}")

        metrics_dict = {}
        for metric in self.metrics_list:
            metrics_dict[metric] = eval('_' + metric).avg
        return metrics_dict

    def plot_epoch_metric(self, epoch, train_dict, val_dict):
        for metric in self.metrics_list:
            self.writer.add_scalars(metric, {"train " + metric: train_dict[metric], "val " + metric: val_dict[metric]}, epoch)

    def save_model(self, epoch):
        if not osp.isdir(self.cfg.model_path):
            os.mkdir(self.cfg.model_path)
        state = {
            'state_dict': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epoch': epoch
        }
        torch.save(state, osp.join(self.cfg.model_path, f"model_{epoch}.pth"))
    
    def update_lr(self):
        if self.lr_scheduler is not None:
            self.lr_scheduler.step()

    def forward(self):
        self.print_configs()
        if self.cfg.resume is not None:
            start_epoch = self.resume() + 1
        else:
            start_epoch = 0

        for epoch in range(start_epoch, self.cfg.epochs):
            self.logger.info(f"Training Epoch = {epoch}")
            train_metrics_dict = self.epoch_forward(isTrain=True, epoch=epoch)
            with torch.no_grad():
                self.logger.info(f"Validating Epoch = {epoch}")
                val_metrics_dict = self.epoch_forward(isTrain=False, epoch=epoch)
            self.plot_epoch_metric(epoch, train_metrics_dict, val_metrics_dict)
            self.save_model(epoch)
            self.update_lr()

            

class BaseDistTrainer(BaseTrainer):
    def __init__(self, cfg, model, dataset_list, metrics_list):
        super(BaseDistTrainer, self).__init__(cfg, model, dataset_list, metrics_list)
    
    def init_device(self):
        self.device = torch.device("cuda", self.cfg.local_rank)
    
    def init_model(self, model):
        self.logger.debug("Using Distributed Model")
        self.model = torch.nn.parallel.DistributedDataParallel(model.cuda(), device_ids=[self.cfg.local_rank])
    
    def init_dataloader(self, train_set, val_set):
        train_sampler = DistributedSampler(train_set) 
        val_sampler = DistributedSampler(val_set) 
        self.train_loader = DataLoader(train_set, batch_size=self.cfg.batchSize, sampler=train_sampler)
        self.val_loader = DataLoader(val_set, batch_size=self.cfg.batchSize, sampler=val_sampler)

def init_dist(gpu_id, nprocs, local_rank):
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id
    torch.distributed.init_process_group(backend="nccl",
                                        init_method='tcp://127.0.0.1:23456',
                                        world_size=nprocs,
                                        rank=local_rank
    )
    # local_rank = torch.distributed.get_rank()
    torch.cuda.set_device(local_rank)
