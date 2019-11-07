import json
import numpy as np
import seaborn as sns
import random
import math
import sys

sns.set()


with open('Schedule.csmo') as f:
    data = json.load(f)

courses = data['schedules'][0]['items']

"""
# this is for random color generator
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(color):
    k = hilo(color[0], color[1], color[2])
    return list(k - u for u in color)

for i in range(len(courses)):
    back = list(np.random.choice(range(256), size=3))
    title = complement(back)
    print('\\defineevent{%d}{%.2f}{%.2f}{%.2f}{%.2f}{%.2f}{%.2f}' %
            (i, back[0]/256, back[1]/256, back[2]/256,
             title[0]/256, title[1]/256, title[2]/256))
"""

#colors = sns.hls_palette(len(courses), l=.5, s=.5)
#colors = sns.color_palette("hls", len(courses))
colors = sns.color_palette(str(sys.argv[1]), n_colors=len(courses))
random.shuffle(colors)

for i in range(len(courses)):
    (r, g, b) = [i * 256 for i in colors[i]]
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))

    if hsp > 127.5:
        print('\\defineevent{%d}{%.3f}{%.3f}{%.3f}{%.3f}{%.3f}{%.3f}' %
                (i, colors[i][0], colors[i][1], colors[i][2],
                0.2, 0.2, 0.2))
    else:
        print('\\defineevent{%d}{%.3f}{%.3f}{%.3f}{%.3f}{%.3f}{%.3f}' %
                (i, colors[i][0], colors[i][1], colors[i][2],
                0.8, 0.8, 0.8))

print('\\defineevent{%d}{%.3f}{%.3f}{%.3f}{%.3f}{%.3f}{%.3f}' %
        (66, 0, 0, 0,
        1, 1, 1)) # total black

print('%%%%%%%%%%%%%%')
print(r"""\begin{timetable}
\hours{8}{10}{1}
\englishdays{1}""")

c_i = -1 # color index

for c in courses:
    c_i = c_i + 1
    cid = c['title'].replace('\t', ' ')
    for slot in c['meetingTimes']:
        start = '{' + str(slot['startHour']) + str(slot['startMinute']).zfill(2) + '}'
        end = '{' + str(slot['endHour']) + str(slot['endMinute']).zfill(2) + '}'
        i = 1
        loc = slot['location']
        type = slot['courseType']
        instr = slot['instructor']
        for day, bool in slot['days'].items():
            if bool:
                print('\\event', i , '%s%s{%s {\\tiny %s}}{\\tiny %s}{%s}{%d}' %
                        (start, end, cid, type, instr, loc, c_i))
            i = i + 1
