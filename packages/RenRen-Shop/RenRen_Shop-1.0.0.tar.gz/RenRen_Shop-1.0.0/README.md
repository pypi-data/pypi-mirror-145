# README
***
|   author    | YarnBlue |
|:-----------:|:--------:|
| description | 人人商城后台管理 |
|   version   |  0.1.4   |

## 说明
该项目基于人人商城代理商韩辰科技所属域名地址，下版本会适配人人商城不同代理商

## 预告
版本更新计划
- [ ] 适配各代理商
- [ ] 评论模块
- [ ] 应用模块
- [ ] 待补充...

## 安装
pip install RenRen_Shop

## 主要结构
<details><summary>goods：商品模块</summary>
GoodsInfo : 商品信息<br>
AddGoods : 增加商品<br>
EditGoods : 编辑商品<br>
FetchGoods : 获取商品列表
</details>
<details><summary>category：商品分类模块</summary>
Category : 商品分类<br>
</details>
<details><summary>group：商品分组模块</summary>
GroupsInfo : 商品分组信息<br>
FetchGroups : 获取商品分组列表<br>
AddGroup : 增加商品分组<br>
UpdateGroup : 更新商品分组
</details>
<details><summary>log：操作日志模块</summary>
LogInfo : 账户操作日志信息<br>
FetchLogList : 获取操作日志列表<br>
</details>
<details><summary>upload：上传模块</summary>
ImgUploader : 上传图片<br>
</details>
<details><summary>photo_album：图册模块</summary>
AddAlbum : 增加图片分组<br>
</details>

## 使用
使用上下文管理器：<br>
填入账号密码，登录后获取操作权，结束后自动登出<br>
例如：

```python
from RenRen_Shop.factory import Factory

with Factory(username='你的账号', password='你的密码') as client:
    print(client.shop_ids)  # 拥有管理权的店铺ID列表
    print(client.shop_names)  # 拥有管理权的店铺列表
    print(client.shop_id)  # 当前管理的店铺ID,初始化默认使用第一个店铺
    print(client.shop_name)  # 当前管理的店铺名
    client.switch_shop(myshop=125)  # 店铺切换
    client.goods.GoodsInfo.goods_info(id=2658)  # 商品2658的信息
    goods = client.goods.FetchGoods
    goods.next(status=0)  # 增加筛选条件
    print(goods.result()) # 获取商品列表，翻页调用next()
```
批量管理实例：
```python
from RenRen_Shop.factory import Factory

with Factory(username='', password='') as client:
    goods = client.goods.FetchGoods
    while goods.next(keywords='零食'):
        for result in goods.result():
            id = result['id']
            client.goods.EditGoods.edit_goods_by_first_level(id=id, is_commission=1, stock=100)

```
代码实现将所有标题中包含【零食】的商品，统一开启分销，设置库存为100

当然也可以使用内置方法MassUpdateGoods:
```python
from RenRen_Shop.factory import Factory

with Factory(username='', password='') as client:
    goods = [1254, 1255, 1256] # 你需要修改的商品id
    kwargs = {
        'stock': 100,
        'is_commission': 0,
        'status': 0
    }  # 你需要修改的商品属性
    client.app.MassUpdateGoods.mash_update_goods(*goods, **kwargs)
```
## 结语
基于本项目，可实现多种批量管理功能，例如批量导出商品信息，批量修改商品信息，批量上传商品，批量对商品进行商品分组；在实际生产过程，批量化操作多属于不可逆过程，请做好数据备份，本项目对生产问题概不负责，请谨慎操作。
