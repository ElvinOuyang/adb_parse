import requests, bs4, re

# get project page and prepare Soup
project_page = requests.get("http://www.adb.org/projects/49106-002/main")
project_pageSoup = bs4.BeautifulSoup(project_page.text, 'lxml')
# print(project_pageSoup.prettify())  # test

# Filter for all data area relevant to the work
project_raw_data = project_pageSoup.find_all('td')
# print(project_raw_data)  # test
# print(type(project_raw_data))  # test

# Define the universal search term (need two versions, based on how old the project is)
search_terms = [
    'Project Name', 'Project Number', 'Country', 'Project Status',
    'Project Type / Modality of Assistance', 'Strategic Agendas',
    'Gender Equity and Mainstreaming', 'Impact',
    'Description', 'Project Rationale and Linkage to Country/Regional Strategy',
    'Responsible ADB Officer', 'Responsible ADB Department',
    'Responsible ADB Division', 'Concept Clearance', 'Fact Finding', 'MRM',
    'Approval', 'Last Review Mission', 'Last PDS Update',
    ]

# Create a function that test the matching
def match_term(tag_string, search_term):
    if re.match(search_term, tag_string):
        return True
    else:
        False

# Create a dictionary for each project
project_detail = {}
# Standardized Scrapping for most information
for td in project_raw_data:
    td_string = td.string
    for term in search_terms:
        if match_term(str(td_string), term):
            project_detail[term] = td.next_sibling.next_sibling.text

# Specific Scraping for detailed information
for td in project_raw_data:
    td_string = td.string
    # Import Source of Funding
    if match_term(str(td_string), 'Source of Funding / Amount'):
        project_detail['Source of Funding'] = td.next_sibling.next_sibling.th.string
        project_detail['Funding Amount'] = td.next_sibling.next_sibling.td.next_sibling.next_sibling.string
    # Import Funding Details
    elif match_term(str(td_string),'ADB'):
        project_detail['ADB Funding'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[0].string
        project_detail['Cofinancing Funding'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[1].string
        project_detail['Counterpart Gov'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[2].string
        project_detail['Counterpart Beneficiaries'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[3].string
        project_detail['Counterpart Project Sponsor'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[4].string
        project_detail['Counterpart Others'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[5].string
        project_detail['Total Funding'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[6].string
        project_detail['Cumulative Disbursement Date'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[7].string
        project_detail['Cumulative Disbursement Amount'] = \
            td.parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[8].string
    # Import sector/subsector category
    elif match_term(str(td_string),'Sector / Subsector'):
        project_detail['Sector'] =\
            td.next_sibling.next_sibling.strong.string
        project_detail['Subsector'] =\
            td.next_sibling.next_sibling.strong.string.next_element
    # Import executing agency
    elif match_term(str(td_string),'Executing Agencies'):
        project_detail['Executing Agency'] =\
            td.next_sibling.next_sibling.span.string
        project_detail['Executing Agency Address'] = \
            td.next_sibling.next_sibling.span.next_sibling.next_sibling.text

# Import milestones table
for tag in project_pageSoup.find('table', class_='milestones').descendants:
    if match_term(str(tag),'Original'):
        project_detail['Signing Date'] = tag.parent.parent.next_sibling.next_sibling.find_all('td')[1].string
        project_detail['Effectivity Date'] = tag.parent.parent.next_sibling.next_sibling.find_all('td')[2].string
        project_detail['Closing - Original'] = tag.parent.parent.next_sibling.next_sibling.find_all('td')[3].string
        project_detail['Closing - Revised'] = tag.parent.parent.next_sibling.next_sibling.find_all('td')[4].string
        project_detail['Closing - Actual'] = tag.parent.parent.next_sibling.next_sibling.find_all('td')[5].string


# Define string cleaning function
def clean_string(string):
    return ' '.join(str(string).split())

# Clean up values
for key in project_detail.keys():
    cleaned_value = clean_string(project_detail[key])
    project_detail[key] = cleaned_value
"""End of Project Detail Creation Code"""


# Print project detail dictionary for checking
def print_dict_sorted(dictionary):
    key_list = []
    for key in dictionary.keys():
        key_list.append(key)
    key_list.sort()
    for key in key_list:
        print(key + ":" + str(dictionary[key]))

print_dict_sorted(project_detail)  # test