# Restaurant Data Simulators

## Project Description
```
This project is a collection of data simulators for a theoretical restaurant chain. 
The data simulators are used to generate data for a restaurant's menu, inventory, and sales. 
The data simulators are designed to be used in conjunction with a restaurant management system to generate data for testing and development purposes.
```

## Environment Setup Steps (mac)
```
cd /Users/{USER}/Desktop/{REPOS_DIRECTORY}

mkdir {REPO_FOLDER}

cd {REPO_FOLDER}

python3.11 -m venv {VENV_NAME}

source {VENV_NAME}/bin/activate
 
pip install --upgrade pip wheel python-dotenv setuptools requests pandas plotly

pip install {ADDITIONAL_PACKAGES}

pip freeze > requirements.txt

echo "{VENV_NAME}/
_archive/
_notes/
_notes.txt
generated_data/
venv/
__pycache__/
*.pyc
*/migrations/*
db.sqlite3
.env
staticfiles/" > .gitignore

cat .gitignore

git init

gh auth status

gh auth login

gh repo create {REPO_FOLDER} --private

git remote add origin https://github.com/{GITHUB_USERNAME}/{REPO_FOLDER}

git remote -v

git add .

git commit -m "Initial commit"

git push -u origin main
```

