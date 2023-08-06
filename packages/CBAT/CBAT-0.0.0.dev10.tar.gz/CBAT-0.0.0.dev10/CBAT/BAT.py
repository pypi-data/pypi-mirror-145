import requests
from bs4 import BeautifulSoup


def run(val, check=None, web_url=None, select=None, v1=None, v2=None, v3=None, v4=None, v5=None, v6=None, space1=None, space2=None, space3=None, space4=None, space5=None, space6=None, find_class=None, element=None, _class=None):

    if (not val):
        return print("No Value Specified.")
    elif (val):
        if (not web_url):
            return print("No Web URL Specified.")

        if (check) and (select) and (v1):
            try:
                request = requests.get(web_url, 'lxml')
                print("Checking")
                lst = """"""

                soup = BeautifulSoup(request.text, 'html.parser')

                for element in soup.select(select):
                    if (v1):
                        v = element.select(v1)
                        for i in v:
                            print(i.text)
                            lst += i.text
                            if (space1):
                                print("\n")
                                lst += "\n"
                        if (v2):
                            vv = element.select(v2)
                            for i in vv:
                                print(i.text)
                                lst += i.text
                                if (space2):
                                    print("\n")
                                    lst += "\n"
                            if (v3):
                                vvv = element.select(v3)
                                for i in vvv:
                                    print(i.text)
                                    lst += i.text
                                    if (space3):
                                        print("\n")
                                        lst += "\n"
                                if (v4):
                                    vvvv = element.select(v4)
                                    for i in vvvv:
                                        print(i.text)
                                        lst += i.text
                                        if (space4):
                                            print("\n")
                                            lst += "\n"
                                    if (v5):
                                        vvvvv = element.select(v5)
                                        for i in vvvvv:
                                            print(i.text)
                                            lst += i.text
                                            if (space5):
                                                print("\n")
                                                lst += "\n"
                                        if (v6):
                                            vvvvvv = element.select(v6)
                                            for i in vvvvvv:
                                                print(i.text)
                                                lst += i.text
                                                if (space6):
                                                    print("\n")
                                                    lst += "\n"
                print(lst)
                return lst
            except requests.exceptions.RequestException as e:
                print("Error processing..\n\n\n\n\n\n {0}".format(e))
    elif (find_class):
        if (not web_url):
            return print("No Web URL Specified.")

        if (check) and (element) and (_class):
            try:
                request = requests.get(web_url, 'lxml')
                print("Checking")

                soup = BeautifulSoup(request.text, 'html.parser')

                elements = soup.find_all('{0}'.format(
                    element), attrs={"class": _class})

                return print(elements)
            except requests.exceptions.RequestException as e:
                print("Error processing..\n\n\n\n\n\n {0}".format(e))
    else:
        return print("Hmmm. Something went wrong when trying to run a BAT, please try again.")
