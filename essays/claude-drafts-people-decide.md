# Claude Drafts, People Decide

This repo has one rule that shapes everything else in it: Claude drafts, scores, and flags. A person decides on escalations, pricing, and commitments.

It is worth explaining why that line sits where it does, because it is not a statement about what AI can't do. It is a statement about what a customer relationship is.

## What a customer relationship runs on

A customer renews because they believe two things: that the product delivers value, and that the people behind it will keep their word. The second belief is built one commitment at a time. "We'll have that fixed by Friday." "Your price won't change this year." "If response times slip, you get a credit."

Every one of those is a promise made by a person, on behalf of a company, and the company has to keep it. If a commitment gets made without anyone deciding to make it, the company is on the hook for something nobody agreed to. That is true whether the commitment came from an overeager new CSM or a model that wrote "we can do that" because it sounded helpful.

So the line is not "AI is bad at judgment." The line is that commitments need an owner, and the owner has to be someone who can be held to them.

## What Claude is good at in CS

Within that line, there is a lot of room. Most of a CSM's week is not spent making commitments. It is spent assembling information so that they can.

- **Gathering and summarizing.** Pulling usage, tickets, notes, and contract terms into one view of an account. The [account review](../prompts/account-review.md) and [handoff packet](../prompts/handoff-packet.md) prompts do this.
- **Applying rules consistently.** Scoring every account the same way, every week, and flagging every band drop. People are inconsistent at this, and not because they are careless: they have 40 accounts and a calendar full of meetings.
- **Drafting.** First versions of emails, QBR outlines, and internal updates, with the facts in place and the commitments marked for someone to approve.
- **Catching what slipped.** An informal promise buried in a sales thread. An executive sponsor nobody has spoken to in 95 days. A renewal notice period about to pass.

Each of these makes the human decision better informed and faster. None of them makes the decision.

## How the line is enforced

Saying "people decide" is easy. Building it into the tools takes specific choices, and the prompts and specs in this repo try to make them:

- **Placeholders instead of promises.** The [customer email](../prompts/customer-email.md) prompt writes `[NEEDS APPROVAL: what and from whom]` wherever a commitment would go. The draft cannot be sent as-is without someone resolving it.
- **Routing instead of recommending.** The [contract redline](../prompts/contract-redline-summary.md) prompt says who needs to weigh in on each change. It does not say whether to accept it.
- **Evidence instead of verdicts.** The [competency evaluation](../prompts/csm-competency-evaluation.md) gathers examples per area. A manager decides what they add up to.
- **Read by default, writes confirmed.** The [HubSpot agent interface](../specs/hubspot-agent-interface.md) lets an agent read freely, propose changes as a diff, and apply them only after a person confirms each batch.

The pattern is the same everywhere: the model does the work up to the point of decision, makes the decision easy to see, and stops.

## The cost of getting it wrong in the other direction

There is a failure mode on the other side, too. A team that trusts nothing the model produces will re-check every summary and rewrite every draft, and get none of the benefit. Worse, it will keep making decisions on the same incomplete information it always had.

The answer is not blanket trust or blanket suspicion. It is knowing which parts of the output to check. Every prompt in this repo ends with its known failure modes for that reason: they tell the reviewer where to look. A reviewer who knows that the renewal prep prompt tends to overstate thin outcomes can check the value story in two minutes, rather than re-doing the whole prep.

## Measuring it honestly

The same discipline applies to the business case. Time saved is real, but it is only worth money if it is used. Freed hours that turn into more accounts per CSM, or a hire you don't need to make, are savings. Freed hours that vanish into more meetings are not. The [ROI calculator](../tools/roi_calculator.py) reports the cash return on its own for that reason.

A copilot pays for itself when it helps people make better decisions, sooner, about the accounts that matter. That is a high bar, and it is the right one.
