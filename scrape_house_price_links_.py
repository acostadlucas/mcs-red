#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


# 1. Obtener el HTML de la página del ranking
url = "https://www.theglobaleconomy.com/rankings/house_price_index/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Lanza error si la petición falla


# In[3]:


# 2. Parsear HTML con BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")


# In[4]:


# 3. Buscar la tabla principal y extraer los links
table = soup.find("table")
country_links = []

if table:
    rows = table.find_all("tr")
    for row in rows:
        cell = row.find("td")
        if cell and cell.a:
            relative_link = cell.a["href"]
            full_url = f"https://www.theglobaleconomy.com{relative_link}"
            country_links.append(full_url)


# In[5]:


# 4. Mostrar resultado
print("Links encontrados:", len(country_links))
for link in country_links:
    print(link)


# In[ ]:




