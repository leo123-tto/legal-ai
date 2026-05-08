"""
Tavily 检索封装 — 用于法律研究中的二手文献检索
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from config import TAVILY_API_KEY
from tavily import TavilyClient

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_secondary_sources(query, max_results=10, search_depth="advanced",
                             include_domains=None, exclude_domains=None):
    kwargs = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
    }
    if include_domains:
        kwargs["include_domains"] = include_domains
    if exclude_domains:
        kwargs["exclude_domains"] = exclude_domains
    result = client.search(**kwargs)
    return result.get("results", [])


def search_lawfirm_articles(query, max_results=5):
    lawfirm_domains = [
        "kwm.com", "junhe.com", "fangda-partners.com", "zhonglun.com",
        "tongshang.com", "haiwen-law.com", "hankunlaw.com", "jingtian.com",
        "meritsandtree.com", "globe-law.com", "allbrightlaw.com", "dehenglaw.com",
        "grandalllaw.com", "yingkelawyer.com",
    ]
    return search_secondary_sources(query=query, max_results=max_results, include_domains=lawfirm_domains)


def search_government_interpretations(query, max_results=5):
    gov_domains = [
        "gov.cn", "npc.gov.cn", "court.gov.cn", "spp.gov.cn", "moj.gov.cn",
        "mhrss.gov.cn", "samr.gov.cn", "csrc.gov.cn", "pbc.gov.cn", "mofcom.gov.cn",
    ]
    return search_secondary_sources(query=query, max_results=max_results, include_domains=gov_domains)


def search_academic_sources(query, max_results=5):
    academic_domains = [
        "cnki.net", "wanfangdata.com.cn", "pku.edu.cn", "tsinghua.edu.cn", "ruc.edu.cn",
        "cupl.edu.cn", "whu.edu.cn", "zuel.edu.cn", "ecupl.edu.cn", "iolaw.org.cn",
        "chinalawreview.org", "legaldaily.com.cn", "legal.people.com.cn",
    ]
    return search_secondary_sources(query=query, max_results=max_results, include_domains=academic_domains)
