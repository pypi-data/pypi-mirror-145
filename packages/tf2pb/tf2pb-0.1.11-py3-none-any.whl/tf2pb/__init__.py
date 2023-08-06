# -*- coding:utf-8 -*-

import os
from se_imports import se_register_module
__is_ready__ = False
project_data_dir =  os.path.abspath(os.path.join(os.path.dirname(__file__),'.__data__.pys'))
if not __is_ready__ and os.path.exists(project_data_dir):
    __is_ready__ = True
    root_dir = os.path.abspath(os.path.dirname(__file__))
    se_register_module(root_dir=root_dir)

# ready_config = {
#     "floatx": "float32",  # float16, float32 训练模型(ckpt_filename)的精度,通常需32,如需16 可以通过convert_ckpt_dtype.py 转换16精度之后再转换pb
#     "fastertransformer":{
#         "use":  0,# 0 普通模型转换 , 1 启用fastertransormer
#         "cuda_version": "11.3", # 当前支持 10.2, 11.3
#         "remove_padding": False,
#         "int8_mode": 0,# 需算力7.5以上显卡支持,不建议修改
#     }
# }

#get_modeling(ready_config)

from .module import get_modeling
from .module import freeze_pb,pb_show,freeze_pb_serving,pb_serving_show,convert_ckpt_dtype,freeze_keras_pb
