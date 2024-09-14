# TryHackMe room description summarizer

It is very important to take notes during exercises, but can be exhausting and annoying. To be quicker at taking notes I wrote a simple script that crawls descriptions from a given TryHackMe room, which will be used to send to ollama running in the background. Ollama will output a concise summary of the descriptions using a modified prompt.
I assume that you already have a instance running of ollama, otherwise go [here](https://github.com/ollama/ollama) to get started with it.

If you want to summarize a room which requires a subscription, you need to set the `THM_SID` to your `connect_sid` - Value when logged in at TryHackMe.


## Installtion

1. Clone this repo and install the python requirements
```sh
git clone https://github.com/januwe/thm-summarizer.git
cd thm-summarizer
python3 -m pip install -r requirements.txt
```

2. Set environment variables in example env file and rename it
<details>
<summary>`env.example`</summary>

```sh
# TryHackMe vars
THM_SID="" # optional - only needed if you want to summarize a paid room

# Ollama vars
OLLAMA_URL="" # e.g. "http://localhost:11434"
OLLAMA_MODEL="" # e.g. "llama3.1"
```

</details>

```sh
mv env.example .env
```

3. Run script to summarize room (e.g. rrootme)
```sh
python3 thm_summarizer.py -r "rrootme"
```
