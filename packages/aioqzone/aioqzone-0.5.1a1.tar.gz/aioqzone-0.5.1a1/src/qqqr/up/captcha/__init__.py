import asyncio
import base64
import json
import re
from math import floor
from random import choices, randint, random
from time import time
from typing import Any, Dict, Iterable, Tuple, cast
from urllib.parse import unquote, urlencode

from aiohttp import ClientSession as Session
from multidict import MutableMultiMapping, istr
from yarl import URL

from jssupport.execjs import ExecJS
from jssupport.jsjson import json_loads

from .jigsaw import Jigsaw

PREHANDLE_URL = "https://t.captcha.qq.com/cap_union_prehandle"
SHOW_NEW_URL = "https://t.captcha.qq.com/cap_union_new_show"
VERIFY_URL = "https://t.captcha.qq.com/cap_union_new_verify"

time_s = lambda: int(1e3 * time())
rnd6 = lambda: str(random())[2:8]


def hex_add(h: str, o: int):
    if h.endswith("#"):
        return h + str(o)
    if not h:
        return o
    return hex(int(h, 16) + o)[2:]


class ScriptHelper:
    def __init__(self, appid: int, sid: str, subsid: int) -> None:
        self.aid = appid
        self.sid = sid
        self.subsid = subsid

    def parseCaptchaConf(self, iframe: str):
        m = re.search(r"window\.captchaConfig=(\{.*\});", iframe)
        assert m
        ijson = m.group(1)
        self.conf: Dict[str, Any] = json_loads(ijson)  # type: ignore

    def cdn(self, cdn: int) -> str:
        assert cdn in (0, 1, 2)
        assert isinstance(self.conf, dict)
        data = {
            "aid": self.aid,
            "sess": self.conf["sess"],
            "sid": self.sid,
            "subsid": self.subsid + cdn,
        }
        if cdn:
            data["img_index"] = cdn
        path = self.conf[f"cdnPic{cdn if cdn else 1}"]
        return f"https://t.captcha.qq.com{path}?{urlencode(data)}"

    @staticmethod
    def slide_js_url(iframe):
        m = re.search(r"https://captcha\.gtimg\.com/1/tcaptcha-slide\.\w+\.js", iframe)
        assert m
        return m.group(0)

    @staticmethod
    def tdx_js_url(iframe):
        m = re.search(r'src="(/td[xc].js.*?)"', iframe)
        assert m
        return "https://t.captcha.qq.com" + m.group(1)


class VM:
    vmAvailable = 0
    vmByteCode = 0

    def __init__(self, tdx: str, header: MutableMultiMapping[str]) -> None:
        assert "User-Agent" in header
        assert "cookie" in header
        assert "Referer" in header
        self.tdx = ExecJS(js=self.constructWindow(header) + tdx)

    @staticmethod
    def constructWindow(header: MutableMultiMapping[str]):
        window = 'var href="%s",ua="%s",cookie="%s"\n' % (
            header["Referer"],
            header["User-Agent"],
            header["cookie"],
        )
        from pathlib import Path

        with open(Path(__file__).parent / "window.js") as f:
            window += f.read()
        return window

    async def getData(self):
        return unquote((await self.tdx("window.TDC.getData", True)).strip())

    async def getInfo(self) -> dict:
        return cast(dict, json_loads(await self.tdx("window.TDC.getInfo")))

    def setData(self, d: dict):
        self.tdx.addfunc("window.TDC.setData", d)

    def clearTc(self):
        return self.tdx("window.TDC.clearTc")

    async def getCookie(self):
        return (await self.tdx.get("window.document.cookie")).strip()


class Captcha:
    sess = None
    createIframeStart = 0
    subsid = 1

    # (c_login_2.js)showNewVC-->prehandle
    # prehandle(recall)--call tcapcha-frame.*.js-->new_show
    # new_show(html)--js in html->loadImg(url)
    def __init__(self, session: Session, ssl_context, appid: int, sid: str):
        self.session = session
        self.ssl = ssl_context
        self.appid = appid
        self.sid = sid

        self.session.headers.update({istr("referer"): "https://xui.ptlogin2.qq.com/"})

    @property
    def base64_ua(self):
        return base64.b64encode(self.session.headers["User-Agent"].encode()).decode()

    async def prehandle(self, xlogin_url):
        """
        call this before call `show`.

        args:
            xlogin_url: the url requested in QRLogin.request

        returns:
            dict

        example:
        ~~~
            {
                "state": 1,
                "ticket": "",
                "capclass": "1",
                "subcapclass": "15",
                "src_1": "cap_union_new_show",
                "src_2": "template/new_placeholder.html",
                "src_3": "template/new_slide_placeholder.html",
                "sess": "s0FXwryrkuYcdadBBb1d3_xihwN-42KXNAQQg6_5FKAuF-MdGmSlD9H7hQg29GLnk7uQLrsgHVRCQ7Mu1ylB6jY-XqrWaGPmoUfNJfJKjTY0ahaC16M6qb8bBsKJH67j8UPnI3r84TI35HMgtKh_t40jkHbp1l67l55rKEm4HHA27oIiEvD1rtUvb8UK2Rgfe7mb4wtuAvMrG-wVpZkamFhvx0e0GHlVCeDwBQ7o7cn0h4oH1V9pLN6GBkGiqBgHeTdFKqJH-FqNI*",
                "randstr": "",
                "sid": "874820883465668800"
            }
        ~~~
        """
        CALLBACK = "_aq_596882"
        data = {
            "aid": self.appid,
            "protocol": "https",
            "accver": 1,
            "showtype": "embed",
            "ua": self.base64_ua,
            "noheader": 1,
            "fb": 1,
            "enableDarkMode": 0,
            "sid": self.sid,
            "grayscale": 1,
            "clientype": 2,
            "cap_cd": "",
            "uid": "",
            "wxLang": "",
            "lang": "zh-CN",
            "entry_url": xlogin_url,
            # 'js': '/tcaptcha-frame.a75be429.js'
            "subsid": self.subsid,
            "callback": CALLBACK,
            "sess": "",
        }
        self.createIframeStart = time_s()
        async with self.session.get(PREHANDLE_URL, params=data, ssl=self.ssl) as r:
            r.raise_for_status()
            m = re.search(CALLBACK + r"\((\{.*\})\)", await r.text())

        assert m
        r = m.group(1)
        r = json.loads(r)
        self.sess = r["sess"]
        self.subsid = 2
        return r

    async def iframe(self):
        assert self.sess, "call prehandle first"

        data = {
            "aid": self.appid,
            "protocol": "https",
            "accver": 1,
            "showtype": "embed",
            "ua": self.base64_ua,
            "noheader": 1,
            "fb": 1,
            "enableDarkMode": 0,
            "sid": self.sid,
            "grayscale": 1,
            "clientype": 2,
            "sess": self.sess,
            "fwidth": 0,
            "wxLang": "",
            "tcScale": 1,
            "uid": "",
            "cap_cd": "",
            "subsid": self.subsid,
            "rnd": rnd6(),
            "prehandleLoadTime": time_s() - self.createIframeStart,
            "createIframeStart": self.createIframeStart,
        }
        async with self.session.get(SHOW_NEW_URL, params=data, ssl=self.ssl) as r:
            self.session.headers.update({istr("referer"): str(r.url)})
            self.prehandleLoadTime = data["prehandleLoadTime"]
            return await r.text()

    async def getBlob(self, iframe: str):
        js_url = ScriptHelper.slide_js_url(iframe)
        async with self.session.get(js_url, ssl=self.ssl) as r:
            r.raise_for_status()
            js = await r.text()
        m = re.search(r"'(!function.*;')", js)
        assert m
        return m.group(1)

    async def getTdx(self, iframe: str):
        js_url = ScriptHelper.tdx_js_url(iframe)
        header = self.session.headers.copy()
        header["cookie"] = "; ".join(
            f"{k}={v.value}"
            for k, v in self.session.cookie_jar.filter_cookies(URL("qq.com")).items()
        )
        async with self.session.get(js_url) as r:
            r.raise_for_status()
            self.vm = VM(await r.text(), header=header)

        m = re.search(r"TDC_itoken=([\w%]+);?", await self.vm.getCookie())
        assert m
        c = m.group(1)
        self.session.cookie_jar.update_cookies({"TDC_itoken": c})
        return self.vm

    async def matchMd5(self, iframe: str, powCfg: dict) -> Tuple[int, int]:
        if not hasattr(self, "_matchMd5"):
            blob = await self.getBlob(iframe)
            m = re.search(r",(function\(\w,\w,\w\).*?duration.*?),", blob)
            assert m
            blob = m.group(1)
            blob = f"var n=Object();!{blob}(null,n,null);"
            blob += "function matchMd5(p, m){return n.getWorkloadResult({nonce:p,target:m})}"
            self._matchMd5 = ExecJS(js=blob).bind("matchMd5")
        d = await self._matchMd5(powCfg["prefix"], powCfg["md5"])
        d = cast(Dict[str, int], json_loads(d.strip("\n")))
        return int(d["ans"]), int(d["duration"])

    @staticmethod
    def imitateDrag(x: int):
        assert x < 300
        # 244, 1247
        t = randint(1200, 1300)
        n = randint(50, 65)
        X = lambda i: randint(1, max(2, i // 10)) if i < n - 15 else randint(6, 12)
        Y = lambda: choices([-1, 1, 0], cum_weights=[0.1, 0.2, 1], k=1)[0]
        T = lambda: randint(*choices(((65, 280), (6, 10)), cum_weights=(0.05, 1), k=1)[0])
        xs = ts = 0
        drag = []
        for i in range(n):
            xi, ti = X(i), T()
            drag.append([xi, Y(), ti])
            xs += xi
            ts += ti
        drag.append([max(1, x - xs), Y(), max(1, t - ts)])
        drag.reverse()
        return drag

    async def rio(self, urls: Iterable[str]) -> Tuple[bytes, ...]:
        async def inner(url):
            async with self.session.get(url, ssl=self.ssl) as r:
                r.raise_for_status()
                return await r.content.read()

        return await asyncio.gather(*(inner(i) for i in urls))

    async def verify(self):
        """
        example:
        ~~~
        {
            "errorCode": "0",
            "randstr": "@VTn",
            "ticket": "t03UtRJOy9txaidDDdx5FBzSN_uwipfzMGe1pjDMIoO3dS2UUp1EEWiuZmIotD_709cAYhPGWo2M-uQZxorFH8JtGEhqpSYeRQ1h84opX2TQYWGRFATffLj8vsw_U3YJPHR5MPcvHsVGtM*",
            "errMessage": "",
            "sess": ""
        }
        ~~~
        """
        s = ScriptHelper(self.appid, self.sid, self.subsid)
        iframe = await self.iframe()
        s.parseCaptchaConf(iframe)
        Ians, duration = await self.matchMd5(iframe, s.conf["powCfg"])
        await self.getTdx(iframe)

        waitEnd = time() + 0.6 * random() + 0.9

        j = Jigsaw(*await self.rio(s.cdn(i) for i in range(3)), top=floor(int(s.conf["spt"])))

        self.vm.setData({"clientType": 2})
        self.vm.setData({"coordinate": [10, 24, 0.4103]})
        self.vm.setData(
            {
                "trycnt": 1,
                "refreshcnt": 0,
                "slideValue": self.imitateDrag(floor(j.left * j.rate)),
                "dragobj": 1,
            }
        )
        self.vm.setData({"ft": "qf_7P_n_H"})
        collect = await self.vm.getData()
        data = {
            "aid": self.appid,
            "protocol": "https",
            "accver": 1,
            "showtype": s.conf["showtype"],
            "ua": self.base64_ua,
            "noheader": s.conf["noheader"],
            "fb": 1,
            "enableDarkMode": 0,
            "sid": self.sid,
            "grayscale": 1,
            "clientype": 2,
            "sess": s.conf["sess"],
            "fwidth": 0,
            "wxLang": "",
            "tcScale": 1,
            "uid": s.conf["uid"],
            "cap_cd": "",
            "rnd": rnd6(),
            "prehandleLoadTime": self.prehandleLoadTime,
            "createIframeStart": self.createIframeStart,
            "subsid": self.subsid,
            "cdata": 0,
            "vsig": s.conf["vsig"],
            "websig": s.conf["websig"],
            "subcapclass": s.conf["subcapclass"],
            "fpinfo": "",
            "ans": f"{j.left},{j.top};",
            "nonce": s.conf["nonce"],
            "vlg": f"{self.vm.vmAvailable}_{self.vm.vmByteCode}_1",
            "pow_answer": hex_add(s.conf["powCfg"]["prefix"], Ians) if Ians else Ians,
            "pow_calc_time": duration,
            "eks": (await self.vm.getInfo())["info"],
            "tlg": len(collect),
            s.conf["collectdata"]: collect,
            # TODO: unknown
            # 'vData': 'gC*KM-*rjuHBcUjIt9kL6SV6JGdgfzMmP0BiFcaDg_7ctHwCjeoz4quIjb2FTgdJLBeCcKCZB_Mv7suXumolfmpSKZVIp7Un2N3b*fbwHX9aqRgjp5fmsgkf6aOgnhU_ttr_4xJZKVjStGX*hMwgBeHE_zuz-iDKy1coGdurLh559T6MoBdJdMAxtIlGJxAexbt6eDz3Aw5pD_tR01ElO7YY',
        }
        await asyncio.sleep(max(0, waitEnd - time()))
        async with self.session.post(VERIFY_URL, data=data, ssl=self.ssl) as r:
            self.sess = None
            self.createIframeStart = 0
            self.prehandleLoadTime = 0
            r = await r.json()

        if int(r["errorCode"]):
            raise RuntimeError(f"Code {r['errorCode']}: {r['errMessage']}")
        return r
