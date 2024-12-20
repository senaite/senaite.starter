# Custom View Components

The `browser` package holds all browser views and other UI related view components.


## Browser Views

A browser view is implemented as a subclass of `Products.Five.browser.BrowserView`:

``` python title="myview.py"
from Products.Five.browser import BrowserView

class MyView(BrowserView):

    def __init__(self, context, request):
        super(MyView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        return "%s was called on %s" % (self.__name__, repr(self.context))
```

Afterwards, it must be registered as a callable endpoint for a specific context in the `configure.zcml`:

``` xml title="configure.zcml"
  <browser:page
      for="*"
      name="myview"
      class=".myview.MyView"
      permission="zope2.View"
      layer="senaite.starter.interfaces.ISenaiteStarter"
      />
```

- `for`: Defines the context interface where the view will be registered. The `*` means that it is available everywhere.
- `name`: The view name that can be used in the URL, e.g. `http://localhost:8080/senaite/samples/myview`.
- `class`: The class that implements the view logic.
- `permission`: The required permission to call the view. `zope2.View` means that every authenticated user can access the view.
- `layer`: The browser layer interface to allow browser view overrides of views with the same name.

The traverser will call then the `__call__` method of the class when the
endpoint is reached and output the following message:

``` xml
myview was called on <Samples at /senaite/samples>
```

### Rendering a page template

Returning plain text is most of the time not very useful, unless you want to
export data in CSV, XML, JSON or another raw computer readable format.

This is where page templates come in that render in a specific area of your
SENAITE site, e.g. the content area.

So let us change the view class to render a page template instead:

``` python title="myview.py"
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyView(BrowserView):
    template = ViewPageTemplateFile("myview.pt")

    def __init__(self, context, request):
        super(MyView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()
```

The template will be called in the `__call__` method and rendered directly in HTML by the server.

``` xml title="myview.pt"
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      metal:use-macro="here/main_template/macros/master"
      i18n:domain="senaite.starter">
  <body>
    <metal:content-title fill-slot="content-title">
      <h1 i18n:translate="">My first SENAITE View</h1>
    </metal:content-title>

    <metal:content-description fill-slot="content-description">
      <p>A view that displays our class name and the current context</p>
    </metal:content-description>

    <metal:content-core fill-slot="content-core">
      <code tal:content="python:view.__name__"/> was called on <code tal:content="python:repr(context)"/>
    </metal:content-core>
  </body>
</html>
```


## Viewlets

A browser viewlet is implemented as a subclass of `plone.app.layout.viewlets.ViewletBase`:

``` python title="footer.py"
from plone.app.layout.viewlets.common import FooterViewlet as Base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class FooterViewlet(Base):
    index = ViewPageTemplateFile("templates/footer.pt")
```

The template will be called in the `__call__` method and rendered directly in HTML by the server.

``` xml title="templates/footer.pt"
<footer i18n:domain="senaite.core"
        id="senaite-footer">

  <div class="row">
    <div class="col-md-12">
      <hr/>
      <!-- footer portlets -->
      <div tal:on-error="nothing" tal:replace="structure view/render_footer_portlets" />
      <div class="float-left">
        RIDING BYTES GmbH
        <abbr title="Copyright">&copy;</abbr> 2024
      </div>
      <div class="float-right">
        <ul class="nav nav-pills">
          <li><a class="nav-link" href="https://www.senaite.com" title="Visit the Website" target="_blank"><i class="fas fa-globe"></i></a></li>
        </ul>
      </div>
    </div>
  </div>
</footer>

```
