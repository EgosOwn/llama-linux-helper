# LLaMA Linux Helper 🐧🤝🏼🦙

This simple Python script wraps [llama.cpp](https://github.com/ggerganov/llama.cpp) to generate and (optionally) execute Linux shell commands from natural language. (NO GPU REQUIRED)

By default, it will use ~/llama.cpp/models/7B/ggml-model-f16-ggjt.bin but you can change this with the environment variables LLAMA_DIR and LINUX_HELP_LLAMA_MODEL respectively. The latter is a model file relative to the LLAMA_DIR/models/ directory.

I tested it with both LLaMA 7B and LLaMA 30B* (*actually Alpaca 30B but I don't think it matters since I don't use the instruct prompt)

There is a speed trade off, the larger models produce better results but take longer to run. On my i5-8400 I find 7B faster than searching the web or deciphering man pages, but not so for 30B.

## Installation and Usage

You need Python on Linux and LLaMA.cpp installed. From there you can drop the script, make it executable, and run it like so:

```./linux-help.py "Create zip file containing data.txt"```

Example result:

```zip -r data.zip data.txt```

It will ask if you want to run the resulting command, enter "y" if so, otherwise the command will not run.


# TODO (help welcome)

* Allow controling llama.cpp parameters from arguments
* Add option to include command explanation
* Add option to dump to a .sh file when LLaMA produces results starting with a shebang.
* Bash/zsh auto completion
* Do an Alpaca-type fine tuning (Will never distribute resulting model)

Maybe:

* Multiple prompt options
* Auto or manually specify distro or shell in the prompt
* Allow executing on remote SSH server (but copy back the results to run them)
* YOLO mode - Flag to auto exec resulting command (WCGW)
* Daemon mode to contextually suggest commands based on current session (Copilot will do this so likely will never implement)
