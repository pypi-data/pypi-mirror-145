#!D:\Projects\venv\cda_downloader\Scripts\python.exe
import argparse

from cda_downloader import CDA


a = CDA(multithreading=0, use_api=True, progress_bar=True)
print(a.get_video_urls("https://www.cda.pl/video/13617843"))

parser = argparse.ArgumentParser()
parser.add_argument("url", help="Provide valid video url", type=str)
args = parser.parse_args()

a = CDA(multithreading=0, use_api=True, progress_bar=True)
print(a.get_video_urls(args.url))
