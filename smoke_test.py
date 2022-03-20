#-*- coding: utf-8 -*-
from selenium import webdriver
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

SITE_URL = 'http://www.shop-expertplus.expertplus-demo.ru'
CATALOG_SLUG = '/catalog/dlja-doma/'

SEARCH_CANON_SLUG = '/catalog/find/?find=canon'
CALLBACK_HEADER = 'Обратный звонок'
SENDMAIL_HEADER = 'Обратная связь'

customer_info = {
    'fio': u'Тест Тестович',
    'email': 'email@email.ru',
    'phone': '7777777777',
    'town': u'Тестовецк',
    'street': u'Тестовая',
    'house': '7'
}

menu = {
    'Главная': '',
    'Новости': '/news/',
    'Оплата': '/content/payments/',
    'Доставка': '/content/delivery/'
}

sidebar_menu = {
    'cart-link': '/order/',
    'small-favorite-link': '/catalog/favorites/',
    'small-compare-link': '/catalog/compare/',
    'user-link': '/users_login/'
}

class SmokeTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(SITE_URL)

    def popup_check(self, element_id, header):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, '{}'.format(element_id)))
        )
        self.driver.find_element_by_xpath("//div[@id='{}']/header[text()='{}']".format(element_id, header))

    def test_order(self):
        self.driver.find_element_by_css_selector('.catalog-category-item').click()
        self.driver.find_element_by_css_selector('.catalog-podmenu-image-block').click()
        self.driver.find_element_by_css_selector('.product-item').click()
        self.driver.find_element_by_css_selector('.button-buy').click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[a/text()='Оформить заказ']"))
        ).click()
        self.driver.find_element_by_xpath("(//label[input/@name='dostavka_id'])[2]").click()
        select = Select(self.driver.find_element_by_name('dostavka_day'))
        select.select_by_value(u'Не имеет значения')
        select = Select(self.driver.find_element_by_name('dostavka_time'))
        select.select_by_value(u'Не имеет значения')
        for name, keys in customer_info.items():
            self.driver.find_element_by_name(name).send_keys(keys)
        self.driver.find_element_by_xpath("(//label[input/@name='sposob_oplaty_id'])").click()
        self.driver.find_element_by_xpath("//button[text()='Оформить заказ']").click()
        self.driver.find_element_by_xpath("//p[text()='Ваш заказ был успешно оформлен!']")
        self.driver.close()

    def test_header_menu(self):
        self.driver.find_element_by_xpath("//span[text()='Каталог']").click()
        self.driver.find_element_by_xpath("(//li/a[text()='Для дома'])[2]").click()
        assert self.driver.current_url, SITE_URL+CATALOG_SLUG
        for menu_item, slug in menu.items():
            self.driver.find_element_by_xpath("//a[text()='{}']".format(menu_item)).click()
            assert self.driver.current_url, SITE_URL + slug
        self.driver.close()

    def test_sidebar_menu(self):
        for menu_item, slug in sidebar_menu.items():
            self.driver.find_element_by_css_selector('.{}'.format(menu_item)).click()
            assert self.driver.current_url, SITE_URL + slug
        self.driver.find_element_by_css_selector('.callback-link').click()
        self.popup_check('callback', CALLBACK_HEADER)
        self.driver.find_element_by_css_selector('.close').click()
        self.driver.find_element_by_css_selector('.sendmail-link').click()
        self.popup_check('sendmail', SENDMAIL_HEADER)
        self.driver.close()

    def test_search(self):
        self.driver.find_element_by_name('find').send_keys("canon")
        self.driver.find_element_by_css_selector('.search-button').click()
        assert self.driver.current_url, SITE_URL + SEARCH_CANON_SLUG
        self.driver.close()

    def test_auth(self):
        self.driver.find_element_by_css_selector('.user-link').click()
        self.driver.find_element_by_name('email_login').send_keys("test@gmail.com")
        self.driver.find_element_by_name('password_login').send_keys("test")
        self.driver.find_element_by_xpath("//*[text()='Войти']").click()
        # Дальнейшая проверка невозможна, так как полноценная авторизация на данном демо-сайте недоступна
        self.driver.close()

    def test_header_callback(self):
        self.driver.find_element_by_css_selector('.header-callback').click()
        self.popup_check('callback', CALLBACK_HEADER)
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
