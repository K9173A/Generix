"""
A module for file wrappers.
"""
import os
import itertools


class File:
    """
    Wrapper for an ordinary file.
    """
    def __init__(self, path, mode='a', encoding='utf-8', create=True):
        """
        Constructs file wrapper.
        :param path: path to the file.
        :param mode: opening mode.
        :param encoding: encoding system.
        :param create: create file if it does not exist.
        """
        self._path = path
        self._encoding = encoding
        self._mode = mode
        self._handle = None
        self._pos = 0

        if create and not self.exists():
            self.create()

    def __enter__(self):
        """
        Opens file handle for the context manager.
        :return: reference to the class instance.
        """
        self._handle = self.open(self._mode)
        return self

    def __exit__(self, *args):
        """
        Automatically closes file handle after all work is complete.
        :param args: additional parameters.
        :return: None.
        """
        self.close()

    def create(self):
        """
        Creates file.
        :return: None.
        """
        self._handle = self.open('w+')
        self.close()

    def open(self, mode):
        """
        Opens file in a needed mode.
        :param mode: opening mode.
        :return: file handle.
        """
        return open(self._path, mode, encoding=self._encoding)

    def delete(self):
        """
        Deletes a file from an OS.
        :return: None.
        """
        self.close()
        os.remove(self._path)

    def close(self):
        """
        Closes file handle.
        :return: None.
        """
        self._handle.close()

    def write(self, data):
        """
        Writes data to the file.
        :param data: data to be written.
        :return: None.
        """
        self._handle.write(data)

    def size(self):
        """
        Gets size of file.
        :return: file size.
        """
        return os.stat(self._path).st_size

    def seek(self, offset, whence=0):
        """
        Gets current cursor position at the offset.
        :param offset: the position of the read/write pointer within the file.
        :param whence: this is optional and defaults to 0 which means absolute file positioning,
        other values are 1 which means seek relative to the current position and 2 means seek
        relative to the file's end.
        :return: None.
        """
        self._handle.seek(offset, whence)

    def exists(self):
        """
        Checks whether file exists or not.
        :return: True if file exists, otherwise - False.
        """
        return os.path.isfile(self._path)

    def lines_count(self):
        """
        Gets amount of lines (quotes) in the WDMFile.
        :return: amount of lines.
        """
        return sum(1 for _ in open(self._path))

    def read_n_lines(self, n):
        """
        Reads n lines from the current cursor position.
        :param n: amount of lines.
        :return: list of n lines.
        """
        new_pos = self._pos + n
        lines = itertools.islice(self.open('r'), self._pos, new_pos)
        self._pos = new_pos
        return lines
