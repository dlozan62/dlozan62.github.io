"""Regression tests for the generated-site validation boundary."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from scripts import check_site


class GeneratedSiteTests(TestCase):
    def test_new_sprint_page_is_checked(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            for relative_path in check_site.REQUIRED_PAGES:
                page = site / relative_path
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text("<html><body></body></html>", encoding="utf-8")
            stylesheet = site / "assets/css/style.css"
            stylesheet.parent.mkdir(parents=True)
            stylesheet.write_text("", encoding="utf-8")
            future_page = site / "sprints/sprint-2/index.html"
            future_page.parent.mkdir(parents=True)
            future_page.write_text('<img src="/missing.png">', encoding="utf-8")

            errors = StringIO()
            with patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 1)
            self.assertIn("sprints/sprint-2/index.html has 1 image(s) without alt text", errors.getvalue())
