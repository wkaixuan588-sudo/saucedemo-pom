# Swag Labs (saucedemo.com) PO 模式自动化测试

基于 **Python + Playwright + Pytest** 的 UI 自动化测试项目，采用 **Page Object（PO）模式**，
页面层（`pages/`）与用例层（`tests/`）分离。

## 测试业务流程

`登录(standard_user / secret_sauce)` → `添加两款商品到购物车`
→ `打开购物车校验商品与价格` → `填写收货信息`
→ `校验订单总览(小计/税费/总价)` → `提交订单` → `断言 "Thank you for your order!"`

## 目录结构

```
saucedemo_pom/
├── pages/                          # 页面层：元素定位 + 页面操作 + 页面断言
│   ├── base_page.py                # 页面基类（URL、公共方法）
│   ├── login_page.py               # 登录页
│   ├── inventory_page.py           # 商品库存页
│   ├── cart_page.py                # 购物车页
│   ├── checkout_info_page.py       # 结算第一步：收货信息
│   ├── checkout_overview_page.py   # 结算第二步：订单总览
│   └── checkout_complete_page.py   # 结算完成页
├── tests/                          # 用例层：只描述业务流程与断言，不写选择器
│   ├── conftest.py                 # 公共夹具与测试数据
│   ├── test_login.py               # 登录用例
│   └── test_checkout_flow.py       # 加购 + 结算主流程用例
├── pytest.ini                      # pytest 配置（默认有头模式）
└── requirements.txt                # 依赖清单
```

## 环境准备

```bash
cd saucedemo_pom
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium      # 首次需要下载浏览器
```

## 运行测试

```bash
# 有头模式运行（pytest.ini 已默认 --headed）
pytest

# 仅运行主流程用例
pytest tests/test_checkout_flow.py

# 无头模式运行（CI 中使用）
pytest -o addopts="--browser=chromium"

# 失败时自动截图/录像/trace 输出到 test-results/（pytest-playwright 内置）
```

## 设计说明

1. **分层**：用例层（`tests/`）只表达业务步骤与业务断言；选择器与元素操作全部收敛在页面层（`pages/`），
   页面改版时只需修改对应页面对象。
2. **选择器**：全部使用站点提供的 `data-test` 属性（如 `[data-test="add-to-cart-sauce-labs-backpack"]`），
   稳定且可读；商品名通过 slug 拼接选择器。
3. **等待策略**：saucedemo 为 React 单页应用，URL 跳转完成后 DOM 仍在挂载，
   数据读取方法内置 `wait_for(state="attached")`；断言统一使用 `expect()` 自动重试。
4. **金额校验**：总览页按 `小计 = 商品价格之和`、`税费 = 小计 × 8%`、`总价 = 小计 + 税费` 动态计算后与页面比对。
