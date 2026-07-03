# Why Your Morning Routine is Broken (and How Nine Decisions Fix It)

Founders do not have a productivity problem. They have a prioritisation problem. Every morning starts with a full list and ends with the loudest items crossed off, not the most important ones. The urgent crowds out the consequential. The day that felt busy produced nothing that compounds.

The Morning Brief changes the input before the day starts.

---

## What the nine decisions are

Every business turns on a small number of recurring forks. Not tasks. Not projects. Decisions that come back again and again, and whose answers, over time, determine the shape of the business.

Examples: which work to take on this week, whether to build or buy, which channel gets the content, which hire fills the next gap. The specifics belong to your business, not to a framework.

The nine decisions are not a list you follow. They are a filter you apply. When you name them once and keep them in a file, every brief you run passes today's priorities through that filter. The items that do not touch any of the nine move to the bottom. The items that advance one or more move to the top.

That is the entire mechanism.

---

## Why nine

Nine is not a magic number. It is a working number.

Fewer than five and the filter is too coarse. Decisions that feel different collapse into each other and the brief loses resolution. More than twelve and the list becomes a taxonomy instead of a tool. You start debating which category a thing belongs to instead of deciding what to do first.

Nine fits in working memory. You can hold nine things without counting them. That matters when you are reading a brief at 7am before the day starts.

---

## Why writing it down matters

Named decisions make patterns visible. Keep a `friday/nine-decisions.md` file and update it over time. You start to see which decisions keep coming back. Which have gone automatic. Which the business has moved past.

Update this file once a quarter and you are running a different business. One that uses the recurring decisions as a compass, not a generic to-do app.

---

## What the brief does not do

The Morning Brief does not connect to your inbox. It does not read your calendar. It does not pull live data from any system.

That is not a limitation. That is the design.

You bring your priorities. The brief gives them structure. The value is not in the data source; it is in the filter. Paste your open items. Get back a decision-mapped read of the day. That is a different operating mode than opening your inbox and reacting.

When you want it pulling from your real stack and running before you wake up, that is Friday. That is the difference between a command you run and a system that runs itself.

---

## The growing config

The Morning Brief is the third capability in the ladder.

The Voice Installer (the `/voice-installer` command) wrote `friday/voice.md`. The Decision Runner (the `/decide` command) appended to `friday/decisions.md`. This command adds `friday/nine-decisions.md` and `friday/morning.md`.

Open your `friday/` folder after this runs. You built that by hand. Each file represents a real capability running on your machine.

---

## Run it now

You need Claude Code installed and open. If you do not have it yet: https://docs.anthropic.com/claude-code

```
curl -fsSL https://raw.githubusercontent.com/ronsleyvaz/Friday-Foundation/release/install.sh | bash -s -- brief
```

Then in Claude Code:

```
/brief
```

The first run names your nine decisions. Every run after that takes two minutes and gives you a brief built around your business, not a generic productivity list.

---

Built by Amplify AI at amplifyais.com
