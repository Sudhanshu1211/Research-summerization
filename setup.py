import setuptools

with open("README.md", "r", encoding = 'utf-8') as f:
    long_description = f.read()

_version_ = '0.0.0'

REPO_NAME = 'summerization-backend'
AUTHOR_USER_NAME = 'Sudhanshu1211'
SRC_REPO = 'src'
AUTHOR_EMAIL = 'sudhanshugoogly1211@gmail.com'

setuptools.setup(
    name = SRC_REPO,
    version=_version_,
    author = AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='Smart assistant for research summarization',
    long_description=long_description,
    long_description_content = "text/markdown",
    url = f'https://github/com/{AUTHOR_USER_NAME}/{REPO_NAME}',
    project_urls = {
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
},


)