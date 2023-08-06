**class HTMLPageHeader**
==========================

This class has been completly rewritten.

* A new context named `header-logo` has been introducted for the logo and the
  site title (used by `basecomponents.ApplLogo` and
  `basecomponents.ApplicationName`) to be displyed on the very left of the
  navbar.

* Breadcrumbs have been moved from the main header to a specific
  `div#breadcrumbs`.

* A new `headers_classes` attribute now provides the match between context
  and bootsrap classes ::

    basetemplates.HTMLPageHeader.headers_classes = {
        'header-left': 'navbar-left',
        'header-right': 'navbar-right',
    }


* A new `css` attribute provides the possibility to easily customize the
  header navbar and breadcrumbs ::

    basetemplates.HTMLPageHeader.css = {
        'header-navbar': 'navbar-default',
        'breadcrumbs':   'cw-breadcrumbs-default'
    }
