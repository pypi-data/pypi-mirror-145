#
#  Copyright (C) 2020 Codethink Limited
#  Copyright (C) 2020 Seppo Yli-Olli
#  Copyright (C) 2021 Abderrahim Kitouni
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. If not, see <http://www.gnu.org/licenses/>.
#
#  Authors:
#         Valentin David <valentin.david@codethink.co.uk>
#         Seppo Yli-Olli <seppo.yli-olli@iki.fi>
#         Abderrahim Kitouni <akitouni@gnome.org>

import os
import re
import shutil
import tarfile
import zipfile
import stat
import urllib.request
import json
from datetime import datetime
from buildstream import Source, SourceError, utils


def strip_top_dir(members, attr):
    for member in members:
        path = getattr(member, attr)
        trail_slash = path.endswith("/")
        path = path.rstrip("/")
        splitted = getattr(member, attr).split("/", 1)
        if len(splitted) == 2:
            new_path = splitted[1]
            if trail_slash:
                new_path += "/"
            setattr(member, attr, new_path)
            yield member


def make_key(item):
    for download in item[1]:
        if download["packagetype"] == "sdist":
            try:
                date = datetime.strptime(
                    download["upload_time_iso_8601"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            except ValueError:
                date = datetime.strptime(
                    download["upload_time_iso_8601"], "%Y-%m-%dT%H:%M:%SZ"
                )
            return date
    return datetime.fromtimestamp(0)


class PyPISource(Source):
    BST_MIN_VERSION = "2.0"

    def configure(self, node):
        node.validate_keys(
            [
                "url",
                "name",
                "sha256sum",
                "include",
                "exclude",
                "index",
                "scheme",
                "match_pattern",
            ]
            + Source.COMMON_CONFIG_KEYS
        )

        self.load_ref(node)
        self.name = node.get_str("name", None)
        if self.name is None:
            raise SourceError(f"{self}: Missing name")
        self.include = node.get_str_list("include", [])
        self.exclude = node.get_str_list("exclude", [])
        self.index = node.get_str("index", "https://pypi.org/pypi")
        self.scheme = node.get_str("scheme", None)
        if self.scheme is not None:
            self.match_pattern = node.get_str("match_pattern", None)
            if self.match_pattern is None:
                raise SourceError(
                    f"{self}: match_pattern mandatory when "
                    "scheme configured"
                )

    def preflight(self):
        pass

    def get_unique_key(self):
        return [self.original_url, self.sha256sum]

    def load_ref(self, node):
        self.sha256sum = node.get_str("sha256sum", None)
        self.original_url = node.get_str("url", None)
        if self.original_url is not None:
            self.url = self.translate_url(self.original_url)
        else:
            self.url = None

    def get_ref(self):
        if self.original_url is None or self.sha256sum is None:
            return None
        return {"url": self.original_url, "sha256sum": self.sha256sum}

    def set_ref(self, ref, node):
        node["url"] = self.original_url = ref["url"]
        node["sha256sum"] = self.sha256sum = ref["sha256sum"]

    def track(self):
        url = f"{self.index}/{self.name}/json"

        with urllib.request.urlopen(url) as response:
            payload = json.loads(response.read())

        releases = payload["releases"]
        if not releases:
            raise SourceError(
                f"{self}: Cannot find any tracking for {self.name}"
            )
        selected_release = None
        if self.include or self.exclude:
            includes = list(map(re.compile, self.include))
            excludes = list(map(re.compile, self.exclude))
            urls = self._calculate_latest(releases, includes, excludes)
        else:
            urls = releases[payload["info"]["version"]]
        found_ref = None
        for url in urls:
            if url["packagetype"] == "sdist":
                built_url = url["url"]
                if self.scheme is not None:
                    built_url = built_url.replace(
                        self.match_pattern, f"{self.scheme}:"
                    )
                found_ref = {
                    "sha256sum": url["digests"]["sha256"],
                    "url": built_url,
                }
                break

        if found_ref is None:
            raise SourceError(
                f"{self}: Did not find any sdist for {self.name} {selected_release}"
            )

        return found_ref

    def _calculate_latest(self, releases, includes, excludes):
        for release, urls in sorted(
            releases.items(), key=make_key, reverse=True
        ):
            if excludes:
                excluded = False
                for exclude in excludes:
                    if exclude.match(release):
                        excluded = True
                        break
                if excluded:
                    continue
            if includes:
                for include in includes:
                    if include.match(release):
                        return urls
            else:
                return urls

        raise SourceError(f"{self}: No matching release")

    def _get_mirror_dir(self):
        return os.path.join(
            self.get_mirror_directory(), utils.url_directory_name(self.name)
        )

    def _get_mirror_file(self, sha=None):
        return os.path.join(self._get_mirror_dir(), sha or self.sha256sum)

    def fetch(self):
        # More or less copied from _downloadablefilesource.py
        try:
            with self.tempdir() as tempdir:
                default_name = os.path.basename(self.url)
                request = urllib.request.Request(self.url)
                request.add_header("Accept", "*/*")
                request.add_header("User-Agent", "BuildStream/1")

                with urllib.request.urlopen(request) as response:
                    info = response.info()
                    filename = info.get_filename(default_name)
                    filename = os.path.basename(filename)
                    local_file = os.path.join(tempdir, filename)
                    with open(local_file, "wb") as dest:
                        shutil.copyfileobj(response, dest)

                if not os.path.isdir(self._get_mirror_dir()):
                    os.makedirs(self._get_mirror_dir())

                sha256 = utils.sha256sum(local_file)
                os.rename(local_file, self._get_mirror_file(sha256))
                return sha256

        except (
            urllib.error.URLError,
            urllib.error.ContentTooShortError,
            OSError,
        ) as e:
            raise SourceError(
                f"{self}: Error mirroring {self.url}: {e}", temporary=True
            ) from e

    def stage(self, directory):
        if not os.path.exists(self._get_mirror_file()):
            raise SourceError(
                f"{self}: Cannot find mirror file {self._get_mirror_file()}"
            )
        if self.url.endswith(".zip"):
            with zipfile.ZipFile(self._get_mirror_file(), mode="r") as zipf:
                exec_rights = (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) & ~(
                    stat.S_IWGRP | stat.S_IWOTH
                )
                noexec_rights = exec_rights & ~(
                    stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                )
                # Taken from zip plugin. It is needed to ensure reproducibility of permissions
                for member in strip_top_dir(zipf.infolist(), "filename"):
                    written = zipf.extract(member, path=directory)
                    rel = os.path.relpath(written, start=directory)
                    assert not os.path.isabs(rel)
                    rel = os.path.dirname(rel)
                    while rel:
                        os.chmod(os.path.join(directory, rel), exec_rights)
                        rel = os.path.dirname(rel)

                    if os.path.islink(written):
                        pass
                    elif os.path.isdir(written):
                        os.chmod(written, exec_rights)
                    else:
                        os.chmod(written, noexec_rights)
        else:
            with tarfile.open(self._get_mirror_file(), "r:gz") as tar:
                tar.extractall(
                    path=directory,
                    members=strip_top_dir(tar.getmembers(), "path"),
                )

    def is_cached(self):
        return os.path.isfile(self._get_mirror_file())


def setup():
    return PyPISource
