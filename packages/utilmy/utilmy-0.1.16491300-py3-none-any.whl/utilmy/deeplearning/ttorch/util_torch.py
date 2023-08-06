# -*- coding: utf-8 -*-
MNAME = "utilmy.deeplearning.torch.util_torch"
HELP = """ utils for torch training

"""
import os, random, numpy as np, glob, pandas as pd, matplotlib.pyplot as plt ;from box import Box
from copy import deepcopy

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, accuracy_score, roc_curve, auc, roc_auc_score, precision_score, recall_score, precision_recall_curve, accuracy_score


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset


#############################################################################################
from utilmy import log, log2

def help():
    """function help        
    """
    from utilmy import help_create
    ss = HELP + help_create(MNAME)
    log(ss)


#############################################################################################
def test_all():
    """function test_all
    Args:
    Returns:
        
    """
    log(MNAME)
    test()
    # test2()


def test2():
    """function test2
    Args:
    Returns:
        
    """
    arg = Box({
      "dataurl":  "https://github.com/caravanuden/cardio/raw/master/cardio_train.csv",
      "datapath": './cardio_train.csv',

      ##### Rules
      "rules" : {},

      #####
      "train_ratio": 0.7,
      "validation_ratio": 0.1,
      "test_ratio": 0.2,

      "model_type": 'dataonly',
      "input_dim_encoder": 16,
      "output_dim_encoder": 16,
      "hidden_dim_encoder": 100,
      "hidden_dim_db": 16,
      "n_layers": 1,


      ##### Training
      "seed": 42,
      "device": 'cpu',  ### 'cuda:0',
      "batch_size": 32,
      "epochs": 1,
      "early_stopping_thld": 10,
      "valid_freq": 1,
      'saved_filename' :'./model.pt',

    })



###############################################################################################
def device_setup(arg):
    """function device_setup
    Args:
        arg:   
    Returns:
        
    """
    device = arg.device
    seed   = arg.seed
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if 'gpu' in device :
        try :
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        except Exception as e:
            log(e)
            device = 'cpu'
    return device


def dataloader_create(train_X=None, train_y=None, valid_X=None, valid_y=None, test_X=None, test_y=None,  arg=None):
    """function dataloader_create
    Args:
        train_X:   
        train_y:   
        valid_X:   
        valid_y:   
        test_X:   
        test_y:   
        arg:   
    Returns:
        
    """
    batch_size = arg.batch_size
    train_loader, valid_loader, test_loader = None, None, None

    if train_X is not None :
        train_X, train_y = torch.tensor(train_X, dtype=torch.float32, device=arg.device), torch.tensor(train_y, dtype=torch.float32, device=arg.device)
        train_loader = DataLoader(TensorDataset(train_X, train_y), batch_size=batch_size, shuffle=True)
        log("data size", len(train_X) )

    if valid_X is not None :
        valid_X, valid_y = torch.tensor(valid_X, dtype=torch.float32, device=arg.device), torch.tensor(valid_y, dtype=torch.float32, device=arg.device)
        valid_loader = DataLoader(TensorDataset(valid_X, valid_y), batch_size=valid_X.shape[0])
        log("data size", len(valid_X)  )

    if test_X  is not None :
        test_X, test_y   = torch.tensor(test_X,  dtype=torch.float32, device=arg.device), torch.tensor(test_y, dtype=torch.float32, device=arg.device)
        test_loader  = DataLoader(TensorDataset(test_X, test_y), batch_size=test_X.shape[0])
        log("data size:", len(test_X) )

    return train_loader, valid_loader, test_loader




###############################################################################################
def model_load(arg):
    """function model_load
    Args:
        arg:   
    Returns:
        
    """
    model_eval = model_build(arg=arg, mode='test')

    checkpoint = torch.load( arg.saved_filename)
    model_eval.load_state_dict(checkpoint['model_state_dict'])
    log("best model loss: {:.6f}\t at epoch: {}".format(checkpoint['loss'], checkpoint['epoch']))


    ll = Box({})
    ll.loss_rule_func = lambda x,y: torch.mean(F.relu(x-y))
    ll.loss_task_func = nn.BCELoss()
    return model_eval, ll # (loss_task_func, loss_rule_func)
    # model_evaluation(model_eval, loss_task_func, arg=arg)


def model_train(model, losses, train_loader, valid_loader, arg:dict=None ):
    """function model_train
    Args:
        model:   
        losses:   
        train_loader:   
        valid_loader:   
        arg ( dict ) :   
    Returns:
        
    """
    arg      = Box(arg)  ### Params
    arghisto = Box({})  ### results



    #### Core model params
    model_params   = arg.model_info[ arg.model_type]
    lr             = model_params.get('lr',  0.001)
    optimizer      = torch.optim.Adam(model.parameters(), lr=lr)
    loss_task_func = losses.loss_task_func


    #### Train params
    model_type = arg.model_type
    # epochs     = arg.epochs
    early_stopping_thld    = arg.early_stopping_thld
    counter_early_stopping = 1
    # valid_freq     = arg.valid_freq
    seed=arg.seed
    log('saved_filename: {}\n'.format( arg.saved_filename))
    best_val_loss = float('inf')


    for epoch in range(1, arg.epochs+1):
      model.train()
      for batch_train_x, batch_train_y in train_loader:
        batch_train_y = batch_train_y.unsqueeze(-1)
        optimizer.zero_grad()



        ###### Base output #########################################
        output    = model(batch_train_x, alpha=alpha).view(batch_train_y.size())


        ###### Loss Rule perturbed input and its output  #####################
        loss_rule = loss_rule_calc(model, batch_train_x, loss_rule_func, output, arg )


        #### Total Losses  ##################################################
        scale = 1
        loss  = alpha * loss_rule + scale * (1 - alpha) * loss_task
        loss.backward()
        optimizer.step()


      # Evaluate on validation set
      if epoch % arg.valid_freq == 0:
        model.eval()
        if  model_type.startswith('ruleonly'):  alpha = 1.0
        else:                                   alpha = 0.0

        with torch.no_grad():
          for val_x, val_y in valid_loader:
            val_y = val_y.unsqueeze(-1)

            output = model(val_x, alpha=alpha).reshape(val_y.size())
            val_loss_task = loss_task_func(output, val_y).item()

            # perturbed input and its output
            pert_val_x = val_x.detach().clone()
            pert_val_x[:,rule_ind] = get_perturbed_input(pert_val_x[:,rule_ind], pert_coeff)
            pert_output = model(pert_val_x, alpha=alpha)    # \hat{y}_{p}    predicted sales from perturbed input

            val_loss_rule = loss_rule_func(output.reshape(pert_output.size()), pert_output).item()
            val_ratio = verification(pert_output, output, threshold=0.0).item()

            val_loss = val_loss_task

            y_true = val_y.cpu().numpy()
            y_score = output.cpu().numpy()
            y_pred = np.round(y_score)

            y_true = y_pred.reshape(y_true.shape[:-1])
            y_pred = y_pred.reshape(y_pred.shape[:-1])

            val_acc = mean_squared_error(y_true, y_pred)

          if val_loss < best_val_loss:
            counter_early_stopping = 1
            best_val_loss = val_loss
            best_model_state_dict = deepcopy(model.state_dict())
            log('[Valid] Epoch: {} Loss: {:.6f} (alpha: {:.2f})\t Loss(Task): {:.6f} Acc: {:.2f}\t Loss(Rule): {:.6f}\t Ratio: {:.4f} best model is updated %%%%'
                  .format(epoch, best_val_loss, alpha, val_loss_task, val_acc, val_loss_rule, val_ratio))
            torch.save({
                'epoch': epoch,
                'model_state_dict': best_model_state_dict,
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_val_loss
            }, arg.saved_filename)
          else:
            log('[Valid] Epoch: {} Loss: {:.6f} (alpha: {:.2f})\t Loss(Task): {:.6f} Acc: {:.2f}\t Loss(Rule): {:.6f}\t Ratio: {:.4f}({}/{})'
                  .format(epoch, val_loss, alpha, val_loss_task, val_acc, val_loss_rule, val_ratio, counter_early_stopping, early_stopping_thld))
            if counter_early_stopping >= early_stopping_thld:
              break
            else:
              counter_early_stopping += 1


def model_evaluation(model_eval, loss_task_func, arg, dataset_load1, dataset_preprocess1 ):
    """function model_evaluation
    Args:
        model_eval:   
        loss_task_func:   
        arg:   
        dataset_load1:   
        dataset_preprocess1:   
    Returns:
        
    """
    ### Create dataloader
    df = dataset_load1(arg)
    train_X, test_X, train_y, test_y, valid_X, valid_y = dataset_preprocess1(df, arg)

    ######
    train_loader, valid_loader, test_loader = dataloader_create( train_X, test_X, train_y, test_y, valid_X, valid_y, arg)
    model_eval.eval()
    with torch.no_grad():
      for te_x, te_y in test_loader:
        te_y = te_y.unsqueeze(-1)

      output         = model_eval(te_x, alpha=0.0)
      test_loss_task = loss_task_func(output, te_y.view(output.size())).item()

    log('\n[Test] Average loss: {:.8f}\n'.format(test_loss_task))

    ########## Pertfubation
    pert_coeff = arg.rules.pert_coeff
    rule_ind   = arg.rules.rule_ind
    model_type = arg.model_type
    alphas     = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]


    model_eval.eval()

    # perturbed input and its output
    pert_test_x = te_x.detach().clone()
    pert_test_x[:,rule_ind] = get_perturbed_input(pert_test_x[:,rule_ind], pert_coeff)
    for alpha in alphas:
      model_eval.eval()
      with torch.no_grad():
        for te_x, te_y in test_loader:
          te_y = te_y.unsqueeze(-1)

        if model_type.startswith('dataonly'):
          output = model_eval(te_x, alpha=0.0)
        elif model_type.startswith('ours'):
          output = model_eval(te_x, alpha=alpha)
        elif model_type.startswith('ruleonly'):
          output = model_eval(te_x, alpha=1.0)

        test_loss_task = loss_task_func(output, te_y.view(output.size())).item()

        if model_type.startswith('dataonly'):
          pert_output = model_eval(pert_test_x, alpha=0.0)
        elif model_type.startswith('ours'):
          pert_output = model_eval(pert_test_x, alpha=alpha)
        elif model_type.startswith('ruleonly'):
          pert_output = model_eval(pert_test_x, alpha=1.0)

        test_ratio = verification(pert_output, output, threshold=0.0).item()

        y_true = te_y.cpu().numpy()
        y_score = output.cpu().numpy()
        y_pred = np.round(y_score)

        test_acc = mean_squared_error(y_true.squeeze(), y_pred.squeeze())

      log('[Test] Average loss: {:.8f} (alpha:{})'.format(test_loss_task, alpha))
      log('[Test] Accuracy: {:.4f} (alpha:{})'.format(test_acc, alpha))
      log("[Test] Ratio of verified predictions: {:.6f} (alpha:{})".format(test_ratio, alpha))
      log()



#####################################################################################################################
def get_metrics(y_true, y_pred, y_score):
    """function get_metrics
    Args:
        y_true:   
        y_pred:   
        y_score:   
    Returns:
        
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    return acc, prec, recall, fpr, tpr, roc_auc



#############################################################################################
class model_dummy(nn.Module):
  def __init__(self, input_dim, output_dim, hidden_dim=4):
    super(DataEncoder, self).__init__()
    self.input_dim = input_dim
    self.output_dim = output_dim
    self.net = nn.Sequential(nn.Linear(input_dim, hidden_dim),
                             nn.ReLU(),
                             nn.Linear(hidden_dim, output_dim))

  def forward(self, x):
    return self.net(x)



def test_dataset_classification_fake(nrows=500):
    """function test_dataset_classification_fake
    Args:
        nrows:   
    Returns:
        
    """
    from sklearn import datasets as sklearn_datasets
    ndim    =11
    coly    = 'y'
    colnum  = ["colnum_" +str(i) for i in range(0, ndim) ]
    colcat  = ['colcat_1']
    X, y    = sklearn_datasets.make_classification(n_samples=nrows, n_features=ndim, n_classes=1,
                                                   n_informative=ndim-2)
    df         = pd.DataFrame(X,  columns= colnum)
    df[coly]   = y.reshape(-1, 1)

    for ci in colcat :
      df[ci] = np.random.randint(0,1, len(df))

    pars = { 'colnum': colnum, 'colcat': colcat, "coly": coly }
    return df, pars




###################################################################################################
if __name__ == "__main__":
    import fire 
    fire.Fire() 
    # test_all()


