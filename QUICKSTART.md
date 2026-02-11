# Quick Start Guide - EMA40S Statistics Generator

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Python Dependencies

Open a terminal/command prompt and navigate to the `ema40s_assessment` folder:

```bash
cd ema40s_assessment
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

### Step 3: Generate Your First Test

1. **In the left sidebar:**
   - Ensure "12E5.S.1 - Measures of Central Tendency" is checked ✓
   - Set "Mean/Median/Mode" slider to 3
   - Set "Trimmed Mean" slider to 2
   - Leave difficulty on "Mixed"

2. **Click the big blue button:** "🎲 Generate New Test"

3. **View your test:**
   - Click on any question to expand it
   - See the context, question, and answer key
   - Check the solution steps

4. **Right sidebar shows:**
   - Total questions and marks
   - Outcome coverage
   - Difficulty distribution

### Step 4: Try Different Configurations

**Make it easier:**
- Change difficulty to "Easy (Level 1-2)"
- Generate a new test
- Notice smaller numbers and simpler datasets

**Make it harder:**
- Change to "Hard (Level 3-5)"
- Generate again
- Notice decimals, larger numbers, or no modes

**Add your own data:**
- Check "Use custom lookup tables"
- Upload your `WorksheetMergeMasterSourceFile.xlsx`
- Your names, cities, and venues will appear in questions!

## 📊 Sample Questions Generated

### Mean/Median/Mode (Easy)
```
Ms. Smith tracked daily earnings from babysitting over 7 days. 
The values recorded were:

4, 3, 7, 2, 4, 9, 1

Calculate the mean, median, and mode.

Answer:
Mean: 4.3
Median: 4
Mode: 4
```

### Trimmed Mean (Medium)
```
The annual salaries for employees at Local Business are shown below. 
The values are:

$26,000, $29,000, $27,000, $30,000, $28,000, $15,000, $60,000

a) Calculate the arithmetic mean.
b) Identify any outliers and calculate the trimmed mean.

Answer:
a) $30,714
b) Outliers: $15,000 (low) and $60,000 (high)
   Trimmed mean: $28,000
```

## 🎯 What Works Now

✅ **Mean/Median/Mode Questions**
- Random datasets at 5 difficulty levels
- Multiple contexts (attendance, scores, earnings, tips, sales)
- Proper mode handling (no mode, single mode, multiple modes)
- 1 or 2 marks

✅ **Trimmed Mean Questions**
- Automatic outlier generation
- Two-part questions (a, b)
- Multiple contexts (salaries, times, temperatures, scores)
- 2 marks (1+1)

✅ **Smart Features**
- Varied phrasing for each question type
- Contextual data from lookup tables
- Reproducible tests with seed numbers
- Solution steps generated automatically

## 🔧 Customization Tips

### Adding New Contexts

Want questions about hockey stats? Book sales? Temperature readings?

Edit `mean_median_mode_generator.py` and add to `CONTEXT_TEMPLATES`:

```python
{
    "id": "hockey_goals",
    "template": "{name} tracked goals scored by {city} hockey team over {period} games.",
    "uses": ["name", "city", "period"]
}
```

### Adjusting Difficulty

Want more challenging datasets?

Edit the `_generate_dataset()` method in any generator:
- Change value ranges
- Adjust dataset sizes
- Add more decimals
- Include negative numbers

## 📝 Next Steps

### Ready for More?

**Immediate additions needed:**
- Weighted Mean generator
- Percentile Rank generator
- PDF export
- DOCX export

**Want to contribute contexts?**
Share your ideas for:
- Sports statistics scenarios
- Business/retail contexts
- Science experiment data
- Weather/environmental data

## ❓ Common Questions

**Q: Can I use this without the lookup table file?**
A: Yes! The system has built-in fallback data. Your tests will work, just with repeated names/cities.

**Q: How do I get the same test again?**
A: Use a custom seed! Check "Use custom seed", enter a number, generate. Same seed = same test.

**Q: Can students see the answer key?**
A: No, currently it's in the preview only. When we add PDF export, you'll be able to create separate student and teacher versions.

**Q: Does this match provincial exam format?**
A: Yes! Mark allocations and question structures match the 2017-2018 provincial exams and student booklets.

**Q: Can I edit the generated questions?**
A: Not yet in the app, but once we add DOCX export, you can open in Word and edit freely.

## 🐛 Troubleshooting

**"ModuleNotFoundError"**
- Run: `pip install -r requirements.txt`

**"Address already in use"**
- Another Streamlit app is running
- Close it, or use: `streamlit run app.py --server.port 8502`

**Questions look weird/repetitive**
- You're using fallback data (only 5 names, cities, etc.)
- Upload your `WorksheetMergeMasterSourceFile.xlsx` for variety

**Want different number ranges?**
- This is expected! Difficulty levels control the ranges
- Level 1: 0-10
- Level 3: 10-100
- Level 5: Can include decimals

## 📧 Feedback

This is version 0.1 - a working prototype! 

**What's working well?**
**What should change?**
**What context scenarios would you like?**

Let me know and I'll prioritize development accordingly!

---

**Happy Testing! 🎉**
