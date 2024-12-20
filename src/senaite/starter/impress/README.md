# How to create custom SENAITE IMPRESS Reports

Add your custom publication reports for [SENAITE IMPRESS](https://github.com/senaite/senaite.impress).


## Package overview

The `senaite.starter.impress` package contains the following contents:

``` shell
senaite.starter.impress
├── README.md
├── __init__.py
├── configure.zcml
├── reports
│   ├── MultiReport.pt
│   └── SingleReport.pt
├── reportview.py
└── templates
    ├── alerts.pt
    ├── attachments.pt
    ├── controls.pt
    ├── css.pt
    ├── discreeter.pt
    ├── footer.pt
    ├── header.pt
    ├── info.pt
    ├── interpretations.pt
    ├── js.pt
    ├── remarks.pt
    ├── results.pt
    ├── results_transposed.pt
    ├── signatures.pt
    └── summary.pt
```

## Introduction

SENAITE allows to register custom reports from an external package without the
need to change the core codebase.

!!! info

    The current package ships already with a boilerplate for a multi- and a single report in the `reports` folder.


!!! note

    Remember to activate your custom reports via the [SENAITE Impress Controlpanel](http://localhost:8080/senaite/@@impress-controlpanel) after you installed this packgage in the [SENAITE Add-on Controlpanel](http://localhost:8080/senaite/prefs_install_products_form)


## Single vs. Multi Reports

SENAITE distinguishes between multi- and single reports. A multi report
prints the results of multiple samples below the results of the first (primary)
sample in one PDF, while a single report generates a new PDF for each sample.

A multi report is identified by its file name that either starts or end with the
word "multi". All other reports are considered single reports.


## Report templates

The main report templates are located in the `reports` folder, that is
registered via `configure.zcml`:

``` xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone">

  <include package="plone.resource" file="meta.zcml"/>

  ...

  <plone:static
      directory="reports"
      type="senaite.impress.reports"
      name="senaite.starter"/>

</configure>
```

Report templates are written in the [Zope Page Template](https://zope.readthedocs.io/en/latest/zopebook/ZPT.html)
language and act as the "View" in an [Model–view–controller (MVC)](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) design pattern.

Each report is divided into multiple sections that are located in the
`templates` folder, e.g. `templates/header.pt`, `templates/summary.pt`,
`templates/footer.pt` etc.:


``` xml
<tal:report>

  <!-- REPORT CONTROLS -->
  <tal:t replace="structure python:view.render_controls(context, **options)" />

  <!-- REPORT JS -->
  <tal:t replace="structure python:view.render_js(context, **options)" />

  <!-- REPORT CSS -->
  <tal:t replace="structure python:view.render_css(context, **options)" />

  <!-- REPORT HEADER -->
  <tal:t replace="structure python:view.render_header(context, **options)" />

  <!-- REPORT INFO -->
  <tal:t replace="structure python:view.render_info(context, **options)" />

  <!-- REPORT ALERTS -->
  <tal:t replace="structure python:view.render_alerts(context, **options)" />

  <!-- REPORT SUMMARY -->
  <tal:t replace="structure python:view.render_summary(context, **options)" />

  <!-- REPORT RESULTS -->
  <tal:t replace="structure python:view.render_results(context, **options)" />

  <!-- RESULTS INTERPRETATION -->
  <tal:t replace="structure python:view.render_interpretations(context, **options)" />

  <!-- SAMPLE REMARKS -->
  <tal:t replace="structure python:view.render_remarks(context, **options)" />

  <!-- REPORT ATTACHMENTS -->
  <tal:t replace="structure python:view.render_attachments(context, **options)" />

  <!-- REPORT SIGNATURES -->
  <tal:t replace="structure python:view.render_signatures(context, **options)" />

  <!-- REPORT DISCREETER -->
  <tal:t replace="structure python:view.render_discreeter(context, **options)" />

  <!-- REPORT FOOTER -->
  <tal:t replace="structure python:view.render_footer(context, **options)" />

</tal:report>
```

Section templates are fetched from the "Controller" view (`view`) (1), e.g.:
{ .annotate }

1. [View Code in GitHub](https://github.com/senaite/senaite.impress/blob/2.x/src/senaite/impress/analysisrequest/reportview.py)

``` xml
  <!-- REPORT HEADER -->
  <tal:t replace="structure python:view.render_header(context, **options)" />
```

## Report controllers

There are separate report controllers registered for multi- and single templates.
They are located in the `reportview` module and are registered as [Multi Adpaters](https://zopecomponent.readthedocs.io/en/latest/narr.html#adapters) in the `configure.zcml`:

``` xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone">


  <!-- Context aware report controller for Single Reports -->
  <adapter
      for="* * senaite.starter.interfaces.ISenaiteStarter"
      name="AnalysisRequest"
      factory=".reportview.SingleReportView"
      provides="senaite.impress.interfaces.IReportView"
      permission="zope2.View"/>

  <!-- Context aware report controller for Multi Reports -->
  <adapter
      for="* * senaite.starter.interfaces.ISenaiteStarter"
      name="AnalysisRequest"
      factory=".reportview.MultiReportView"
      provides="senaite.impress.interfaces.IMultiReportView"
      permission="zope2.View"/>

  ...

</configure>
```

All complex logic, including hooking in new template sections, should be implemented here:

``` python
from senaite.impress.analysisrequest.reportview import \
    MultiReportView as BaseMultiReportView


class MultiReportView(BaseMultiReportView):
    """Controller view for multi-reports
    """
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
```


## Report models

Inside report templates and controllers, the objects (sample, analysis, client,
contact, laboratory etc.) are wrapped into a [SENAITE SuperModel](https://github.com/senaite/senaite.impress/blob/2.x/src/senaite/impress/analysisrequest/model.py).
These wrapped objects act as the "Model" and provide the data to be displayed in a more transparent way.

This allows the template designer to access the required data from the database schema name directly.


## Development cycle

To develop a new report, the SENAITE server should be run in foreground (debug)
mode to avoid caching of the page templates.



## Further Information and References

- [SENAITE IMPRESS GitHub Code Repository](https://github.com/senaite/senaite.impress)
- [Using Zope Page Templates](https://zope.readthedocs.io/en/latest/zopebook/ZPT.html)
- [ZOPE Component Architecture](https://zopecomponent.readthedocs.io/en/latest/narr.html)
- [Ask questions on SENAITE Community Site](https://community.senaite.org)
- [SENAITE Core Contribution Guide](https://github.com/senaite/senaite.core/blob/2.x/CONTRIBUTING.md)
