#!/usr/bin/env python3
import os, sys, requests
from argparse import ArgumentParser, FileType
from yaml import safe_load as load
from jinja2 import Template, Environment


def main():
  parser = ArgumentParser()
  parser.add_argument('input', type=FileType('r'))
  parser.add_argument('output', nargs='?', type=FileType('w'), default=sys.stdout)
  args = parser.parse_args()
  result = jam(args.input)
  args.output.write(result)


def jam(input):
  config = load(input)
  env = Environment()
  env.filters['download'] = download
  template = env.from_string(get_template(config['template']))
  return template.render(data=config['data'])


def get_template(template):
  if isinstance(template, str):
    return template
  if isinstance(template, dict):
    return download(template['url'])
  raise ValueError('Does not support template of type %s' % type(template))


def download(url):
    return requests.get(url).text


if __name__ == "__main__":
  if not os.isatty(0):
    print(jam(sys.stdin))
  else:
    main()
