import os
import torch
from utils.network import CNN, UNet

def load_model(opt, device):
    cnet = UNet(1, 1)
    cnet.load_state_dict(torch.load(os.path.join(opt.m, "CNet.pth")))
    cnet.to(device)
    cnet.eval()

    ssnet = UNet(1, 1)
    ssnet.load_state_dict(torch.load(os.path.join(opt.m, "SSNet.pth")))
    ssnet.to(device)
    ssnet.eval()

    cnn1 = CNN()
    cnn1.load_state_dict(torch.load(os.path.join(opt.m, "CNN1.pth")))
    cnn1.to(device)
    cnn1.eval()
    
    cnn2 = CNN()
    cnn2.load_state_dict(torch.load(os.path.join(opt.m, "CNN2.pth")))
    cnn2.to(device)
    cnn2.eval()
    
    cnn3 = CNN()
    cnn3.load_state_dict(torch.load(os.path.join(opt.m, "CNN3.pth")))
    cnn3.to(device)
    cnn3.eval()
    
    cnn4 = CNN()
    cnn4.load_state_dict(torch.load(os.path.join(opt.m, "CNN4.pth")))
    cnn4.to(device)
    cnn4.eval()
    
    cnn5 = CNN()
    cnn5.load_state_dict(torch.load(os.path.join(opt.m, "CNN5.pth")))
    cnn5.to(device)
    cnn5.eval()
    return cnet, ssnet, cnn1, cnn2, cnn3, cnn4, cnn5