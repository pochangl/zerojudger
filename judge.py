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
        raise NotImplemented

class redirect_stdin(contextlib._RedirectStream):
    _stream = "stdin"


class DefaultJudge(Judge):
    def judge(self, inputStr: str, outputStr: str, answer: str) -> Result:
        with redirect_stdin(io.StringIO(inputStr)) as stdin, contextlib.redirect_stdout(io.StringIO()) as stdout:
            stdin.write(inputStr)
            stdin.seek(0)
            try:
                exec(answer, {}, {})
            except Exception as err:
                stdout.seek(0)
                return Result(JUDGE_RESULT='WA', USEROUT=outputStr, SYSTEMOUT=stdout.read(), MESSAGE=str(err))
        stdout.seek(0)
        out = stdout.read()
        if out.strip() != outputStr.strip():
            return Result(JUDGE_RESULT='WA', USEROUT=outputStr, SYSTEMOUT=out)
        else:
            return Result(JUDGE_RESULT='AC')


result = {"$JUDGE_RESULT": "", "$LINECOUNT": "",
          "$USEROUT": "", "$SYSTEMOUT": "", "$MESSAGE": ""}


def main(argv):
    if len(argv) != 3:
        print('special.py [inputfile] [ansfile] [outputfile]')
        sys.exit(2)

    infile = open(argv[0], 'r', encoding='UTF-8')
    ansfile = open(argv[1], 'r', encoding='UTF-8')
    outfile = open(argv[2], 'r', encoding='UTF-8')

    for index, (out, ans) in enumerate(zip_longest(outfile.readlines(), ansfile.readlines()), 1):
        if ans is None:
            result["$JUDGE_RESULT"] = "OLE"
            result["$LINECOUNT"] = str(index)
            result["$USEROUT"] = out.strip()
            result["$MESSAGE"] = "多餘的輸出。"
            return
        if out is None:
            result["$JUDGE_RESULT"] = "WA"
            result["$LINECOUNT"] = str(index)
            result["$MESSAGE"] = "沒有完整輸出答案。"
            return
        if out.strip() != ans.strip():
            result["$JUDGE_RESULT"] = "WA"
            result["$LINECOUNT"] = str(index)
            result["$USEROUT"] = out.strip()
            result["$SYSTEMOUT"] = ans.strip()
            result["$MESSAGE"] = "您的答案比對不符合。"
            return
    result["$JUDGE_RESULT"] = "AC"


if __name__ == "__main__":
    main(sys.argv[1:])
    for key in result:
        print(key+"="+result[key])
