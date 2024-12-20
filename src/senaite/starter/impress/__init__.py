# -*- coding: utf-8 -*-

from senaite.impress.config import PAPERFORMATS
from senaite.starter import logger


logger.info("Patching Paperformat")

PAPERFORMATS["A4"] = {
    "name": "DIN A4",
    "format": "A4",
    "margin_top": 12.0,
    "margin_right": 15.0,
    "margin_bottom": 15.0,
    "margin_left": 15.0,
    "page_width": 210.0,
    "page_height": 297.0,
}
