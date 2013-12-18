from bs4 import BeautifulSoup
import os
import glob
import json
import csv

dir_name = "/Users/ramnathkrishnamurthy/Dropbox/Pingpong/LDMI/Christmas Campaign/User List Htmls/Cognizant Christians/"
output_dir_name = "/Users/ramnathkrishnamurthy/Dropbox/Pingpong/LDMI/Christmas Campaign/User List/"
#for files in os.listdir(dir_name):
#  if files.endswith(".htm"):
#    print files
for page in glob.glob(dir_name + "*.htm"):
  page_name = os.path.basename(page)
  print page_name
  soup = BeautifulSoup(open(page))
  container_tag = soup.select("div._4_yl > div")
  with open(output_dir_name + os.path.splitext(page_name)[0] + ".csv", "wb") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=",")
    csvwriter.writerow(["Name", "fbuid"])
    for tag in container_tag:
      if tag.has_attr("data-bt"):
        data = tag.get("data-bt")
        data = json.loads(data)
        name_tag = tag.select("div._zs > a")[0]
        print name_tag.string, data.get("id") 
        csvwriter.writerow([name_tag.string, data.get("id")])
  
