# This test.py file
# confirm
import random
import faker
import pandas as pd
import re

# Initialize Faker for synthetic data generation
fake = faker.Faker()

# Constants
TOTAL_RECORDS = 100000
SUBJECT_CODES = ['CS1010', 'CS1020', 'CS1030', 'CS1040', 'CS1050']
GROUPS = ['B1', 'B2', 'B3', 'B4', 'B5']
COHORT_ID = 'MU2024GRP'

# Function to create a unique identifier for each student
def create_student_identifier(index):
    return f'{COHORT_ID}{index:03}'

# Generate the dataset
records = []
for i in range(1, TOTAL_RECORDS + 1):
    name = fake.name()
    student_id = create_student_identifier(i)
    subjects = random.sample(SUBJECT_CODES, random.randint(3, 5))
    email_address = f'{student_id.lower()}@universitydomain.edu'
    group = random.choice(GROUPS)
    
    records.append([name, student_id, ', '.join(subjects), email_address, group])

# Convert to DataFrame and save as CSV
df = pd.DataFrame(records, columns=['Student Name', 'Student ID', 'Subjects', 'Email', 'Group'])
df.to_csv('student_data.csv', index=False)

# Load the dataset from the CSV
df = pd.read_csv('student_data.csv')

# Define regular expressions for pattern matching
patterns = {
    'Student ID': r'(MU2024GRP\d{3})',
    'Email': r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})',
    'Subjects': r'(CS\d{4})',
    'Group': r'(B\d)'
}

# Function to extract and count regex matches
def extract_and_count_matches(column_name, pattern):
    column_content = df[column_name].astype(str)
    extracted_values = column_content.str.extract(pattern)
    match_count = extracted_values[0].value_counts()
    return match_count

# Extract and count matches for each pattern
match_counts = {}
for column, pattern in patterns.items():
    match_counts[column] = extract_and_count_matches(column, pattern)

# Display the extracted groups and their counts
for column, counts in match_counts.items():
    print(f'\nMatch counts for {column}:')
    print(counts)
