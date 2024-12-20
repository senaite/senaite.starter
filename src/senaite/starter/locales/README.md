# Translate SENAITE Starter and SENAITE into your language

This guide explains how you can translate SENAITE Starter and SENAITE into your language.

## Prepare the development environment

Please make sure you have [setup the development version SENAITE LIMS](/index.html#how-to-setup-the-development-version-senaite-lims).

This configuration installs the script `update_translations` into the `bin` folder of the buildout directory.

```
$ bin/update_translations
Processing Domain senaite.starter
senaite.starter-1.0.0/src/senaite/starter/locales/en/LC_MESSAGES/senaite.starter.po: 0 added, 0 removed
Processing Domain senaite.starter [DONE]
Processing Domain senaite.core
Processing language en for Domain senaite.core
Processing Domain plone
Processing language en for Domain plone
```

The script fills the translation files located in the `locales` folder with all
of the found translations strings of each domain:

``` shell
locales
├── en
│   └── LC_MESSAGES
│       ├── plone-override.po
│       ├── plone.po
│       ├── senaite.core-override.po
│       ├── senaite.core.po
│       └── senaite.starter.po
├── senaite.starter-manual.pot
└── senaite.starter.pot
```

!!! note

    The `senaite-core-override.po` and `plone-override.po` translations files are always merged *after* the original translation files of these domains get copied from the codebase.
    This preserves your custom translations.

    Example:

    If you would like to have the "Clients" folder renamed into "Projects", you would add this into your `senaite.core-override.po`:
    ```po
    msgid "Clients"
    msgstr "Projects"
    ```

    Running the `update_translations` script again copies the changed translation string into `senaite.core-override.po`.


!!! tip

    If you need another language to translate, e.g. German (`de`), you can simply recursively copy the `en` folder structure to `de`. Make sure the containing `*.po` files are empty and run the `update_translations` script again:

    ```shell
    $ cd src/senaite/starter/locales
    $ cp -r en de
    $ for f in $(find de -name "*.po"); do
    \   echo "" > $f
    \ done
    $ cd ../../../..
    $ bin/update_translations
    ```

!!! tip
    You can use [POEDIT](https://poedit.net/) to edit the `*.po` files in the correct format.


## Contribute translations to SENAITE

Changing or adding translations for SENAITE in your local add-on is a good
approach to have individual wordings directly applied in your site.

However, updating them directly in SENAITE Core or its dependent add-ons might
be a good idea to have them applied to future versions of SENAITE and make the
whole project grow.

This can be achieved over the [Transifex](https://www.transifex.com) platform, because all translations are managed there.


## Further Information and References


- [SENAITE Transifex Project](https://app.transifex.com/senaite/)
- [SENAITE Core Transifex Dashboard](https://app.transifex.com/senaite/senaite-core/dashboard)
- [Ask questions on SENAITE Community Site](https://community.senaite.org)
- [SENAITE Core Contribution Guide](https://github.com/senaite/senaite.core/blob/2.x/CONTRIBUTING.md)
