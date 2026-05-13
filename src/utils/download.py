def download(url: str):
    import requests
    from tqdm import tqdm
    from pathlib import Path

    filename = url.split("/")[-1]
    path = Path(filename)

    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(path, "wb") as file:
        if total_size > 0:
            with tqdm(
                total=total_size, unit="B", unit_scale=True, desc=filename
            ) as pbar:
                for data in response.iter_content(chunk_size=8192):
                    file.write(data)
                    pbar.update(len(data))
        else:
            for data in response.iter_content(chunk_size=8192):
                file.write(data)

    print(f"Downloaded to {path}")
    return path


def download_zip(url, extract_to="."):
    import zipfile
    from pathlib import Path

    extract_path = Path(extract_to)
    extract_path.mkdir(parents=True, exist_ok=True)
    path = None

    try:
        path = download(url=url)

        print(f"Extracting to {extract_path}...")
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        print("Extraction complete!")

        path.unlink()
        print(f"Removed zip file: {path}")

        return str(extract_path)

    except Exception as e:
        if path and path.exists():
            path.unlink()
        raise Exception(f"Failed: {e}")
