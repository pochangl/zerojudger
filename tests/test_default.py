from io import StringIO
from contextlib import redirect_stdout
from unittest import TestCase
from judge import DefaultJudge
from .utils import createfile


class DefaultJudgeTest(TestCase):
    def test_basic(self):
        judge = DefaultJudge()
        stdout = StringIO()
        with redirect_stdout(stdout), createfile('input') as infile, createfile('output input') as ansfile, createfile('a = input(); print(f"output {a}")') as solfile:
            judge.run(input_file_name=infile.name, solution_file_name=solfile.name, answer_file_name=ansfile.name)
        stdout.seek(0)
        self.assertEqual(stdout.read(), '$JUDGE_RESULT=AC\n$LINECOUNT=\n$MESSAGE=\n$SYSTEMOUT=\n$USEROUT=\n')
