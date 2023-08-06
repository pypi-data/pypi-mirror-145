import unittest

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.devtools.htmlparser import XMLValidator


class BoostrapTheMainTemplateTC(CubicWebTC):

    def test_valid_xhtml_index(self):
        with self.admin_access.web_request() as req:
            self.view('index', req=req)

    def test_valid_xhtml_error(self):
        valid = self.content_type_validators.get('text/html', XMLValidator)()
        with self.admin_access.web_request() as req:
            valid.parse_string(self.vreg['views'].main_template(req, 'error-template'))


if __name__ == '__main__':
    unittest.main()
