import os
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

# Setup logging
def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
    return logging.getLogger()

# Save log entry
def save_log(pin_id, title, description, link, metadata, date, log_file):
    with open(log_file, 'a') as log:
        log.write(f"{pin_id}\t{title}\t{description}\t{link}\t{metadata}\t{date}\n")

# Download from a URL
def download_from_url(url, dest_folder, logger):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = os.path.join(dest_folder, url.split("/")[-1])
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            logger.info(f"Downloaded: {file_name}")
            return file_name
        else:
            logger.error(f"Failed to download {url}, status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred while downloading {url}: {str(e)}")

# Download media based on input
def download_media(path, dir, max_threads, cut_length, board_timestamp, log_timestamp, force, re_scrape, update_all, exclude_section, image_only, video_only, https_proxy, http_proxy, cookies_file):
    logger = setup_logging('log-pinterest-downloader.log')
    
    # Here you should add logic to handle Pinterest API interaction or scraping
    # For now, it is a placeholder to demonstrate functionality
    logger.info(f"Starting download for path: {path}")
    
    # Example URLs (replace with actual Pinterest URL fetching logic)
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
    
    # Setting proxies if provided
    proxies = {}
    if https_proxy:
        proxies['https'] = https_proxy
    if http_proxy:
        proxies['http'] = http_proxy

    # Create directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Use ThreadPoolExecutor to download media concurrently
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(download_from_url, url, dir, logger) for url in urls]
        for future in futures:
            future.result()
    
    logger.info("Download completed")

# Streamlit interface
def main():
    st.title("Pinterest Downloader")

    # User inputs
    path = st.text_input("Pinterest Path or URL")
    dir = st.text_input("Directory to Save Downloads", value="images")
    max_threads = st.number_input("Max Threads", value=5)
    cut_length = st.number_input("Max Filename Length", value=255)
    board_timestamp = st.checkbox("Add Timestamp to Board Directory")
    log_timestamp = st.checkbox("Add Timestamp to Log File")
    force = st.checkbox("Force Re-download")
    re_scrape = st.checkbox("Re-scrape All Media")
    update_all = st.checkbox("Update All Folders")
    exclude_section = st.checkbox("Exclude Sections")
    image_only = st.checkbox("Download Images Only")
    video_only = st.checkbox("Download Videos Only")
    https_proxy = st.text_input("HTTPS Proxy")
    http_proxy = st.text_input("HTTP Proxy")
    cookies_file = st.file_uploader("Cookies File", type=["txt"])

    if st.button("Start Download"):
        # Prepare cookies file if uploaded
        if cookies_file is not None:
            with open("cookies.txt", "wb") as f:
                f.write(cookies_file.getbuffer())
            cookies_file_path = "cookies.txt"
        else:
            cookies_file_path = None

        # Set up logging
        logger = setup_logging('log-pinterest-downloader.log')

        # Start downloading
        with st.spinner("Downloading..."):
            download_media(
                path=path, 
                dir=dir, 
                max_threads=max_threads, 
                cut_length=cut_length, 
                board_timestamp=board_timestamp,
                log_timestamp=log_timestamp, 
                force=force, 
                re_scrape=re_scrape, 
                update_all=update_all, 
                exclude_section=exclude_section,
                image_only=image_only, 
                video_only=video_only, 
                https_proxy=https_proxy, 
                http_proxy=http_proxy, 
                cookies_file=cookies_file_path
            )

        st.success("Download Completed!")

    # Display log file
    if os.path.exists("log-pinterest-downloader.log"):
        with open("log-pinterest-downloader.log", "r") as log:
            log_content = log.read()
            st.text_area("Log", log_content, height=300)

if __name__ == '__main__':
    main()
