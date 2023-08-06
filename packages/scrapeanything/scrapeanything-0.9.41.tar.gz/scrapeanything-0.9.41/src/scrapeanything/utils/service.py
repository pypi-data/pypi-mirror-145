from scrapeanything.utils.config import Config
from scrapeanything.database.repository import Repository
from scrapeanything.database.models import Model
from scrapeanything.utils.constants import *
import requests

class Service:

    def __init__(self, config: Config=None, repository: Repository=None) -> None:
        if repository is not None:
            self.repository = repository
    
        if config is not None:
            self.config = config
    
    def __del__(self):
        if hasattr(self, 'repository'):
            self.repository.close()

    def all(self) -> 'list[Model]':
        entities = self.repository.all(entity_type=self.entity_type)
        return entities

    def load(self, entity: Model) -> Model:
        entity = self.repository.load(entity=entity)
        return entity

    def save(self, entity: Model) -> None:
        self.repository.save(entity=entity)

    def wget(self, url: str, parameters: dict=None, method: Requests.Methods=Requests.Methods.GET, response_type: Requests.ResponseTypes=Requests.ResponseTypes.JSON) -> any:
        if method == Requests.Methods.GET:
            response = requests.get(url=url, data=parameters)
        elif method == Requests.Methods.POST:
            response = requests.post(url=url, data=parameters)
        else:
            raise Exception(f'{method} method is not supported')

        if response_type == Requests.ResponseTypes.JSON:
            return response.json()
        elif response_type == Requests.ResponseTypes.STRING:
            return response.text
        else:
            raise Exception(f'{response_type} response type is not supported')