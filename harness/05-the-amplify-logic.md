<!-- Content licensed under LICENSE-CONTENT. See that file for terms. -->

# 05 - The Amplify Logic

The `/amplify` command implements the Amplify AI method: a diagnostic framework for founders who want to grow their business with AI without burning out or losing direction.

This guide explains how the command's logic maps to the method. Read it if you want to understand what is happening under the hood, or if you want to adapt the diagnostic for your own context.

The full method is in the book: https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

---

## The core idea

Every business has eight vital signs. Some are healthy. Some need attention. The Amplify method says: find the weakest vital signs in your highest-priority growth area, fix those first, and use AI to do it without adding complexity.

The diagnostic is not a quiz. It is a structured conversation that produces a prioritised plan you can act on Monday morning.

---

## The eight vital signs

The `/amplify` command asks you to score eight areas of your business from 1 to 10:

| Vital sign | What it measures | Growth area |
|---|---|---|
| Leads | Quality and volume of your pipeline | Revenue |
| Meetings | Qualified sales conversations per month | Revenue |
| Sales | Close rate and conversion | Revenue |
| Profit | Margins and financial sustainability | Revenue |
| Content | Publishing consistency and engagement | Brand |
| Partnerships | Referral network and strategic alliances | Brand |
| Audience | Reach and community engagement | Audience |
| Team | How well your team handles the workload | Operations |

A score of 7-10 is healthy. A score of 4-6 is a warning. A score of 1-3 is critical.

---

## The four growth areas (priority order)

Amplify organises growth into four areas, in priority order:

1. **Revenue** (Leads, Meetings, Sales, Profit) -- financial foundation first. Until revenue is stable, everything else is hard.
2. **Brand** (Content, Partnerships) -- trust and credibility in your market. Builds on revenue.
3. **Audience** (Audience) -- sustainable community and reach. Builds on brand.
4. **Operations** (Team) -- scalable systems and efficiency. Builds on everything.

The diagnostic starts with Revenue and works forward. If your Revenue area is solid, it looks at Brand. And so on.

---

## How the diagnostic finds your priority area

The `/amplify` command:

1. Calculates an average score for each growth area from your vital signs.
2. Reads your two Profit and Sales scores. If either is 4 or below, Revenue is your priority, regardless of everything else.
3. If Profit and Sales are above 4 but your Partnerships score is 4 or below, it looks at whether trust (Brand) or pipeline growth (Revenue) is the primary issue.
4. If Revenue and Brand are both solid, it checks whether you are ready for Audience building or Operations scaling.

The output is a named priority area, not a vague "you need to work on everything."

---

## How the recommendation is structured

The recommendation follows the six-step Amplify Pyramid:

1. **Identify** -- what is the foundation? What are the business goals and brand identity?
2. **Interpret** -- what does the current state tell us? Where are the biggest gaps?
3. **Streamline** -- what existing processes can be optimised?
4. **Customise** -- what needs to be personalised to this business?
5. **Predict** -- what opportunities are coming that can be prepared for?
6. **Amplify** -- how does this scale into a lasting legacy?

The diagnostic generates a recommendation that starts at Step 1 (Identify) and goes as far as the business stage warrants. A startup gets Steps 1-3. A scaling business gets all six.

---

## The SymbioEthical check

Before the plan is finalised, the command runs a five-question ethics check on the recommendation:

1. Does it align with the founder's stated business goals?
2. Does it reduce cognitive load rather than add to it?
3. Does it solve a meaningful, real problem?
4. Is it transparent and honest to customers?
5. Does it create a long-term human-AI working relationship rather than a quick shortcut?

If any answer is no, the recommendation is adjusted. The Amplify method treats AI as a collaborator, not a replacement.

---

## The 1-1-1-1-1 plan

The output plan follows the "five ones" from the book:

1. One product or service to focus on.
2. One target market to win first.
3. One 12-month outcome to aim for.
4. One team member who owns AI implementation.
5. One AI tool to master before adding more.

This prevents the trap of implementing too much AI at once and losing track of what is working.

---

## AI tools matched to experience level

The command suggests AI tools based on the founder's self-reported experience level:

- **Beginning** with AI: free or low-cost tools with simple interfaces (ChatGPT for scripts, Canva AI for visuals, Zapier for simple automation).
- **Building** with AI: mid-tier platforms with more capability (HubSpot AI features, ConvertKit automation, Monday.com AI).
- **Advanced** with AI: custom implementations and enterprise platforms (custom GPT models, Salesforce Einstein, predictive analytics).

The principle: master one tool before adding the next.

---

## What gets written to friday/growth.md

The diagnostic writes a file with:

- Your vital sign scores and what they reveal.
- Your business stage and priority growth area.
- Your biggest opportunity (named specifically).
- A six-step Pyramid recommendation.
- The SymbioEthical check result.
- The AI tools matched to your level.
- Your 1-1-1-1-1 plan.
- The success metrics to track.

This file is your reference for the next 90 days.

---

For the full book: https://www.amazon.com/Amplify-Integrating-Intelligence-Humanity-Acceleration/dp/1998756831

---

Built by Amplify AI at amplifyais.com
