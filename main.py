import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("iptv_processing.log"), logging.StreamHandler()],
)

# URL of the raw README.md file
README_URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/README.md"

# Define output folders
M3U_FOLDER = "m3u_files"
PROCESSED_FOLDER = "processed"
os.makedirs(M3U_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def clean_category_name(name):
    """Remove unwanted symbols, spaces, country codes, and &nbsp; from category names."""
    cleaned_name = name.replace(
        "&nbsp;", " "
    )  # Replace non-breaking space with regular space
    cleaned_name = re.sub(r"[^\w\s]", "", cleaned_name)  # Remove special characters
    cleaned_name = re.sub(
        r"\s+", "_", cleaned_name.strip()
    )  # Replace spaces with underscores
    return cleaned_name


def fetch_readme(url):
    """Fetch the README.md content from the repository."""
    logging.info(f"Fetching README.md from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Successfully fetched README.md")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching README.md: {e}")
        return None


def extract_m3u_links_with_names(readme_content):
    """Extract .m3u links and their corresponding names from the README.md content."""
    logging.info("Extracting .m3u links and names from README.md content")
    matches = re.findall(
        r"<td>(.+?)</td>.*?<code>(https://[^\s]+\.m3u(?:8)?)</code>", readme_content
    )
    m3u_links = {clean_category_name(name): url for name, url in matches}
    logging.info(f"Found {len(m3u_links)} .m3u links")
    return m3u_links


def download_m3u_file(name, url):
    """Download an .m3u file and save it locally."""
    filename = os.path.join(M3U_FOLDER, f"{name}.m3u")
    try:
        logging.info(f"Downloading .m3u file '{name}' from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        logging.info(f"Saved .m3u file to {filename}")
        return filename
    except requests.RequestException as e:
        logging.error(f"Failed to download .m3u file '{name}' from {url}: {e}")
        return None


def check_url_availability(url):
    """Check if a URL is available."""
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            logging.info(f"URL is available: {url}")
            return True
        else:
            logging.warning(
                f"URL is unavailable (status code {response.status_code}): {url}"
            )
            return False
    except requests.RequestException as e:
        logging.error(f"Error checking URL {url}: {e}")
        return False


def process_m3u_file(name, file_path):
    """Process an .m3u file, checking the availability of each link."""
    logging.info(f"Processing .m3u file: {file_path}")
    available_links = []
    unavailable_links = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        current_metadata = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                current_metadata = line
            elif line.startswith("http"):
                is_available = check_url_availability(line)
                if is_available:
                    available_links.append(f"{current_metadata}\n{line}")
                else:
                    unavailable_links.append(f"{current_metadata}\n{line}")

        # Save results to separate files
        available_file = os.path.join(PROCESSED_FOLDER, f"available_{name}.m3u")
        unavailable_file = os.path.join(PROCESSED_FOLDER, f"unavailable_{name}.m3u")

        with open(available_file, "w", encoding="utf-8") as file:
            file.write("\n".join(available_links))
        logging.info(f"Saved available links for '{name}' to {available_file}")

        with open(unavailable_file, "w", encoding="utf-8") as file:
            file.write("\n".join(unavailable_links))
        logging.info(f"Saved unavailable links for '{name}' to {unavailable_file}")

    except Exception as e:
        logging.error(f"Error processing .m3u file '{name}': {e}")


def main():
    """Main function to fetch, process, and save .m3u links."""
    logging.info("Starting script to process .m3u links from README.md")

    # Fetch the README.md file
    readme_content = fetch_readme(README_URL)
    if not readme_content:
        logging.error("Failed to fetch README.md. Exiting script.")
        return

    # Extract .m3u links and names
    m3u_links = extract_m3u_links_with_names(readme_content)
    if not m3u_links:
        logging.warning("No .m3u links found in README.md. Exiting script.")
        return

    # Download and process each .m3u file
    with ThreadPoolExecutor(max_workers=5) as executor:
        for name, m3u_link in m3u_links.items():
            m3u_file = download_m3u_file(name, m3u_link)
            if m3u_file:
                executor.submit(process_m3u_file, name, m3u_file)

    logging.info("Script completed successfully")


if __name__ == "__main__":
    main()
