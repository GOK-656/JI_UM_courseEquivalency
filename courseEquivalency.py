import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime

url = "https://app.ji.sjtu.edu.cn/equivalence/university/index/2"
html = requests.get(url=url)

if html.status_code == 200:
    soup = BeautifulSoup(html.text, "html.parser")
    course_text = soup.find("div", id="list").find_all("li")

    titles = ["Dept.", "Code", "Title", "Credits1", "Equivalency", "Credits2", "Category", "Level", "Fields",
              "Expiration"]
    data = [[] for _ in range(len(titles))]

    for courseInfo in course_text:
        info = courseInfo.find_all("span")
        i = 0
        for item in info:
            data[i].append(item.text.strip())
            i += 1

    courseList = zip(titles, data)
    df = pd.DataFrame(dict(courseList))

    today = datetime.date.today()
    output_path = "./JI_UM_CourseEquivalency_{}{}{}.xlsx".format(today.year, today.month, today.day)
    df.to_excel(output_path, index=False)
    print("Updated!")
else:
    print("Error")
    exit(-1)
