# Student Data Cleaning — n8n ETL

Reads a student enrollment CSV, cleans the data, removes
duplicate emails, filters records and exports a clean CSV.

## Cleaning
- Trim whitespace.
- Standardise names, cities and course names.
- Lowercase emails and payment values.
- Identify duplicates using the cleaned Email field.

## Filter rule
Keep students whose Fee_Paid is "yes" AND whose email
passes a basic email-format check.

Missing phone and city values are retained.
Incomplete email addresses are excluded, not guessed.

## Results
- Input: 50 students
- Duplicates removed: 0
- Filtered out: 31
- Output: 19 students

## Workflow
Manual Trigger → Read File → Extract CSV → Code →
Remove Duplicates → Filter → Convert to CSV → Write File
