import re

import re

# Your SQL table definitions as a single string
sql_definitions = """
"pre_ranking_filter_log" filter_key varchar(50), "timestamp" date, task int foreign key, primary key;
"pre_ranking_filter_key_mapping" filter_key_zh varchar(50), filter_key varchar(50), filter_key_en varchar(50),
filter_stage varchar(50), filter_stage_zh varchar(50), filter_type_zh varchar(50), filter_type_en varchar(50) foreign key, primary key;
"predicted_metric_log" "date" date, task int, avg_ctr float, avg_cvr float, avg_unit_price float, avg_ecpm float foreign key, primary key;
"real_metric_log" "date" date, task int, avg_ctr float, avg_cvr float, avg_unit_price float, avg_ecpm float foreign key, primary key;
"request_log" "date" date, request_id varchar(20), task int foreign key, primary key request_id varchar(20);
"""

# Use regular expressions to add double quotes around column names
pattern = r'(,[^,]+)(?=(?:,[^,]+)*$)'
modified_sql_definitions = re.sub(pattern, r'"\1"', sql_definitions)# Print the modified SQL definitions
print(modified_sql_definitions)
