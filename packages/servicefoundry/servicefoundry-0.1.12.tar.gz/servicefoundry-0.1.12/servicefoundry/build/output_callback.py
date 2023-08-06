import sys


class OutputCallBack:

    def print_header(self, line):
        sys.stdout.write(line)

    def print_line(self, line):
        sys.stdout.write(line)
