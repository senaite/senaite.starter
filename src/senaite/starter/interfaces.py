# -*- coding: utf-8 -*-

from bika.lims.interfaces import IBikaLIMS
from senaite.core.interfaces import ISenaiteCore


class ISenaiteStarter(IBikaLIMS, ISenaiteCore):
    """Marker interface that defines a Zope 3 browser layer.
    """
