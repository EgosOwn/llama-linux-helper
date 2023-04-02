#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

cpu = str(os.cpu_count())

LLAMA_DIR = str(Path(os.getenv("LLAMA_DIR", "~/llama.cpp/")).expanduser()) + "/"

# Recommend to run with larger models, but it is a speed trade off.
LINUX_HELP_LLAMA_MODEL = LLAMA_DIR + "models/" + os.getenv("LINUX_HELP_MODEL", "7B/ggml-model-f16-ggjt.bin")

try:
	cmd_desc = sys.argv[1]
except IndexError:
	try:
		cmd_desc = input("Describe a command to generate: ")
	except KeyboardInterrupt:
		sys.exit(1)

prompt = f"A linux command that {cmd_desc}:\n" + r"\begin{code}"
input_file = "/tmp/cmd-input"
with open(input_file, "w") as f:
	f.write(prompt)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# TODO allow controlling parameters
cmd = [LLAMA_DIR + "main", "-m", LINUX_HELP_LLAMA_MODEL, "-f", input_file, "-b", "256", "--top_k", "10000", "--temp", "0.1", "--repeat_penalty", "1", "-t", cpu]

res = ""
with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
	for line in process.stdout:
		line = line.decode('utf-8')
		if r"\end{code}" in line:
			process.kill()
			break
			print(line.decode('utf8'))
		res += line


cmd_result = res.split(r"\begin{code}", 1)[1].replace("\end{code}", "").removeprefix("#").removeprefix("$").strip()
cleaned_result = ""
for line in cmd_result.split("\n"):
	line = line.removeprefix("#").removeprefix("$")
	cleaned_result += line
cmd_result = cleaned_result
if cmd_result:
	print("Run this? y/n")
	print(cmd_result)
	if input() == "y":
		os.system(cmd_result)
else:
	print("Output does not seem like a command, but here it is")
	print(res)

	
