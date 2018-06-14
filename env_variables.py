import os

os.environ['TESTDB'] = 'postgresql+psycopg2://joshuakagenyi:#@joshua2016@localhost:5432/testschool'
os.environ['PRODUCTIONDB'] = 'postgresql+psycopg2://joshuakagenyi:#@joshua2016@localhost:5432/school'
os.environ['DEVELOPMENTDB'] = 'postgresql+psycopg2://joshuakagenyi:#@joshua2016@localhost:5432/school'
