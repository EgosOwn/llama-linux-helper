#!/usr/bin/env python3
import os
import sys
from time import time
from pathlib import Path
import argparse

from llama_cpp import Llama


LLAMA_DIR = str(Path(os.getenv("LLAMA_DIR", "~/llama.cpp/")).expanduser()) + "/"

# Recommend to run with larger models, but it is a speed trade off.
LINUX_HELP_LLAMA_MODEL = LLAMA_DIR + "models/" + os.getenv("LINUX_HELP_MODEL", "7B/ggml-model-f16-ggjt.bin")
llm = Llama(model_path=LINUX_HELP_LLAMA_MODEL, verbose=False)
parser = argparse.ArgumentParser(description='Generate a Linux command using LLaMA')
parser.add_argument('cmd', metavar='CMD', type=str,
                    help='description of the command to generate')
parser.add_argument('-k', '--top_k', type=int, default=1000,
                    help='number of top k to consider')
parser.add_argument('-o', '--oneliner', type=bool, default=True,
                    help='if it should be a single line command (default True)')
parser.add_argument('-n', '--max_tokens', type=int, default=50,
                    help='Maximum number of tokens to generate. Setting this too high will usually waste time (default 50))')
parser.add_argument('-p', '--top_p', type=float, default=0,
                    help='number of top p to consider (default 0)')
parser.add_argument('-t', '--temperature', type=float, default=0.8,
                    help='sampling temperature for the language model')
parser.add_argument('-repeat_last_n', type=int, default=10,
                    help='last n tokens to consider for penalize (default 10)')
parser.add_argument('-penalty', '--repeat_penalty', type=float, default=1,
                    help='repeat penalty for the language model (default 1))')

args = parser.parse_args()

cmd_desc = args.cmd

prompt = f"linux command that does the following: {cmd_desc}\n" + r"\begin{code}"


crap = [
    "\begin{pre}",
    "\end{pre}"
]

res = ""

stream = llm(
    prompt,
    max_tokens=360,
    stop=[r"\end{code}", r"\end{pre}"],
    stream=True,
    echo=False,
    temperature=args.temperature,
    top_p=args.top_p,
    top_k=args.top_k

)

code_seen = False

try:
    count = 0
    for part in stream:
        part = part['choices'][0]['text']
        if part.isspace() and not code_seen:
            continue
        code_seen = True
        res += part
        if args.oneliner and "\n" in part:
            break
except KeyboardInterrupt:
    sys.exit(1)

res = res.lstrip().removeprefix("#!/bin/bash").removeprefix("#!/bin/sh").removeprefix('#').removeprefix('$').lstrip()
print(res)