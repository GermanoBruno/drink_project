import requests
from bs4 import BeautifulSoup
import pandas as pd

# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import os

class Recipe():
	def __init__(self, name, ingredients, instructions):
		self.name = name
		self.ingredients = ingredients
		self.instructions = instructions

	def __str__(self):
		rep = self.name + '\n'
		for step in self.ingredients:
			for i in step:
				rep = rep + i + ' '
			rep = rep + '\n'

		rep = rep + self.instructions
		return (rep)

	def getName(self):
		return self.name

	def getIngredients(self):

		return self.ingredients

	def getInstructions(self):

		return self.instructions

	def recipe_to_list(self):
		return [self.name, self.ingredients, self.instructions]


def getPageContent(url):
	req = requests.get(url)
	if req.status_code == 200:
		return req.content
	else:
		return None

def getCategories(content):
	if content != None:
		soup = BeautifulSoup(content, 'lxml')
		cats = soup.find(name='div', class_='drink-cats')

		links = cats.find_all(name='a')

		urlList = []

		for link in links:
			urlList.append(link['href'])
		baseUrl = 'https://cocktailpartyapp.com'
		urlList = [baseUrl + i for i in urlList]
		return urlList
	else:
		return None

def getDrinkList(content):
	if content != None:
		soup = BeautifulSoup(content, 'lxml')
		drinks = soup.find(name='ul', class_='chips')

		drinkList = drinks.find_all(name='li', class_='chip drink-chip')
		urlList = []
		for i in drinkList:
			urlList.append(i.find(name='a')['href'])
		return urlList
	else:
		return None

def getDrinkContent(content):
	if content != None:
		soup = BeautifulSoup(content, 'lxml')
		page = soup.find(name='div', class_='recipe-card')

		drinkName = page.find(name='h1').text

		recipe = page.find(name='div', class_='ingredient-list')
		recipe = recipe.find_all(name='li')
		ingredientList = []
		for step in recipe:
			amount = step.find(name='span', class_='amount').text.strip('\r\n\t').split('\t')
			ingredient = step.find(name='span', class_='ingredient').text.strip('\n')
			newRecipe = [amount[0], amount[-1], ingredient]
			ingredientList.append(newRecipe)

		instructions = page.find(name='div', class_='recipe-instructions').text.strip('\n')
		print(drinkName)
		newDrink = Recipe(drinkName, ingredientList, instructions)
		return newDrink

	else:
		return None

def drink_list_to_df(drink_list):
	col = ["name", "ingredients_list", "instructions"]
	return pd.DataFrame(drink_list, columns = col)