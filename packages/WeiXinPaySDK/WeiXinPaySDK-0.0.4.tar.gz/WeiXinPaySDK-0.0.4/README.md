# WeiXinPaySDK

#### 介绍

WeiXinPaySDK是基于微信支付开发的sdk

### demo

```python
# -*- coding: utf-8 -*-
from WeiXinPaySDK.Pay import Order, Bill
from WeiXinPaySDK.manage import payscore, PayScoreOrder, ServicePeople

# 创建支付订单
order = Order(mode="Native")
new_order = order.create_order(appid="", mchid="", description="", out_trade_no="", notify_url="",
                               amount={"total": 0.1})
print(new_order)

# 申请交易账单
bill = Bill(mode="Native")
bl = bill.apply_trade_bill(bill_type="")
print(bl)

```