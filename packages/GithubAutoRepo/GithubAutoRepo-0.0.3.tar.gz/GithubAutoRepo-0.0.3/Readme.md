## This python module is used to create a github repository automatically and pushing all the files into that repository.

## You can check out the module [GithubAutoRepo](https://pypi.org/project/GithubAutoRepo/0.0.1/#description)

Install this module by,<br>
`
pip install GithubAutoRepo==0.0.1
`
### Use this module: <br>

`import GithubAutoRepo`<br>

### PASS THE FOLLOWING ARGUMENTS:
1. `REPO_PATH`<br>
> Note: REPO_PATH IS THE PATH OF YOUR PROJECT YOU WANT TO UPLOAD TO THE REPOSITORY<br>
3. `GITHUB_TOKEN`<br><br>
4. `GITHUB_USERNAME`<br>

Finally call the method  `autoRepo` by passing the above three arguments <br><br>
`
GithubAutoRepo.autoRepo(REPO_PATH,GITHUB_TOKEN,GITHUB_USERNAME)
`

### Steps to obtain Github API TOKEN:
1. `  Click on Settings ->`<br><br>
2. `  Scroll down and click on developer settings ->`<br><br>
3. `  Click on personal access token ->`<br><br>
4. `  Click on generate new token ->`<br><br>
5. `  Click on all the check boxes and click generate token`<br>

> Made with ❤️



