"""
Missing Dependencies Fixer Module (DepDoctor).
Uses Abstract Syntax Tree (AST) parsing for Python and regex syntax extraction for JS/TS
to catch undeclared imports before your app crashes in production.
"""

from __future__ import annotations
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass
class MissingDependencyFinding:
    package_name: str
    imported_in_file: str
    manifest_file: str
    manifest_type: str  # "python_requirements" or "node_package_json"
    friendly_explanation: str
    suggested_patch_line: str

    def to_dict(self) -> dict:
        return {
            "package_name": self.package_name,
            "imported_in_file": self.imported_in_file,
            "manifest_file": self.manifest_file,
            "manifest_type": self.manifest_type,
            "friendly_explanation": self.friendly_explanation,
            "suggested_patch_line": self.suggested_patch_line,
        }


class DepDoctor:
    """
    Scans project source code using AST, isolates imported libraries,
    and checks them against requirements.txt or package.json.
    """

    # Comprehensive Python Standard Library modules to ignore
    PYTHON_STDLIB = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else {
        "abc", "argparse", "array", "ast", "asyncio", "base64", "binascii", "bisect",
        "builtins", "calendar", "cmath", "cmd", "code", "codecs", "collections", "colorsys",
        "compileall", "concurrent", "configparser", "contextlib", "contextvars", "copy",
        "copyreg", "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime",
        "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email", "encodings",
        "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch",
        "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext", "glob",
        "graphlib", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr",
        "imp", "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword",
        "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox", "mailcap", "marshal",
        "math", "mimetypes", "mmap", "modulefinder", "msilib", "msvcrt", "multiprocessing",
        "netrc", "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib",
        "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib",
        "posix", "pprint", "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc",
        "queue", "quopri", "random", "re", "readline", "reprlib", "resource", "rlcompleter",
        "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil",
        "signal", "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd",
        "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess",
        "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib",
        "tempfile", "termios", "test", "textwrap", "threading", "time", "timeit", "tkinter",
        "token", "tokenize", "tomllib", "trace", "traceback", "tracemalloc", "tty", "turtle",
        "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid",
        "venv", "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound", "wsgiref",
        "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo"
    }

    # Standard Node.js built-ins
    NODE_BUILTINS = {
        "assert", "async_hooks", "buffer", "child_process", "cluster", "console", "constants",
        "crypto", "dgram", "diagnostics_channel", "dns", "domain", "events", "fs", "fs/promises",
        "http", "http2", "https", "inspector", "module", "net", "os", "path", "perf_hooks",
        "process", "punycode", "querystring", "readline", "repl", "stream", "stream/promises",
        "string_decoder", "timers", "timers/promises", "tls", "trace_events", "tty", "url",
        "util", "v8", "vm", "wasi", "worker_threads", "zlib"
    }

    # Common Python package name mappings (import name != pip package name)
    PYTHON_PACKAGE_ALIASES = {
        "PIL": "Pillow",
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "yaml": "PyYAML",
        "bs4": "beautifulsoup4",
        "dotenv": "python-dotenv",
        "jwt": "pyjwt",
    }

    @classmethod
    def extract_python_imports(cls, source_code: str) -> Set[str]:
        """
        Parses Python code using AST and returns top-level package names.
        """
        imported_packages: Set[str] = set()
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            # Fallback to regex if file has partial syntax
            for m in re.finditer(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", source_code, re.MULTILINE):
                imported_packages.add(m.group(1))
            return imported_packages

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_name = alias.name.split(".")[0]
                    imported_packages.add(top_name)
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:  # Not relative import
                    top_name = node.module.split(".")[0]
                    imported_packages.add(top_name)

        return imported_packages

    @classmethod
    def extract_js_imports(cls, source_code: str) -> Set[str]:
        """
        Extracts npm dependencies from JavaScript/TypeScript code using regex patterns.
        """
        imported_packages: Set[str] = set()

        # Matches: import ... from 'package' or "package"
        import_pattern = re.compile(r"""(?:import|export)\s+.*?from\s+['"]([^'"]+)['"]""")
        # Matches: require('package')
        require_pattern = re.compile(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""")

        for match in import_pattern.finditer(source_code):
            raw_path = match.group(1).strip()
            pkg = cls._normalize_npm_package_name(raw_path)
            if pkg:
                imported_packages.add(pkg)

        for match in require_pattern.finditer(source_code):
            raw_path = match.group(1).strip()
            pkg = cls._normalize_npm_package_name(raw_path)
            if pkg:
                imported_packages.add(pkg)

        return imported_packages

    @classmethod
    def _normalize_npm_package_name(cls, raw_path: str) -> Optional[str]:
        """Filters out relative paths and resolves scoped packages (@user/pkg)."""
        if raw_path.startswith((".", "/", "@/", "~")):
            return None
        parts = raw_path.split("/")
        if raw_path.startswith("@") and len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
        return parts[0]

    @classmethod
    def audit_python_repository(
        cls,
        code_files: Dict[str, str],
        requirements_content: str = "",
        manifest_filename: str = "requirements.txt",
    ) -> List[MissingDependencyFinding]:
        """
        Audits Python source files against requirements.txt.
        """
        declared_packages: Set[str] = set()
        for line in requirements_content.splitlines():
            clean = line.strip()
            if clean and not clean.startswith("#"):
                pkg = re.split(r"[><=~]", clean)[0].strip().lower().replace("-", "_")
                declared_packages.add(pkg)

        findings: List[MissingDependencyFinding] = []

        for file_path, source in code_files.items():
            if not file_path.endswith(".py"):
                continue

            imports = cls.extract_python_imports(source)
            for imp in imports:
                if imp in cls.PYTHON_STDLIB:
                    continue

                canonical_name = cls.PYTHON_PACKAGE_ALIASES.get(imp, imp)
                lookup_key = canonical_name.lower().replace("-", "_")

                if lookup_key not in declared_packages:
                    findings.append(
                        MissingDependencyFinding(
                            package_name=canonical_name,
                            imported_in_file=file_path,
                            manifest_file=manifest_filename,
                            manifest_type="python_requirements",
                            friendly_explanation=(
                                f"You used 'import {imp}' in `{file_path}`, but `{canonical_name}` is not listed in `{manifest_filename}`. "
                                f"When you push to Vercel, Railway, or Render, your deployment will fail with 'ModuleNotFoundError'."
                            ),
                            suggested_patch_line=f"{canonical_name}>=0.1.0",
                        )
                    )

        return findings

    @classmethod
    def audit_node_repository(
        cls,
        code_files: Dict[str, str],
        package_json_content: str = "",
        manifest_filename: str = "package.json",
    ) -> List[MissingDependencyFinding]:
        """
        Audits JS/TS source files against package.json dependencies.
        """
        declared_packages: Set[str] = set()
        if package_json_content:
            try:
                pkg_data = json.loads(package_json_content)
                all_deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                declared_packages = set(all_deps.keys())
            except Exception:
                pass

        findings: List[MissingDependencyFinding] = []

        for file_path, source in code_files.items():
            if not file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
                continue

            imports = cls.extract_js_imports(source)
            for imp in imports:
                if imp in cls.NODE_BUILTINS:
                    continue

                if imp not in declared_packages:
                    findings.append(
                        MissingDependencyFinding(
                            package_name=imp,
                            imported_in_file=file_path,
                            manifest_file=manifest_filename,
                            manifest_type="node_package_json",
                            friendly_explanation=(
                                f"You imported `{imp}` in `{file_path}`, but it's not installed in your `{manifest_filename}`. "
                                f"Your build server won't know where to download it!"
                            ),
                            suggested_patch_line=f'npm install {imp}',
                        )
                    )

        return findings

    @classmethod
    def generate_manifest_patch(
        cls,
        missing_findings: List[MissingDependencyFinding],
        original_manifest: str,
        manifest_type: str = "python_requirements",
    ) -> str:
        """
        Creates an auto-repaired manifest string with the missing packages inserted cleanly.
        """
        if manifest_type == "python_requirements":
            lines = original_manifest.splitlines()
            existing_clean = [l.strip() for l in lines]
            added_any = False
            for f in missing_findings:
                pkg_line = f.suggested_patch_line
                pkg_base = pkg_line.split(">=")[0]
                if not any(l.startswith(pkg_base) for l in existing_clean):
                    lines.append(pkg_line)
                    added_any = True
            return "\n".join(lines).strip() + "\n"

        elif manifest_type == "node_package_json":
            try:
                data = json.loads(original_manifest) if original_manifest.strip() else {}
                deps = data.get("dependencies", {})
                for f in missing_findings:
                    if f.package_name not in deps:
                        deps[f.package_name] = "^latest"
                data["dependencies"] = deps
                return json.dumps(data, indent=2) + "\n"
            except Exception:
                return original_manifest

        return original_manifest
