"""
PageElement dataclass 定義 — 用於取代 WebElements.py 中的 dict 結構

使用方式：
    from Library.PageElement import PageElement

    # 建立一個元素
    menu = PageElement(name="Menu", xpath='//a[@class="burger"]', description="漢堡選單")

    # frozen=True：建好後不可修改，避免意外變更
    menu.xpath = "new xpath"  # ❌ 會拋出 FrozenInstanceError

擴充欄位：
    未來若需要加入更多屬性（如 wait_timeout、required、tag 等），
    只需在此檔案新增欄位並設定預設值即可，不影響既有程式碼。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PageElement:
    """網頁元素定義 — 唯讀（frozen=True）
    
    Attributes:
        name:         元素名稱，用於查找
        xpath:        XPath 定位器
        description:  元素說明（選填）
        wait_timeout: 等待超時秒數（選填，預設 10 秒）
        required:     是否為必要元素（選填，預設 True）
    """
    name: str
    xpath: str
    description: str = ""
    wait_timeout: int = 10
    required: bool = True


def build_element_map(elements: list[PageElement]) -> dict[str, str]:
    """將 PageElement 列表轉換為 name -> xpath 的 dict
    
    用於向後相容既有程式碼（如 Cathay_Auto_Test.py 使用 Cathay_Xpath['Menu']）。
    """
    return {e.name: e.xpath for e in elements}
