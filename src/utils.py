from typing import List, Dict, Tuple, Union
import os
from datetime import datetime
import random

class Utils():
    @staticmethod
    def format_ref_id_time(ref_id: int) -> str:
        try:
            ref_id_str = str(ref_id)
            year = ref_id_str[0:4]
            month = ref_id_str[4:6]
            day = ref_id_str[6:8]
            hour = ref_id_str[8:10]
            minute = ref_id_str[10:12]

            formatted_date_time = f"{hour}:{minute} {day}/{month}/{year}"
            return formatted_date_time
        except:
            return "โปรดตรวจสอบด้วยตัวเองอีกครั้ง"

    @staticmethod
    def to_unix_timestamp(timestamp_str: str) -> int:
        """
        This function takes the input string, converts it to a datetime object using 
        the specified format, and then converts the datetime object to a Unix timestamp.
        You can use this Unix timestamp in Grafana for proper time representation.

        Args:
            timestamp_str (str): timestamp like 202304272135, 202302210940572991

        Returns:
            int: Timestamp in Unix
        """
        if not timestamp_str:
            return -1
        
        try: 
            timestamp_str = timestamp_str[:12]
            timestamp_dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M")
            unix_timestamp = int(timestamp_dt.timestamp())
            return unix_timestamp
        except ValueError:
            return -1
        
    @staticmethod
    def find_img(rand_dir: str, spec_img_path=None):
        """
        Getting an image randomly or by specific path.

        Args:
            directory (str): directory
            specific_image_path (_type_, optional): _description_. Defaults to None

        Returns:
            str: _description_
        """
        if spec_img_path:
            spec_img_name = os.path.basename(spec_img_path)
            return spec_img_path, spec_img_name
        # Search for all .jpg files in the specified directory and its subdirectories
        image_files = []
        for root, dirs, files in os.walk(rand_dir):
            for file in files:
                if file.lower().endswith('.jpg'):
                    image_files.append(os.path.join(root, file))

        # If there are no image files, return None
        if not image_files:
            return None

        # Pick a random image file from the list of image files found, and return its path
        random_image_path = random.choice(image_files)
        random_img_name = os.path.basename(random_image_path)
        return random_image_path, random_img_name
    


