# Example trigger rules

The trigger file is what makes skills reliable. Each paragraph names a situation and the skill that must be read first.

- When working on any software project (new app, feature, commit, push, branches, going back to an old state), ALWAYS read the skill `software-project-workflow` first.
- On every `git commit` in the LearnCenter iOS repo, ALWAYS read `learncenter-ios-git` first and push right after the commit.
- Before uploading a new iOS build to TestFlight, ALWAYS read `testflight-upload` first.
- When creating, renaming or moving a skill, or running rm/mv/cp inside iCloud Drive, ALWAYS read `skill-management` first.
- When showing an app screenshot inside a device frame on a website, ALWAYS read `device-mockup-screenshots` first.

Why it works: a short, specific rule per situation is followed far better than one long list of general instructions.
