import scrapy
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Any


class LeroymerinSpider(scrapy.Spider):
    name = "LeroyMerin"
    allowed_domains = ["leroymerlin.com.br"]
    start_urls = ["https://leroymerlin.com.br"]
    
    
    def parse(self, response):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--lang=en-US")
        options.add_argument("accept-encoding=gzip, deflate, br")
        options.add_argument("referer=https://www.google.com/")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)

        self.driver.get("https://www.leroymerlin.com.br/")
        KEY = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-autocomplete="list"]')
        KEY.send_keys("Porcelanato")
        VALLUE = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Buscar"]').click()

        time.sleep(5)

        last_page_number = self.click_last_page_button(self.driver)

        all_urls = []

        if last_page_number is not None:
            for page_number in range(1, last_page_number + 1):
                page_url = self.base_url + str(page_number)
                self.make_request(self.driver, page_url)
                page_urls = self.click_and_get_urls(self.driver)
                all_urls.extend(page_urls)

        self.log("URLs coletadas:")
        for url in all_urls:
            self.log(url)

        products = []

        for url in all_urls:
            self.make_request(self.driver, url)
            product = self.extract_product_details(self.driver)

            yield {
                'nome': product['nome'],
                'detalhespreco': product['detalhespreco'],
                'descricao': product['descricao'],
                'precos': product['precos'],
                
            }

            products.append(product)

        self.log("Detalhes dos produtos:")
        for product in products:
            ...
           

        self.driver.quit()

    def extract_product_details(self, driver):
        driver.implicitly_wait(30)
        product_dict = {}

        try:
            nome = driver.find_elements(By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div/div[1]/h1")[0].text
            product_dict["nome"] = nome
        except:
            pass

        try:
            precos = driver.find_elements(By.XPATH, "/html/body/div[10]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div/span[1]")[0].text
            product_dict["precos"] = float(precos.replace("R$", "").replace(",", "").replace(",", ".").strip())
        except:
            pass

        try:
            preco_detalhes = driver.find_elements(
                By.XPATH, "/html/body/div[10]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[3]/div/strong")[0].text
            product_dict["detalhespreco"] = preco_detalhes
        except:
            pass

        try:
            descricao = driver.find_elements(
                By.XPATH, "/html/body/div[10]/div/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div/div/p")[0].text
            product_dict["descricao"] = descricao
        except:
            pass

        imagens = driver.find_elements(
            By.XPATH, "//div[@class='css-17kvx2v-wrapper__image-wrapper ejgu7z2']//img")
        cont = 0
        for imagem in imagens:
            product_dict["imagem" + str(cont)] = imagem.get_attribute(
                "src").replace("140x140.jpg", "600x600.jpg").replace("140x140.jpeg", "600x600.jpeg")
            cont += 1

        referencias = driver.find_elements(
            By.XPATH, "/html/body/div[10]/div/div[4]/div[2]/table/tbody/tr/th")
        atributos = driver.find_elements(
            By.XPATH, "/html/body/div[10]/div/div[4]/div[2]/table/tbody/tr/td")
        cont = 0
        for referencia in referencias:
            product_dict[referencia.text] = atributos[cont].text
            cont += 1

        return product_dict

        