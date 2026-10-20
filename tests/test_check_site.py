"""Regression tests for the generated-site validation boundary."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from scripts import check_site


class GeneratedSiteTests(TestCase):
    def test_empty_and_unresolved_link_urls_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "_site"
            for relative_path in check_site.REQUIRED_PAGES:
                page = site / relative_path
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text("<html><body></body></html>", encoding="utf-8")
            css = site / "assets/css/style.css"
            css.parent.mkdir(parents=True)
            css.write_text("", encoding="utf-8")
            page = site / "sprints/sprint-3/index.html"
            invalid_cases = (
                ('<a href="" download>Download PDF</a>', "empty href"),
                ('<a download>Download PDF</a>', "empty href"),
                ('<a href="">Previous sprint</a>', "empty href"),
                ('<a href="{{%20\'/assets/pdfs/report.pdf\'%20|%20relative_url%20}}" download>PDF</a>', "unresolved template"),
                ('<a href="%7B%7B%20report%20%7D%7D" download>PDF</a>', "unresolved template"),
            )
            for markup, message in invalid_cases:
                with self.subTest(markup=markup):
                    page.write_text(markup, encoding="utf-8")
                    errors = StringIO()
                    with patch.object(check_site, "ROOT", root), patch.object(check_site, "SITE", site), redirect_stderr(errors):
                        result = check_site.main()
                    self.assertEqual(result, 1)
                    self.assertIn(message, errors.getvalue())

            # A real target and a normal source template must remain valid.
            pdf = site / "assets/pdfs/report.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"%PDF-1.7\n")
            page.write_text('<a href="/assets/pdfs/report.pdf" download>PDF</a>', encoding="utf-8")
            source = root / "sprint-3.html"
            source.write_text("<a href=\"{{ '/assets/pdfs/report.pdf' | relative_url }}\">PDF</a>", encoding="utf-8")
            errors = StringIO()
            with patch.object(check_site, "ROOT", root), patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()
            self.assertEqual(result, 0, errors.getvalue())

            source.write_text("<a href=\"{{%20'/assets/pdfs/report.pdf'%20|%20relative_url%20}}\">PDF</a>", encoding="utf-8")
            errors = StringIO()
            with patch.object(check_site, "ROOT", root), patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()
            self.assertEqual(result, 1)
            self.assertIn("percent-encoded Liquid expression", errors.getvalue())

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
            future_page.parent.mkdir(parents=True, exist_ok=True)
            future_page.write_text('<img src="/missing.png">', encoding="utf-8")

            errors = StringIO()
            with patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 1)
            self.assertIn("sprints/sprint-2/index.html has 1 image(s) without alt text", errors.getvalue())

    def test_relative_links_check_the_destination_anchor(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "_site"
            for relative_path in check_site.REQUIRED_PAGES:
                page = site / relative_path
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text("<html><body></body></html>", encoding="utf-8")
            css = site / "assets/css/style.css"
            css.parent.mkdir(parents=True)
            css.write_text("", encoding="utf-8")
            page = site / "sprints/sprint-3/index.html"
            page.write_text('<a href="../sprint-2/#missing">Report</a>', encoding="utf-8")
            errors = StringIO()
            with patch.object(check_site, "ROOT", root), patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()
            self.assertEqual(result, 1)
            self.assertIn("missing anchor: ../sprint-2/#missing", errors.getvalue())
