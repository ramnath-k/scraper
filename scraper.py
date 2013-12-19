from bs4 import BeautifulSoup
import os
import glob
import json
import csv
import settings

input_dir_name = settings.input_dir_name
output_dir_name = settings.output_dir_name
output_file_prefix = settings.output_file_prefix

for output_file_name in ["male", "female"]:
  with open(output_dir_name + output_file_prefix + output_file_name + ".csv", "wb") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=",")
    csvwriter.writerow(["Name", "fbuid"])

for page in glob.glob(input_dir_name + "*.htm*"):
  page_name = os.path.splitext(os.path.basename(page))[0] 
  print page_name
  if page_name.endswith("female"):
    output_file_name = "female"
  else:
    output_file_name = "male"
  fp = open(page)
  soup = BeautifulSoup(fp)
  container_tag = soup.select("div._4_yl > div")
  with open(output_dir_name + output_file_prefix + output_file_name + ".csv", "ab") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=",")
    for tag in container_tag:
      if tag.has_attr("data-bt"):
        data = tag.get("data-bt")
        data = json.loads(data)
        fbuid = data.get("id")
        name_tag = tag.select("div._zs > a")[0]
        name = name_tag.contents[0]
        print name, fbuid
        csvwriter.writerow([name, fbuid])
  
  if not container_tag:
    fp = open(page)
    content = fp.read()
    search_term = "data-bt=\"&#123;&quot;id&quot;:"
    splits = content.split(search_term)
    splits = splits[1:]
    with open(output_dir_name + output_file_prefix + output_file_name + ".csv", "ab") as csvfile:
      csvwriter = csv.writer(csvfile, delimiter=",")
      for split in splits:
        pos = split.find(',')
        fbuid = split[0:pos]
        split1 = split.split('fref=browse_search\">')
        if len(split1) > 1:
          split1 = split1[1]
          pos1 = split1.find('<span')
          pos = split1.find('</a>')
          if pos1 != -1 and pos1 < pos:
            pos = pos1
          name = split1[0:pos]
          print name, fbuid
          csvwriter.writerow([name, fbuid])

