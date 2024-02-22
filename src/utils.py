from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_content_until(tagname: str, head_tag, include_head=True, join_str="\n") -> str:
    tag_list = []
    current = head_tag

    if include_head is True:
        tag_list.append(current)

    current = current.find_next_sibling()

    while current is not None and current.name != tagname:
        tag_list.append(current)
        current = current.find_next_sibling()

    return f"{join_str}".join([tag.text for tag in tag_list])


class SeleniumDriver:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("-headless")

        self._driver = webdriver.Firefox(
            options=options, service=FirefoxService(GeckoDriverManager().install())
        )

    def get(self, url: str) -> None:
        self._driver.get(url)

    def get_content(self) -> str | None:
        try:
            WebDriverWait(self._driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/h2',
                    )
                )
            )
        except Exception:
            return None
        return self._driver.page_source

    def quit(self) -> None:
        self._driver.quit()
