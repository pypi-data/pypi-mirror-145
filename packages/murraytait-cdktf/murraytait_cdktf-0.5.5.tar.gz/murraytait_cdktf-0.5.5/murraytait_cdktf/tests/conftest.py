import os


def pytest_html_report_title(report):
    git_sha = os.environ.get("GIT_SHA")
    git_ref = os.environ.get("GIT_REF")
    report.title = f'Unit test report for {git_ref} {git_sha}'
