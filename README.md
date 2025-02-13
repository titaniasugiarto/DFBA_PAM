# Template_project



## Getting started

This template is meant as a starting point for creating new repositories for projects in the Industrial Systems Biology group at the institute of Applied Microbiology. This README file will highlight some of the core principles for sharing and creating software/data according to the [FAIR software principles](https://www.nature.com/articles/s41597-022-01710-x).

## Step-by-step plan for using version control with Git
The following step-by-step guidelines will help you create and maintain organized projects on GitLab

1. [Fork this project](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html). Ensure you create a fork from the main branch and make it private
2. [Clone the project](https://docs.gitlab.com/ee/user/project/repository/index.html#clone-a-repository) to your computer
3. [Maintain the project](https://docs.gitlab.com/ee/user/get_started/get_started_managing_code.html) by doing one commit per change, and pushing regularly to Git. [This webpage](https://carpentries-incubator.github.io/fair-research-software/04-version-control.html) from the software carpentries gives a good overview of how to use version control.
4. If you are working of software development, the following branching structure is recommended:
    - `main`: this is the latest *stable* version of the software
    - `develop`: this is were development happens, only merged into main if it is stable
    - `feature`: in a feature branch, you can develop new features for your software. If the feature is ready, it can be merged into main and the branch can be deleted.

More information about collaborating on software projects can be found [here](https://coderefinery.github.io/git-collaborative/)

## Step-by-step plan for creating repositories using the FAIR principles
The following guidelines will help you build your project such that it is easily Findable, Accessible, Interoperable and Reproducible

1. Before you start:
    - Create a venv/conda venv for this specific project
    - Determine which version of Python/pandas/numpy/other basics you will be using and make sure you version pin (e.g. `pandas==0.25.3`) them in your requirements file
    - Replace this README with a landing page describing your project and how people should collaborate.

2. During the development:
    - Regularly update your requirements file. Preferably after each new installation/deinstallation. Keep in mind that package co-dependencies should be deleted manually to keep a clean list or requirements. with conda, you can use `conda list --from-history` to get all the packages you have installed manually (thus not the co-dependencies). More information and an example can be found [here](https://coderefinery.github.io/reproducible-research/dependencies/).
    - See the [Git usage guide](## Step-by-step plan for using version control with Git) for how to maintain your repository.
    - Create a test suite in the `tests` directory. Some guidelines can be found [here](https://carpentries-incubator.github.io/fair-research-software/08-code-correctness.html) and [here](https://suresoft.dev/knowledge-hub/software-testing/). A minimal requirement is writing unit tests using the [Arrange, Act, Assert framework](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
    - Best practice is to introduce a continuous integration (CI) framework. A template can be found in the `.github` and `.gitlab` folder for [GitHub](https://carpentries-incubator.github.io/fair-research-software/ci-for-testing.html) and [GitLab](https://suresoft.dev/knowledge-hub/continuous-integration/gitlab-ci/), respectively.
    - Keep writing documentation! Even though it is tempting to only do this at the end, it is better to start writing your general documentation describing the principles underlying the software early on.
    - Add all confidential files or files/directories such as __pycache__ to the `.gitignore` file. These files will then be ignored by git, and not uploaded to the git server.

3. Before publication:
    - **IMPORTANT**: determine the software licence. This tells the user what it is allowed to do with it. Please note that the licence can be affected by potential future patents, or by the packages you use in your software/repository. The EU provides a great tool for finding out which licence is good for you: a [licence compatibility checker](https://interoperable-europe.ec.europa.eu/collection/eupl/solution/licensing-assistant/compatibility-checker) and an [overview of the commonly used licences](https://interoperable-europe.ec.europa.eu/collection/eupl/solution/licensing-assistant/find-and-compare-software-licenses). More information can be found on [this webpage](https://coderefinery.github.io/social-coding/software-licensing/)
    - Finish your documentation. Make sure you update your [software level documentation](https://carpentries-incubator.github.io/fair-research-software/09-code-documentation.html#software-level-documentation) and your [project level documentation](https://carpentries-incubator.github.io/fair-research-software/09-code-documentation.html#project-level-documentation)
    - Deploy your documentation using [MKDocs](https://carpentries-incubator.github.io/fair-research-software/09-code-documentation.html#documentation-tools), [ReadTheDocs](https://about.readthedocs.com/?ref=readthedocs.org) (example is in the docs directory), or whatever other tool you'd like to use.
    - Make your repository citable by adding a CITATION file. [This tool](https://citation-file-format.github.io/cff-initializer-javascript/#/) will generate the file for you. More information can be found [here](https://coderefinery.github.io/social-coding/software-citation/)

4. Publication:
    - Create a clean copy of the project on the iAMB GitHub page. 
    - If you do not need the history of your project anymore, delete it on GitLab
    - If you are not working on a confidential project and you do not mind people seeing your git history, you can also migrate the GitLab repo to GitHub without loosing anything.

5. After publication: Keep on the maintenance!


```
cd existing_repo
git remote add origin https://git.rwth-aachen.de/iamb/template_project.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.rwth-aachen.de/iamb/template_project/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
