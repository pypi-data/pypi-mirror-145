# -*- coding: utf-8 -*-
'''
    convert_keras.py: keras h5py 权重 转换pb:
'''
import sys
import tensorflow as tf
import tf2pb
import os
from keras.models import Model,load_model
# test pass at tensorflow 1.x


# bert_model is construct by your src code
weight_file = os.path.join(output_dir, 'best_model.h5')
bert_model.load_weights(weight_file , by_name=False)
# or bert_model = load_model(weight_file)


#modify output name
pred_ids = tf.identity(bert_model.output, "pred_ids")

print(bert_model.inputs[0])
print(bert_model.inputs[1])

config = {
    'model': bert_model,# the model your trained
    'input_tensor' : {
        "Input-Token": bert_model.inputs[0], # Tensor such as  bert.Input[0]
        "Input-Segment": bert_model.inputs[1], # Tensor such as  bert.Input[0]
    },
    'output_tensor' : {
        "pred_ids": pred_ids, # Tensor output tensor
    },
    'save_pb_file': r'/root/save_pb_file.pb', # pb filename
}

if os.path.exists(config['save_pb_file']):
    os.remove(config['save_pb_file'])
#直接转换
tf2pb.freeze_keras_pb(config)