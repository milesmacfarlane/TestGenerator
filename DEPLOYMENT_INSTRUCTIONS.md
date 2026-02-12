# 🚀 Adding New Features to Your Streamlit App

## What We're Adding

### ✅ New Question Generators
1. **Weighted Mean** (2 types: percentage & frequency)
2. **Percentile Rank Calculation** (2 marks)
3. **Percentile Rank Conceptual** (1 mark)

### ✅ Lookup Data
- WorksheetMergeMasterSourceFile.xlsx (your existing data)

---

## 📋 Files to Add to GitHub

You need to add these files to your repository:

### 1. **Excel File** (Lookup Tables)
**Location:** `data/WorksheetMergeMasterSourceFile.xlsx`
**Action:** Upload via GitHub web interface

### 2. **New Generators**
**Location:** `src/generators/`
- `weighted_mean.py` (new)
- `percentile_rank.py` (new)

### 3. **Updated App**
**Location:** Root
- `app.py` (replace existing)

---

## 🌐 Step-by-Step: GitHub Web Interface

### Step 1: Add Excel File

1. Go to https://github.com/milesmacfarlane/TestGenerator
2. Click on **`data`** folder
3. Click **"Add file"** → **"Upload files"**
4. Drag `WorksheetMergeMasterSourceFile.xlsx` to the upload area
5. Commit message: "Add lookup data file"
6. Click **"Commit changes"**

### Step 2: Add Weighted Mean Generator

1. Go to https://github.com/milesmacfarlane/TestGenerator/tree/main/src/generators
2. Click **"Add file"** → **"Create new file"**
3. Name: `weighted_mean.py`
4. Paste content (I'll provide below)
5. Commit message: "Add weighted mean generator"
6. Click **"Commit changes"**

### Step 3: Add Percentile Rank Generator

1. Still in `src/generators/`
2. Click **"Add file"** → **"Create new file"**
3. Name: `percentile_rank.py`
4. Paste content (I'll provide below)
5. Commit message: "Add percentile rank generator"
6. Click **"Commit changes"**

### Step 4: Update App

1. Go to https://github.com/milesmacfarlane/TestGenerator
2. Click on **`app.py`**
3. Click the **pencil icon** (✏️) to edit
4. Replace ALL content with new version (I'll provide)
5. Commit message: "Update app with new generators"
6. Click **"Commit changes"**

---

## 📝 What Changes

### Before (v0.1):
- Mean/Median/Mode ✅
- Trimmed Mean ✅
- Total: 2 question types

### After (v0.2):
- Mean/Median/Mode ✅
- Trimmed Mean ✅
- **Weighted Mean ✅ NEW**
- **Percentile Rank (Calc) ✅ NEW**
- **Percentile Rank (Conceptual) ✅ NEW**
- Total: 5 question types

### New Features:
- ✅ Uses your Excel lookup data automatically
- ✅ 2 types of weighted mean (percentage & frequency)
- ✅ Provincial exam-aligned percentile questions
- ✅ Conceptual understanding questions
- ✅ Complete Statistics unit coverage

---

## 🎯 Testing After Deployment

### Auto-Deploy
Streamlit Cloud will automatically redeploy when you push changes (takes ~2 minutes).

### Test Checklist

1. **Visit:** https://mactestgenerator.streamlit.app/

2. **Check Data Loaded:**
   - Look for real names from your Excel file
   - Should see actual city names, jobs, etc.
   - Not just "Alex Chen, Winnipeg" anymore

3. **Test Weighted Mean:**
   - Set slider to 2-3
   - Generate test
   - Should see course grade tables OR frequency data

4. **Test Percentile Rank:**
   - Set calculation slider to 2
   - Set conceptual slider to 1
   - Generate test
   - Should see PR = (b/n) × 100 questions
   - Should see conceptual "justify why..." question

5. **Generate Full Test:**
   - MMM: 2
   - Trimmed: 2
   - Weighted: 2
   - PR Calc: 2
   - PR Concept: 1
   - Total: 9 questions, ~15-18 marks
   - Should complete Statistics unit coverage!

---

## 🐛 Troubleshooting

### If App Crashes After Update:

1. **Check Streamlit Cloud Logs:**
   - Go to https://share.streamlit.io/
   - Find your app
   - Click "Logs"
   - Look for error messages

2. **Common Issues:**
   - **Import Error:** Check file names match exactly
   - **File Not Found:** Check Excel file is in `data/` folder
   - **Syntax Error:** Check copy-paste was complete

3. **Quick Fix:**
   - Revert the commit on GitHub
   - App will roll back to working version
   - Fix the issue and try again

### If Data Isn't Loading:

Check that `WorksheetMergeMasterSourceFile.xlsx` is in the `data/` folder, not root.

**Correct:** `data/WorksheetMergeMasterSourceFile.xlsx` ✅
**Wrong:** `WorksheetMergeMasterSourceFile.xlsx` ❌

---

## 📊 Expected Output Examples

### Weighted Mean (Percentage Type)
```
Ms. Chen is calculating their final grade in Mathematics. 
The grading breakdown is shown below.

Category | Score | Weight
---------|-------|-------
Homework | 85    | 10%
Quizzes  | 72    | 20%
Midterm  | 90    | 30%
Project  | 88    | 15%
Final    | 82    | 25%

Calculate the final score using a weighted mean.

Answer: 84.15
```

### Weighted Mean (Frequency Type)
```
Mr. Park works as a server and received tips during one shift.

2 tips of $6.00
3 tips of $8.00
5 tips of $10.00
4 tips of $12.00

Calculate the mean.

Answer: $9.71
```

### Percentile Rank (Calculation)
```
Below is a list of credit scores for people applying for loans.

620, 655, 706, 722, 722, 768, 775, 778, 780, 784,
784, 800, 803, 816, 824, 824, 831, 840, 849, 852

Calculate the percentile rank for a score of 800.

Answer: 55 (or 55th percentile)
```

### Percentile Rank (Conceptual)
```
Alex must write an entrance exam. A minimum grade of 75% is required.
Last year their mark was in the 70th percentile. They were not accepted.
This year their mark is in the 80th percentile.

Justify why it cannot be determined if they will be accepted this year.

Answer: Percentile rank only shows relative position, not actual grade.
An 80th percentile score does not guarantee the minimum 75% grade.
```

---

## 🎓 Curriculum Coverage

After this update, you'll have **COMPLETE** Statistics unit coverage:

### 12E5.S.1 - Measures of Central Tendency
- ✅ Mean, Median, Mode
- ✅ Outliers & Trimmed Mean
- ✅ Weighted Mean (both types)
- ✅ Contextual problems

### 12E5.S.2 - Percentile Rank
- ✅ Calculate PR using formula
- ✅ Understand percentile vs percentage
- ✅ Apply to real scenarios

---

## 📈 Version History

**v0.1.0** (Initial)
- Mean/Median/Mode
- Trimmed Mean

**v0.2.0** (This Update) ← YOU ARE HERE
- ✅ Weighted Mean
- ✅ Percentile Rank
- ✅ Complete lookup data integration
- ✅ Complete Statistics unit

**v0.3.0** (Future)
- PDF Export
- DOCX Export
- Question bank management

---

## 🎉 Next Steps After Deployment

1. **Test thoroughly** with colleagues
2. **Share the URL** with your department
3. **Collect feedback** on question quality
4. **Track usage** (Streamlit Cloud has basic analytics)

Then we can move on to:
- Home Finance unit
- PDF/DOCX export
- Multiple choice questions
- More units!

---

## 📞 Need Help?

**If anything goes wrong:**
1. Check Streamlit Cloud logs
2. Verify files are in correct locations
3. Check GitHub commits went through

**Ready to add the files?**
I'll provide the exact content for each file next!
