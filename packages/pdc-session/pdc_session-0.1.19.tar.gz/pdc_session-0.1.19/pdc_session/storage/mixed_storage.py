from .local_storage import LocalStorage, SessionNotFound
from .cloud_storage import CloudStorage


class MixedStorage(LocalStorage):
    cloud_storage: CloudStorage
    
    def __init__(self, dirsession: str = '/pdc_session/') -> None:
        super().__init__(dirsession)
        
        self.cloud_storage = CloudStorage()
    
    
    def get_session(self, username: str):
        try:
            hasil = super().get_session(username)
        
        except SessionNotFound as e:
            hasil = self.cloud_storage.get_session(username)
        
        return hasil
            