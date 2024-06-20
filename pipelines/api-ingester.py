import http.client
import json

#================================#
#   Fetch Universities Example   #
#================================#

def fetchUniversities(apiUrl, country = None):
    try:
        # create api url
        if (country != None):
            apiUrl += "?country=" + country

        # get host and path
        urlParts = apiUrl.split('/', 1)
        host, path = urlParts[0], urlParts[1]
        path = "/" + path

        # make http connection
        conn = http.client.HTTPConnection(host)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status != 200:
            print(f"{response.status} Error fetching data: {response.reason}")
            return {}
        
        # parse data into dictionary
        data = response.read()
        universities = json.loads(data)

        name = ''
        domains = ''
        result = dict()
        for uni in universities:
            name = uni['name']
            domains = uni['domains']
            result[name] = domains
        
        return result
    
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return {}

apiUrl = 'universities.hipolabs.com/search'

# api call for universities in the United States
uniUS = fetchUniversities(apiUrl, 'United+States')

# api call for universities in Spain
uniES = fetchUniversities(apiUrl, 'Spain')

print(uniUS)
print(uniES)


#================================#
#   Fetch Pages From Debewiki    #
#================================#

def fetchPages(apiUrl, date = None):
    try:
        # create api url
        if (date != None):
            apiUrl += "?fromDate=" + date

        # get host and path
        urlParts = apiUrl.rsplit('/', 1)
        host, path = urlParts[0], urlParts[1]
        path = "/" + path

        # make http connection
        conn = http.client.HTTPConnection(host)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status != 200:
            print(f"{response.status} Error fetching data: {response.reason}")
            return {}
        
        # parse data into dictionary
        data = response.read()
        pages = json.loads(data)

        id = 0
        content = ''
        result = dict()
        for page in pages:
            id = page['ID']
            content = page['ContentHTML']
            result[id] = content
        
        return result
    
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return {}

apiUrl = 'debewiki/DebeWiki/Api/FetchPages'

# api call for all pages
allPages = fetchPages(apiUrl)

# api call for pages after April 30, 2024
recentPages = fetchPages(apiUrl, "2024-04-30")

print(allPages)
print(recentPages)
