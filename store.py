import requests
from os import mkdir


class Store:
    def __init__(self, save=False):
        self.save = save

    def store(self, urls, location):
        try:
            mkdir(location)
        except Exception as e:
            pass
        with open(f'{location}index.txt', 'w') as fd:
            for i in urls:
                # if self.save and location == 'relevant/':
                #     with open(f'{location}{i[0]}.html', 'w') as html:
                #         html.writelines(requests.get(i[0]))
                fd.writelines(f'{i[0]}->{i[1]}\n')

