# Data Directory

This directory contains lookup tables used for generating contextual variety in questions.

## Expected Files

### WorksheetMergeMasterSourceFile.xlsx

This Excel file should contain the following sheets:

**Required Sheets:**
- `Names` - Person names with titles (Mr., Ms., Dr., etc.)
- `PlacesCDN` - Canadian cities with provinces
- `Theaters` - Theater and venue names
- `Courses` - Course names
- `SummerJobs` - Summer job descriptions
- `Businesses` - Business names

**Optional Sheets:**
- `Vehicles` - Vehicle makes and models
- `Currency` - Currency information
- `Municipalities` - Municipality names

## File Format

### Names Sheet
Columns: `Code`, `FullName`, `FirstName`, `LastName`, `Title`, `Gender` (optional)

### PlacesCDN Sheet  
Columns: `City`, `Province/Territory`, `Abbr`

### Theaters Sheet
Columns: `BusinessName`

### Courses Sheet
Columns: `Course Title`

### SummerJobs Sheet
Columns: `Summer Job Descriptions`

### Businesses Sheet
Columns: `BusinessName`

## Fallback Data

If no Excel file is provided, the system uses built-in fallback data with:
- 5 sample names
- 5 Canadian cities
- 5 theaters
- 5 courses
- 5 summer jobs
- Basic business names

## Adding Your Data

1. Place your `WorksheetMergeMasterSourceFile.xlsx` file in this directory
2. Ensure it has the required sheets with proper column names
3. Restart the application

OR

Use the app interface:
1. Check "Use custom lookup tables"
2. Upload your Excel file
3. Data will be used for that session

## Data Privacy

**Note:** The `.gitignore` file is configured to exclude `WorksheetMergeMasterSourceFile.xlsx` by default if uncommented. If your file contains sensitive data (real student names, etc.), ensure it's not committed to the repository.
