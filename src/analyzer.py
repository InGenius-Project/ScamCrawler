from bs4 import BeautifulSoup, Tag
from src.model import Job
from typing import List


class PageAnalyzer104:
    def __init__(self, page_source: str) -> None:
        self._soup: Tag = BeautifulSoup(page_source, "html.parser")
        self._detail_soup = self._soup.find("div", class_="job-address")

        self._json_data = self._soup.find("script", {"type": "application/ld+json"})

        # TODO: Analyze the json data
        print(self._json_data.text)

    def get_area(self) -> str | None:
        result = self._detail_soup.find_next("span")
        if result is None:
            return result
        return self._combine_list_or_str(result.text)

    def get_worktype(self) -> str | None:
        result = self._detail_soup["worktype"]
        return self._combine_list_or_str(result)

    def get_content(self) -> str | None:
        content = self._detail_soup["jobdescription"]
        return self._combine_list_or_str(content)

    def get_jobname(self) -> str | None:
        u_tags = self._soup.find_all("u")
        result = list(filter(lambda x: x.has_attr("data-v-fd30369a"), u_tags))
        result = [x.text for x in result]
        return self._combine_list_or_str(result)

    def get_companyname(self) -> str | None:
        result = self._soup.find("a", {"data-gtm-head": "公司名稱"})
        if result is None:
            return None
        return self._combine_list_or_str(result.text)

    def get_industry(self) -> str | None:
        pass

    def get_salary(self) -> str | None:
        result = self._detail_soup["salary"]
        return self._combine_list_or_str(result)

    def get_job(self) -> Job | None:
        content = self.get_content()
        if content is None:
            return None

        area = self.get_area()
        jobName = self.get_jobname()
        companyName = self.get_companyname()
        industry = self.get_industry()
        salary = self.get_salary()
        jobType = self.get_jobname()

        return Job(
            content=content,
            companyName=companyName,
            industry=industry,
            area=area,
            jobName=jobName,
            salary=salary,
            jobType=jobType,
        )

    def _combine_list_or_str(self, data: str | List[str] | None) -> str | None:
        if data is None:
            return None

        if isinstance(data, list):
            return ", ".join(data)

        if isinstance(data, str):
            return data

        return str(data)
