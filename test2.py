from openai import OpenAI
import clip
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
import os
import numpy as np
from typing import List, Union, Tuple
from PIL import Image
import base64
import matplotlib.pyplot as plt

#https://cookbook.openai.com/examples/custom_image_embedding_search