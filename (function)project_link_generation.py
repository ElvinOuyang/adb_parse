def get_project_link(project_table_link):
    # A function that returns a list of ADB project URLs.
    import requests, bs4
    adb_table = requests.get(project_table_link)
    adb_tableSoup = bs4.BeautifulSoup(adb_table.text)
    project_links_Soup = adb_tableSoup.select('tbody a')
    project_links = []
    while len(project_links_Soup):
        project_url_dict = project_links_Soup.pop()
        project_url = project_url_dict['href']
        project_links.append(project_url)
    return project_links

# Generate a list of ADB project table URLs
project_table_links = ['http://www.adb.org/projects/search/status/approved?keywords=&page=' + str(page)
                       for page in range(1, 10)]

# Create a list for all ADB approved projects by calling the function get_project_link
project_links_main = []
for project_table_link in project_table_links:
    project_links_main.append(get_project_link(project_table_link))
print(project_links_main)

# Todo: write the list-dictionary into an excel file automatically

