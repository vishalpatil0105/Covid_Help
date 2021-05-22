from bs4 import BeautifulSoup
import lxml
import requests

URL = 'https://www.mohfw.gov.in/'

response = requests.get(url=URL)
covid_data_web = response.text
covid_data = BeautifulSoup(covid_data_web, parser="html.parse", features="lxml")


total_data = covid_data.find_all(name='strong', class_='mob-hide')
total_data = [data.getText() for data in total_data]
total_cases = total_data[1]
total_cases = total_cases.replace(u'\xa0', u' ') + " Today's Count"
print(total_cases)
total_recoveries = total_data[3]
total_recoveries = total_recoveries.replace(u'\xa0', u' ') + " Today's Count"
total_death = total_data[5]
total_death = total_death.replace(u'\xa0', u' ') + " Today's Count"


vaccinated_data = covid_data.find_all(name='span', class_='coviddata')
vaccinated_data = [data.getText() for data in vaccinated_data]
total_vaccinated_people = vaccinated_data[0]
total_vaccinated_people = total_vaccinated_people.replace(u'\xa0', u' ')