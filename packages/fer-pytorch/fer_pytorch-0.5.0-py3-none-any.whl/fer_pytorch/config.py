import os
from pathlib import Path


class CFG:
    # Package path
    PACKAGE_DIR = Path(__file__).resolve().parent
    # Data path
    DATASET_PATH = "fer_pytorch/dataset"
    TRAIN_PATH = os.path.join(DATASET_PATH, "data/FER2013Train/")
    TRAIN_CSV = os.path.join(DATASET_PATH, "new_train.csv")
    VAL_PATH = os.path.join(DATASET_PATH, "data/FER2013Valid/")
    VAL_CSV = os.path.join(DATASET_PATH, "new_val.csv")
    TEST_PATH = os.path.join(DATASET_PATH, "data/FER2013Test/")
    TEST_CSV = os.path.join(DATASET_PATH, "new_test.csv")
    # Logging
    LOG_DIR = "fer_pytorch/logs"
    OUTPUT_DIR = "pl"

    # Model setup
    # chk = "fer_pytorch/models/resnet34_best.pt"
    chk = None
    model_name = "resnet34"
    pretrained = True

    # Main config
    GPU_ID = 0
    seed = 42
    target_size = 7
    target_col = "label"

    # Train configs
    MIXED_PREC = False  # Flag for mixed precision training
    debug = False
    epochs = 50
    early_stopping = 7
    batch_size = 32
    size = 224
    MEAN = [0.485, 0.456, 0.406]  # ImageNet values
    STD = [0.229, 0.224, 0.225]  # ImageNet values
    num_workers = 4
    print_freq = 100

    # Optimizer config
    lr = 2e-2
    momentum = 0.9
    min_lr = 1e-2
    weight_decay = 1e-5
    gradient_accumulation_steps = 1
    max_grad_norm = 1000
