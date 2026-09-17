"""Regression tests for the generated-site validation boundary."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from scripts import check_site


class GeneratedSiteTests(TestCase):
    def test_vendored_gem_files_are_not_project_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "_site"
            for relative_path in check_site.REQUIRED_PAGES:
                page = site / relative_path
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text("<html><body></body></html>", encoding="utf-8")
            stylesheet = site / "assets/css/style.css"
            stylesheet.parent.mkdir(parents=True)
            stylesheet.write_text("", encoding="utf-8")
            gem_readme = root / "vendor/bundle/ruby/3.3.0/gems/ffi/ext/ffi_c/libffi/README.md"
            gem_readme.parent.mkdir(parents=True)
            gem_readme.write_text("<<<<<<< HEAD\n", encoding="utf-8")

            errors = StringIO()
            with patch.object(check_site, "ROOT", root), patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 0, errors.getvalue())

            (root / "README.md").write_text("<<<<<<< HEAD\n", encoding="utf-8")
            errors = StringIO()
            with patch.object(check_site, "ROOT", root), patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 1)
            self.assertIn("README.md contains a merge-conflict marker", errors.getvalue())
            self.assertNotIn("vendor/bundle", errors.getvalue())

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
