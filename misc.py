import os
import functools
import aqt

SUPPORT_DIR = os.path.join(os.path.dirname(__file__), "support")
ANKI21_VERSION = int(aqt.appVersion.split('.')[-1])
config = aqt.mw.addonManager.getConfig(__name__)
iter_fields = functools.partial(zip, config['src_fields'], config['dst_fields'])
