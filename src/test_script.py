from receipt_processor import VPayExtractor
import re
from utils import Utils

formatted_ref_id = "202302251753069243"
clean_text = Utils.format_ref_id_time(formatted_ref_id)
print(clean_text)