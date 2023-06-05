import subprocess
from io import StringIO
from contextlib import redirect_stdout
from unittest import TestCase
from judge import ExecJudge
from .utils import createfile


class ExecJudgeTest(TestCase):

    def test_execute(self):
        judge = ExecJudge()
        stdout = StringIO()
        with redirect_stdout(stdout), createfile('print(add(1, 2))') as infile, createfile('3') as outfile, createfile('def add(a, b):\n  return a + b') as ansfile:
            judge.execute(None, 'print(add(1, 2))',
                        'def add(a, b):\n  return a + b')
        stdout.seek(0)
        self.assertEqual(stdout.read(
        ), '3\n')

    def test_cmd(self):
        with createfile('print(add(1, 2))') as infile, createfile('3') as outfile, createfile('def add(a, b):\n  return a + b') as ansfile:
            result = subprocess.Popen(['python3', 'judge.py', infile.name, ansfile.name, outfile.name], stdout=subprocess.PIPE)
            stdout, _ = result.communicate()

        self.assertEqual(
            stdout.decode(), '$JUDGE_RESULT=AC\n$LINECOUNT=\n$MESSAGE=\n$SYSTEMOUT=\n$USEROUT=\n')

    def test_basic(self):
        judge = ExecJudge()
        stdout = StringIO()
        with redirect_stdout(stdout), createfile('print(add(1, 2))') as infile, createfile('3') as outfile, createfile('def add(a, b):\n  return a + b') as ansfile:
            judge.run(input_file_name=infile.name,
                      output_file_name=outfile.name, answer_file_name=ansfile.name)
        stdout.seek(0)
        self.assertEqual(stdout.read(
        ), '$JUDGE_RESULT=AC\n$LINECOUNT=\n$MESSAGE=\n$SYSTEMOUT=\n$USEROUT=\n')
