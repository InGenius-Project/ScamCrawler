from bs4 import BeautifulSoup, Tag
import re
from src.model import Job
from typing import List
import json


class PageAnalyzer104:
    def __init__(self, page_source: str) -> None:
        self._soup: Tag = BeautifulSoup(page_source, "html.parser")
        self._raw_data = self._soup.find("script", {"type": "application/ld+json"})

        if self._raw_data is None:
            raise Exception("Json format not found")

        self._json_data = json.loads(self._raw_data.text)
        description = self._json_data[2].get("description")
        self._description = self._parse_description(description)

    def _parse_description(self, description: str) -> str:
        description = re.sub(r"&lt;br&gt;", "\n", description)
        description = re.sub(r"&lt;.*?&gt;", "", description)
        return description

    def get_area(self) -> str | None:
        area = self._json_data[2]["jobLocation"]["address"]["addressLocality"]
        street = self._json_data[2]["jobLocation"]["address"]["streetAddress"]
        return self._combine_list_or_str(area + street)

    def get_title(self) -> str | None:
        title = self._json_data[2].get("title")
        return self._combine_list_or_str(title)

    def get_worktype(self) -> str | None:
        worktype = re.search(r"工作性質：(.*?)\n", self._description)
        if worktype is None:
            return None
        worktype = worktype.group(1)
        return worktype

    def get_content(self) -> str | None:
        return self._combine_list_or_str(self._description)

    def get_jobname(self) -> str | None:
        jobname = re.search(r"職務類別：(.*?)\n", self._description)
        if jobname is None:
            return None
        jobname = jobname.group(1)
        return self._combine_list_or_str(jobname)

    def get_companyname(self) -> str | None:
        companyName = self._json_data[2]["hiringOrganization"]["name"]
        return self._combine_list_or_str(companyName)

    def get_industry(self) -> str | None:
        industry = self._json_data[2]["industry"]
        return self._combine_list_or_str(industry)

    def get_salary(self) -> str | None:
        unitText = self._json_data[2]["baseSalary"]["value"]["unitText"]
        salary = self._json_data[2]["baseSalary"]["value"].get("value")
        if salary is None:
            return None
        currency = self._json_data[2]["baseSalary"]["currency"]

        if unitText == "MONTH":
            if "月薪" in salary:
                return self._combine_list_or_str(salary + f" ({currency})")
            return self._combine_list_or_str(f"月薪{salary} ({currency})")

        if unitText == "HOUR":
            if "時薪" in salary:
                return self._combine_list_or_str(salary + f" ({currency})")
            return self._combine_list_or_str(f"時薪{salary} ({currency})")

        return None

    def get_workhour(self) -> str | None:
        workhour = self._json_data[2]["workHours"]
        return self._combine_list_or_str(workhour)

    def get_job(self) -> Job | None:
        content = self.get_content()
        if content is None:
            return None

        area = self.get_area()
        jobName = self.get_jobname()
        companyName = self.get_companyname()
        industry = self.get_industry()
        salary = self.get_salary()
        jobType = self.get_worktype()
        workHour = self.get_workhour()

        return Job(
            content=content,
            companyName=companyName,
            industry=industry,
            area=area,
            jobName=jobName,
            salary=salary,
            jobType=jobType,
            workHour=workHour,
        )

    def _combine_list_or_str(self, data: str | List[str] | None) -> str | None:
        if data is None:
            return None

        if isinstance(data, list):
            return ", ".join(data)

        if isinstance(data, str):
            return data
