# saucedemo.com UI 自动化测试报告

| 项目 | 内容 |
|---|---|
| 被测对象 | Swag Labs（https://www.saucedemo.com/）电商演示站 |
| 测试类型 | UI 功能自动化回归（Playwright + Pytest，PO 模式） |
| 报告日期 | 2026-10-29 |
| 执行环境 | 本地 macOS / Chromium 1243 无头；CI GitHub Actions ubuntu-latest |
| 用例规模 | 20 条（登录 9 / 排序 4 / 购物车 3 / 结算 4） |
| 设计文档 | [docs/test-design.md](test-design.md) |

## 一、执行结果

| 指标 | 本地（无头） | CI（GitHub Actions） |
|---|---|---|
| 用例执行 | 20 / 20 | 20 / 20 |
| 通过率 | **100%** | **100%** |
| 总耗时 | 23 ~ 41s（两次采样） | 54s |
| 冒烟集（-m smoke） | 1 条 / 2.4s | — |

> 说明：回归用例 100% 通过 ≠ 站点无缺陷。站点内置的 4 个演示缺陷**不属于回归断言范围**
> （写入断言会使回归永久失败），由独立探测脚本发现并走缺陷流程，见下节。

## 二、缺陷汇总（共 4 个，全部由自动化发现）

| 编号 | 标题 | 严重程度 | 类型 | 发现手段 |
|---|---|---|---|---|
| [BUG-001](bugs/BUG-001.md) | 部分商品加购静默失败，角标不变且无任何提示 | **Critical** | 功能 | 负向用例固化（tests/test_cart.py） |
| [BUG-002](bugs/BUG-002.md) | 全部商品图被替换为同一张 404 占位图 | Major | UI/内容 | 探测脚本（图片 src 唯一性比对） |
| [BUG-003](bugs/BUG-003.md) | 购物车图标错位并与排序下拉重叠 441px² | Minor | UI/布局 | 探测脚本（几何坐标对比法） |
| [BUG-004](bugs/BUG-004.md) | 特定账号登录首屏耗时 5.11s（对照 0.07s，≈73×） | Major | 性能 | 探测脚本（计时对照实验） |

严重程度分布：Critical 1 / Major 2 / Minor 1。

### 检测方法备注（面试官可能追问）

- BUG-002 的占位图**可正常加载**（naturalWidth>0），常规"图片加载失败"断言检测不到，
  需比对 src——"元素存在"≠"内容正确"；
- BUG-003 未用截图肉眼比对，而是同视口两账号的 bounding box 对比 + 矩形重叠判定，可量化、可进 CI；
- BUG-004 采用同口径计时对照（对照组测 2 次），避免网络抖动导致的误报。

## 三、覆盖情况与未覆盖项

已覆盖：登录等价类矩阵（6 账号）、登录边界值、4 种排序、购物车加购/移除/角标联动、
结算主流程金额校验（小计/8% 税/总价动态计算）、收货信息必填判定表。

未覆盖（后续迭代）：
1. 结算页 Cancel / continue-shopping 次要返回路径；
2. 多浏览器矩阵（chromium/webkit/firefox）与移动视口；
3. 视觉回归基线（当前仅几何断言）；
4. 多用户并发与弱网场景。

## 四、风险评估与建议

| 风险 | 等级 | 建议 |
|---|---|---|
| BUG-001 静默失败造成订单流失 | 高 | 修复优先；加购与状态强一致 + 失败必须可感知 |
| 商品图/布局缺陷影响购买决策与可用性 | 中 | 图片映射回归校验；关键控件几何断言纳入 CI |
| 登录性能 73 倍劣化 | 中 | 关键路径建立性能基线（P95 阈值断言） |
| 外部演示站点变更导致 CI 误报 | 低 | 已配每周定时巡检，变更时可快速定位是否环境问题 |

## 五、结论

- 核心购买主链路（登录 → 加购 → 结算 → 下单）在 standard_user 下功能正常，**可发布**；
- 4 个内置缺陷已全部定位、留证并提交缺陷报告，其中 1 个 Critical 建议修复后复验；
- 回归资产（20 用例 + 探测脚本 + CI）已就绪，支持后续持续回归。

## 附录：复现方式

```bash
# 全量回归
pytest -o addopts="--browser=chromium"

# 冒烟
pytest -m smoke

# Allure 报告
pytest -o addopts="--browser=chromium" --alluredir=allure-results
allure generate allure-results -o allure-report --clean && allure open allure-report

# 缺陷证据采集
.venv/bin/python scripts/find_defects.py
```
