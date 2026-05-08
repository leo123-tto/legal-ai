"""
元典律师检索 - API 客户端（通过引用避免文件重名冲突）
"""
import sys
import os

_api_ref_path = os.path.dirname(__file__)
if _api_ref_path not in sys.path:
    sys.path.insert(0, _api_ref_path)

# 从元技能导入原始模块，不重名冲突
import importlib
_yuandian_ref = importlib.import_module("yuandian_api")

# ── 重新暴露所有公共接口 ──

# 底层
_post = _yuandian_ref._post
_get = _yuandian_ref._get
_extract_items = _yuandian_ref._extract_items
_extract_total = _yuandian_ref._extract_total
_fetch_all_pages = _yuandian_ref._fetch_all_pages

# 法律法规
search_fagui = _yuandian_ref.search_fagui
get_fagui_detail = _yuandian_ref.get_fagui_detail
search_fatiao = _yuandian_ref.search_fatiao
get_fatiao_detail = _yuandian_ref.get_fatiao_detail
law_vector_search = _yuandian_ref.law_vector_search

# 案例
search_qwal = _yuandian_ref.search_qwal
search_ptal = _yuandian_ref.search_ptal
get_case_detail = _yuandian_ref.get_case_detail
case_vector_search = _yuandian_ref.case_vector_search

# 企业定位
enterprise_search = _yuandian_ref.enterprise_search
get_company_info = _yuandian_ref.get_company_info
get_company_detail = _yuandian_ref.get_company_detail
get_enterprise_base_info = _yuandian_ref.get_enterprise_base_info

# 工商治理
enterprise_change_info = _yuandian_ref.enterprise_change_info
enterprise_pledge = _yuandian_ref.enterprise_pledge
enterprise_frozen_equity = _yuandian_ref.enterprise_frozen_equity
enterprise_guaranty = _yuandian_ref.enterprise_guaranty
enterprise_out_invest = _yuandian_ref.enterprise_out_invest

# 诉讼执行
enterprise_writ_agg = _yuandian_ref.enterprise_writ_agg
enterprise_writ_list = _yuandian_ref.enterprise_writ_list
enterprise_court_session_notice = _yuandian_ref.enterprise_court_session_notice
enterprise_court_notice = _yuandian_ref.enterprise_court_notice
enterprise_executions = _yuandian_ref.enterprise_executions
enterprise_executed_person = _yuandian_ref.enterprise_executed_person

# 行政合规
enterprise_punishment = _yuandian_ref.enterprise_punishment
enterprise_abnormal_operation = _yuandian_ref.enterprise_abnormal_operation
enterprise_serious_illegal = _yuandian_ref.enterprise_serious_illegal
enterprise_corporate_tax = _yuandian_ref.enterprise_corporate_tax

# 知识产权
enterprise_brand = _yuandian_ref.enterprise_brand
enterprise_patent = _yuandian_ref.enterprise_patent
enterprise_soft_right = _yuandian_ref.enterprise_soft_right
enterprise_works_right = _yuandian_ref.enterprise_works_right
enterprise_icp = _yuandian_ref.enterprise_icp

# 企业聚合总览
enterprise_aggregation_summary = _yuandian_ref.enterprise_aggregation_summary
