class Job:
    def __init__(
        self,
        content: str,
        title: str | None = None,
        companyName: str | None = None,
        industry: str | None = None,
        area: str | None = None,
        salary: str | None = None,
        other: str | None = None,
        jobName: str | None = None,
    ) -> None:
        self.content = content
        self.title = title
        self.companyName = companyName
        self.industry = industry
        self.area = area
        self.salary = salary
        self.other = other
        self.jobName = jobName

    @staticmethod
    def get_TC_name(value: str) -> str:
        translate_dict = {
            "content": "內文",
            "title": "標題",
            "companyName": "公司名稱",
            "industry": "產業",
            "area": "地區",
            "salary": "薪資",
            "other": "其他資訊",
            "jobName": "職稱",
        }
        result = translate_dict.get(value)
        if result is None:
            return ""
        return result

    def combine(self) -> str:
        result = ""
        for var_name, var_value in self.__dict__.items():
            if var_value is None:
                continue
            result = result + f"{self.get_TC_name(var_name)}:\n{var_value}\n\n"
        return result
