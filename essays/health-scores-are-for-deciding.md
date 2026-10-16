# Health Scores Are for Deciding, Not Reporting

Every CS team has a health score. Most of them are ignored.

They are ignored for a predictable reason: the score was designed to be reported, not used. It shows up on a dashboard, colored green, yellow, or red, and it summarizes the account in a way that feels informative. But when a CSM looks at a Yellow account and asks "what should I do about this?", the score has no answer. And when an account that was Green for a year churns, nobody is surprised that the score missed it, because nobody believed it in the first place.

A health score earns its place only if it changes what someone does. That requirement has consequences for how you build one.

## It has to explain itself

A score of 62 means nothing. "62, because usage is down 18% and only one of four goals is on track" is something a CSM can act on.

So every score should come with its breakdown and its top drivers: the signals pulling it down the most. In this repo's [scoring model](../frameworks/account-health-scoring.md#outputs), a driver is the signal with the largest gap, weighted by how much that signal matters. The calculation is simple on purpose. A model that a CSM cannot check by hand is a model they will not trust when it disagrees with them.

## It has to admit what it doesn't know

The fastest way to destroy trust in a health score is to score missing data as zero.

An account whose usage export broke last month is not an account with zero usage. If the score treats it that way, it turns Red, someone panics, the CSM explains that the data is broken, and everyone learns that the score is unreliable. They are right.

Missing data should be unknown. Score what you have, say how much of the picture that covers, and when coverage is too low, say so instead of producing a confident number. "Insufficient data" is an honest band. It is also an action: fix the data.

## It has to bend to the things that matter more

Some events matter more than any weighted average. A customer who has sent a notice of non-renewal is at risk no matter how much they use the product. An account whose executive sponsor just left is not Green, whatever the index says.

These overrides should be explicit, few, and written down, so that everyone knows which events trump the math. And CSMs should be able to override a band, with a written reason, because they know things the data doesn't: that this customer only uses the product at month-end, or that the sponsor who went quiet is on parental leave. Overrides that are reviewed monthly become one of the best sources of calibration data you have.

## It has to trigger something

A band is useful only if each band means something will happen. Red should start an escalation with an owner and a deadline. A band drop should put the account at the top of the CSM's week. Green with an expansion signal should start a qualification conversation.

If nothing happens when an account turns Red, the score is decoration. The [escalation logic](../frameworks/escalation-logic.md) and the [weekly brief](../prompts/weekly-csm-brief.md) in this repo are the other half of the scoring model. Without them, the score would just be another number.

## It has to be tested against reality

The only question that matters about a health score is whether it predicted what happened. Take every account that churned in the last year and ask what band it was in 90 days before its renewal. If most of them were Green or Yellow, the score is not measuring risk, whatever its weights say.

Run that back-test every quarter. Change the weights when it fails. Record the churned accounts the score missed, and look for the signal that would have caught them. A score that is never tested drifts into a story the team tells itself.

## The short version

Build the score backwards from the decision. Decide what a CSM should do differently for a Red account, then build a score that reliably finds those accounts, explains why, admits when it can't tell, and gets checked against what actually happened.

Everything else is a dashboard.
