# excel_path = '/Users/riyapalkhiwala/Downloads/DIiabetes_data_2_28_2024_with_categories.xlsx'
# df = pd.read_excel(excel_path)

# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
# df = df.where(pd.notnull(df), None)

# data_to_insert = df.to_dict('records')



# start_id = 1  

# for document in data_to_insert:
    
#     document['id'] = start_id
#     start_id += 1

#     # Split categories by newline if the category field exists and is a string
#     if 'category' in document and isinstance(document['category'], str):
#         document['category'] = document['category'].split('\n')


# result = collection.insert_many(data_to_insert)

#collection.drop()


# image_download_path = '/Users/riyapalkhiwala/Desktop/Spring2024/CS682/new/diabetes_umass_nursing/static/assets/images/link_images'
# total_images_downloaded = 0

# def get_extension_from_url(image_url):
#     if '?' in image_url:
#         image_url = image_url.split('?')[0]  # Remove query parameters
#     extension = image_url.split('/')[-1].split('.')[-1]
#     return extension

# def clean_filename(image_url):
#         # Split the filename and keep only the part before the '?'
#         filename = image_url.split('/')[-1].split('?')[0]
#         # Remove any additional extensions if present
#         parts = filename.split('.')
#         cleaned_filename = parts[0] + '.' + parts[-1]
#         return cleaned_filename


# def download_image(image_url, article_id, image_download_path):
#     # Initialize filename to None
#     filename = None

#     if image_url.startswith('data:image'):
#         match = re.search(r'base64,(.*)', image_url)
#         if match:
#             base64_data = match.group(1)
#             image_data = base64.b64decode(base64_data)
#             # Infer the extension from the MIME type in the data URL
#             extension = image_url.split(';')[0].split('/')[1]
#             filename = f"{article_id}.{extension}"
#         else:
#             print("No base64 content found in data URL.")
#             return None
#     else:
#         response = requests.get(image_url, stream=True)
#         if response.status_code == 200:
#             image_url=clean_filename(image_url)
#             extension = get_extension_from_url(image_url)
#             image_data = response.content
#             filename = f"{article_id}.{extension}"
#         else:
#             print(f"Failed to download image from {image_url}")
#             return None

#     # If a filename was set, save the image data to a file
#     if filename:
#         save_path = os.path.join(image_download_path, filename)
#         with open(save_path, 'wb') as f:
#             f.write(image_data)
#         print(f"Image saved as {filename}")
#         return filename

#     return filename


# def get_first_image_url(page_url):
#     response = requests.get(page_url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         image = soup.find('img')
#         if image and 'src' in image.attrs:
#             return image['src']
#     return None

# def update_article_image(article_id, image_filename):
#     # Update the article document in MongoDB to include the image filename
#     # result = collection.update_one({'_id': article_id}, {'$set': {'image_filename': image_filename}})
#     collection.find_one({'_id': article_id})
#     result = collection.update_one({'_id': article_id}, {'$set': {'image_filename': image_filename}})
#     # if result:
#     #     print(f"Found  documents.")


# def download_images():
#     total_images_downloaded = 0
    
#     for article in collection.find():
#         link = article.get('link')
       
#         article_id = article.get('_id')
#         print(article_id)
#         if link:
#             first_image_url = get_first_image_url(link)
#             if first_image_url:
#                 if not first_image_url.startswith(('http:', 'https:')):
#                     first_image_url = requests.compat.urljoin(link, first_image_url)
#                 image_filename = download_image(first_image_url, article_id, image_download_path)
#                 if image_filename:
#                     update_article_image(article_id, image_filename)
#                     total_images_downloaded += 1
#                     print(f"Downloaded and updated {article_id} with image {image_filename}")
#             else:
#                 update_article_image(article_id, "about-us.jpg")
#     print(f"Total images downloaded and updated in MongoDB: {total_images_downloaded}")


# def download_images_in_thread():
#     thread = threading.Thread(target=download_images)
#     thread.start()



# collection.update_many({}, {'$unset': {'article_template': ""}})





# <nav class="navbar navbar-static-top">
#           <div class="navbar-main">      
#                <div class="container">
#                     <div id="navbar" class="navbar-collapse collapse">
#                          <ul class="nav navbar-nav">
#                               {% if sub_heading_1 %}<li><a  href=#{{ sub_heading_tag_1 }}>{{sub_heading_1}}</a></li>{% endif %}
#                               {% if sub_heading_2 %}<li><a  href=#{{ sub_heading_tag_2 }}>{{sub_heading_2}}</a></li>{% endif %}
#                               {% if sub_heading_3 %}<li><a  href=#{{ sub_heading_tag_3 }}>{{sub_heading_3}}</a></li>{% endif %}
#                               {% if sub_heading_4 %}<li><a  href=#{{ sub_heading_tag_4 }}>{{sub_heading_4}}</a></li>{% endif %}
#                               {% if sub_heading_5 %}<li><a  href=#{{ sub_heading_tag_5 }}>{{sub_heading_5}}</a></li>{% endif %}
#                               {% if sub_heading_6 %}<li><a  href=#{{ sub_heading_tag_6 }}>{{sub_heading_6}}</a></li>{% endif %}
#                               {% if sub_heading_7 %}<li><a  href=#{{ sub_heading_tag_7 }}>{{sub_heading_7}}</a></li>{% endif %}
#                           </ul>
#               </div> <!-- /#navbar -->
#             </div> <!-- /.container -->     
#           </div> <!-- /.navbar-main -->
#         </nav>