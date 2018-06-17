#!/usr/bin/env python3
"""Update projects.json then run: ./generate_readme.py > README.md"""

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


def print_generated_projects():
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
                    tagline.append(
                        'languages: **_{:s}_**'.format(', '.join(p['languages'])))
                if 'technologies' in p:
                    tagline.append(
                        'technologies: **_{:s}_**'.format(', '.join(p['technologies'])))
                for tag in tagline:
                    print('  * ' + tag)
                print('\n')

    print_projects(nongames)
    print('## Games')
    print_projects(games)


def print_generated_link_references():
    global name_to_links
    print('[//]: #')
    for name, link in name_to_links.items():
        print('[{:s}]:<{:s}>'.format(name, link))


def main():
    PROJECTS_JSON_FILENAME = 'projects.json'

    MD_BEGIN = """# **Projects**
My projects and their Github links.
Organized into [projects](#projects) and [games](#games) sorted chronologically.
"""

    MD_END = """## Thanks for visiting!
If you have any questions, you can send me a message or reach me at nickwu@alumni.ubc.ca.
"""

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
    print_generated_projects()
    print(MD_END)
    print_generated_link_references()


if __name__ == '__main__':
    main()
