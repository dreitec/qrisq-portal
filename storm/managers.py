from django.db.models.manager import Manager


class StormManager(Manager):
    def __init__(self):
        super().__init__()
        self._db = 'storm'
    
    def db_manager(self, using=None, hints=None):
        obj = super().db_manager(using=using, hints=hints)
        obj._db = 'storm'
        return obj