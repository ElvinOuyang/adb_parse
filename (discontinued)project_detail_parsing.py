
# This file can only successfully parse one specific web page from adb

import requests, bs4
project_page = requests.get("http://www.adb.org/projects/49106-002/main")
# Create a bs4 tag file that can be navigated with element names
project_pageSoup = bs4.BeautifulSoup(project_page.text)
# .findAll will return all 'td' elements in project_pageSoup
project_raw_data = project_pageSoup.findAll('td')
# Use the list reference [n] to identify each element to use
print(project_pageSoup.findAll('h3',attrs={'class':'block-title'})[-1].find_next('a').contents[1])

# Todo: go through the [n] and create a comprehensive dictionary for this project

# Parse the information from the elements and assign keys
project_details = {
    'id': project_raw_data[3].string,  # .string will only return the string within the element
    'country': project_raw_data[5].string,
    'approval status': project_raw_data[7].string,
    'project type': project_raw_data[9].string,
    'source of funding': project_raw_data[11].findAll('tr')[0].string,
    'total funding': project_raw_data[13].string,
    'sector': project_raw_data[19].text,
    'description': project_raw_data[23].string,
    'project rationale and linkage to country/regional strategy': project_raw_data[25].string,
    'impact': project_raw_data[27].string,
    'project outcome': project_raw_data[29].string,
    'progress toward outcome': project_raw_data[31].text,
    'project output': project_raw_data[33].text,
    'implementation progress': project_raw_data[35].text,
    'geographical location': project_raw_data[37].text,
    'environmental aspects': project_raw_data[39].text,
    'involuntary resettlement': project_raw_data[41].text,
    'stakeholder involvement - design stage': project_raw_data[45].text,
    'stakeholder involvement - implementation stage': project_raw_data[47].text,
    'business opportunity - consulting services': project_raw_data[49].text,
    'business opportunity - procurement': project_raw_data[51].text,
    'responsible adb officer': project_raw_data[53].text,
    'responsible adb department': project_raw_data[55].text,
    'responsible adb division': project_raw_data[57].text,
    'executing agency name':project_raw_data[59].findAll('span')[0].string,
    'executing agency address':project_raw_data[59].findAll('span')[1].string,
    'timetable - concept clearance':project_raw_data[61].text,
    'timetable - fact finding':project_raw_data[63].text,
    'timetable - mrm':project_raw_data[65].text,
    'timetable - approval':project_raw_data[67].text,
    'timetable - last review mission':project_raw_data[69].text,
    'timetable - last pdf update':project_raw_data[71].text,
    'fund - adb': project_raw_data[88].text,
    'fund - cofinancing': project_raw_data[89].text,
    'fund - counterpart, gov': project_raw_data[90].text,
    'fund - counterpart, beneficiaries':project_raw_data[91].text,
    'fund - counterpart, project sponsor': project_raw_data[92].text,
    'fund - counterpart, others': project_raw_data[93].text,
    'fund - total': project_raw_data[94].text,
    'fund - cumulative disbursement, date': project_raw_data[95].text,
    'fund - cumulative disbursement, amount': project_raw_data[96].text,
    # Identify the "Related Project" in ADB website
    'related project - id':
    project_pageSoup.findAll('h3', attrs={'class': 'block-title'})[-1].find_next('span').string,
    'related project - name':
    project_pageSoup.findAll('h3', attrs={'class': 'block-title'})[-1].find_next('a').contents[1],
    }


def print_dict_sorted(dictionary):
    key_list = []
    for key in dictionary.keys():
        key_list.append(key)
    key_list.sort()
    for key in key_list:
        print(key + ":" + str(dictionary[key]))

print_dict_sorted(project_details)

# Lesson Learnt:
# Instead of using sequence numbers to identify elements in HTML, always find a tangible alternative
# For instance, to identify the funding amount, identify "Total Funding" and locate the numbers with relative location
