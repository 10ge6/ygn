import lxml.etree as ET
import sys
import re

xml_file = open(sys.argv[1], 'r')
xml_input = xml_file.read()
xml_file.close()

res = re.search(r'<type>turing</type>&#13;\n\t(.*?)&#13;\n</structure>', xml_input, re.DOTALL).group(1)
res = re.sub(r'		<!--(.*?)-->&#13;\n', '', res)

tm = ET.fromstring(res)

table = []
symbols_header = [' ']
reads = {}
delta = 0
delta_keep = 0
state_count = 0

for itr, curr_input in enumerate(tm.xpath('/automaton/transition/read/text()')):
    if curr_input not in reads:
        delta_keep = itr - delta
        reads[curr_input] = delta_keep
        symbols_header.append('\\('+curr_input+'\\)')
    else:
        delta += 1

for itr, curr_input in enumerate(tm.xpath('/automaton/transition/write/text()')):
    if curr_input not in reads:
        delta_keep += 1
        reads[curr_input] = delta_keep
        symbols_header.append('\\('+curr_input+'\\)')

if tm.xpath('/automaton/transition/read[1][not(text())]'):
    reads['\\square'] = delta_keep + 1
    symbols_header.append('\\(\\square\\)')

table.append(symbols_header)

for child in tm:
    if child.tag == "state":
        table.append(['\\(-\\)' for _ in range(len(reads)+1)])
        state_count += 1
        table[state_count][0] = '\\('+child.attrib.get('name')+'\\)'
    elif child.tag == "transition":
        transition_str = '\\('
        table_x = -1
        table_y = -1
        for val in child:
            if val.tag == "from":
                table_y = int(val.text)+1
            elif val.tag == "read":
                if not isinstance(val.text, str):
                    val.text = "\\square"
                table_x = reads[val.text]+1
            elif (val.tag == "write" and isinstance(val.text, str)) or val.tag == "move":
                transition_str += (val.text + ',')
            elif val.tag == "to":
                transition_str += (table[int(val.text)+1][0][2:-2] + ',')
            elif val.tag == "write":
                transition_str += '\\square,'
        transition_str = '\\)'.join(transition_str.rsplit(',', 1))
        table[table_y][table_x] = transition_str
    else:
        print("ATTEMPTED TO PARSE MALFORMATTED XML INPUT!")
        exit

print("\\begin{tabular}{ ",end='')
for c in range(len(reads)+1):
    print("|c",end='')
print("| }\n    \\hline")
for y in range(state_count+1):
    print("    ",end='')
    for x in range(len(reads)+1):
        if x < len(reads):
            print(table[y][x],end=' & ')
        else:
            print(table[y][x],end=' \\\\\n    \\hline\n')
print("\\end{tabular}",end='')