import sys
import io
import contextlib
from dataclasses import dataclass, field, asdict
from enum import Enum


class JUDGE_RESULT(Enum):
    ACCEPT = 'AC'
    WRONG_ANSWER = 'WA'


@dataclass
class Result:
    JUDGE_RESULT: str = field(default_factory=str)
    LINECOUNT: str = field(default_factory=str)
    USEROUT: str = field(default_factory=str)
    SYSTEMOUT: str = field(default_factory=str)
    MESSAGE: str = field(default_factory=str)


class Judge:
    def run(self, input_file_name: str, output_file_name: str, answer_file_name: str):
        with open(input_file_name) as infile, open(output_file_name) as outfile, open(answer_file_name) as ansfile:
            inputStr = infile.read()
            outputStr = outfile.read()
            answerStr = ansfile.read()

        result = self.judge(inputStr=inputStr, outputStr=outputStr, answer=answerStr)
        data = asdict(result)
        keys = list(data.keys())
        keys.sort()
        for key in keys:
            print("$"+key+"="+data[key])

    def judge(self, inputStr: str, outputStr: str, answer: str) -> Result:
        with redirect_stdin(io.StringIO(inputStr)) as stdin, contextlib.redirect_stdout(io.StringIO()) as stdout:
            try:
                self.execute(stdin=stdin, inputStr=inputStr, answerStr=answer)
            except Exception as err:
                stdout.seek(0)
                return Result(JUDGE_RESULT='WA', USEROUT=outputStr, SYSTEMOUT=stdout.read(), MESSAGE=str(err))
        stdout.seek(0)
        out = stdout.read()
        if out.strip() != outputStr.strip():
            return Result(JUDGE_RESULT='WA', USEROUT=outputStr, SYSTEMOUT=out)
        else:
            return Result(JUDGE_RESULT='AC')

    def execute(self, inputStr: str, outputStr: str):
        raise NotImplemented

class redirect_stdin(contextlib._RedirectStream):
    _stream = "stdin"


class DefaultJudge(Judge):
    def execute(self, stdin: io.IOBase, inputStr: str, answerStr: str):
        stdin.write(inputStr)
        stdin.seek(0)
        exec(answerStr, {}, {})


if __name__ == "__main__":
    infile, ansfile, outfile, *args = sys.argv[1:]
    DefaultJudge().run(input_file_name=infile, output_file_name=outfile, answer_file_name=ansfile)
