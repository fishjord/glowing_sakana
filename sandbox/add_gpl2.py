#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
	print "USAGE: add_gpl2.py <file whose template should be modified>"
	sys.exit(1)

template = """/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */"""

new_template = """/*
 * Copyright (C) 2012 Michigan State University <rdpstaff at msu.edu>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */"""

text = open(sys.argv[1]).read()

open(sys.argv[1], "w").write(text.replace(template, new_template))
