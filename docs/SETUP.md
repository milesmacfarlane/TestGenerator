# Setup and Deployment Guide

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/milesmacfarlane/TestGenerator.git
   cd TestGenerator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Add your lookup data**
   ```bash
   # Copy your Excel file to the data directory
   cp /path/to/WorksheetMergeMasterSourceFile.xlsx data/
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - Automatically opens at `http://localhost:8501`
   - Or manually navigate to that URL

### Verify Installation

Run this test to ensure everything works:

```bash
# Test the statistics calculator
python -c "import sys; sys.path.insert(0, 'src'); from statistics_calculator import StatisticsCalculator; print('✓ Calculator OK')"

# Test the data manager  
python -c "import sys; sys.path.insert(0, 'src'); from data_manager import DataManager; dm = DataManager('data/WorksheetMergeMasterSourceFile.xlsx'); print('✓ Data Manager OK')"
```

## Project Structure Explained

```
TestGenerator/
│
├── app.py                     # Main entry point - run this
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── QUICKSTART.md             # 5-minute start guide
├── LICENSE                    # MIT license
├── .gitignore                # Git exclusions
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── data_manager.py       # Interfaces with Excel lookup tables
│   ├── statistics_calculator.py  # Core math functions
│   ├── question_models.py    # Data structures (Question, Assessment)
│   │
│   └── generators/           # Question generators
│       ├── __init__.py
│       ├── mean_median_mode.py   # MMM questions
│       └── trimmed_mean.py       # Trimmed mean questions
│
├── data/                     # Lookup tables
│   ├── README.md            # Data format documentation
│   └── WorksheetMergeMasterSourceFile.xlsx  # Your data (optional)
│
├── docs/                     # Documentation (future)
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
│
└── tests/                    # Unit tests (future)
    └── test_generators.py
```

## Development Workflow

### Making Changes

1. Create a new branch
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Make your changes

3. Test locally
   ```bash
   streamlit run app.py
   ```

4. Commit and push
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/my-new-feature
   ```

5. Create Pull Request on GitHub

### Adding a New Question Generator

1. Create new file in `src/generators/`
   ```python
   # src/generators/my_new_generator.py
   
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent))
   
   from question_models import Question
   from statistics_calculator import StatisticsCalculator
   from data_manager import DataManager
   
   class MyNewGenerator:
       def __init__(self, data_manager):
           self.data = data_manager
           self.calc = StatisticsCalculator()
       
       def generate_question(self, difficulty=2):
           # Your generator logic here
           pass
   ```

2. Import in `app.py`
   ```python
   from generators.my_new_generator import MyNewGenerator
   ```

3. Add slider control in sidebar
   ```python
   num_my_questions = st.slider("My Question Type", 0, 10, 0)
   ```

4. Add to generation logic
   ```python
   my_gen = MyNewGenerator(data_manager)
   for i in range(num_my_questions):
       q = my_gen.generate_question(difficulty=diff)
       questions.append(q)
   ```

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)

**Free hosting for Streamlit apps**

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository: `milesmacfarlane/TestGenerator`
5. Set main file: `app.py`
6. Deploy!

**Notes:**
- Free tier: Public apps only
- Data file: Upload via app interface (not in repo)
- URL: `https://yourusername-testgenerator.streamlit.app`

### Option 2: Local Network Deployment

**Run on school server for teacher access**

1. Install on server
2. Run with network access:
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```
3. Access from other computers: `http://server-ip:8501`

### Option 3: Docker Container

**For containerized deployment**

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t testgenerator .
docker run -p 8501:8501 testgenerator
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'src'"
**Solution:** Run from project root directory
```bash
cd TestGenerator
streamlit run app.py
```

### "FileNotFoundError: WorksheetMergeMasterSourceFile.xlsx"
**Solution:** This is expected - system uses fallback data. To use your data:
- Place Excel file in `data/` directory, OR
- Upload via app interface

### Port 8501 already in use
**Solution:** Use different port
```bash
streamlit run app.py --server.port 8502
```

### Questions have repeated names/cities
**Solution:** You're using fallback data (only 5 examples each). Add your Excel file for variety.

### Changes not appearing
**Solution:** Streamlit caches. Click "Rerun" or use:
```bash
streamlit run app.py --server.runOnSave true
```

## Performance Tips

### Large Lookup Tables
If your Excel file is large (>1000 rows per sheet):
- System loads entire file into memory
- First load may take 2-3 seconds
- Subsequent questions are fast

### Generating Many Questions
- 10 questions: <1 second
- 50 questions: 1-2 seconds
- 100 questions: 3-5 seconds

## Security Considerations

### Data Privacy
- Don't commit sensitive data to GitHub
- Use `.gitignore` to exclude Excel files
- Upload data via app interface instead

### Deployment
- Streamlit Cloud: Apps are public by default
- Local network: Secure your server
- Docker: Use environment variables for secrets

## Getting Help

### Issues
Report bugs: [GitHub Issues](https://github.com/milesmacfarlane/TestGenerator/issues)

### Questions
- Check [QUICKSTART.md](QUICKSTART.md)
- Check [README.md](README.md)
- Open a GitHub Issue

### Contributing
See contributing guidelines in [README.md](README.md)

## Version History

**v0.1.0** (Current)
- Initial release
- Mean/Median/Mode generator
- Trimmed Mean generator
- Basic Streamlit interface

**Planned v0.2.0**
- Weighted Mean generator
- Percentile Rank generator
- PDF export

**Planned v0.3.0**
- Multiple choice questions
- DOCX export
- Question bank management
