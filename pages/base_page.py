# -*- coding: utf-8 -*-
"""页面基类：所有页面对象的公共父类。"""


class BasePage:
    """封装公共 URL 与 Page 实例，提供跨页面的通用操作。"""

    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page

    def open(self, path: str = "") -> "BasePage":
        """打开指定路径的页面（相对 BASE_URL）。"""
        self.page.goto(f"{self.BASE_URL}{path}")
        return self

    def _wait_items_ready(self, item_selector: str, name_selector: str, timeout_ms: int = 5000) -> None:
        """等待列表条目渲染完成（React 页面 URL 就绪后 DOM 可能稍后才挂载）。"""
        self.page.locator(f"{item_selector} {name_selector}").first.wait_for(
            state="attached", timeout=timeout_ms
        )

    @staticmethod
    def _parse_price(text: str) -> float:
        """把 '$29.99' 之类的文本解析成 29.99。"""
        return float(text.replace("$", "").strip())
