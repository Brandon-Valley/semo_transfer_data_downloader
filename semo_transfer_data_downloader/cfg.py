from pathlib import Path

_SCRIPT_PARENT_DIR_PATH = Path(__file__).parent
REPO_ROOT_DIR_PATH = _SCRIPT_PARENT_DIR_PATH.parent
WORK_DIR_PATH = REPO_ROOT_DIR_PATH / "work"
WORK_HTML_DOWNLOADS_DIR_PATH = WORK_DIR_PATH / "html_downloads"
WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "inst_list_html"
WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "equiv_list_html"