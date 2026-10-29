# -*- coding: utf-8 -*-
"""缺陷探测脚本：自动化复现并采集 saucedemo 内置缺陷的证据。

与 tests/ 回归用例的分工：故意埋的缺陷不进回归断言（否则回归永远红），
由本脚本专项探测，产出量化数据与截图证据，对应 docs/bugs/ 下的缺陷报告。

用法：
    .venv/bin/python scripts/find_defects.py
输出：
    - 控制台 JSON 汇总（每个缺陷的量化证据）
    - docs/bugs/evidence/ 下的截图证据
"""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://www.saucedemo.com/"
EVIDENCE_DIR = Path(__file__).resolve().parent.parent / "docs" / "bugs" / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

findings = {}


def login(page, user: str, password: str = "secret_sauce") -> float:
    """登录并返回从点击到进入 inventory 的耗时（秒）。"""
    page.goto(BASE)
    page.fill('[data-test="username"]', user)
    page.fill('[data-test="password"]', password)
    start = time.perf_counter()
    page.click('[data-test="login-button"]')
    page.wait_for_url("**/inventory.html", timeout=60_000)
    page.wait_for_selector(".inventory_item_name")
    return time.perf_counter() - start


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()

    # ========== 缺陷 1：problem_user 商品图全部替换为同一张 404 占位图 ==========
    # 注意：占位图本身可正常加载（naturalWidth>0），必须比对 src 才能发现
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    login(page, "problem_user")
    page.wait_for_timeout(500)  # 等图片发起加载
    srcs = page.locator(".inventory_item_img img").evaluate_all("els => els.map(e => e.src)")
    filenames = [s.split("/")[-1] for s in srcs]
    findings["BUG-002_problem_user_images"] = {
        "total_images": len(srcs),
        "distinct_srcs": len(set(srcs)),
        "all_same_placeholder": len(set(srcs)) == 1,
        "placeholder_file": filenames[0],
    }
    page.screenshot(path=str(EVIDENCE_DIR / "bug-002-problem-user-inventory.png"), full_page=True)
    ctx.close()

    # ========== 缺陷 2：visual_user 购物车图标错位并与排序控件重叠 ==========
    # 检测方法：与 standard_user 的同元素几何坐标对比 + 重叠判定（几何法可量化）
    geometry = {}
    for user in ["standard_user", "visual_user"]:
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        login(page, user)
        geometry[user] = page.locator('[data-test="shopping-cart-link"]').bounding_box()
        ctx.close()
    std_cart, vis_cart = geometry["standard_user"], geometry["visual_user"]
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    login(page, "visual_user")
    vis_sort = page.locator('[data-test="product-sort-container"]').bounding_box()
    overlap_x = max(0, min(vis_cart["x"] + vis_cart["width"], vis_sort["x"] + vis_sort["width"]) - max(vis_cart["x"], vis_sort["x"]))
    overlap_y = max(0, min(vis_cart["y"] + vis_cart["height"], vis_sort["y"] + vis_sort["height"]) - max(vis_cart["y"], vis_sort["y"]))
    findings["BUG-003_visual_user_layout"] = {
        "standard_cart": {k: round(v) for k, v in std_cart.items()},
        "visual_cart": {k: round(v) for k, v in vis_cart.items()},
        "offset_px": {"dx": round(vis_cart["x"] - std_cart["x"]), "dy": round(vis_cart["y"] - std_cart["y"])},
        "overlaps_sort_dropdown": overlap_x > 0 and overlap_y > 0,
        "overlap_area_px": round(overlap_x * overlap_y),
    }
    page.screenshot(path=str(EVIDENCE_DIR / "bug-003-visual-user-inventory.png"), full_page=True)
    page.screenshot(
        path=str(EVIDENCE_DIR / "bug-003-visual-user-header-zoom.png"),
        clip={"x": 950, "y": 0, "width": 330, "height": 120},  # 头部右侧特写：图标与下拉重叠
    )
    ctx.close()

    # ========== 缺陷 3：error_user 部分商品静默加购失败 ==========
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    login(page, "error_user")
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()  # 正常商品
    page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()  # 问题商品
    page.wait_for_timeout(500)
    badge = page.locator('[data-test="shopping-cart-badge"]')
    error_banner = page.locator('[data-test="error"]')
    findings["BUG-001_error_user_silent_add_failure"] = {
        "clicked_add_buttons": 2,
        "badge_count": badge.inner_text() if badge.count() else None,
        "error_banner_visible": error_banner.count() > 0,
        "console_errors": [],
    }
    page.screenshot(path=str(EVIDENCE_DIR / "bug-001-error-user-badge.png"))
    ctx.close()

    # ========== 缺陷 4：performance_glitch_user 登录性能劣化（对照实验） ==========
    timings = {}
    for user in ["standard_user", "performance_glitch_user", "standard_user"]:
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        timings[user] = round(login(page, user), 2)
        ctx.close()
    findings["BUG-004_performance_glitch_login"] = {
        "login_seconds": timings,
        "note": "standard_user 测两次取对照，排除网络抖动",
    }

    browser.close()

print(json.dumps(findings, ensure_ascii=False, indent=2))
print(f"\n截图证据已保存到: {EVIDENCE_DIR}")
