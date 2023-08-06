from typing import List, Tuple


class CecaSorter(object):
    def __init__(
        self, contents: str, delimiter: str, project_modules: List[str]
    ) -> None:
        self.contents = contents
        self.delimiter = delimiter
        self.insert_counter = 0
        self.first_library = ["__future__"]
        self.first_libs: List[Tuple[str, str]] = []
        # the simplest approach to handle which modules
        # comes from builtin library is
        # to simple freeze complete list of them.
        self.standard_library = [
            "abc", "anydbm", "argparse", "array",
            "asynchat", "asyncore", "atexit", "base64", "BaseHTTPServer",
            "bisect", "bz2", "calendar", "cgitb", "cmd", "codecs",
            "collections", "commands", "compileall", "ConfigParser",
            "contextlib", "Cookie",
            "copy", "cPickle", "cProfile", "cStringIO", "csv", "datetime",
            "dbhash", "dbm", "decimal", "difflib", "dircache", "dis",
            "doctest",
            "dumbdbm", "EasyDialogs", "exceptions", "filecmp", "fileinput",
            "fnmatch", "fractions", "functools", "gc", "gdbm", "getopt",
            "getpass", "gettext", "glob", "grp", "gzip", "hashlib", "heapq",
            "hmac", "imaplib", "imp", "inspect", "itertools", "json",
            "linecache",
            "locale", "logging", "mailbox", "math", "mhlib", "mmap",
            "multiprocessing", "operator", "optparse", "os", "os.path", "pdb",
            "pickle", "pipes", "pkgutil", "platform", "plistlib", "pprint",
            "profile", "pstats", "pwd", "pyclbr", "pydoc", "Queue", "random",
            "re", "readline", "resource", "rlcompleter", "robotparser",
            "sched",
            "select", "shelve", "shlex", "shutil", "signal",
            "SimpleXMLRPCServer",
            "site", "sitecustomize", "smtpd", "smtplib", "socket",
            "SocketServer",
            "sqlite3", "string", "StringIO", "struct", "subprocess", "sys",
            "sysconfig", "tabnanny", "tarfile", "tempfile", "textwrap",
            "threading", "time", "timeit", "trace", "traceback", "unittest",
            "urllib", "urllib2", "urlparse", "usercustomize", "uuid",
            "warnings",
            "weakref", "webbrowser", "whichdb", "xml", "xml.etree.ElementTree",
            "xmlrpclib", "zipfile", "zipimport", "zlib"
        ]
        self.standard_libs: List[Tuple[str, str]] = []
        self.proj_libs: List[Tuple[str, str]] = []
        self.other_libs: List[Tuple[str, str]] = []
        self.project_modules = project_modules

    def is_standard_library(self, library: str) -> bool:
        return library in self.standard_library

    def is_project_library(self, library: str) -> bool:
        return library.split('.')[0] in self.project_modules

    def is_first_library(self, library: str) -> bool:
        return library in self.first_library

    def append_libs(self, libs: List[Tuple[str, str]]) -> None:
        for line in libs:
            self.filtered.insert(
                self.insert_counter + self.first_import_line - 1, line[1])
            self.insert_counter += 1
        self.filtered.insert(
            self.insert_counter + self.first_import_line - 1, '')
        self.insert_counter += 1

    def reorganize(self) -> str:
        self.filtered = []
        contents = self.contents.splitlines()
        self.first_import_line = 0
        end_line = 0
        line_no = 1

        counter = 0
        while counter < len(contents):
            line = contents[counter]
            base_line = line
            if line.startswith('import') or line.startswith('from'):
                # pep8 compatible syntax handling.
                if "(" in line:
                    base_line = line
                    next_line = ""
                    while ")" not in next_line and counter < len(contents):
                        counter += 1

                        try:
                            next_line = contents[counter]
                        except IndexError:
                            break

                        base_line += "\n" + next_line
                if not self.first_import_line:
                    # mark first occurence of import statement.
                    self.first_import_line = line_no
                source = line.split()[1]
                if self.is_standard_library(source):
                    self.standard_libs.append((source, base_line))
                elif self.is_project_library(source):
                    self.proj_libs.append((source, base_line))
                elif self.is_first_library(source):
                    self.first_libs.append((source, base_line))
                else:
                    self.other_libs.append((source, base_line))
            elif self.first_import_line and not end_line and not line.strip():
                # ignore empty lines in the imports area.
                pass
            else:
                if line.strip():
                    if self.first_import_line:
                        end_line = line_no
                self.filtered.append(line)
                line_no += 1
            counter += 1

        # sort each import section.
        self.standard_libs.sort()
        self.first_libs.sort()
        self.proj_libs.sort()
        self.other_libs.sort()

        if self.first_libs:
            self.append_libs(self.first_libs)
        if self.standard_libs:
            self.append_libs(self.standard_libs)
        if self.other_libs:
            self.append_libs(self.other_libs)
        if self.proj_libs:
            self.append_libs(self.proj_libs)

        self.filtered.insert(
            self.insert_counter + self.first_import_line - 1, '')
        return "\n".join(self.filtered)
