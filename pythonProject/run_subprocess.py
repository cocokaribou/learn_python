#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import shlex

# 문자열 명령어 실행
def subprocess_open(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

# 배치 파일 등 실행
def subprocess_open_when_shell_false(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

# 문자열 명령어 실행
# shell 변수를 false 로 줄경우(default가 false) 명령어를 shelx.split() 함수로 프로세스가 인식 가능하게 잘라 주어야 함
def subprocess_open_when_shell_false_with_shelx(command):
    popen = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

# 커맨드 리스트 처리
# 커맨드 리스트를 이전 처리의 결과(stdout)를 다음 처리의 입력(stdin)으로 입력하여 순차적으로 처리
def subprocess_pipe(cmd_list):
    prev_stdin = None
    last_p = None

    for str_cmd in cmd_list:
        cmd = str_cmd.split()
        last_p = subprocess.Popen(cmd, stdin=prev_stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        prev_stdin = last_p.stdout

    (stdoutdata, stderrdata) = last_p.communicate()
    return stdoutdata, stderrdata


def main():
    idx = 0
    while idx < 5:  # scroll 5 times
        did = idx % 3
        print(f"index:{subprocess_open('python3 /Users/kwangbokchoi/python_sample/instagram-crawler-master/crawler.py following -u nice.english.sam -o ./output_following.txt -i '+ str(did))}")
        idx += 1

    # print subprocess_open_when_shell_false("./test.sh")
    # test.sh
    # #!/bin/bash
    # echo "aaa" | wc -l > b.txt
    # 실행결과
    # --> ('', '') 파일 b.txt 생성

    # print subprocess_open_when_shell_false_with_shelx('echo -n "aaa"')
    # 실행결과
    # ('aaa', '')

    # print subprocess_open_when_shell_false_with_shelx('echo "aaa" | wc -l')
    # 실행결과
    # ('aaa | wc -l\n', '')

    # print subprocess_pipe(['echo "aaa"', "wc -l"])
    # 실행결과
    # ('1\n', '')

if __name__ == "__main__":
    main()     
