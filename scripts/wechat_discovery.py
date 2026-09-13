#!/usr/bin/env python3
"""Minimal no-login WeChat article discovery / canonicalization helper.

Source ownership: ``wechat.discovery`` (test-stage route established by
TASK-20260913-012). It bridges the concrete gap observed in evidence:

    Sogou weixin result page (candidate generator)
      -> wrapped ``/link?url=...`` URL (NOT canonical, never returned as such)
      -> same-session GET with Referer returns a JS-assembly body
      -> assembled ``https://mp.weixin.qq.com/s?...&signature=...`` URL

Boundaries inherited from the TASK-20260913-012 contract:

- public result pages only; no login, no imported/credential cookies. The only
  cookies used are the anonymous ones Sogou itself sets during this request
  flow (session-scoped ``CookieJar``, never persisted);
- CAPTCHA / anti-bot bodies are classified and surfaced, never bypassed and
  never hammered (bounded pacing between resolutions);
- discovery output is candidate evidence, not truth; callers must verify a
  promoted URL per Phase B (host, canonical form, title material match,
  publisher identity) before treating it as usable.

The module is standard library only and prints JSON to stdout; it never writes
files. Pure helpers (URL classification, HTML extraction, title matching) are
separated from the network layer so focused tests run offline.
"""

from __future__ import annotations

import argparse
import difflib
import http.cookiejar
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
SOGOU_WEIXIN_SEARCH = "https://weixin.sogou.com/weixin"
MP_HOST = "mp.weixin.qq.com"

_CANDIDATE_RE = re.compile(r'<h3>\s*<a[^>]*href="(/link\?url=[^"]+)"[^>]*>(.*?)</a>', re.S)
_ACCOUNT_TAIL_RE = re.compile(
    r'class="(?:account|txt-box|s-p)[^"]*"[^>]*>.*?(?:alt="([^"]*)"|>([^<]{2,30}))<', re.S
)
_ASSEMBLED_FRAGMENTS_RE = re.compile(r"url \+= '([^']*)'")
_JS_REPLACE_RE = re.compile(r'window\.location\.replace\("([^"]+)"\)')

_MSG_TITLE_RE = re.compile(r"var msg_title = '(.*?)'")
_NICKNAME_RE = re.compile(r'var nickname = "?([^";]*)"?')
_JS_NAME_RE = re.compile(r'id="js_name"[^>]*>\s*([^<]+?)\s*<')
_OG_TITLE_RE = re.compile(r'<meta property="og:title" content="([^"]*)"')
_OG_AUTHOR_RE = re.compile(r'<meta property="og:article:author" content="([^"]*)"')
_PUBLISH_TIME_RE = re.compile(r"var ct = \"(\d+)\"")
_CREATE_TIME_RE = re.compile(r'var createTime = \'([^\']*)\'')


# ---------------------------------------------------------------------------
# Pure helpers (offline-testable)
# ---------------------------------------------------------------------------

def classify_mp_url(url: str) -> Dict[str, Any]:
    """Classify a candidate URL without fetching it.

    Returns ``{"host_ok": bool, "form": str}`` where ``form`` is one of:
    ``public_slug`` (/s/<id>), ``signed_query`` (/s?src=..&signature=..),
    ``wrapped_link`` (Sogou /link?url=), ``search_page`` (/s? with no
    signature, e.g. listing pages), ``not_wechat``.
    """
    parsed = urllib.parse.urlsplit(url)
    host_ok = parsed.netloc.lower() == MP_HOST
    if not host_ok:
        return {"host_ok": False, "form": "not_wechat"}
    path = parsed.path
    query = urllib.parse.parse_qs(parsed.query)
    if path.startswith("/link"):
        return {"host_ok": False, "form": "wrapped_link"}
    if path.rstrip("/") == "/s":
        if query.get("signature"):
            return {"host_ok": True, "form": "signed_query"}
        return {"host_ok": True, "form": "search_page"}
    if re.fullmatch(r"/s/[\w-]+", path):
        return {"host_ok": True, "form": "public_slug"}
    return {"host_ok": True, "form": "other"}


def is_canonical_mp_url(url: str) -> bool:
    """True iff the URL is an mp.weixin.qq.com article URL (never a /link wrap)."""
    cls = classify_mp_url(url)
    return cls["host_ok"] and cls["form"] in ("public_slug", "signed_query")


def normalize_title(text: str) -> str:
    """Fold width/case and strip punctuation/whitespace for material matching."""
    folded = unicodedata.normalize("NFKC", text or "").casefold()
    return re.sub(r"[\s\W_]+", "", folded, flags=re.UNICODE)


def title_material_match(discovery_title: str, page_title: str) -> bool:
    """Phase B title check: containment or >=0.6 similarity after normalization."""
    a, b = normalize_title(discovery_title), normalize_title(page_title)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.6


def extract_results(html: str) -> List[Dict[str, Optional[str]]]:
    """Extract candidate (title, account, link_path) triples from a result page."""
    out: List[Dict[str, Optional[str]]] = []
    for m in _CANDIDATE_RE.finditer(html):
        title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        title = re.sub(r"\s+", " ", title)
        tail = html[m.end(): m.end() + 1500]
        acc = _ACCOUNT_TAIL_RE.search(tail)
        account = (acc.group(1) or acc.group(2)).strip() if acc else None
        out.append({"title": title, "account": account, "link_path": m.group(1)})
    return out


def classify_link_body(body: str) -> Dict[str, Any]:
    """Classify a resolved /link response body.

    ``classification`` is one of ``captcha``, ``js_assembled`` (with
    ``assembled_url``), ``js_replace`` (with ``assembled_url``), ``unknown``.
    """
    if "antispider" in body or "验证码" in body or "VerifyCode" in body:
        return {"classification": "captcha"}
    if "window.location.replace" in body:
        fragments = _ASSEMBLED_FRAGMENTS_RE.findall(body)
        if fragments:
            return {"classification": "js_assembled", "assembled_url": "".join(fragments)}
        m = _JS_REPLACE_RE.search(body)
        if m:
            return {"classification": "js_replace", "assembled_url": m.group(1)}
    return {"classification": "unknown"}


def extract_article_fields(html: str) -> Dict[str, Optional[str]]:
    """Extract Phase B/C fields from a canonical article page."""
    title = None
    m = _MSG_TITLE_RE.search(html)
    if m and m.group(1).strip():
        title = m.group(1).strip()
    if not title:
        m = _OG_TITLE_RE.search(html)
        if m:
            title = m.group(1).strip()
    account = None
    m = _NICKNAME_RE.search(html)
    if m and m.group(1).strip():
        account = m.group(1).strip()
    if not account:
        m = _JS_NAME_RE.search(html)
        if m:
            account = m.group(1).strip()
    author = None
    m = _OG_AUTHOR_RE.search(html)
    if m:
        author = m.group(1).strip()
    publish_time = None
    m = _CREATE_TIME_RE.search(html) or _PUBLISH_TIME_RE.search(html)
    if m:
        publish_time = m.group(1).strip()
    return {"title": title, "account": account, "author": author, "publish_time": publish_time}


def verify_candidate(
    discovery_title: Optional[str],
    url: str,
    article_fields: Dict[str, Optional[str]],
) -> Dict[str, Any]:
    """Phase B verification of a promoted candidate against its page fields."""
    cls = classify_mp_url(url)
    title_match = (
        title_material_match(discovery_title, article_fields.get("title") or "")
        if discovery_title and article_fields.get("title")
        else None
    )
    return {
        "url": url,
        "host_ok": cls["host_ok"],
        "form": cls["form"],
        "canonical": is_canonical_mp_url(url),
        "title_match": title_match,
        "page_title": article_fields.get("title"),
        "account": article_fields.get("account"),
        "author": article_fields.get("author"),
    }


# ---------------------------------------------------------------------------
# Network layer (thin orchestration; stdlib only, no login, nothing persisted)
# ---------------------------------------------------------------------------

class SogouDiscovery:
    """Session-scoped no-login discovery against public Sogou weixin pages."""

    def __init__(self, timeout: float = 40.0, resolve_pace_seconds: float = 2.0):
        self.timeout = timeout
        self.resolve_pace_seconds = resolve_pace_seconds
        self._cookie_jar = http.cookiejar.CookieJar()
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cookie_jar))

    def _get(self, url: str, referer: Optional[str] = None) -> Tuple[int, str, str]:
        headers = {"User-Agent": USER_AGENT}
        if referer:
            headers["Referer"] = referer
        req = urllib.request.Request(url, headers=headers)
        try:
            with self._opener.open(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.status, body, resp.geturl()
        except urllib.error.HTTPError as exc:  # type: ignore[attr-defined]
            body = exc.read().decode("utf-8", errors="replace")
            return exc.code, body, url

    def search(self, query: str) -> Dict[str, Any]:
        search_url = SOGOU_WEIXIN_SEARCH + "?" + urllib.parse.urlencode({"type": "2", "query": query})
        status, body, final_url = self._get(search_url)
        captcha = "antispider" in body or "验证码" in body or "VerifyCode" in body
        return {
            "query": query,
            "http": status,
            "captcha": captcha,
            "candidates": [] if captcha else extract_results(body),
            "referer": final_url,
        }

    def resolve(self, link_path: str, referer: str) -> Dict[str, Any]:
        status, body, _ = self._get(SOGOU_WEIXIN_SEARCH.rstrip("/weixin") + link_path, referer=referer)
        result: Dict[str, Any] = {"http": status}
        result.update(classify_link_body(body))
        if result.get("assembled_url"):
            result["canonical_url"] = result["assembled_url"]
        return result

    def discover(self, query: str, max_resolve: int = 2) -> Dict[str, Any]:
        """Search then resolve the top candidates; on CAPTCHA it stops (no retry)."""
        out: Dict[str, Any] = {"query": query}
        search = self.search(query)
        out.update({k: search[k] for k in ("http", "captcha")})
        out["candidates"] = search["candidates"][:max_resolve]
        out["resolutions"] = []
        if search["captcha"]:
            out["stopped_reason"] = "captcha_on_search"
            return out
        for cand in out["candidates"]:
            res = self.resolve(cand["link_path"], referer=search["referer"])
            res["candidate_title"] = cand["title"]
            out["resolutions"].append(res)
            time.sleep(self.resolve_pace_seconds)
        return out


def verify_article_url(url: str) -> Dict[str, Any]:
    """Fetch a canonical article URL and return Phase B verification fields."""
    opener = urllib.request.build_opener()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    status, body = None, ""
    try:
        with opener.open(req, timeout=40) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:  # type: ignore[attr-defined]
        status = exc.code
    fields = extract_article_fields(body)
    result = verify_candidate(None, url, fields)
    result["http"] = status
    return result


# ---------------------------------------------------------------------------
# CLI (stdout JSON only; no file writes)
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_search = sub.add_parser("search", help="list discovery candidates for a query")
    p_search.add_argument("query")
    p_discover = sub.add_parser("discover", help="search + resolve top candidates")
    p_discover.add_argument("query")
    p_discover.add_argument("--max-resolve", type=int, default=2)
    p_verify = sub.add_parser("verify", help="Phase B verification of a candidate URL")
    p_verify.add_argument("url")
    args = parser.parse_args(argv)

    if args.command == "search":
        payload = SogouDiscovery().search(args.query)
    elif args.command == "discover":
        payload = SogouDiscovery().discover(args.query, max_resolve=args.max_resolve)
    else:
        payload = verify_article_url(args.url)
    print(json.dumps(payload, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
