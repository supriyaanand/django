from django.test import SimpleTestCase
from django.test.utils import str_prefix
from django.utils.safestring import mark_safe

from ..utils import render, setup


class MakeListTests(SimpleTestCase):
    """
    The make_list filter can destroy existing escaping, so the results are
    escaped.
    """

    @setup({'make_list01': '{% autoescape off %}{{ a|make_list }}{% endautoescape %}'})
    def test_make_list01(self):
        output = render('make_list01', {"a": mark_safe("&")})
        self.assertEqual(output, str_prefix("[%(_)s'&']"))

    @setup({'make_list02': '{{ a|make_list }}'})
    def test_make_list02(self):
        output = render('make_list02', {"a": mark_safe("&")})
        self.assertEqual(output, str_prefix("[%(_)s&#39;&amp;&#39;]"))

    @setup({'make_list03':
        '{% autoescape off %}{{ a|make_list|stringformat:"s"|safe }}{% endautoescape %}'})
    def test_make_list03(self):
        output = render('make_list03', {"a": mark_safe("&")})
        self.assertEqual(output, str_prefix("[%(_)s'&']"))

    @setup({'make_list04': '{{ a|make_list|stringformat:"s"|safe }}'})
    def test_make_list04(self):
        output = render('make_list04', {"a": mark_safe("&")})
        self.assertEqual(output, str_prefix("[%(_)s'&']"))
