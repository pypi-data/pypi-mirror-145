import yaml
from yaml.loader import SafeLoader
from os.path import exists
import os
from pybtex.database import BibliographyData, Entry
import warnings

warnings.warn('Warning Message: 4')
bib_data = BibliographyData({
    'article-minimal': Entry('article', [
        ('author', 'L[eslie] B. Lamport'),
        ('title', 'The Gnats and Gnus Document Preparation System'),
        ('journal', "G-Animal's Journal"),
        ('year', '1986'),
    ]),
})

bib_data.to_file(file='references.bib', bib_format='bibtex')

if not os.path.exists('assets'):
    os.mkdir('assets')
    print("Directory ", 'assets', " Created ")


def CreateFileInRepo(filename, yml_data):
    with open(filename, 'w') as f:
        data = yaml.dump(yml_data, f, sort_keys=False, default_flow_style=False)


file_exists = exists(os.getcwd() + '/audit-dog.yml')

if not file_exists:
    with open('spec.yml', 'r') as f:
        yaml_data = list(yaml.load_all(f, Loader=SafeLoader))

    yml_data = [{'client': yaml_data[0]['client'], 'repo_name': yaml_data[0]['name'],
                 'repo_description': yaml_data[0]['description']}]
    CreateFileInRepo('audit-dog.yml', yml_data)

file_exists = exists(os.getcwd() + '/README.md')
if not file_exists:
    yml_data = 'An audit agent for policy compliance inspection across projects and teams.\n\n **Workinks** \n\n [Gitlab](https://gitlab.com/sigil-scientific-enterprises/audit-dog)'
    with open('README.md', 'w') as f:
        f.write(yml_data)
