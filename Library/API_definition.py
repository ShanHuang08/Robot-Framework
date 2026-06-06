import requests
import urllib3
from Library.Robot_definition import log, log_color
urllib3.disable_warnings()
from time import perf_counter, sleep
import httpx


class API_Methods():

    # ─────────────────────────────────────────────
    # 核心方法：統一處理所有 HTTP 請求與例外
    # GET / PATCH / POST / PUT / DELETE 皆呼叫此方法，避免重複程式碼
    # ─────────────────────────────────────────────
    def _send_request(self, method: str, url: str, params=None, body=None,
                      auth=None, timeout=10, exp_code=None, allow_retry=False, retries=3):
        """
        統一發送 HTTP 請求的核心方法，所有公開方法皆透過此方法執行。

        參數:
            method:      HTTP 方法，如 'GET'、'POST'、'PATCH'、'PUT'、'DELETE'
            url:         請求的目標 URL
            params:      URL 查詢參數（選填）
            body:        請求體，會以 JSON 格式傳送（選填）
            auth:        認證資訊，如 (username, password) 元組（選填）
            timeout:     等待回應的超時秒數，預設 10 秒
            exp_code:    預期的 HTTP 狀態碼（僅用於日誌記錄，不做實際驗證）
            allow_retry: 超時時是否自動重試（目前僅 GET 使用）
            retries:     最大重試次數，預設 3 次
        """
        # 組合日誌訊息：有 params 時一併記錄
        params_info = f" with params {params}" if params else ""
        body_info = f" and body {body}" if body else ""
        log(f"making {method} request to {url}{params_info}{body_info} and expected return {exp_code}")

        try:
            # body 為 None 時不傳 json，避免 requests 送出 Content-Type: application/json
            if body is not None:
                response = requests.request(method, url, params=params, auth=auth,
                                            json=body, verify=False, timeout=timeout)
            else:
                response = requests.request(method, url, params=params, auth=auth,
                                            verify=False, timeout=timeout)
            return response

        # ── 連線超時：GET 支援重試，其他方法直接拋出例外 ──
        except requests.exceptions.ConnectTimeout as e:
            if allow_retry:
                log(f'ConnectTimeout，啟動重試: {e}')
                return self.Retry_api(method, url, auth, retries)
            raise Exception(f'ConnectTimeout: {e}')

        # ── 一般請求超時：GET 支援重試，其他方法直接拋出例外 ──
        except requests.exceptions.Timeout as e:
            if allow_retry:
                log(f'Timeout，啟動重試: {e}')
                return self.Retry_api(method, url, auth, retries)
            raise Exception(f'Timeout: {e}')

        # ── HTTP 錯誤（4xx / 5xx）──
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')

        # ── 連線層級錯誤（DNS 失敗、拒絕連線等）──
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')

        # ── urllib3 底層讀取超時 ──
        except urllib3.exceptions.ReadTimeoutError as e:
            raise Exception(f'ReadTimeoutError: {e}')


    # ─────────────────────────────────────────────
    # 公開方法：對外保持原有簽名，內部統一呼叫 _send_request
    # ─────────────────────────────────────────────
    def GET_Request(self, url, params=None, auth=None, timeout=20, retries=3, exp_code=None):
        """
        發送 GET 請求。
        預設 timeout 20 秒，超時會自動重試 3 次。
        """
        return self._send_request('GET', url, params=params, auth=auth,
                                  timeout=timeout, exp_code=exp_code,
                                  allow_retry=True, retries=retries)

    def PATCH_Request(self, url, auth, body, params=None, timeout=10, exp_code=None):
        """
        發送 PATCH 請求，帶 JSON body。
        預設 timeout 10 秒，不支援自動重試。
        """
        return self._send_request('PATCH', url, params=params, body=body,
                                  auth=auth, timeout=timeout, exp_code=exp_code)

    def POST_Request(self, url, auth, body, params=None, timeout=10, exp_code=None):
        """
        發送 POST 請求，帶 JSON body。
        預設 timeout 10 秒，不支援自動重試。
        """
        return self._send_request('POST', url, params=params, body=body,
                                  auth=auth, timeout=timeout, exp_code=exp_code)

    def PUT_Request(self, url, auth, body, params=None, timeout=10, exp_code=None):
        """
        發送 PUT 請求，帶 JSON body。
        預設 timeout 10 秒，不支援自動重試。
        """
        return self._send_request('PUT', url, params=params, body=body,
                                  auth=auth, timeout=timeout, exp_code=exp_code)

    def DELETE_Request(self, url, auth, exp_code=None):
        """
        發送 DELETE 請求。
        預設 timeout 10 秒，不支援自動重試。
        """
        return self._send_request('DELETE', url, auth=auth,
                                  timeout=10, exp_code=exp_code)


    # ─────────────────────────────────────────────
    # 重試機制
    # ─────────────────────────────────────────────
    def Retry_api(self, method: str, url: str, auth, retries: int):
        """
        API 重試機制 — 當請求超時時自動重新嘗試。

        參數:
            method:  HTTP 方法（目前主要支援 GET）
            url:     目標 URL
            auth:    認證資訊
            retries: 最大重試次數

        運作方式:
            1. 每次重試前等待 N 秒（退避機制），避免對伺服器造成瞬間壓力
            2. 透過 _send_request 發送請求（allow_retry=False 防止無限遞迴）
            3. 收到 200 立即回傳，非 200 則記錄並繼續重試
            4. 全部失敗後，在 log 中列出每次失敗的狀態碼，並拋出例外
        """
        log(f'<b>開始重試 {method} {url}，最多 {retries} 次</b>')

        fail_records = []  # 記錄每次重試的失敗結果，格式：["1. 503", "2. 504"]

        for attempt in range(1, retries + 1):
            # 退避等待：第 1 次等 1 秒、第 2 次等 2 秒，依此類推
            sleep(attempt)
            log(f'重試第 {attempt} 次（timeout 20 秒）')

            try:
                # 使用 _send_request 發請求，allow_retry=False 避免觸發無限遞迴
                res = self._send_request(method, url, auth=auth, timeout=20,
                                         exp_code=200, allow_retry=False)

                if res.status_code == 200:
                    log(f'重試成功（第 {attempt} 次）')
                    return res
                else:
                    # 記錄非 200 的狀態碼
                    fail_records.append(f"{attempt}. status_code={res.status_code}")
                    log_color(f'重試第 {attempt} 次失敗，status_code={res.status_code}', 'red')

            except Exception as e:
                fail_records.append(f"{attempt}. {type(e).__name__}: {e}")
                log_color(f'重試第 {attempt} 次發生例外: {e}', 'red')

        # 所有重試都失敗，拋出例外並附上失敗明細
        fail_detail = '\n'.join(fail_records)
        raise Exception(f"{method} {url} 重試 {retries} 次後仍失敗：\n{fail_detail}")


    # ─────────────────────────────────────────────
    # 狀態碼驗證
    # ─────────────────────────────────────────────
    def Check_if_status_code_match(self, actual: int, expect: int):
        """
        檢查 HTTP 回應的狀態碼是否符合預期。

        參數:
            actual: 實際回傳的 status_code（如 res.status_code）
            expect: 預期的 status_code（如 200、404）
        """
        if actual != expect:
            log_color(f"Status code should be {expect} but it is {actual}", "red")
        else:
            log(f"Status code is expected: {actual}")
        return actual == expect


    # ─────────────────────────────────────────────
    # 效能測試工具
    # ─────────────────────────────────────────────
    def GET_Avg_Res_Time(self, url: str, count: int):
        """
        使用 httpx 非同步計算 API 平均回應時間。

        參數:
            url:   要測試的 API URL
            count: 請求次數

        回傳:
            True  — 平均回應時間 < 500ms
            False — 平均回應時間 >= 500ms
        """
        import asyncio
        Total_time = 0

        async def get_res_time():
            Total = 0
            async with httpx.AsyncClient(http2=True) as client:
                for _ in range(count):
                    start_time = perf_counter() * 1000
                    await client.get(url)
                    end_time = perf_counter() * 1000
                    elapsed_time = end_time - start_time
                    log(f"GET {url} url execution time = {elapsed_time:.4f} ms")
                    Total += elapsed_time
                return Total

        log(f"<b>===== Check Average Response Time for {count} times =====</b>")
        try:
            Total_time = asyncio.run(get_res_time())
        except Exception as e:
            log(f"Connection Error: {e}")
        log(f"<b>===== Check Average Response Time for {count} times =====</b>")

        Avg_res_Time = Total_time / count
        if Avg_res_Time > 500:
            log_color(f'Average api response time is {Avg_res_Time:.4f} ms, greater than 500 ms', 'red')
            return False
        else:
            log(f'Average api response time is {Avg_res_Time:.4f} ms, less than 500 ms')
            return True

    def measure_overhead(self):
        """測量系統呼叫 perf_counter 本身的開銷時間（毫秒）"""
        start_time = perf_counter() * 1000
        end_time = perf_counter() * 1000
        return end_time - start_time
