# uni-course-scraper


Crawls Rutgers University course catalog page scraping subject and course names
writes data json file in the form:
catalog : { subject: { 'courseID': ..., 'courseTitle': ... }, ... } saved as catalog.json

firestore.py sends data to firestore db
