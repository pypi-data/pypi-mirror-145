# Thymio plug-in for Thonny

Plug-in for [Thonny](https://thonny.org/), the _Python IDE for beginners_, to run Python programs on the [Thymio II](https://thymio.org) mobile robot. Based on the module `tdmclient`.

In Thonny, select the menu Tools>Manage Packages, type _tdmclient_ty_ in the search box, and click the button Search on PyPI. Click the link _tdmclient_ty_ in the result list (normally the only result), then the Install button below.

To install the current development version from this github repository, in Thonny, type the following commands in the Shell panel, then quit and restart Thonny.
```
import pip
pip.main(["install",
          "--force-reinstall",
          "git+https://github.com/epfl-mobots/tdmclient-ty"])
```
