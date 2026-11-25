#!/usr/bin/env python3
import sys
from ambuild2 import run

parser = run.BuildParser(sourcePath=sys.path[0], api='2.2')
parser.options.add_argument('--sm-path', required=True, help='Path to SourceMod')
parser.options.add_argument('--mms-path', required=True, help='Path to Metamod:Source')
parser.options.add_argument('--hl2sdk-root', required=True, help='Directory containing hl2sdk-tf2')
parser.options.add_argument('--targets', default='x86,x86_64', help='Comma-separated architectures')
parser.options.add_argument('--enable-debug', action='store_true', dest='debug')
parser.options.add_argument('--enable-optimize', action='store_true', dest='opt')
parser.Configure()
