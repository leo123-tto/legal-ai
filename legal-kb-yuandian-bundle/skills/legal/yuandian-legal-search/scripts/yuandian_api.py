"""
元典 API 接口调用库 - 完整版
覆盖：法律法规、法条、案例（权威+普通）、企业信息（定位/工商/诉讼/行政/知产）
认证：X-Api-Key 头部
Base：https://open.chineselaw.com/open
"""

import requests
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from config import API_KEY

BASE_URL = "https://open.chineselaw.com/open"

HEADERS_JSON = {
    "accept": "application/json;charset=UTF-8",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY,
}

HEADERS_GET = {
    "accept": "application/json;charset=UTF-8",
    "X-Api-Key": API_KEY,
}

# ─── 底层请求 ────────────────────────────────────────

def _post(path, payload, timeout=30):
    """POST 请求，返回 data 或 None"""
    try:
        resp = requests.post(f"{BASE_URL}{path}", headers=HEADERS_JSON,
                             json=payload, timeout=timeout)
    except requests.Timeout:
        print(f"[超时] {path}: 请求超时 ({timeout}s)")
        return None
    except requests.ConnectionError:
        print(f"[网络错误] {path}: 连接失败")
        return None
    try:
        result = resp.json()
    except Exception:
        print(f"[非JSON响应] {path}: HTTP {resp.status_code}, 内容: {resp.text[:300]}")
        return None
    code = result.get("code")
    if code == 200:
        return result.get("data")
    # 语义检索的返回结构可能不同
    if code is None and result.get("data") is not None:
        return result.get("data")
    print(f"[错误] {path}: code={code}, {result.get('message', result.get('msg', '未知错误'))}")
    return None


def _get(path, params=None, timeout=30):
    """GET 请求，返回 data 或 None"""
    try:
        resp = requests.get(f"{BASE_URL}{path}", headers=HEADERS_GET,
                            params=params, timeout=timeout)
    except requests.Timeout:
        print(f"[超时] {path}: 请求超时 ({timeout}s)")
        return None
    except requests.ConnectionError:
        print(f"[网络错误] {path}: 连接失败")
        return None
    try:
        result = resp.json()
    except Exception:
        print(f"[非JSON响应] {path}: HTTP {resp.status_code}, 内容: {resp.text[:300]}")
        return None
    code = result.get("code")
    if code == 200:
        return result.get("data")
    print(f"[错误] {path}: code={code}, {result.get('message', '未知错误')}")
    return None


def _extract_items(result):
    """标准化分页检索返回：将 {"total": N, "lst": [...]} 转成 [...]，兼容已有列表格式"""
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        lst = result.get("lst") or result.get("list") or result.get("dataList")
        if lst is not None:
            return lst
    return result


def _extract_total(result):
    """提取检索结果总数"""
    if isinstance(result, dict):
        return result.get("total") or result.get("totalCount") or 0
    if isinstance(result, list):
        return len(result)
    return 0


def _fetch_all_pages(func, max_pages=20, page_arg="page_no", sleep_seconds=0):
    """自动翻页拉取企业分页接口。

    用法：_fetch_all_pages(lambda page_no: enterprise_brand(tyshxydm=USCC, page_no=page_no))
    默认最多 20 页，避免积分爆炸；max_pages=0 表示不限制。
    返回合并后的 data dict，list 为所有页拼接，附 _meta。
    """
    import time
    all_items = []
    last = {}
    page_no = 1
    fetched_pages = 0
    total = None
    while True:
        data = func(page_no)
        if not isinstance(data, dict):
            break
        last = data
        items = data.get("list") or data.get("lst") or []
        all_items.extend(items)
        fetched_pages += 1
        if total is None:
            total = data.get("total") or data.get("totalCount")
        if not data.get("hasMore"):
            break
        if max_pages and fetched_pages >= max_pages:
            break
        page_no += 1
        if sleep_seconds:
            time.sleep(sleep_seconds)
    result = {k: v for k, v in last.items() if k not in ("list", "lst")}
    result["list"] = all_items
    result["_meta"] = {
        "fetched_pages": fetched_pages,
        "fetched_items": len(all_items),
        "total": total,
        "max_pages_limit": max_pages if max_pages else "unlimited",
    }
    return result


# ═══════════════════════════════════════════════════════
# A. 法律法规组（POST）
# ═══════════════════════════════════════════════════════

def search_fagui(keyword=None, search_mode=None, fgmc=None, sxx=None,
                 xljb_1=None, fbrq_start=None, fbrq_end=None,
                 ssrq_start=None, ssrq_end=None, top_k=10):
    """法规关键词检索（最常用法规入口）"""
    payload = {"top_k": top_k}
    if keyword: payload["keyword"] = keyword
    if search_mode: payload["search_mode"] = search_mode
    if fgmc: payload["fgmc"] = fgmc
    if sxx: payload["sxx"] = sxx
    if xljb_1: payload["xljb_1"] = xljb_1
    if fbrq_start: payload["fbrq_start"] = fbrq_start
    if fbrq_end: payload["fbrq_end"] = fbrq_end
    if ssrq_start: payload["ssrq_start"] = ssrq_start
    if ssrq_end: payload["ssrq_end"] = ssrq_end
    return _post("/rh_fg_search", payload)


def get_fagui_detail(id=None, fgmc=None, refer_date=None):
    """法规详情（优先用 id）"""
    payload = {}
    if id: payload["id"] = id
    if fgmc: payload["fgmc"] = fgmc
    if refer_date: payload["refer_date"] = refer_date
    return _post("/rh_fg_detail", payload)


def search_fatiao(keyword, search_mode=None, fgmc=None, sxx=None,
                  xljb_1=None, fbrq_start=None, fbrq_end=None,
                  ssrq_start=None, ssrq_end=None, top_k=10):
    """法条关键词检索"""
    payload = {"keyword": keyword, "top_k": top_k}
    if search_mode: payload["search_mode"] = search_mode
    if fgmc: payload["fgmc"] = fgmc
    if sxx: payload["sxx"] = sxx
    if xljb_1: payload["xljb_1"] = xljb_1
    if fbrq_start: payload["fbrq_start"] = fbrq_start
    if fbrq_end: payload["fbrq_end"] = fbrq_end
    if ssrq_start: payload["ssrq_start"] = ssrq_start
    if ssrq_end: payload["ssrq_end"] = ssrq_end
    return _post("/rh_ft_search", payload)


def get_fatiao_detail(id=None, fgmc=None, ftnum=None, refer_date=None):
    """法条详情"""
    payload = {}
    if id: payload["id"] = id
    if fgmc: payload["fgmc"] = fgmc
    if ftnum: payload["ftnum"] = ftnum
    if refer_date: payload["refer_date"] = refer_date
    return _post("/rh_ft_detail", payload)


def law_vector_search(query, rewrite_flag=True, effect1=None, sxx="现行有效",
                      top_k=10):
    """法规语义检索——适合不知精确标题时按主题/问题搜索"""
    payload = {"query": query, "rewrite_flag": rewrite_flag, "return_num": top_k}
    filters = {}
    if sxx: filters["sxx"] = sxx
    if effect1: filters["effect1"] = effect1
    if filters:
        payload["fatiao_filter"] = filters
    return _post("/law_vector_search", payload)


# ═══════════════════════════════════════════════════════
# B. 案例文书组（POST + GET）
# ═══════════════════════════════════════════════════════

def search_qwal(qw=None, search_mode=None, title=None, ah=None,
                ay=None, jbdw=None, xzqh_p=None, wszl=None, ajlb=None,
                ja_start=None, ja_end=None, top_k=10):
    """权威案例关键词检索（指导性/典型案例/公报案例）"""
    payload = {"top_k": top_k}
    if qw: payload["qw"] = qw
    if search_mode: payload["search_mode"] = search_mode
    if title: payload["title"] = title
    if ah: payload["ah"] = ah
    if ay: payload["ay"] = ay
    if jbdw: payload["jbdw"] = jbdw
    if xzqh_p: payload["xzqh_p"] = xzqh_p
    if wszl: payload["wszl"] = wszl
    if ajlb: payload["ajlb"] = ajlb
    if ja_start: payload["ja_start"] = ja_start
    if ja_end: payload["ja_end"] = ja_end
    return _post("/rh_qwal_search", payload)


def search_ptal(qw=None, fxgc=None, search_mode=None, title=None, ah=None,
                ay=None, jbdw=None, xzqh_p=None, wszl=None, ajlb=None,
                ja_start=None, ja_end=None, yyft=None, ft_search_mode=None,
                top_k=10):
    """普通案例关键词检索"""
    payload = {"top_k": top_k}
    if qw: payload["qw"] = qw
    if fxgc: payload["fxgc"] = fxgc
    if search_mode: payload["search_mode"] = search_mode
    if title: payload["title"] = title
    if ah: payload["ah"] = ah
    if ay: payload["ay"] = ay
    if jbdw: payload["jbdw"] = jbdw
    if xzqh_p: payload["xzqh_p"] = xzqh_p
    if wszl: payload["wszl"] = wszl
    if ajlb: payload["ajlb"] = ajlb
    if ja_start: payload["ja_start"] = ja_start
    if ja_end: payload["ja_end"] = ja_end
    if yyft: payload["yyft"] = yyft
    if ft_search_mode: payload["ft_search_mode"] = ft_search_mode
    return _post("/rh_ptal_search", payload)


def get_case_detail(type, id=None, ah=None):
    """案例详情（type='qwal' 或 'ptal'）"""
    params = {"type": type}
    if id: params["id"] = id
    if ah: params["ah"] = ah
    return _get("/rh_case_details", params)


def case_vector_search(query, rewrite_flag=True, xzqh_p=None, xzqh_c=None,
                       cj=None, fayuan=None, wszl=None, wenshu_type=None,
                       dianxing=None, ja_start=None, ja_end=None, top_k=10):
    """案例语义检索——适合按争点/问题找裁判规则"""
    payload = {"query": query, "rewrite_flag": rewrite_flag, "return_num": top_k}
    filters = {}
    if xzqh_p: filters["xzqh_p"] = xzqh_p
    if xzqh_c: filters["xzqh_c"] = xzqh_c
    if cj: filters["cj"] = cj
    if fayuan: filters["fayuan"] = fayuan
    if wszl: filters["wszl"] = wszl
    if wenshu_type: filters["wenshu_type"] = wenshu_type
    if dianxing: filters["dianxing"] = dianxing
    if ja_start: filters["ja_start"] = ja_start
    if ja_end: filters["ja_end"] = ja_end
    if filters:
        payload["wenshu_filter"] = filters
    return _post("/case_vector_search", payload)


# ═══════════════════════════════════════════════════════
# C. 企业信息组（全部 GET）
# ═══════════════════════════════════════════════════════

# ── C1. 企业定位 ──

def enterprise_search(name, top_k=10):
    """按企业名称关键词搜索企业候选列表（轻量）"""
    params = {"name": name, "top_k": top_k}
    return _get("/rh_enterpriseSearch", params)


def get_company_info(name, num=2):
    """按企业名称/股票简称查询企业详情聚合（重）"""
    params = {"name": name, "num": num}
    return _get("/rh_company_info", params)


def get_company_detail(id=None, tyshxydm=None):
    """按 id 或统一社会信用代码获取企业聚合全景"""
    params = {}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_company_detail", params)


def get_enterprise_base_info(id=None, tyshxydm=None):
    """企业基本信息（轻量版）"""
    params = {}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseBaseInfo", params)


# ── C2. 工商与治理 ──

def enterprise_change_info(id=None, tyshxydm=None, page_no=1):
    """企业变更记录列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseChangeInfo", params)


def enterprise_pledge(id=None, tyshxydm=None, page_no=1):
    """企业股权出质信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterprisePledge", params)


def enterprise_frozen_equity(id=None, tyshxydm=None, page_no=1):
    """企业股权冻结信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseFrozenEquity", params)


def enterprise_guaranty(id=None, tyshxydm=None, page_no=1):
    """企业对外担保信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseGuaranty", params)


def enterprise_out_invest(id=None, tyshxydm=None, page_no=1):
    """企业对外投资信息列表（财产线索/关联方/尽调第10章高价值接口）"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseOutInvest", params)


# ── C3. 诉讼与执行风险 ──

def enterprise_writ_agg(id=None, tyshxydm=None):
    """企业涉诉信息聚合统计（先看轮廓，再看明细）"""
    params = {}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseWritAgg", params)


def enterprise_writ_list(id=None, tyshxydm=None, page_no=1):
    """企业涉诉文书列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseWritList", params)


def enterprise_court_session_notice(id=None, tyshxydm=None, page_no=1):
    """企业开庭公告列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseCourtSessionNotice", params)


def enterprise_court_notice(id=None, tyshxydm=None, page_no=1):
    """企业法院公告列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseCourtNotice", params)


def enterprise_executions(id=None, tyshxydm=None, page_no=1):
    """企业失信被执行人信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseExecutions", params)


def enterprise_executed_person(id=None, tyshxydm=None, page_no=1):
    """企业被执行人信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseExecutedPerson", params)


# ── C4. 行政与合规风险 ──

def enterprise_punishment(id=None, tyshxydm=None, page_no=1):
    """企业行政处罚信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterprisePunishment", params)


def enterprise_abnormal_operation(id=None, tyshxydm=None, page_no=1):
    """企业经营异常记录列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseAbnormalOperation", params)


def enterprise_serious_illegal(id=None, tyshxydm=None, page_no=1):
    """企业严重违法记录列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseSeriousIllegal", params)


def enterprise_corporate_tax(id=None, tyshxydm=None, page_no=1):
    """企业欠税公告记录列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseCorporateTax", params)


# ── C5. 知识产权与线上资产 ──

def enterprise_brand(id=None, tyshxydm=None, page_no=1):
    """企业商标信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseBrand", params)


def enterprise_patent(id=None, tyshxydm=None, page_no=1):
    """企业专利信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterprisePatent", params)


def enterprise_soft_right(id=None, tyshxydm=None, page_no=1):
    """企业软件著作权信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseSoftRight", params)


def enterprise_works_right(id=None, tyshxydm=None, page_no=1):
    """企业作品著作权信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseWorksRight", params)


def enterprise_icp(id=None, tyshxydm=None, page_no=1):
    """企业网站备案信息列表"""
    params = {"pageNo": page_no}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseIcp", params)


# ── C6. 企业聚合总览 ──

def enterprise_aggregation_summary(id=None, tyshxydm=None):
    """企业聚合总览——一次性拉取18个维度的统计汇总（对外投资/商标/专利/软著/著作权/网站备案/变更记录/失信/被执行/开庭公告/法院公告/股权冻结/行政处罚/股权出质/对外担保/经营异常/欠税公告/严重违法），非年度统计取 top 20。省积分，适合尽调第一眼总览。"""
    params = {}
    if id: params["id"] = id
    if tyshxydm: params["tyshxydm"] = tyshxydm
    return _get("/rh_enterpriseAggregationSummary", params)
