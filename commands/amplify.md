---
name: amplify
description: Run the Amplify growth diagnostic on your business. Scores your eight vital signs, detects your business stage, maps to your priority growth quadrant, runs the SymbioEthical check, and writes a prioritised 90-day plan to friday/growth.md. Based on the Amplify AI method.
---
<!-- Content licensed under LICENSE-CONTENT. See that file for terms. -->
# /amplify

Run the Amplify growth diagnostic. This command walks you through eight business vital signs, finds your biggest growth opportunity, runs an ethics check on the recommendation, matches AI tools to your experience level, and writes a prioritised plan to `friday/growth.md`.

You, Claude, run the whole flow below in order, using your own file tools. There is no module to import and nothing to install. Everything happens in this session.

The method behind this command is described in full in the book: https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

---

## Step 1: Read the founder's voice profile (if it exists)

Check whether `friday/voice.md` exists in the current directory. If it does, read it and write all output from this command in the founder's voice, matching their tone, rhythm, signature phrases, and banned words.

If `friday/voice.md` does not exist, write in a direct, plain style: short sentences, no hedging, active voice.

## Step 2: Explain the diagnostic

Tell the founder:

> The Amplify diagnostic takes about five minutes. You will score eight areas of your business from 1 to 10. Honest scores get you a useful plan. Optimistic scores get you a plan that misses the real gap.
>
> After the scores, I will ask one more question about your primary challenge. Then I will work out your priority growth area, your biggest opportunity, and a 90-day plan.

## Step 3: Score the eight vital signs

Tell the founder:

> Score each area from 1 to 10.
> 1-3 means it is actively limiting your growth.
> 4-6 means it needs attention but is not a crisis.
> 7-10 means it is working and can be built on.

Ask for scores one at a time, waiting for each answer before moving to the next:

1. **Leads** -- How strong is your lead flow right now? Quality and volume of new prospects coming in.
2. **Meetings** -- How many qualified sales conversations do you have each month? Are they turning into opportunities?
3. **Sales** -- How is your close rate? Are you converting conversations into paying clients or customers?
4. **Profit** -- How are your margins? Is the business financially sustainable and generating cash?
5. **Content** -- How consistently are you publishing? Is your content generating engagement and authority?
6. **Partnerships** -- How active is your referral and partnership network? Are you getting introductions?
7. **Audience** -- How large and engaged is your audience across all channels?
8. **Team** -- How well does your team handle the workload? Are you the bottleneck?

After collecting all eight scores, summarise them back to the founder:

> Here is where you are:
> - Revenue area (Leads, Meetings, Sales, Profit): [list the four scores]
> - Brand area (Content, Partnerships): [list the two scores]
> - Audience area: [the score]
> - Operations area (Team): [the score]

## Step 4: Identify the primary challenge

Ask:

> One more question. Which of these feels like your biggest challenge right now? Pick the one that is most true today.
>
> A) Growing revenue -- getting more clients, better close rates, or bigger deals
> B) Building brand trust -- becoming better known and more credible in your market
> C) Expanding audience -- growing your reach and community
> D) Improving operations -- removing bottlenecks and scaling without burning out

Wait for their answer (A, B, C, or D).

## Step 5: Detect business stage and priority growth area

Work out the stage and the priority quadrant using this logic:

**Stage detection:**

Look at the Profit and Sales scores first:
- If either Profit or Sales is 4 or below, the founder is at the **Startup stage**. Revenue is the priority, regardless of the other scores.
- If both Profit and Sales are above 4, check Partnerships. If Partnerships is 4 or below and the primary challenge is brand trust, the priority is **Brand**. If Partnerships is 4 or below and the challenge is revenue growth, stay on **Revenue**.
- If Profit, Sales, and Partnerships are all above 4, check the Team score. If Team is 6 or below and the primary challenge is operations, the priority is **Operations**. If the primary challenge is expanding audience, the priority is **Audience**.
- If all scores are strong (7+), the founder is at the **Scaling stage**. Operations is the priority.

**Quadrant priority order (use this to break ties):**
1. Revenue (most urgent, foundational)
2. Brand (builds on revenue)
3. Audience (builds on brand)
4. Operations (builds on everything)

Tell the founder their stage and priority area:

> You are at the [Startup / Growing / Established / Scaling] stage. Your priority growth area is [Revenue / Brand / Audience / Operations].
>
> Here is why: [one or two sentences using the logic above to explain the call].

## Step 6: Find the biggest opportunity

Within the priority growth area, find the lowest individual score. That is the biggest opportunity.

For each growth area, the relevant vital signs are:
- **Revenue**: Leads, Meetings, Sales, Profit
- **Brand**: Content, Partnerships
- **Audience**: Audience
- **Operations**: Team

Tell the founder:

> Within [priority area], your lowest-scoring vital sign is [name] at [score]/10.
>
> That is your biggest leverage point. Raising [name] from [score] to 7 would [describe the specific downstream impact: more pipeline / stronger brand trust / broader reach / more capacity].

If two vital signs are tied for lowest, name both and explain that fixing either one would move the priority area.

## Step 7: Build the six-step Amplify Pyramid recommendation

Generate a recommendation using all six steps of the Amplify Pyramid. Each step builds on the last. Go as deep as the business stage warrants: startups get a solid foundation (steps 1-3); established or scaling businesses get the full ladder.

**Step 1 - Identify:** What is the foundation? Clarify the business goal this recommendation is in service of and the brand identity it needs to reinforce. One sentence each.

**Step 2 - Interpret:** What does the vital sign analysis tell us? Name the gap specifically. What would it mean for revenue, trust, or capacity if this were fixed?

**Step 3 - Streamline:** What existing process is the bottleneck? What could be simplified, automated, or removed entirely to fix the gap without adding new work?

**Step 4 - Customise:** What needs to be tailored to this specific business, audience, or sales process? What template, script, or workflow would make this personal rather than generic?

**Step 5 - Predict:** What opportunity does this unlock in the next 3-12 months if executed well? What signal would tell the founder they are on track?

**Step 6 - Amplify:** How does this scale into a lasting advantage? What does this look like when it compounds over two or three years?

Write the recommendation under a heading: "Your Amplify Recommendation".

## Step 8: Run the SymbioEthical check

Before finalising the recommendation, run five checks. Ask yourself whether the recommendation:

1. Aligns clearly with the business goals the founder stated or implied.
2. Reduces their mental load rather than adding new complexity.
3. Solves a meaningful real problem, not a vanity metric.
4. Is honest and transparent to customers and the market.
5. Builds a long-term human-AI working relationship rather than replacing human judgment.

If any check fails, adjust the recommendation before writing it to the file. Note the adjustment briefly under a heading: "Ethics check."

If all checks pass, write: "Ethics check: passed (all five SymbioEthical criteria met)."

## Step 9: Ask about AI experience level

Ask:

> One last question: how would you describe your current experience with AI tools?
>
> A) Beginning -- I am new to AI tools, I want simple and free
> B) Building -- I use a few AI tools regularly and want to go deeper
> C) Advanced -- I build with AI, I want custom and integrated solutions

Wait for their answer.

## Step 10: Suggest AI tools matched to experience level

Based on their experience level and their priority growth area, suggest three AI tools. Use this mapping as your guide (adapt the specific tools to what is current and available in 2025-2026):

**Beginning:**
- Revenue: ChatGPT for sales scripts, Calendly for scheduling automation, email sequences via Mailchimp or similar
- Brand: Canva AI for content visuals, Grammarly for writing consistency, Buffer or similar for social scheduling
- Audience: ChatGPT for content ideation, Google Analytics for insight, a social scheduling tool
- Operations: Notion AI for documentation, Zapier for simple automation, Loom for training

**Building:**
- Revenue: HubSpot AI features, Clay or Apollo for lead research, a CRM with automation
- Brand: A content writing assistant, social listening tools, Hootsuite or similar AI insights
- Audience: ConvertKit or similar for email automation, YouTube analytics, audience segmentation tools
- Operations: Monday.com or Linear with AI, Slack automation, a meeting transcription tool

**Advanced:**
- Revenue: Custom GPT or Claude-based workflows, Salesforce Einstein or similar, predictive pipeline analytics
- Brand: Custom brand voice AI, advanced social monitoring, reputation and sentiment tracking
- Audience: Custom recommendation engines, advanced segmentation, predictive lifetime value models
- Operations: Custom workflow automation, AI-powered business intelligence, process mining tools

Write the suggestions under a heading: "AI tools matched to your level."

## Step 11: Write the 1-1-1-1-1 implementation plan

Write a 90-day plan using the five ones:

1. **One product or service** to focus on. Name the specific thing, not a category.
2. **One target market** to win first. The specific type of customer you are going after in the next 90 days.
3. **One 12-month outcome** to aim for. A specific, measurable number: revenue, meetings booked, audience size, or efficiency gain.
4. **One team member** who owns AI implementation. If the founder is solo, it is them -- and that is worth stating explicitly.
5. **One AI tool** to master first. From the list in Step 10, pick the single most useful one for the priority area.

Write this under a heading: "Your 90-day 1-1-1-1-1 plan."

## Step 12: Write the success metrics

Name the three leading indicators the founder should track in the next 30 days to know the plan is working. Match them to the priority growth area:

- **Revenue**: lead quality or volume, meetings booked, pipeline value
- **Brand**: content publishing frequency, engagement rate, inbound mentions or referrals
- **Audience**: new audience members per week, engagement rate, email open rate
- **Operations**: hours saved per week, team capacity, tasks automated

Write these under a heading: "What to track in the next 30 days."

## Step 13: Write friday/growth.md

Create the `friday/` folder if it does not exist. Write `friday/growth.md` using this structure:

```
# Growth Diagnostic: <YYYY-MM-DD>

## Vital sign scores

- Leads: <score>/10
- Meetings: <score>/10
- Sales: <score>/10
- Profit: <score>/10
- Content: <score>/10
- Partnerships: <score>/10
- Audience: <score>/10
- Team: <score>/10

## Business stage

<Stage name> -- <one sentence on why>

## Priority growth area

<Area name>

Biggest opportunity: <vital sign name> (<score>/10)

<One or two sentences on the specific downstream impact of fixing this>

## Your Amplify Recommendation

<The six-step recommendation from Step 7>

## Ethics check

<Result from Step 8>

## AI tools matched to your level

<The three tools from Step 10>

## Your 90-day 1-1-1-1-1 plan

1. One product or service: <specific answer>
2. One target market: <specific answer>
3. One 12-month outcome: <specific measurable number>
4. One team member owns AI: <name or "you, as the solo founder">
5. One AI tool to master first: <specific tool>

## What to track in the next 30 days

1. <metric>
2. <metric>
3. <metric>

---
For the full Amplify method: https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831
```

Fill every section from the diagnostic. Do not leave placeholders.

After writing, print:

> Your growth diagnostic is at `friday/growth.md`. Read it, share it with your team, and come back to it in 30 days to check the leading indicators.
>
> For the full Amplify method -- all six steps, the complete vital sign framework, and the case studies -- the book is at https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

## What comes next

`friday/growth.md` is your 90-day reference. The leading indicators in "What to track" are your weekly check-in questions.

The full Friday stack -- nine specialists running against your real inbox, calendar, and business data, applying the Amplify method daily -- is at friday.amplifyais.com.

---

Built by Amplify AI at amplifyais.com
