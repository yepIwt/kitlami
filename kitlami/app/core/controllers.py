from blacksheep.server.controllers import Controller


class ApiController(Controller):
    @classmethod
    def route(cls) -> str:
        return "/api"