from typing import List, Optional
from ..schemas.schemas import Application, ApplicationCreate, ApplicationUpdate

class ApplicationStorage:
    def __init__(self):
        self._applications = []
        self._id_counter = 1

    def list(self) -> List[Application]:
        return self._applications

    def get(self, app_id: int) -> Optional[Application]:
        for app in self._applications:
            if app.id == app_id:
                return app
        return None

    def create(self, app_in: ApplicationCreate) -> Application:
        app = Application(id=self._id_counter, **app_in.dict())
        self._applications.append(app)
        self._id_counter += 1
        return app

    def update(self, app_id: int, app_in: ApplicationUpdate) -> Optional[Application]:
        app = self.get(app_id)
        if app:
            app.title = app_in.title
            app.description = app_in.description
            return app
        return None

    def delete(self, app_id: int) -> bool:
        app = self.get(app_id)
        if app:
            self._applications.remove(app)
            return True
        return False
