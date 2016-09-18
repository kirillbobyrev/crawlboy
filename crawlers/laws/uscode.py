# -*- coding: utf-8 -*-
'''Extract data from U.S. Code XML files from http://uscode.house.gov

$ python3 uscode.py ../../data/laws/uscode/xml
'''

from bs4 import BeautifulSoup, NavigableString
import argparse
import os
import json

def main(directory, outfile):
    sections_total = 0
    for uscode_file in os.listdir(directory):
        if not uscode_file.endswith('.xml'):
            continue
        input_file = open(os.path.join(directory, uscode_file), 'r')
        title = BeautifulSoup(input_file.read(None), "lxml")
        if (title.title is None) or (title.title.heading is None):
            continue
        title_num = title.title.num['value']
        title_heading = title.title.heading.string
        print('Crawling {}...'.format(uscode_file))
        sections = 0
        for chapter in title.find_all('chapter'):
            chapter_num = chapter.num['value']
            chapter_heading = chapter.heading.string
            for section in chapter.find_all('section'):
                if section.heading is None or section.num is None or \
                   section.content is None:
                    continue
                section_num = section.num['value']
                section_heading = section.heading.text.strip()
                text = section.content.text.strip()
                next_section = {
                    'title': {'num': title_num,
                              'heading': title_heading},
                    'chapter': {'num': chapter_num,
                                'heading': chapter_heading},
                    'section': {'num': section_num,
                                'heading': section_heading,
                                'text': text}
                }
                outfile.write(json.dumps(next_section) + '\n')
                sections += 1
        print('Extracted {} sections.'.format(sections))
        sections_total += sections
    print('Extracted {} sections in total.'.format(sections_total))
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl U.S. Code.')
    parser.add_argument('dir', type=str,
                        help='Directory containing XML U.S. Code dump.')
    parser.add_argument('outfile', type=argparse.FileType('w'),
                        help='Dump sections to this file.')
    args = parser.parse_args()
    main(args.dir, args.outfile)
