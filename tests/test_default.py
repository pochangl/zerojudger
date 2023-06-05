import contextlib
from io import StringIO
from contextlib import redirect_stdout
from unittest import TestCase
from judge import DefaultJudge
import tempfile

@contextlib.contextmanager
def createfile(str):
    with tempfile.NamedTemporaryFile() as infile:
        infile.write(str.encode())
        infile.seek(0)
        yield infile


class DefaultJudgeTest(TestCase):
    def test_basic(self):
        judge = DefaultJudge()
        stdout = StringIO()
        with redirect_stdout(stdout), createfile('input') as infile, createfile('output input') as outfile, createfile('a = input(); print(f"output {a}")') as ansfile:
            judge.run(input_file_name=infile.name, output_file_name=outfile.name, answer_file_name=ansfile.name)
        stdout.seek(0)
        self.assertEqual(stdout.read(), '$JUDGE_RESULT=AC\n$LINECOUNT=\n$MESSAGE=\n$SYSTEMOUT=\n$USEROUT=\n')
