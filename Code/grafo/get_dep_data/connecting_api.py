import urllib.request, urllib.parse, urllib.error
import json
# Core URL of the API 
api_url = "https://dadosabertos.camara.leg.br/api/v2"
def get_information(rest_of_url,**kwargs):
    """
    This function is responsible to take the final of the url and the arguments(if exists). 
    The function then concats the core api url with the parameter and parse the query arguments
    to make the request, returning a json object with the data.

    """
    url = api_url+rest_of_url
    if kwargs:
        url = url +"?" + urllib.parse.urlencode(kwargs['kwargs'],quote_via=urllib.parse.quote)

    #print(url)
    data = {}
    while True:
        try:
            data = urllib.request.urlopen(url).read().decode()
            break
        except urllib.error.HTTPError:
            print("tentando..")
            continue
        except urllib.error.URLError:
            print("erro de url, continuando a tentar..")
            continue
        

    json_data = json.loads(data)
    return json_data

#get_information(rest_of_url="/deputados",kwargs={"itens":"100"})