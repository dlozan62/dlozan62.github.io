"""Regression tests for the generated-site validation boundary."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from scripts import check_site


class GeneratedSiteTests(TestCase):
    def write_valid_site(self, site):
        for relative_path in check_site.REQUIRED_PAGES:
            page = site / relative_path
            page.parent.mkdir(parents=True, exist_ok=True)
            pdf = check_site.PUBLIC_DOCUMENTS.get(relative_path)
            link = f'<a href="/{pdf}">PDF</a>' if pdf else ""
            page.write_text(f"<html><body>{link}</body></html>", encoding="utf-8")
        for relative_pdf in check_site.PUBLIC_DOCUMENTS.values():
            pdf = site / relative_pdf
            pdf.parent.mkdir(parents=True, exist_ok=True)
            pdf.write_bytes(b"%PDF-1.4\n")
        stylesheet = site / "assets/css/style.css"
        stylesheet.parent.mkdir(parents=True, exist_ok=True)
        stylesheet.write_text("", encoding="utf-8")

    def test_vendored_gem_files_are_not_project_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "_site"
            self.write_valid_site(site)
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
            self.write_valid_site(site)
            future_page = site / "sprints/sprint-2/index.html"
            future_page.parent.mkdir(parents=True, exist_ok=True)
            future_page.write_text('<img src="/missing.png">', encoding="utf-8")

            errors = StringIO()
            with patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 1)
            self.assertIn("sprints/sprint-2/index.html has 1 image(s) without alt text", errors.getvalue())

    def test_public_document_requires_its_pdf_link(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            self.write_valid_site(site)
            relative_page = "sprints/sprint-2/change-log/index.html"
            (site / relative_page).write_text("<html><body>Change log</body></html>", encoding="utf-8")

            errors = StringIO()
            with patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 1)
            self.assertIn("does not link to its matching PDF", errors.getvalue())

    def test_private_artifact_link_is_rejected(self):
        with TemporaryDirectory() as directory:
            site = Path(directory)
            self.write_valid_site(site)
            page = site / "index.html"
            page.write_text('<a href="/assets/pdfs/sprint-2-retrospective.pdf">Private</a>', encoding="utf-8")

            errors = StringIO()
            with patch.object(check_site, "SITE", site), redirect_stderr(errors):
                result = check_site.main()

            self.assertEqual(result, 1)
            self.assertIn("links to a private sprint artifact", errors.getvalue())
