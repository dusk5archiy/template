from gdown.download import download
import zipfile
from pathlib import Path
import os


def gdrive_download(file_id: str, output_dir="."):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    url = f"https://drive.google.com/uc?id={file_id}"
    zip_path = None

    try:
        zip_file = download(
            url=url, output=os.path.join(output_dir, "download.zip"), quiet=False
        )
        print(zip_file)
        assert isinstance(zip_file, str)
        zip_path = Path(zip_file)
        if not zip_path.exists():
            raise Exception("Download failed: File not found")

        print(f"Extracting to {output_path}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_path)

        print(f"Extraction complete! Files extracted to: {output_path}")

        zip_path.unlink()
        print(f"Removed zip file: {zip_path}")

        return zip_file

    except Exception as e:
        if zip_path and zip_path.is_file():
            zip_path.unlink()
        raise Exception(f"Failed to download and extract: {e}")
