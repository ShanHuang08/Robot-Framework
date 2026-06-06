from Library.PageElement import PageElement, build_element_map

# ─────────────────────────────────────────────
# Cathay 元素定義（dataclass 列表）
# ─────────────────────────────────────────────
Cathay_Elements: list[PageElement] = [
    PageElement(
        name="Menu",
        xpath='//a[@class="cubre-a-burger"]',
        description="左上角漢堡選單",
    ),
    PageElement(
        name="產品介紹",
        xpath='//div[@class="cubre-o-nav__content"]//*[contains(text(),"產品介紹")]',
        description="導航列產品介紹入口",
    ),
    PageElement(
        name="信用卡",
        xpath='//div[@class="cubre-o-menuLinkList__btn"]//*[contains(text(),"信用卡")]',
        description="選單中的信用卡選項",
    ),
    PageElement(
        name="掛失信用卡",
        xpath='//*[contains(text(),"掛失信用卡")]',
        description="掛失信用卡選項",
    ),
    PageElement(
        name="Card Service list",
        xpath='/html/body/div[1]/header/div/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/a',
        description="卡片服務列表連結",
    ),
    PageElement(
        name="卡片介紹",
        xpath='//a[contains(text(),"卡片介紹")]',
        description="卡片介紹頁面連結",
    ),
    PageElement(
        name="所有卡",
        xpath='//div[@class="cubre-m-compareCard__title"]',
        description="所有卡區塊標題",
    ),
    PageElement(
        name="卡片介紹Tabs",
        xpath='//div[@class="cubre-m-anchor__fixBox"]//a',
        description="卡片介紹頁的錨點分頁（多個元素）",
    ),
    PageElement(
        name="停發卡Tab",
        xpath='//div[@class="cubre-m-anchor__fixBox"]//*[contains(text(),"停發卡")]',
        description="停發卡分頁標籤",
    ),
    PageElement(
        name="停發卡Tab_active",
        xpath='//div[@class="cubre-m-anchor__fixBox"]//a[contains(@class, "is-active")]',
        description="目前選中的停發卡分頁",
    ),
]

# ─────────────────────────────────────────────
# Twitch 元素定義（dataclass 列表）
# ─────────────────────────────────────────────
Twitch_Elements: list[PageElement] = [
    PageElement(
        name="Click Browse",
        xpath='//a[@href="/directory"]//div[contains(text(), "瀏覽")]',
        description="側邊欄瀏覽按鈕",
    ),
    PageElement(
        name="Search input field",
        xpath='//header[@id="twilight-sticky-header-root"]//input[@placeholder="搜尋"]',
        description="頂部搜尋輸入框",
    ),
    PageElement(
        name="StarCraft II icon",
        xpath='//img[@alt="StarCraft II"]',
        description="StarCraft II 遊戲圖示",
    ),
    PageElement(
        name="StarCraft II title",
        xpath='//p[@title="StarCraft II"]',
        description="StarCraft II 遊戲標題",
    ),
    PageElement(
        name="Follow button",
        xpath='//button[@data-a-target="game-directory-follow-button"]',
        description="追蹤按鈕",
    ),
    PageElement(
        name="3rd video pic",
        xpath='//main[@id="page-main-content-wrapper"]//div[@role="list"]/div[3]//img[@class="tw-image"]',
        description="直播列表第 3 個影片縮圖",
    ),
    PageElement(
        name="h1 title",
        xpath='//h1[contains(text(), "StarCraft II")]',
        description="頁面 h1 標題（含 StarCraft II 字樣）",
    ),
    PageElement(
        name="Description",
        xpath='//main[@id="page-main-content-wrapper"]//p//span',
        description="遊戲描述文字",
    ),
    PageElement(
        name="4th video pic",
        xpath='//*[@id="page-main-content-wrapper"]/div[3]/div/div/div[4]//img[@class="tw-image"]',
        description="直播列表第 4 個影片縮圖",
    ),
    PageElement(
        name="5th video pic",
        xpath='//*[@id="page-main-content-wrapper"]/div[3]/div/div/div[5]//img[@class="tw-image"]',
        description="直播列表第 5 個影片縮圖",
    ),
    PageElement(
        name="Video Controller",
        xpath='//section[@id="channel-player"]',
        description="影片播放器區塊",
    ),
    PageElement(
        name="Check controller is hidden",
        xpath='//section[@id="channel-player"]/parent::div[@data-a-visible="false"]',
        description="檢查播放器外層容器是否隱藏",
        required=False,
    ),
    PageElement(
        name="Check controller div is hidden",
        xpath='//div[@data-a-visible="false"]',
        description="檢查 div 層級是否隱藏",
        required=False,
    ),
]

# ─────────────────────────────────────────────
# 向後相容：保持 Cathay_Xpath / Twitch_Xpath 的 dict 用法
# 既有程式碼（如 Cathay_Xpath['Menu']）仍可正常運作
# ─────────────────────────────────────────────
Cathay_Xpath = build_element_map(Cathay_Elements)
Twitch_Xpath = build_element_map(Twitch_Elements)
