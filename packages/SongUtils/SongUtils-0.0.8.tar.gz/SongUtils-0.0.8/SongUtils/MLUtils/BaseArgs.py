import argparse
from argparse import Namespace
import yaml

class YamlParams:
    def __init__(self, yaml_path):
        self.params = yaml.safe_load(open(yaml_path).read())

    def __getattr__(self, item):
        return self.params.get(item, None)

def get_base_parser():
    parser = argparse.ArgumentParser()
    # training procedure
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batchSize", type=int, default=64)
    parser.add_argument("--resume", type=str, default=None)

    # optimizing procedure
    parser.add_argument("--optimizer-type", type=str, choices=['sgd', 'adam'], default='sgd')
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--lr_scheduler_type", type=str, default=None, choices=["none", "lambdalr"])
    parser.add_argument("--weight-decay", type=float, default=0.)

    # save logs and results
    parser.add_argument("--log-freq", type=int, default=100)
    parser.add_argument("--log-level", type=str, choices=['INFO', 'DEBUG'], default='DEBUG')
    parser.add_argument("--summary-path", type=str, default="./debug_summary")
    parser.add_argument("--model-path", type=str, default="./debug_saved_model")

    # Misc
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--gpu-id", type=str, default="0")
    return parser

def get_dist_base_parser():
    parser = get_base_parser()
    parser.add_argument("--local_rank", type=int)
    parser.add_argument("--nprocs", type=int, default=1)
    return parser


if __name__ =="__main__":
    def _my_args(basic_parser):
        basic_parser.add_argument("--test", type=str, default="testing")
        basic_parser.add_argument("--val", type=str, default="validating")
        cfg = parser.parse_args()
        return cfg
    basic_parser = get_basic_parser()
    cfg = _my_args(basic_parser)
    print(cfg.test)
    print(cfg.model_path)
