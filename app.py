"""
EMA40S Statistics Assessment Generator
Streamlit Application
"""

import streamlit as st
import sys
from pathlib import Path
import random
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import our modules
from data_manager import DataManager
from generators.mean_median_mode import MeanMedianModeGenerator
from generators.trimmed_mean import TrimmedMeanGenerator
from question_models import Assessment

# Page config
st.set_page_config(
    page_title="EMA40S Test Generator",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'test' not in st.session_state:
    st.session_state.test = None

# Title
st.title("📊 EMA40S Test Generator")
st.markdown("**Grade 12 Essential Mathematics - Statistics Unit**")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Test Configuration")
    
    # Data source
    st.subheader("Data Source")
    use_custom_data = st.checkbox("Use custom lookup tables", value=False)
    
    if use_custom_data:
        uploaded_file = st.file_uploader(
            "Upload WorksheetMergeMasterSourceFile.xlsx",
            type=['xlsx']
        )
        if uploaded_file:
            # Save temporarily
            temp_path = "temp_lookup_tables.xlsx"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.read())
            data_manager = DataManager(temp_path)
            st.success("✓ Custom data loaded")
        else:
            data_manager = DataManager("data/WorksheetMergeMasterSourceFile.xlsx")
            st.info("Using fallback data")
    else:
        data_manager = DataManager("data/WorksheetMergeMasterSourceFile.xlsx")
    
    st.markdown("---")
    
    # Learning Outcomes
    st.subheader("Learning Outcomes")
    outcome_s1 = st.checkbox("12E5.S.1 - Measures of Central Tendency", value=True)
    outcome_s2 = st.checkbox("12E5.S.2 - Percentile Rank", value=False, disabled=True)
    st.caption("⚠️ Percentile Rank coming soon")
    
    selected_outcomes = []
    if outcome_s1:
        selected_outcomes.append("12E5.S.1")
    if outcome_s2:
        selected_outcomes.append("12E5.S.2")
    
    st.markdown("---")
    
    # Question Types
    st.subheader("Question Mix")
    
    num_mmm = st.slider(
        "Mean/Median/Mode",
        min_value=0,
        max_value=10,
        value=3,
        help="Basic calculations (1-2 marks each)"
    )
    
    num_trimmed = st.slider(
        "Trimmed Mean",
        min_value=0,
        max_value=5,
        value=2,
        help="Identify outliers and calculate (2 marks each)"
    )
    
    num_weighted = st.slider(
        "Weighted Mean",
        min_value=0,
        max_value=5,
        value=0,
        disabled=True,
        help="Coming soon"
    )
    
    num_percentile = st.slider(
        "Percentile Rank",
        min_value=0,
        max_value=5,
        value=0,
        disabled=True,
        help="Coming soon"
    )
    
    st.markdown("---")
    
    # Difficulty
    st.subheader("Difficulty Level")
    difficulty_mode = st.select_slider(
        "Select difficulty",
        options=["Easy (Level 1-2)", "Mixed (Level 1-3)", "Hard (Level 3-5)"],
        value="Mixed (Level 1-3)"
    )
    
    st.markdown("---")
    
    # Options
    st.subheader("Options")
    include_answer_key = st.checkbox("Include Answer Key", value=True)
    include_work_space = st.checkbox("Include Work Space", value=True)
    show_outcomes = st.checkbox("Show Learning Outcomes", value=False)
    
    st.markdown("---")
    
    # Randomization
    st.subheader("Randomization")
    use_seed = st.checkbox("Use custom seed")
    if use_seed:
        seed_value = st.number_input("Seed", value=12345, min_value=1)
        random.seed(seed_value)
    else:
        seed_value = random.randint(1, 999999)
        random.seed(seed_value)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Generate Test")
    
    if st.button("🎲 Generate New Test", type="primary", use_container_width=True):
        if not selected_outcomes:
            st.error("Please select at least one learning outcome")
        elif num_mmm + num_trimmed == 0:
            st.error("Please select at least one question type")
        else:
            with st.spinner("Generating your test..."):
                # Parse difficulty
                if "Easy" in difficulty_mode:
                    difficulty_range = [1, 2]
                elif "Mixed" in difficulty_mode:
                    difficulty_range = [1, 2, 3]
                else:
                    difficulty_range = [3, 4, 5]
                
                # Initialize generators
                mmm_gen = MeanMedianModeGenerator(data_manager)
                trimmed_gen = TrimmedMeanGenerator(data_manager)
                
                # Generate questions
                questions = []
                
                for i in range(num_mmm):
                    diff = random.choice(difficulty_range)
                    marks = random.choice([1, 2])
                    q = mmm_gen.generate_question(difficulty=diff, marks=marks)
                    questions.append(q)
                
                for i in range(num_trimmed):
                    diff = random.choice(difficulty_range)
                    q = trimmed_gen.generate_question(difficulty=diff, marks=2)
                    questions.append(q)
                
                random.shuffle(questions)
                
                # Create assessment
                version_id = datetime.now().strftime("%Y%m%d") + f"-{seed_value}"
                
                test = Assessment(
                    title="Statistics Unit Test",
                    unit="Statistics",
                    version_id=version_id,
                    questions=questions,
                    date_generated=datetime.now().strftime("%Y-%m-%d"),
                    include_answer_key=include_answer_key,
                    include_work_space=include_work_space,
                    show_outcomes=show_outcomes
                )
                
                st.session_state.test = test
                st.success(f"✓ Generated test with {len(questions)} questions!")
                st.rerun()
    
    # Display test
    if st.session_state.test:
        test = st.session_state.test
        
        st.markdown("---")
        st.subheader("Test Preview")
        
        st.markdown(f"""
**Test Information:**
- Version: {test.version_id}
- Questions: {len(test.questions)}
- Total Marks: {test.total_marks}
- Estimated Time: {test.estimated_time_minutes} minutes
        """)
        
        st.markdown("---")
        
        for i, q in enumerate(test.questions, 1):
            with st.expander(f"**Question {i}** {q.get_marks_display()}" + 
                           (f" - {q.get_outcomes_display()}" if show_outcomes else "")):
                
                st.markdown(f"**Context:** {q.context}")
                st.markdown(f"**Question:**")
                st.text(q.question_text)
                
                if include_work_space:
                    st.markdown("*[Space for student work]*")
                
                if include_answer_key:
                    st.markdown("---")
                    st.markdown("**Answer Key:**")
                    
                    if q.parts:
                        for part in q.parts:
                            st.markdown(f"**{part.letter})** {part.answer}")
                    else:
                        st.markdown(f"**Answer:** {q.answer}")
                    
                    with st.expander("Show solution steps"):
                        for step in q.solution_steps:
                            st.text(step)

with col2:
    st.header("Statistics")
    
    if st.session_state.test:
        test = st.session_state.test
        
        st.metric("Questions", len(test.questions))
        st.metric("Total Marks", test.total_marks)
        st.metric("Est. Time", f"{test.estimated_time_minutes} min")
        
        st.markdown("---")
        
        st.subheader("Outcome Coverage")
        outcome_counts = test.get_outcome_coverage()
        for outcome, count in outcome_counts.items():
            st.text(f"{outcome}: {count}")
        
        st.markdown("---")
        
        st.subheader("Difficulty")
        diff_dist = test.get_difficulty_distribution()
        for level in sorted(diff_dist.keys()):
            st.text(f"Level {level}: {diff_dist[level]}")
        
        st.markdown("---")
        
        st.subheader("Question Types")
        type_dist = test.get_question_type_distribution()
        for qtype, count in type_dist.items():
            st.text(f"{qtype}: {count}")
        
        st.markdown("---")
        
        st.subheader("Export")
        st.info("📄 PDF/DOCX export coming soon!")
    
    else:
        st.info("Generate a test to see statistics")

st.markdown("---")
st.caption("EMA40S Test Generator v0.1 | Manitoba Education")
