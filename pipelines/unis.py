import http.client
import json


def fetchUniversities(country: str) -> dict:
        """
        Get the list of universities for a given country.
        :param country: The name of the country to get the university list for.
        :return: The list of universities or an error message.
        """

        apiUrl = "universities.hipolabs.com/search"

        try:
            # create api url
            if country != None:
                apiUrl += "?country=" + country

            print(apiUrl)

            # get host and path
            urlParts = apiUrl.split("/", 1)
            host, path = urlParts[0], urlParts[1]
            path = "/" + path

            # make http connection
            conn = http.client.HTTPConnection(host)
            conn.request("GET", path)
            response = conn.getresponse()

            if response.status != 200:
                result = f"{response.status} Error fetching data: {response.reason}"
                return {}

            # parse data into dictionary
            data = response.read()
            universities = json.loads(data)

            name = ""
            domains = ""
            result = dict()
            for uni in universities:
                name = uni["name"]
                domains = uni["domains"]
                result[name] = domains

            return result

        except Exception as e:
            results = f"Error while fetching data: {e}"
            return {}
        
uniUS = fetchUniversities("United+States")

print(uniUS)