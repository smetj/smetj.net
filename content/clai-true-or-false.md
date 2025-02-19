Title: Clai - True or False
Date: 2025-02-18 21:00  
Modified: 2025-02-18 21:00  
Category: Technology  
Tags: cli, llm, ai
Slug: clai-true-or-false
Authors: Jelle Smet  
Description: Creating true or false statements with Clai.  
Image: images/clai-true-or-false.webp

## Intro

[Clai](https://github.com/smetj/clai/) is a CLI tool to interact with large
language models (LLMs). One of my goals was to have the ability to feed data
into it and evaluate true or false statements such that it can be used to
implement complex logic in Bash scripts or pipelines, such as GitHub workflows.

## Initial Results

My first attempt was to create a prompt that returns `true`, `false`, or
`inconclusive`. The idea was to get `inconclusive` whenever the user did not
provide enough data for the LLM to determine `true` or `false`:

```text
You can only answer using one of 3 values: true, false, or inconclusive. True to affirm, false to negate, or inconclusive if the question cannot be answered with true or false.
```

The results were inconsistent, with no clear way to understand why, as it only
responded with true, false, or inconclusive.

!!! note "¬‿¬"  
    An initial realization was that, despite aligning various model parameters,
    I could not achieve the same results through the API as compared to the UI.
    I'm not entirely sure why, but prompts through the UI were significantly
    more accurate than those done through the API.

One example I couldn't get to work was:

```bash
git diff -U1000 | clai --bool --prompt "Does the code change in this diff include a corresponding new unit test or change to an existing unit test?"
inconclusive
```

Even clearly flawed examples were stubbornly answered with `inconclusive`, while the same prompt done over the UI was consistently correct.

## Revisiting the Approach

To gain insight into its reasoning, I extended the prompt to include the reason for its conclusion. Surprisingly, prompts previously answered incorrectly were now answered correctly.

!!! note "( ͡° ͜ʖ ͡°)_/¯"  
    It seems that requesting a reasoning for the answer significantly improved
    the accuracy of the responses.

Additionally, I decided to drop the `inconclusive` option as it complicated
matters. Instead, I opted for it to answer `false` and explain why there was
insufficient context. This approach better suits structured output. This changed
my prompt to:

```text
Analyze the following statement or question without inferring missing
information and provide a structured response containing two elements:
1. Answer – A definitive 'True' or 'False' based on the given information.
2. Reason – A brief explanation justifying both the answer and whether the context was sufficient or not.
```

## Structured Output

Since the answer now consists of two parts —a true/false and a reason— we need a
reliable way to parse the output. OpenAI offers a feature that allows the LLM to
reply with 
[structured output](https://openai.com/index/introducing-structured-outputs-in-the-api/).

From an API perspective, you simply need to provide a JSON schema describing the
[response format](https://github.com/smetj/clai/blob/819a07309ff30e550c82246f6b215173d613416f/clai/__init__.py#L33).
This also makes it more reliable for `Clai` to match its return code to the
answer: `0` for `true` or `1` for `false`.

## Examples

### True

```bash
echo "red and yellow" | clai --bool --prompt "Does mixing these two colors yield orange?"
{"answer":true,"reason":"Mixing red and yellow colors together yields orange. The context provided is sufficient to determine this outcome."}
```

### False/Conclusive

```bash
echo "red and blue" | clai --bool --prompt "Does mixing these two colors yield orange?"
{"answer":false,"reason":"Mixing red and blue typically yields purple, not orange. The context provided is sufficient to determine this."}
```

### False/Inconclusive

```bash
echo "red and" | clai --bool --prompt "Does mixing these two colors yield orange?"
{"answer":false,"reason":"The statement is incomplete as it only provides one color, 'red', and does not specify the second color needed to determine if mixing them yields orange. Therefore, the context is insufficient to answer the question definitively."}
```
### Exit codes

The exit code is mapped to the outcome of the evaluation. `0` for `true` and `1`
for `false` which allows for all kinds of creative logic constructions in Bash.

```bash
response=$(git diff | clai --bool --prompt "This diff includes a unit test") || echo $response | jq .reason
"The provided diff does not include any unit test code. It only shows changes to a markdown file, which includes text and formatting changes, but no code that would constitute a unit test. Therefore, the statement is false based on the given information."
```


## Final words

While developing this feature, I have gained some interesting insights into the
behaviors of LLMs:

- Despite efforts to align parameters, responses from the UI are more accurate
  than those from the API. This can quickly become a distraction when focusing
  on alignment. You probably should not to get too caught up in this.
- Requesting LLMs to provide references for the data supporting their answers
  results in more accurate responses compared to simply asking for the answer.

I suspect that due to the rapid developments in LLMs, this specific knowledge
may not remain relevant for long. However, gaining exposure to the behavioral
challenges of LLMs has been the most valuable aspect.

I hope the `--bool` feature proves useful to you and allows you to develop a
quick and simple solution to a problem that might otherwise be more complex and
time-consuming. If not, perhaps my shared observations can assist or inspire you
in your current projects.
