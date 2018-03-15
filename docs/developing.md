# SSPINN Development Procedure

This guide will walk you through the development process used by contributors to SSPINN. It assumes that the package is already installed correctly and that you are compitent in using git version control.

**1. We require that all individual development be emplimented on a new Fork**
 * Navigate to the [SSPINN repository](https://github.com/awild82/SSPINN), and in the top right corner click on "Fork"
 
**2. Clone your forked  repo**
 * At the command line run `git clone <your_fork_url>`
 * Run installation script `python setup.py install --user`
 
**3. Make your changes!**
 * In your local repo, make any changes or additions that you'd like to see in SSPINN code

**4. Format changes to SSPINN compliancy**
 * *SSPINN is pep8 compliant code*
 * We suggest checking your code for pep8 compliancy by running `flake8 your_changes.py`
  * Flake8 can be installed at the command line by running `pip install flake8`
 * Once your code passes flake8 tests, push them to your forked repo on github
  * `git add your_changes.py`
  * `git commit -m "Your commit message"`
  * `git push`

**5. Open pull request!**
 * To ensure code quality, SSPINN developers require travis.yml checks
 * Once your code passes travis checks a fellow contributor will approve of your changes and merge your forked repo to the SSPINN master branch!
 * **Thank you for your help!**
