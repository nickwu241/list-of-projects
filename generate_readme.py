"""Update projects.json then run: python generate_readme.py | tee README.md index.md"""

import codecs
import collections
import json
import sys

def md_bold(message):
    return '**' + message + '**'

def md_italics(message):
    return '*' + message + '*'

def md_link_project(name):
    global name_to_links
    return '[' + name + ']' if name in name_to_links else name

def generate_projects():
    global nongames
    global games

    def print_projects(year_to_projects):
        for year, projects in year_to_projects.items():
            print('### ' + str(year))
            for p in projects:
                print('{:s} - {:s}\n'.format(
                    md_bold(md_link_project(p['name'])),
                    p['description']))
                tagline = []
                if 'languages' in p:
                    tagline.append('languages: **_{:s}_**'.format(', '.join(p['languages'])))
                if 'technologies' in p:
                    tagline.append('technologies: **_{:s}_**'.format(', '.join(p['technologies'])))
                if tagline:
                    print('  * ' + ', '.join(tagline))
                print('\n')

    print_projects(nongames)
    print('## Games')
    print_projects(games)

def generate_link_references():
    global name_to_links
    print('[//]: #')
    for name, link in name_to_links.items():
        print('[{:s}]:<{:s}>'.format(name, link))

def main():
    PROJECTS_JSON_FILENAME = 'projects.json'

    MD_BEGIN = '# **Projects**\n\
My projects and their Github links.\n\
Organized into [projects](#projects) and [games](#games) sorted chronologically.\n'

    MD_END = '## Thanks for visiting!\n\
If you have any questions, you can send me a message or reach me at nickwu@alumni.ubc.ca.\n'
    
    global name_to_links
    global nongames
    global games

    # set output to UTF-8
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    def append_project(project, project_dict):
        year = project['year']
        if year in project_dict:
            project_dict[year].append(project)
        else:
            project_dict[year] = [project]

    name_to_links = collections.OrderedDict()
    nongames = collections.OrderedDict()
    games = collections.OrderedDict()
    with codecs.open(PROJECTS_JSON_FILENAME, 'r', 'utf-8') as fp:
        projects = json.load(fp)

    for p in projects:
        if 'ghlink' in p:
            name_to_links[p['name']] = p['ghlink']

        append_project(p, games if 'game' in p['tags'] else nongames)

    print(MD_BEGIN)
    generate_projects()
    print(MD_END)
    generate_link_references()

if __name__ == '__main__':
    main()
