Contributing to JuMonC
======================

This page documents at a very high level how to contribute to JuMonC.

The JuMonC development is built upon the following components:

1. [Issues][] identify any issues including bugs and feature requests.

2. [Merge Requests][] are collections of changes that address issues.

Reporting Issues
================

If you have a bug report or a feature request for JuMonC, you can use the
[issues][] tracker to report a [new issue][].

To report an issue.

1. Register GitLab Access to create an account and select a user name.
2. Create a [new issue][].
3. Ensure that the  issue has a **Title** and **Description**
   with enough details for someone to reproduce the issue.
   See [Gitlab Markdown] guide for styling the **Description**. Include
   screenshots and samples whenever possible. Typically, reporter
   **should not** set any other fields for the issue, including
   **Assignee**, **Milestone**, or **Labels**.


Fixing issues
=============

Typically, one addresses issues by writing code. To start contributing to JuMonC:

1.  Register GitLab Access to create an account and select a user name.

2.  Fork JuMonC into your user's namespace on GitLab.

    2.1 [Create an access token] for your repo, that allows reads and writes to the repository. Copy the token value.

    2.2 [Create a CI variable] that is named `AUTO_DOC_TOKEN`. It should be set to masked, but not protected. 
    
    This allows the CI to automatically push changes in te automatic generated documentation.

3.  Create a local clone of your JuMonC fork repository. Optionally configure
    Git to use SSH instead of HTTPS.
    Then clone:

        $ git clone https://....
        $ cd jumonc
    The main repository will be configured as your `origin` remote.

4.  Create a new branch, e.g.: `git checkout -b "fix_issue_1"`

5.  Install the [Dependencies][], you could use a virtual enviroment for the python dependencies.

6.  Edit files and create commits (repeat as needed):

        $ edit file1 file2 file3
        $ git add file1 file2 file3
        $ git commit

    Commit messages must be thorough and informative so that
    reviewers will have a good understanding of why the change is
    needed before looking at the code. Appropriately refer to the issue
    number, if applicable.

7.  Push commits in your topic branch to your fork in GitLab:

        $ git push origin ...

8.  See test results in CI/CD on GitLab

9.  Visit your fork in GitLab, browse to the "**Merge Requests**" link on the
    left, and use the "**New Merge Request**" button in the upper right to
    create a Merge Request.


[Gitlab Markdown]: https://gitlab.jsc.fz-juelich.de/help/user/markdown.md
[Dependencies]: https://gitlab.jsc.fz-juelich.de/witzler1/jumonc#installation
[Issues]: https://gitlab.jsc.fz-juelich.de/witzler1/jumonc/-/issues
[new issue]: https://gitlab.jsc.fz-juelich.de/witzler1/jumonc/-/issues/new
[Merge Requests]: https://gitlab.jsc.fz-juelich.de/witzler1/jumonc/-/merge_requests
[Create an access token]: https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html
[Create a CI variable]: https://www.cloudsavvyit.com/15480/how-to-set-variables-in-your-gitlab-ci-pipelines/

