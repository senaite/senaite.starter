# -*- coding: utf-8 -*-

from senaite.impress.analysisrequest.reportview import \
    MultiReportView as BaseMultiReportView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as PT


class MultiReportView(BaseMultiReportView):
    """Controller view for multi-reports
    """
    JS_TEMPLATE = PT("templates/js.pt")
    CSS_TEMPLATE = PT("templates/css.pt")
    CONTROLS_TEMPLATE = PT("templates/controls.pt")
    HEADER_TEMPLATE = PT("templates/header.pt")
    INFO_TEMPLATE = PT("templates/info.pt")
    ALERTS_TEMPLATE = PT("templates/alerts.pt")
    SUMMARY_TEMPLATE = PT("templates/summary.pt")
    RESULTS_TEMPLATE = PT("templates/results.pt")
    RESULTS_TRANSPOSED_TEMPLATE = PT("templates/results_transposed.pt")
    INTERPRETATIONS_TEMPLATE = PT("templates/interpretations.pt")
    REMARKS_TEMPLATE = PT("templates/remarks.pt")
    ATTACHMENTS_TEMPLATE = PT("templates/attachments.pt")
    SIGNATURE_TEMPLATE = PT("templates/signatures.pt")
    DISCREETER_TEMPLATE = PT("templates/discreeter.pt")
    FOOTER_TEMPLATE = PT("templates/footer.pt")

    def __init__(self, context, collection, request):
        super(MultiReportView, self).__init__(collection, request)

    @property
    def primary_sample(self):
        """Primary sample of the collection
        """
        if len(self.collection) == 0:
            raise ValueError("No reports in collection!")
        return self.collection[0]


class SingleReportView(MultiReportView):
    """Controller view for single-reports
    """
    def __init__(self, context, model, request):
        super(SingleReportView, self).__init__(context, [model], request)
