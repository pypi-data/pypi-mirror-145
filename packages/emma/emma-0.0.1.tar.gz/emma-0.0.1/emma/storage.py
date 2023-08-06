import hashlib
import os.path

from django.core.files.storage import FileSystemStorage


class ContentAddressableStorage(FileSystemStorage):

    def _save(self, name, content):
        name = super()._save(name, content)
        full_path = os.path.join(self.location, name)
        with open(full_path, 'rb') as reader:
            content = reader.read()
        digest = hashlib.sha256(content).hexdigest()
        dir1, dir2, filename = digest[:2], digest[2:4], digest[4:]
        _, extension = os.path.splitext(name)
        new_name = filename + extension
        new_dir = os.path.join(self.location, 'contents', dir1, dir2)
        os.makedirs(new_dir, exist_ok=True)
        new_path = os.path.join(new_dir, new_name)
        if os.path.exists(new_path):
            os.remove(full_path)
        else:
            os.rename(full_path, new_path)
        os.symlink(new_path, full_path)
        return name
