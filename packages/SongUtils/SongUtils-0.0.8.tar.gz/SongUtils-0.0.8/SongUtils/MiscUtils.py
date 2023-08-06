import torch

def load_weights(model, weights_path):
    ckpt = torch.load(weights_path, map_location='cpu')
    model_weights = ckpt['state_dict']
    model.load_state_dict(model_weights)
    return model