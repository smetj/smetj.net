Title: Cutting through slop with minimal time and attention
Date: 2025-10-30 20:00
Modified: 2025-10-30 20:00
category: productivity
Tags: clai, youtube, AI
Slug: cutting-through-slop-with-minimal-time-and-attention
Authors: Jelle Smet
image: images/cutting-through-slop-with-minimal-time-and-attention.png

----

> *We are living in the attention economy more than ever. While algorithms
   initially used human-made content to captivate our attention, they are now
   bombarding us with AI generated slop. What tools can we apply to cut
   through this and extract the essence saving precious time and attention.*

----

# AI generated slop

The other day, I was browsing YouTube and my attention was caught by one of
its suggestions titled: *"The Heartbreaking Tragedy of Chip Foose from
Overhaulin'"* with a thumbnail showing Chip in the front and a car crash in
the background.

I remember watching the show when I was younger, fascinated by his drawing
skills and tasteful car overhauls. He always came across as a nice person, so
yes, I got emotionally engaged thinking the worst given the dramatic
backdrop. The algorithm got me on its hook and started to reel me in as I
clicked the video and started watching. A couple of minutes in, I felt that
the content was being dragged out, the images started to repeat and the story
did a lot of backtracking which made me realize that I was probably watching
AI-generated content. Surprisingly, reading the description, it was actually
tagged as AI generated content. With a total length of around 28 minutes, I
wasn't going to spend more of my time on this slop.

But still ... What happened to the guy? ..


# Forging a new axe

As it won't be the last time I'll have to deal with this nonsense I'm going to
need something which allows me to extract what I need to know from a Youtube
video without having to spend any time to it. Luckily, the necessary tools
already exist, and thanks to a 50 year old Unix principle[^1], we can create
something quickly which does exactly that.

## yt-dlp

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is a feature-rich command-line
audio/video downloader which allows us to download the captions of Youtube
videos. The many options are a little involved so we create the following
convenience function in `Bash` which downloads the captions, strips off all
XML syntax and spits out the results to STDOUT:

```bash
get-yt-captions (){
    tmp=$(mktemp);
    trap 'rm -f "$tmp" "$tmp.en.srv1"' RETURN;
    yt-dlp --skip-download \
           --no-warnings -q \
           --write-auto-sub --sub-format srv1 --sub-lang en \
           -o "$tmp" "$1";
    xmllint --xpath '//text/text()' "$tmp.en.srv1"
}
```

## clai

[Clai](https://github.com/smetj/clai) is a CLI tool I wrote to interact with
various LLM/AI models. It allows us to to pipe the aforementioned downloaded
captions into it and process them however we desire.

```
$ echo "Roses are red" | clai prompt "Complete the poem's opening sentence."
Roses are red, violets are blue.
```

# Putting it all together

```text
$ get-yt-captions 'https://www.youtube.com/watch?v=TffKMCop8xw' | \
clai prompt "Summarize in a single sentence what happened to Chip."

After rising to TV stardom on Overhaulin’, Chip endured punishing workloads
and reputational fallout from a partner’s scandal, then quietly withdrew from
public life to build cars privately and focus on his family.
```

Ah, great to read that Chip is doing just fine. ✌️ 😎

### Closing words

Hopefully this little workflow helps you cut through the artificial fog and
keep your attention focused where it matters.

Stay sharp, stay curious, and don’t let the slop win.


# Footnotes

[^1]: [Pipeline(Unix)](https://en.wikipedia.org/wiki/Pipeline_%28Unix%29)
