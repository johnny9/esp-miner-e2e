"""Interact with web GUI via Selenium."""
from __future__ import annotations

from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore


class WebGUI:
    def __init__(self, ip: str):
        self.url = f"http://{ip}"
        self.driver = webdriver.Firefox()

    def open(self):
        self.driver.get(self.url)

    def quit(self):
        self.driver.quit()

    def get_hashrate(self) -> float:
        element = self.driver.find_element(By.ID, "hashrate")
        return float(element.text.split()[0])
