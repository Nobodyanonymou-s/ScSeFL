#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
import numpy as np
from torchvision import datasets, transforms
import torch
import time
from blockchain import Blockchain
from blockchain import account
from blockchain import transaction
from ePoW import PPPorcess
from utils.sampling import mnist_iid, mnist_noniid, cifar_iid
from utils.options import args_parser
from models.Update import LocalUpdate
from models.Nets import MLP, CNNMnist, CNNCifar
from models.Fed import FedAvg
from models.test import test_img
from decimal import Decimal, ROUND_HALF_UP
status = 0
block = Blockchain()
block.create_genesis_block()

def benefit_cal(acc_last,acc):
    temp = ((acc/100)**2-(acc_last/100)**2)
    num = Decimal(temp)
    benefit = float(num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    #= round(temp,2)
    if benefit <= 0:
        benefit = 0.01
    gasfee = benefit*0.1
    return benefit, gasfee

def send_parameter(full):
    global status
    if full >= 10 :
        status = 1
    else:
        status = 0
        return

def new_transaction(benefit,gasfee):
    transaction0 = transaction(gasfee,0)
    transaction1 = transaction(benefit,1)
    temp = []
    temp.append(benefit)
    temp.append(gasfee)
    #required_fields = ["author", "content"]
    
    #for field in required_fields:
    #    if not tx_data.get(field):
    #        return "Invalid transaction data", 404
    #tx_data["timestamp"] = time.time()

    block.add_new(benefit)
    return "Success"

def mine_unconfirmed_transactions():
    result = block.mine()
    if not result:
        return "No transactions to mine"
    else:
        # Making sure we have the longest chain before announcing to the network
        # chain_length = len(blockchain.chain)
        # consensus()
        # if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
        #announce_new_block(blockchain.last_block)
        return "Block #{} is mined.".format(block.last_block().index)
    
def aggregation_N_reward(acc_last,acc,account0,account1,iter):
    global status
    if status == 1:
        benefit, gasfee = benefit_cal(acc_last,acc)
        #print(benefit, gasfee)
        new_transaction(benefit,gasfee)
        mine_unconfirmed_transactions()
        #print(len(blockchain.chain))
        #account0.change(blockchain.get_trans())
        #account1.change(blockchain.get_trans())
        account1.change(benefit)
        print("{:.2f}".format(account1.check()))
        status = 0
if __name__ == '__main__':
    #create account
    global_account = account(0)
    local_account = account(1)
    # parse args
    args = args_parser()
    args.device = torch.device('cuda:{}'.format(args.gpu) if torch.cuda.is_available() and args.gpu != -1 else 'cpu')

    # load dataset and split users
    if args.dataset == 'mnist':
        trans_mnist = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        dataset_train = datasets.MNIST('../data/mnist/', train=True, download=True, transform=trans_mnist)
        dataset_test = datasets.MNIST('../data/mnist/', train=False, download=True, transform=trans_mnist)
        # sample users
        if args.iid:
            dict_users = mnist_iid(dataset_train, args.num_users)
        else:
            dict_users = mnist_noniid(dataset_train, args.num_users)
    elif args.dataset == 'cifar':
        trans_cifar = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        dataset_train = datasets.CIFAR10('../data/cifar', train=True, download=True, transform=trans_cifar)
        dataset_test = datasets.CIFAR10('../data/cifar', train=False, download=True, transform=trans_cifar)
        if args.iid:
            dict_users = cifar_iid(dataset_train, args.num_users)
        else:
            exit('Error: only consider IID setting in CIFAR10')
    else:
        exit('Error: unrecognized dataset')
    img_size = dataset_train[0][0].shape

    # build model
    if args.model == 'cnn' and args.dataset == 'cifar':
        net_glob = CNNCifar(args=args).to(args.device)
    elif args.model == 'cnn' and args.dataset == 'mnist':
        net_glob = CNNMnist(args=args).to(args.device)
    elif args.model == 'mlp':
        len_in = 1
        for x in img_size:
            len_in *= x
        net_glob = MLP(dim_in=len_in, dim_hidden=200, dim_out=args.num_classes).to(args.device)
    else:
        exit('Error: unrecognized model')
    print(net_glob)
    net_glob.train()

    # copy weights
    w_glob = net_glob.state_dict()

    # training
    loss_train = []
    acc_plot = []
    #benefit_plot = []
    time_plot = []
    com_plot = []
    cv_loss, cv_acc = [], []
    val_loss_pre, counter = 0, 0
    net_best = None
    best_loss = None
    val_acc_list, net_list = [], []

    if args.all_clients: 
        print("Aggregation over all clients")
        w_locals = [w_glob for i in range(args.num_users)]

    begin = time.time()
    tWin = 0
    for iter in range(args.epochs):#主循环
        print("========================Main Thread{}============================".format(iter))
        loss_locals = []
        if not args.all_clients:
            w_locals = []
        m = max(int(args.frac * args.num_users), 1)
        idxs_users = np.random.choice(range(args.num_users), m, replace=False)
        is_full = 0
        for idx in idxs_users:
            local = LocalUpdate(args=args, dataset=dataset_train, idxs=dict_users[idx])
            w, loss = local.train(net=copy.deepcopy(net_glob).to(args.device))
            if args.all_clients:
                w_locals[idx] = copy.deepcopy(w)
            else:
                w_locals.append(copy.deepcopy(w))
            loss_locals.append(copy.deepcopy(loss))
            is_full +=1
        send_parameter(is_full)
        #print(is_full)
        # update global weights
        if status == 1:      
           w_glob = FedAvg(w_locals)
        
           # copy weight to net_glob
           net_glob.load_state_dict(w_glob)

        if iter > 0:
           temp = float(acc_round_test)
           acc_last = round(temp,2)
        else:
            acc_last = 0.0
        #test
        tWin += PPPorcess(2,iter,tWin)
        #print(tWin)
        test_glob = net_glob
        acc_round_test, loss_round_test = test_img(test_glob, dataset_test, args)
        print("round accuracy: {:.2f}".format(acc_round_test))
        # print loss
        loss_avg = sum(loss_locals) / len(loss_locals)
        temp = float(acc_round_test)
        round_test = round(temp,2)
        #aggregation_N_reward(acc_last,round_test,global_account,local_account,iter)
        print('Round {:3d}, Average loss {:.3f}'.format(iter, loss_avg))
        plus = time.time()
        print(plus-begin)
        loss_train.append(loss_avg)
        acc_plot.append(round_test)
        time_plot.append(plus-begin)
        com_plot.append(tWin)
        #benefit_plot.append(local_account.check())
    
    # plot loss curve
    # plt.figure()
    # plt.plot(time_plot, loss_train)
    # plt.ylabel('train_loss')
    # plt.savefig('./save/fed_{}_{}_{}_C{}_iid{}.png'.format(args.dataset, args.model, args.epochs, args.frac, args.iid))

    plt.figure()
    plt.plot(time_plot, acc_plot)
    plt.ylabel('train_acc')
    plt.savefig('./save/acc_{}_{}_{}_C{}_iid{}.png'.format(args.dataset, args.model, args.epochs, args.frac, args.iid))

    # plt.figure()
    # plt.plot(range(len(benefit_plot)), benefit_plot)
    # plt.ylabel('train_acc')
    # plt.savefig('./save/benefit_{}_{}_{}_C{}_iid{}.png'.format(args.dataset, args.model, args.epochs, args.frac, args.iid))

    # testing
    net_glob.eval()
    acc_train, loss_train = test_img(net_glob, dataset_train, args)
    acc_test, loss_test = test_img(net_glob, dataset_test, args)
    print("Training accuracy: {:.2f}".format(acc_train))
    print("Testing accuracy: {:.2f}".format(acc_test))
    np.array(acc_plot)
    np.array(time_plot)
    acc_str = '['
    time_str = '['
    com_str = '['
    for i in range(0,50):
        acc_str += '{:.2f}, '.format(acc_plot[i])
        time_str += '{:.2f}, '.format(time_plot[i])
        com_str += '{:.2f}, '.format(com_plot[i])
    acc_str +=']'
    time_str += ']'
    com_str += ']'
    print(acc_str)
    print(time_str)
    print(com_str)
    #print("{:.2f}".format(benefit_plot))
