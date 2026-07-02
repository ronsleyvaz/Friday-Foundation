# Skill-Writing Playbook

Notes for writing your own Friday Foundation commands, so they stay useful instead of rotting into an unreliable mess. Every command you scaffold with `/new-capability` should be checked against the five failure modes below before you consider it done.

## The five failure modes

**Premature completion.** A step ends before the work is actually finished, because the model's attention slipped to "looking done" instead of "being done." If a step in your command says "ask the founder for their priorities," Claude might take the first vague answer and move on. Fix it by giving the step a clear finish line: "ask for at least three priorities, and confirm they're done before moving on."

**Duplication.** The same instruction shows up in more than one place, worded slightly differently each time. This costs you twice: it's more to maintain, and it makes Claude unsure which version is authoritative. If two steps in your command both explain how to read the voice profile, collapse them into one.

**Sediment.** Old instructions pile up because adding a new caveat feels safe and deleting an old one feels risky. Every command that gets edited a dozen times without a clean-up pass ends up carrying dead weight: instructions for a case that no longer applies, or a step that was superseded by a later one but never removed. Read your command file end to end occasionally and cut what no longer earns its place.

**Sprawl.** The command is too long, even if every line still does something. A command that was supposed to take five minutes but now has fifteen steps, because you kept bolting new asks onto it, is sprawling. If a command has grown past what a founder can run in one sitting, split it into two commands rather than one long one.

**No-op.** An instruction that Claude was already going to do by default. Telling Claude to "be thorough" or "think carefully" changes nothing; it's not a real instruction, it's noise. Every line in your command should change what Claude actually does. If you can delete a sentence and nothing in the output would differ, delete it.

## The completion-criterion discipline

Every step in a Friday command should end with a way to tell "done" from "not done." Not a vague sense that the step is finished, a real check.

A weak step: "Ask the founder about their nine decisions."

A strong step: "Ask the founder to list their nine decisions. Accept at least five, and confirm they're done before moving on."

The strong version is checkable: you can point at the moment it's satisfied. Where it matters, make the criterion exhaustive too, not just "produce a summary" but "every priority from the founder's list is accounted for in the output." A vague completion criterion is where premature completion sneaks in.

## Using this with `/new-capability`

When you scaffold a new command, walk each step you write against this list:

1. Does every step have a checkable finish line?
2. Does any instruction say the same thing a different step already said?
3. Is there a caveat left over from an earlier version of the command that no longer applies?
4. Could this command be split into two shorter, more focused ones?
5. Is every sentence actually changing what Claude does, or just restating what it would do anyway?

A command that passes all five stays reliable the tenth time you run it, not just the first.

---

Built by Amplify AI at amplifyais.com
