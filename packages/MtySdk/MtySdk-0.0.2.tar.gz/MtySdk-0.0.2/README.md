# MtySdk介绍

- MtySdk目前是为麦田云际公司内部成员公司开发的局域网服务API.

# 快速入门

## 数据回测
```py
#encoding: utf-8
from MtySdk import *

# 使用员工账号连接系统
api = MtyApi(auth=MtyAuth('account', 'password'))
# 按需求注册服务
math = api.query_math('kq_m_shfe_au','2018-01-02','2018-01-04')

# 注册成功情况下消费服务
while api.is_having():
    result = api.get_math(math)
    print(result)
```