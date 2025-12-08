You are an odoo 18 expert and project orchestrator. Help me complete the following tasks.

Task 1 : Use @agent-architect-reviewer to analyze the `sh_document_management` module and the `Odoo_18_Environment_Architecture` folder. For each, generate a `CLAUDE.md` file inside the respective folders.
Task 2 : Use @agent-test-automator to run a comprehensive Live Odoo 18 Instance test. Reference `test_information_for_CLAUDE.md`. Test ALL functions of sh_document_management includes actually clicking all the buttons. Write the final test results to INVESTIGATION_TEST_RESULT.md.
Task 3 : Analyze test result and create fix plan.
Task 4 : Review the fix plan. Your target is not just compile it without error. The criteria is that all functions of the `sh_document_management` module are 100% working correctly in Live Odoo 18 Instance. So please write about the testing case, too.
Task 5 : After you review all the thing, implement fix plan in another worktree. 
Task 6 : Conduct comprehensive deployment test after fix plan completed.
Task 7 : After deployment test pass, update module version and create CHANGELOG.md.

Note 1 : Use MASTER_TASK.md with task summarize to track progress. Each tasks should have formatted tag ID. For example, deployment agent task 001 should be formatted as DEP-T001. After task finished, write the task report to MASTER_TASK.md and commit to git.
Note 2 : Use Parallel sub-agent to speed up independent tasks.
Note 3 : Automatically EXPORT the current **claude codes conversation** whenever auto-compact or manual-compact occurs.
Note 4 : Properly categorize the files generated during the process into the corresponding folders.