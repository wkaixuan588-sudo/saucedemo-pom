# -*- coding: utf-8 -*-
"""测试数据集中管理（夹具放 conftest.py，纯数据放这里）。

商品目录与错误文案均来自对站点的实地探测（见 docs/test-design.md），
与 saucedemo.com 线上行为保持一致。
"""

# ---------------- 账号 ----------------
STANDARD_USER = "standard_user"
STANDARD_PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong_password"

# 登录矩阵：等价类划分（正常/性能异常/界面异常/功能异常/视觉异常/锁定）。
# 所有用户密码均为 secret_sauce；除 locked_out 外均可登录进入 inventory。
LOGIN_MATRIX = [
    # (用户, 预期结果: success|locked, 预期错误提示片段)
    ("standard_user", "success", None),
    ("performance_glitch_user", "success", None),   # 登录后加载慢 ~5s
    ("problem_user", "success", None),              # 商品图片 404（S3 缺陷报告素材）
    ("error_user", "success", None),                # 部分商品静默加购失败
    ("visual_user", "success", None),               # 页面元素错位
    ("locked_out_user", "locked", "Sorry, this user has been locked out"),
]

# ---------------- 商品目录（slug -> (名称, 价格)，默认/字母升序排列） ----------------
PRODUCTS = {
    "sauce-labs-backpack": ("Sauce Labs Backpack", 29.99),
    "sauce-labs-bike-light": ("Sauce Labs Bike Light", 9.99),
    "sauce-labs-bolt-t-shirt": ("Sauce Labs Bolt T-Shirt", 15.99),
    "sauce-labs-fleece-jacket": ("Sauce Labs Fleece Jacket", 49.99),
    "sauce-labs-onesie": ("Sauce Labs Onesie", 7.99),
    "test.allthethings()-t-shirt-(red)": ("Test.allTheThings() T-Shirt (Red)", 15.99),
}
PRODUCT_NAMES_AZ = [name for name, _ in PRODUCTS.values()]  # 默认顺序即 A-Z
PRODUCT_PRICES = [price for _, price in PRODUCTS.values()]

# error_user 实测：这三款商品点击加购后角标不变（静默失败，无报错提示）
ERROR_USER_BROKEN_SLUGS = [
    "sauce-labs-bolt-t-shirt",
    "sauce-labs-fleece-jacket",
    "test.allthethings()-t-shirt-(red)",
]
ERROR_USER_WORKING_SLUG = "sauce-labs-backpack"

# ---------------- 结算收货信息 ----------------
CHECKOUT_FIRST_NAME = "John"
CHECKOUT_LAST_NAME = "Doe"
CHECKOUT_POSTAL_CODE = "100001"

# 结算必填校验（判定表：单字段缺失 → 优先级最高的提示；全空时提示 First Name）
CHECKOUT_REQUIRED_FIELDS = [
    # (缺失字段: first|last|postal, 预期错误文案)
    ("first", "Error: First Name is required"),
    ("last", "Error: Last Name is required"),
    ("postal", "Error: Postal Code is required"),
]
