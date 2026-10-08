# Skills

How I work with an AI assistant using **skills**: small, reusable instruction files that tell the AI exactly how a recurring task is done in my setup. This repo is a cleaned-up selection (no private data, no keys).

## The idea in 3 steps
1. **The problem.** An AI forgets how you work. Every session you re-explain your git routine, your release steps, your quality rules.
2. **The fix.** One folder per task with a `SKILL.md`: when it triggers, the rules, a checklist. The AI reads only the skill that fits the task.
3. **How it fits together.** A short trigger file (see `CLAUDE.md-example.md`) says "for task X, always read skill Y first". Skills can build on each other, for example a git skill for one repo that extends the general project workflow.

## Skills in this repo
| Skill | What it shows |
|---|---|
| `software-project-workflow` | A safe git and GitHub routine: one folder one repo, commit and push after every change, never force-push, explain branches in plain language |
| `learncenter-ios-git` | A specialisation of the workflow for one repo: push right after commit, with a fast-forward safety check |
| `testflight-upload` | Release automation with fastlane: build number, signing via API key, upload |
| `skill-management` | How skills are stored, named and protected (including a hard safety rule after a data-loss incident) |
| `device-mockup-screenshots` | A reusable script-based workflow with ready code and known pitfalls |
| `garderobe-inventar` | Photo in, structured Notion table out, plus analysis rules (demo version: personal measurements and database links removed) |

The skills are written in German because that is my working language; folder names and headers stay English.

## What was removed
Account and key identifiers (replaced by `<PLACEHOLDERS>`), database links, personal measurements and client names.

## In short (English)
Skills are small instruction files that teach an AI assistant how a recurring task is done in my setup: when it triggers, the rules, a checklist. This repo shows six of them and how they fit together through a short trigger file. They are written in German; feel free to copy and adapt them.
