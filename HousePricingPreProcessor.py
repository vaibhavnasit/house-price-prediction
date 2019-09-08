from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import regexp_replace, col, when
import logging
import sys

# Constants
read_format = "com.databricks.spark.csv"
write_format = "csv"
write_mode = "append"
lit_true = "true"
lit_blank = ""
lit_zero = 0
lit_one = 1
lit_two = 2
lit_ten = 10
character_encoding_type = "UTF-8"
escape_character = '"'
regex_special_char = "\$|,"
col_price = 'price'
col_review_scores_rating = 'review_scores_rating'
col_last_scraped = 'last_scraped'


# Function to create a SparkContext
def __init__():
	sc = SparkContext("local", "EuroWings-Digital App")
	print("SparkContext is created!!")
	return sc

# Function to create a SQLContext	
def create_sql_context(sparkContext):
	sqlContext = SQLContext(sparkContext)
	print("SQLContext is created!!")
	return sqlContext

# Function to Read CSV data as specified through source file path and create a data frame
def read_csv_data(sqlContext, source_file_path):
	# Using sqlContext read CSV file and create a dataframe
	df = (sqlContext.read
	.format(read_format)
	.option("header", lit_true)
	.option("inferSchema", lit_true)
	.option("multiLine", lit_true)
	.option("escape", escape_character)
	.option("encoding", character_encoding_type)
	.load(source_file_path))

	# Current dataframe holds all 96 columns but we need to specify only those which can be used for further processing
	df = df.select('last_scraped','city','state','latitude','longitude',
		'property_type','room_type','accommodates','bathrooms','bedrooms',	
		'beds','guests_included','review_scores_rating','price')
	return df

# Function to pre-process the data	
def pre_process_data(df):
	
	# Remove blank rows 
	df = df.dropna('all')
	
	# Replace special characters like "$" or "," from column ['price']
	df = df.withColumn(col_price, regexp_replace(col(col_price), regex_special_char, lit_blank))

	# Replace NaN or null values with '0' for column['review_scores_rating'] (Assumption: People might have not added reviews for some houses) 
	df = df.withColumn(col_review_scores_rating, when(df.review_scores_rating.isNull(), lit_zero).otherwise(df.review_scores_rating))

	# Take only date part for column['last_scraped'] and avoid the Time stamp
	# This column can be used for partitioning purpose on date while writing the output.
	df = df.withColumn(col_last_scraped, df[col_last_scraped].substr(lit_one, lit_ten))

	return df

# Function to write the processed data	
def write_data(df, dest_file_path):
	# Write data in CSV format at desired location into the directory specified
	df.write.mode(write_mode).format(write_format).save(dest_file_path, header = lit_true)

if __name__ == '__main__':
	source_file_path = sys.argv[lit_one]
	dest_file_path = sys.argv[lit_two]

	print ("source_file_path:" + source_file_path)
	print ("dest_file_path:" + dest_file_path)

	# Create a SparkContext
	sc = __init__()

	# Create a SQLContext
	sqlContext = create_sql_context(sc)

	# Read CSV data based on given source file path and create a data frame
	df = read_csv_data(sqlContext, source_file_path)

	# Data Pre-processing
	df = pre_process_data(df)
	df.show()

	print(df.count())
	
	# Writing data to the destination
	write_data(df, dest_file_path)
	#print(res)