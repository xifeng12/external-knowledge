"""Focused offline tests for scripts/wechat_discovery.py (wechat.discovery helper).

Covers URL classification/normalization, candidate extraction, link-body
classification, article field extraction, and Phase B title material matching.
No network access, no file writes.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ek_wechat_discovery", ROOT / "scripts" / "wechat_discovery.py")
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


SOGOU_HTML = """
<div class="txt-box">
  <h3><a href="/link?url=http://mp.weixin.qq.com/s%3F__biz%3DMzA%26sn%3Dabc" target="_blank">不可不知的
    <em>ArcGIS</em> Python开发（PPT可下载）</a></h3>
  <p class="txt-info">对Python感兴趣的不要错过这个PPT</p>
  <div class="s-p"><a href="javascript:void(0);" data-uigs="article_account1"><span>GIS前沿</span></a></div>
</div>
<div class="txt-box">
  <h3><a href="/link?url=http://mp.weixin.qq.com/s%3F__biz%3DMzB%26sn%3Ddef" target="_blank">第二篇文章标题</a></h3>
  <div class="s-p"><a data-uigs="article_account2">图说新语</a></div>
</div>
"""

CAPTCHA_BODY = "<html><head><title>antispider</title></head><body>请输入验证码 VerifyCode</body></html>"

ASSEMBLY_BODY = """
<html><body><script>
var url = '';
url += 'https://mp.weixin.qq.com/s?src=11&timestamp=1789264699&ver=6963';
url += '&signature=H%2AxP2-3GBaEiv4ziv6UxCmuntpUPm3H6TE34lUSw%2AoI4B&new=1';
window.location.replace(url);
</script></body></html>
"""

JS_REPLACE_BODY = '<html><body><script>window.location.replace("https://mp.weixin.qq.com/s/AbCdEf123");</script></body></html>'

ARTICLE_HTML = """
<html><head>
<meta property="og:title" content="不可不知的ArcGIS Python开发（PPT可下载）"/>
<meta property="og:article:author" content="李远祥"/>
</head><body>
<script>
var msg_title = '不可不知的ArcGIS Python开发（PPT可下载）';
var nickname = "GIS前沿";
var createTime = '2020-07-18';
</script>
<h1 class="rich_media_title" id="activity-name"></h1>
<div id="js_name" style="visibility:hidden;">GIS前沿</div>
</body></html>
"""


class UrlClassificationTests(unittest.TestCase):
    def test_public_slug_is_canonical(self):
        cls = mod.classify_mp_url("https://mp.weixin.qq.com/s/XO8Jqu0vEmbikIdrPD598A")
        self.assertEqual(cls, {"host_ok": True, "form": "public_slug"})
        self.assertTrue(mod.is_canonical_mp_url("https://mp.weixin.qq.com/s/XO8Jqu0vEmbikIdrPD598A"))

    def test_signed_query_is_canonical(self):
        url = "https://mp.weixin.qq.com/s?src=11&timestamp=1789264699&ver=6963&signature=H%2AxP2&new=1"
        cls = mod.classify_mp_url(url)
        self.assertEqual(cls, {"host_ok": True, "form": "signed_query"})
        self.assertTrue(mod.is_canonical_mp_url(url))

    def test_wrapped_link_is_never_canonical(self):
        url = "https://weixin.sogou.com/link?url=http%3A%2F%2Fmp.weixin.qq.com%2Fs%3Fsn%3Dabc"
        self.assertEqual(mod.classify_mp_url(url), {"host_ok": False, "form": "not_wechat"})
        self.assertFalse(mod.is_canonical_mp_url(url))
        # even on the mp host itself, /link is not a canonical article form
        self.assertEqual(mod.classify_mp_url("https://mp.weixin.qq.com/link?url=x")["form"], "wrapped_link")
        self.assertFalse(mod.is_canonical_mp_url("https://mp.weixin.qq.com/link?url=x"))

    def test_search_page_and_foreign_host(self):
        self.assertEqual(mod.classify_mp_url("https://mp.weixin.qq.com/s?query=abc")["form"], "search_page")
        self.assertFalse(mod.is_canonical_mp_url("https://mp.weixin.qq.com/s?query=abc"))
        self.assertEqual(mod.classify_mp_url("https://example.com/s/abc")["form"], "not_wechat")


class CandidateExtractionTests(unittest.TestCase):
    def test_extract_results_titles_accounts_links(self):
        cands = mod.extract_results(SOGOU_HTML)
        self.assertEqual(len(cands), 2)
        self.assertEqual(cands[0]["title"], "不可不知的 ArcGIS Python开发（PPT可下载）")
        self.assertEqual(cands[0]["account"], "GIS前沿")
        self.assertTrue(cands[0]["link_path"].startswith("/link?url="))
        self.assertEqual(cands[1]["title"], "第二篇文章标题")
        self.assertEqual(cands[1]["account"], "图说新语")


class LinkBodyClassificationTests(unittest.TestCase):
    def test_captcha_is_classified_not_bypassed(self):
        self.assertEqual(mod.classify_link_body(CAPTCHA_BODY), {"classification": "captcha"})

    def test_js_assembly_yields_assembled_url(self):
        res = mod.classify_link_body(ASSEMBLY_BODY)
        self.assertEqual(res["classification"], "js_assembled")
        self.assertTrue(res["assembled_url"].startswith("https://mp.weixin.qq.com/s?src=11"))
        self.assertIn("signature=H%2AxP2", res["assembled_url"])

    def test_js_replace_direct_url(self):
        res = mod.classify_link_body(JS_REPLACE_BODY)
        self.assertEqual(res["classification"], "js_replace")
        self.assertEqual(res["assembled_url"], "https://mp.weixin.qq.com/s/AbCdEf123")

    def test_unknown_body(self):
        self.assertEqual(mod.classify_link_body("<html><body>hello</body></html>"), {"classification": "unknown"})


class ArticleFieldTests(unittest.TestCase):
    def test_extract_article_fields(self):
        fields = mod.extract_article_fields(ARTICLE_HTML)
        self.assertEqual(fields["title"], "不可不知的ArcGIS Python开发（PPT可下载）")
        self.assertEqual(fields["account"], "GIS前沿")
        self.assertEqual(fields["author"], "李远祥")
        self.assertEqual(fields["publish_time"], "2020-07-18")


class TitleMaterialMatchTests(unittest.TestCase):
    def test_match_tolerates_spacing_punctuation_and_width(self):
        self.assertTrue(
            mod.title_material_match(
                "不可不知的 ArcGIS Python 开发 PPT",
                "不可不知的ArcGIS Python开发（PPT可下载）",
            )
        )
        # full-width vs half-width parentheses
        self.assertTrue(mod.title_material_match("教程（一）", "教程(一)"))

    def test_unrelated_titles_do_not_match(self):
        self.assertFalse(mod.title_material_match("SDE数据定时备份", "国内期刊AIGC审查跟踪解读"))


class VerifyCandidateTests(unittest.TestCase):
    def test_verify_candidate_accepts_matching_candidate(self):
        url = "https://mp.weixin.qq.com/s?src=11&timestamp=1789264699&signature=H%2AxP2&new=1"
        result = mod.verify_candidate("不可不知的 ArcGIS Python 开发 PPT", url, mod.extract_article_fields(ARTICLE_HTML))
        self.assertTrue(result["canonical"])
        self.assertEqual(result["form"], "signed_query")
        self.assertTrue(result["title_match"])
        self.assertEqual(result["account"], "GIS前沿")

    def test_verify_candidate_rejects_wrong_article(self):
        url = "https://mp.weixin.qq.com/s/XO8Jqu0vEmbikIdrPD598A"
        wrong = {"title": "明确AI使用边界，国内期刊AIGC审查跟踪解读来了！", "account": "出版视点", "author": None, "publish_time": None}
        result = mod.verify_candidate("ArcPy使用之一：SDE数据定时备份", url, wrong)
        self.assertTrue(result["canonical"])  # form is fine ...
        self.assertFalse(result["title_match"])  # ... but the article is not the target


if __name__ == "__main__":
    unittest.main()
