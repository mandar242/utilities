#!/usr/bin/env python3
#
# Simplified BSD License https://opensource.org/licenses/BSD-2-Clause)
#

from github import Github


g = Github("1234567890abcdef1234567890abcdef")

repo = g.get_repo("ansible-collections/community.aws")
pulls = repo.get_pulls(state='open', sort='created', base='master')
for pr in pulls:
    print(pr.number)
    pr.edit(base='main')

