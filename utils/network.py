from typing import List

import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(ConvBlock, self).__init__()
        self.conv1 = nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv2 = nn.Conv2d(ch_out, ch_out, kernel_size=3, stride=1, padding=1, bias=False)
        nn.init.normal_(self.conv1.weight, mean=0.0, std=0.02)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=0.02)
        self.batchnorm1 = nn.BatchNorm2d(ch_out)
        self.batchnorm2 = nn.BatchNorm2d(ch_out)
        self.relu = nn.ReLU()

    def forward(self, x):
        h = self.relu(self.batchnorm1(self.conv1(x)))
        h = self.relu(self.batchnorm2(self.conv2(h)))
        return h

class EncodeBlock(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(EncodeBlock, self).__init__()
        self.conv = ConvBlock(ch_in, ch_out)
        self.pool = nn.MaxPool2d((2,2))

    def forward(self, x):
        skip = self.conv(x)
        h = self.pool(skip)
        return h, skip

class DecodeBlock(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(DecodeBlock, self).__init__()
        self.up = nn.ConvTranspose2d(ch_in, ch_out, kernel_size=2, stride=2, padding=0, bias=True)
        self.conv = ConvBlock(ch_out*2, ch_out)

    def forward(self, x, skip):
        h = self.up(x)
        h = self.conv(torch.cat([h, skip], dim=1))
        return h
    
class UNet(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(UNet, self).__init__()
        self.econv0 = nn.Conv2d(ch_in, 64, kernel_size=1, stride=1, padding=0, bias=True)
        nn.init.normal_(self.econv0.weight, mean=0.0, std=0.02)

        self.econv1 = self.make_downblock(64, 64)
        self.econv2 = self.make_downblock(64, 128)
        self.econv3 = self.make_downblock(128, 256)
        self.econv4 = self.make_downblock(256, 512)
        self.bottle = self.make_bottleblock(512, 1024)
        self.dconv4 = self.make_upblock(1024, 512)
        self.dconv3 = self.make_upblock(512, 256)
        self.dconv2 = self.make_upblock(256, 128)
        self.dconv1 = self.make_upblock(128, 64)

        self.dconv0 = nn.Conv2d(64, ch_out, kernel_size=1, stride=1, padding=0, bias=True)
        nn.init.normal_(self.dconv0.weight, mean=0.0, std=0.02)

    def make_downblock(self, ch_in, ch_out):
        return EncodeBlock(ch_in=ch_in, ch_out=ch_out)
    def make_bottleblock(self, ch_in, ch_out):
        return ConvBlock(ch_in=ch_in, ch_out=ch_out)
    def make_upblock(self, ch_in, ch_out):
        return DecodeBlock(ch_in=ch_in, ch_out=ch_out)

    def forward(self, x):
        x = self.econv0(x)
        x, skip1 = self.econv1(x)
        x, skip2 = self.econv2(x)
        x, skip3 = self.econv3(x)
        x, skip4 = self.econv4(x)
        x = self.bottle(x)
        x = self.dconv4(x, skip4)
        x = self.dconv3(x, skip3)
        x = self.dconv2(x, skip2)
        x = self.dconv1(x, skip1)
        x = self.dconv0(x)
        return x
    
class Block(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Block, self).__init__()
        self.conv = nn.Conv3d(in_ch, out_ch, kernel_size=3, stride=1, padding=1, bias=False)
        self.norm = nn.BatchNorm3d(out_ch)
        self.relu = nn.ReLU(inplace=True)
        self.pool = nn.MaxPool3d(2,2)
    def forward(self, x):
        x = self.relu(self.norm(self.conv(x)))
        return self.pool(x)

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.blocks1 = Block(1, 3)
        self.blocks2 = Block(3, 8)
        self.blocks3 = Block(8, 16)
        self.blocks4 = Block(16, 32)
        
        self.fc1 = nn.Linear(5 * 7 * 5 * 32, 128)
        self.fc2 = nn.Linear(128, 2)
    def forward(self, x):
        x = self.blocks1(x)
        x = self.blocks2(x)
        x = self.blocks3(x)
        x = self.blocks4(x)
        _, c, h, w, z = x.shape
        x = x.view(-1, h * w * z * c)
        x = self.fc1(x)
        x = self.fc2(x)
        return x