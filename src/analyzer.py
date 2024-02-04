from bs4 import Tag
from src.model import Job
from typing import List


class PageAnalyzer104:
    def __init__(self, article_tag: Tag) -> None:
        self._parent = article_tag

    def get_area(self) -> str | None:
        bblock_left = self._parent.select_one("div")
        if bblock_left is None:
            return None

        uls = bblock_left.select("ul")
        if uls is None or len(uls) < 2:
            return None

        ul = uls[1]
        area = ul.select_one("li")
        if area is None:
            return None
        return area.get_text()

    def get_content(self) -> str | None:
        bblock_left = self._parent.select_one("div")
        if bblock_left is None:
            return None

        p = bblock_left.select_one("p")
        if p is None:
            return None

        return p.get_text()

    def get_jobname(self) -> str | None:
        result = self._parent.get("data-job-name")
        return self._combine_list_or_str(result)

    def get_companyname(self) -> str | None:
        result = self._parent.get("data-cust-name")
        return self._combine_list_or_str(result)

    def get_industry(self) -> str | None:
        result = self._parent.get("data-indcat-dec")
        return self._combine_list_or_str(result)

    def get_job(self) -> Job | None:
        content = self.get_content()
        if content is None:
            return None

        area = self.get_area()
        jobName = self.get_jobname()
        companyName = self.get_companyname()
        industry = self.get_industry()

        return Job(
            content=content,
            companyName=companyName,
            industry=industry,
            area=area,
            jobName=jobName,
        )

    def _combine_list_or_str(self, data: str | List[str] | None) -> str | None:
        if data is None:
            return None

        if isinstance(data, list):
            return ", ".join(data)

        if isinstance(data, str):
            return data

        return str(data)
