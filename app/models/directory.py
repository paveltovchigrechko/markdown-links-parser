"""
Everything related to Directory class.
"""
import logging
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from app.models.markdown_file import MarkdownFile
from app.utils import constants


class Directory:
    """
    Class that represents a directory where recursively lie the files to be parsed.
    """

    def __init__(self, path: str) -> None:
        """

        :param path (str): Absolute or relative directory path.
        """
        if not isinstance(path, str):
            raise TypeError('Path must be a string.')

        try:
            resolved_path = Path(path).resolve(strict=True)
            if not resolved_path.is_dir():
                logging.error(f'The path "{path}" is not a directory path.')
                raise ValueError('The past must be to a directory.')
        except RuntimeError:
            logging.error(f'Infinite loop when trying to resolve "{path}".')
            raise
        except FileNotFoundError:
            logging.error(f'Cannot find directory by path "{path}".')
            raise

        self.files = {}
        self._path = resolved_path
        self._file_paths = []

    @property
    def path(self):
        return self._path

    def scan_files_by_extension(self, file_extensions: Iterable[str]) -> None:
        """
        Scan recursively all matches by given extensions inside the directory path.
        If the match is a file, create a pathlib.Path, and add the path to it in self._file_paths.
        :param file_extensions: Any iterable of strings representing the file extensions to scan.
        All non-strings are skipped.
        :return: None
        """
        try:
            # Remove duplicated extensions in iterable
            file_extensions_fset = frozenset(file_extensions)
        except TypeError as ex:
            logging.error(ex)
            return None

        for extension in file_extensions_fset:
            if not isinstance(extension, str) or not extension:
                logging.warning(f'Value ~{extension}~ must be a non-empty string, skipping value...')
                continue
            for extension_match in self.path.glob(f'**/*{extension}'):
                if extension_match.is_file():
                    self._file_paths.append(extension_match)

    def init_files(self) -> None:
        for file_path in self._file_paths:
            try:
                markdown_file = MarkdownFile(file_path)
            except (TypeError, ValueError) as ex:
                print(f'Cannot create a file by {file_path}: {ex}')
            else:
                markdown_file.parse_links_and_headings(commented_pattern=constants.COMMENTED_LINE_PATTERN)
                self.files[file_path] = markdown_file

    def validate_markdown_links(self) -> defaultdict[str, list] | None:
        if not self.files:
            print('There are no initiated files in directory.')
            return None

        broken_links = defaultdict(list)
        for markdown_file in self.files.values():
            broken_inbound_links = markdown_file.check_inbound_links()
            if broken_inbound_links:
                broken_links[str(markdown_file.path)].extend(broken_inbound_links)

            if not markdown_file.outbound_links:
                continue

            for line_num, markdown_link in markdown_file.outbound_links:
                path = markdown_link.url_path or ''
                path += markdown_link.url_file
                reference_path = Path(markdown_file.path_wo_name).joinpath(path).resolve()
                if reference_path.exists():
                    if (markdown_link.url_heading
                            and markdown_link.url_heading not in self.files[reference_path].headings):
                        broken_links[str(markdown_file.path)].append((line_num, markdown_link))
                    else:
                        continue
                else:
                    print(f'Not found file by {reference_path}')
                    broken_links[str(markdown_file.path)].append((line_num, markdown_link))

        return broken_links


if __name__ == "__main__":
    pass
# d = Directory('../../../doc-dev/docs')
# d.scan_files_by_extension(['.mdx'])
# d.init_files()
# # for file in d.files:
# #     print(file)
# br = d.validate_markdown_links()
# for file, broken_links in br.items():
#     print(f'File: {file}')
#     for line, broken_link in broken_links:
#         print(f'Line {line}: not found "{broken_link.url}"')
#     print('======================\n')
