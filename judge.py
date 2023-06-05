import sys
import io
import contextlib
from enum import Enum


class JUDGE_RESULT(Enum):
    ACCEPT = 'AC'
    WRONG_ANSWER = 'WA'


class Result:
    def __init__(self, JUDGE_RESULT: str='', LINECOUNT: str='', USEROUT: str='', SYSTEMOUT: str='', MESSAGE: str=''):
        self.JUDGE_RESULT = JUDGE_RESULT
        self.LINECOUNT = LINECOUNT
        self.USEROUT = USEROUT
        self.SYSTEMOUT = SYSTEMOUT
        self.MESSAGE = MESSAGE

    JUDGE_RESULT: str = ''
    LINECOUNT: str = ''
    USEROUT: str = ''
    SYSTEMOUT: str = ''
    MESSAGE: str = ''

    def asdict(self):
        return {
            '$JUDGE_RESULT': self.JUDGE_RESULT,
            '$LINECOUNT': self.LINECOUNT,
            '$USEROUT': self.USEROUT,
            '$SYSTEMOUT': self.SYSTEMOUT,
            '$MESSAGE': self.MESSAGE,
        }


class Judge:
    def run(self, input_file_name: str, solution_file_name: str, answer_file_name: str):
        with open(input_file_name) as infile, open(solution_file_name) as solfile, open(answer_file_name) as ansfile:
            inputStr = infile.read()
            solStr = solfile.read()
            answerStr = ansfile.read()

        result = self.judge(inputStr=inputStr, solStr=solStr, answer=answerStr)
        data = result.asdict()
        keys = list(data.keys())
        keys.sort()
        for key in keys:
            print(key+"="+data[key])

    def judge(self, inputStr: str, solStr: str, answer: str) -> Result:
        with redirect_stdin(io.StringIO(inputStr)) as stdin, contextlib.redirect_stdout(io.StringIO()) as stdout:
            try:
                self.execute(stdin=stdin, inputStr=inputStr, solStr=solStr)
            except Exception as err:
                stdout.seek(0)
                return Result(JUDGE_RESULT='WA', USEROUT=stdout.read(), SYSTEMOUT=answer, MESSAGE=str(err))
        stdout.seek(0)
        out = stdout.read()
        if out.strip() != answer.strip():
            return Result(JUDGE_RESULT='WA', USEROUT=out, SYSTEMOUT=answer)
        else:
            return Result(JUDGE_RESULT='AC')

    def execute(self, stdin: io.IOBase, inputStr: str, solStr: str):
        raise NotImplemented


class redirect_stdin(contextlib._RedirectStream):
    _stream = "stdin"


class DefaultJudge(Judge):
    def execute(self, stdin: io.IOBase, inputStr: str, solStr: str):
        stdin.write(inputStr)
        stdin.seek(0)
        exec(solStr, {}, {})


class ExecJudge(Judge):
    def execute(self, stdin: io.IOBase, inputStr: str, solStr: str):
        glb = {}
        loc = {}
        exec(solStr, glb, loc)
        exec(inputStr, glb, loc)


if __name__ == "__main__":
    infile, ansfile, solfile, *args = sys.argv[1:]
    ExecJudge().run(input_file_name=infile, solution_file_name=solfile, answer_file_name=ansfile)
