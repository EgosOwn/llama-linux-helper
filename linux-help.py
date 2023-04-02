#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path
import argparse

cpu = str(os.cpu_count())

LLAMA_DIR = str(Path(os.getenv("LLAMA_DIR", "~/llama.cpp/")).expanduser()) + "/"

# Recommend to run with larger models, but it is a speed trade off.
LINUX_HELP_LLAMA_MODEL = LLAMA_DIR + "models/" + os.getenv("LINUX_HELP_MODEL", "7B/ggml-model-f16-ggjt.bin")

parser = argparse.ArgumentParser(description='Generate a Linux command using LLaMA')
parser.add_argument('cmd', metavar='CMD', type=str,
                    help='description of the command to generate')
parser.add_argument('-k', '--top_k', type=int, default=10000,
                    help='number of top k to consider')
parser.add_argument('-n', '--max_tokens', type=int, default=50,
                    help='Maximum number of tokens to generate. Setting this too high will usually waste time (default 50))')
parser.add_argument('-p', '--top_p', type=float, default=0.9,
                    help='number of top p to consider (default 0.9)')
parser.add_argument('-t', '--temperature', type=float, default=0.1,
                    help='sampling temperature for the language model')
parser.add_argument('-repeat_last_n', type=int, default=3,
                    help='last n tokens to consider for penalize (default 3)')
parser.add_argument('-penalty', '--repeat_penalty', type=float, default=1,
                    help='repeat penalty for the language model (default 1))')
parser.add_argument('-b', '--batch_size', type=int, default=256,
                    help='batch size for the language model')
args = parser.parse_args()

cmd_desc = args.cmd

prompt = f"linux command that does the following: {cmd_desc}:\n" + r"\begin{code}"
input_file = "/tmp/cmd-input"
with open(input_file, "w") as f:
    f.write(prompt)

# TODO allow controlling parameters
cmd = [LLAMA_DIR + "main",
	"-m", LINUX_HELP_LLAMA_MODEL,
	"-f", input_file, "-b", str(args.batch_size), "--top_k", str(args.top_k), "--temp", str(args.temperature),
	"--repeat_penalty", str(args.repeat_penalty),
	"--repeat_last_n", str(args.repeat_last_n),
	"-t", cpu]

res = ""
try:
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            line = line.decode('utf-8')
            if r"\end{code}" in line:
                process.kill()
                break
            res += line
except KeyboardInterrupt:
    sys.exit(1)

cmd_result = res.split(r"\begin{code}", 1)[1].replace("\end{code}", "").removeprefix("#").removeprefix("$").strip()
cleaned_result = ""
for line in cmd_result.split("\n"):
    line = line.removeprefix("#").removeprefix("$")
    cleaned_result += line
cmd_result = cleaned_result
cmd_result = cmd_result.split("llama_print_timings", 1)[0]
if cmd_result:
    print(cmd_result)
    print("\nRun this? y/n")
    try:
        if input() == "y":
            os.system(cmd_result)
    except KeyboardInterrupt:
        pass
else:
    print("Output does not seem like a command, but here it is:\n")
    print(res)
