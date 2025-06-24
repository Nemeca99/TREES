# Branch Protection Instructions

Since GitHub Copilot coding agent isn't available without a Pro+ or Enterprise license, here's how to manually set up branch protection:

1. Go to your repository on GitHub.com
2. Click on "Settings" tab
3. In the left sidebar, click "Branches"
4. Under "Branch protection rules", click "Add rule"
5. For "Branch name pattern", enter `main`
6. Configure these recommended settings:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1 is recommended)
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Do not allow bypassing the above settings
   - ✅ Restrict who can push to matching branches (add yourself)
   - ✅ Allow force pushes (select who can force push)
   - ❌ Allow deletions (keep this unchecked to protect your main branch)

7. Click "Create" or "Save changes"

This will protect your main branch and enforce good development practices.

## Additional Repository Security Recommendations

1. **Enable Vulnerability Alerts**
   - Go to Settings > Security & analysis
   - Enable Dependabot alerts and security updates

2. **Code Scanning**
   - Enable CodeQL analysis in the same section

3. **Secret Scanning**
   - Enable secret scanning to prevent accidental secrets commits

These manual protections will provide good security for your repository even without Copilot coding agent access.
