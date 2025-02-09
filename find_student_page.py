from bs4 import BeautifulSoup
import requests


def id_student(html_year_page, group_target):
    groups = html_year_page.find_all(class_='tile', onclick=True)
    for group in groups:
        group_name = group.text.strip().split('\r\n')
        if str(group_name[0]) == str(group_target):
            line = str(group['onclick']).split('/')
            line = line[4].split("'")
            return line[0]
    return ""


def current_year(html_year_page, group_target):
    groups = html_year_page.find_all(id='studentGroupsForCurrentYear')
    for group in groups:
        index = id_student(group, group_target)
        if index != "":
            return index
    return ""


def parse_group(index_year, group):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    url_year_page = 'https://timetable.spbu.ru/MATH/StudyProgram/' + index_year
    url_year_page_ru = requests.get(url_year_page, cookies=cookie, timeout=10).text
    html_year_page = BeautifulSoup(url_year_page_ru, "lxml")
    return current_year(html_year_page, group)


def find_group(tag_a, group):
    title = tag_a['title'].split(", ")
    for group_in_title in title:
        if group == group_in_title:
            href_year = tag_a['href'].split('/')
            return href_year[3]
    return ""


def find_year(html_main_page, group):
    year_group = "20" + group.split(".Б")[0]
    for tag_a in html_main_page.find_all('a', href=True, title=True):
        title_year = tag_a.text.strip()
        if title_year == year_group:
            href_index = find_group(tag_a, group)
            if href_index != "":
                parse = parse_group(href_index, group)
                return parse
    return ""


def main_student(group):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    url_main_page = 'https://timetable.spbu.ru/MATH'
    url_main_page_ru = requests.get(url_main_page, cookies=cookie, timeout=10).text
    html_main_page = BeautifulSoup(url_main_page_ru, "lxml")
    number = find_year(html_main_page, group)
    return number


if __name__ == '__main__':
    main_student("21.Б15-мм")
