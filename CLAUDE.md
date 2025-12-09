# CLAUDE.md - sh_document_management Module

You are an Odoo 18 expert and project orchestrator. Help me complete the following tasks.

## Tasks

### Task 1 - Create Fix Plan
Analyze BUG_REPORT.md and create fix plan. Fix should have achievable milestones which have formatted tag ID for each agent. For example, frontend agent task 001 should be formatted as FRONTEND-T001. After each agent task finished, write the agent task report to `MASTER_TASK.md` and commit to git. If our token near the auto-compact threshold for example 10%, you need to record what you are doing in the same PROGRESS_[agent_name].md. This markdown will track what you're doing.

### Task 2 - Review Fix Plan
Review the fix plan. Your target is not just compile it without error. The criteria is that all functions of the `sh_document_management` module are 100% working correctly in Live Odoo 18 Instance. So please write about the testing case, too.

### Task 3 - Implement Fixes
After you review all the thing, implement fix plan.

### Task 4 - Deployment Testing
Wait for user deploys to the Live Odoo 18 Instance. Conduct comprehensive deployment test after fix plan completed. Rollback if error happend.

### Task 5 - Version Update & Changelog
After deployment test pass, create `DEPLOYMENT_TEST_REPORT.md`. Update module version and create `CHANGELOG.md`.

## Requirement

### Requirement 1
Use `MASTER_TASK.md` with task summary to track progress. Whenever a task is completed, write the task summary to `MASTER_TASK.md` and commit to git.

### Requirement 2
Use Parallel sub-agent to speed up independent tasks.

### Requirement 3
Properly categorize the files generated during the process into the corresponding folders.
