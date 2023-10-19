
import scrapy
from scrapy.crawler import CrawlerProcess
import json
from datetime import datetime, timedelta, date
import re
import os
import calendar

class Full_DaySpider(scrapy.Spider):
    name = 'full_day'
    allowed_domains = ['www.awqaf.gov.ae']
    start_urls = ['https://www.awqaf.gov.ae/en/']
    file_name = "prayer_times.json"

    def days_until_end_of_month(self):
        today = datetime.now().date()
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        end_of_month = datetime(today.year, today.month, last_day_of_month).date()
        days_remaining = (end_of_month - today).days
        return days_remaining

    def convert_to_24_hours(self, prayer_time):
     if prayer_time:
        # Ensure that prayer_time is not None before applying the regular expression
        match = re.match(r'(\d+):(\d+) (AM|PM)$', prayer_time, re.IGNORECASE)

        if match:
            hour, minute, period = match.groups()
            hour = int(hour)
            minute = int(minute)

            # Handling special cases for 12 AM and 12 PM
            if period.upper() == 'AM' and hour == 12:
                hour = 0
            elif period.upper() == 'PM' and hour != 12:
                hour += 12

            # Formatting the result in 24-hour format
            time_24h = '{:02}:{:02}'.format(hour, minute)
            return time_24h
     else:
        # Handle the case when prayer_time is None or empty
        # You might want to log an error or return a default value based on your requirements
        return None



    def parse(self, response):
        # if not os.path.isfile(self.file_name):
        #     with open(self.file_name, 'w') as f:
        #         pass  # Create an empty file if it doesn't exist
        prayer_times = {}  # Dictionary to store prayer times data

        remaining_days = self.days_until_end_of_month()
        #today=date.today().day
        with open(self.file_name, 'w') as f:
            for j in range(1, remaining_days + 1):
                current_date = date.today() + timedelta(days=j)
                prayer_times[str(current_date)] = {} 
                               
                for i in range(1, 7):
                    
                    prayer_name = response.xpath("//div/div[2]/span/section[2]/div[1]/div/div[1]/div[2]/div/div[1]/ul[" + str(j) + "]/li[" + str(i) + "]/span/text()[1]").get()
                    prayer_time = response.xpath("//div/div[2]/span/section[2]/div[1]/div/div[1]/div[2]/div/div[1]/ul[" + str(j) + "]/li[" + str(i) + "]/span/text()[2]").get()
                   
                    prayer_time_24h = self.convert_to_24_hours(prayer_time)
                    # Store prayer times in the dictionary
                    prayer_times[str(current_date)][prayer_name] = prayer_time_24h

            json.dump(prayer_times,f, indent=4)
                    
                    
        try:
            # Attempt to load the JSON file to check for decoding errors
            with open(self.file_name, 'r') as file:
                loaded_data = json.load(file)
            print("\nJSON file is in correct format and can be loaded successfully.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
 



# Create a CrawlerProcess object
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    # Other Scrapy settings...
})

# Add your spider to the process
process.crawl(Full_DaySpider)

# Start the process
process.start()


