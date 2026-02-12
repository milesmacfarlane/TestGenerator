"""
EMA40S Statistics Assessment Generator
Streamlit Application - WITH QUESTION LOCKING & RE-ROLL
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
from question_models import Assessment

# Import generators
from generators.mean_median_mode import MeanMedianModeGenerator
from generators.trimmed_mean import TrimmedMeanGenerator

# Try to import new generators
try:
    from generators.weighted_mean import WeightedMeanGenerator
    HAS_WEIGHTED = True
except ImportError:
    HAS_WEIGHTED = False

try:
    from generators.percentile_rank import PercentileRankGenerator
    HAS_PERCENTILE = True
except ImportError:
    HAS_PERCENTILE = False

# Try to import PDF builder
try:
    from pdf_builder import TestPDFBuilder
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

# Page config
st.set_page_config(
    page_title="EMA40S Test Generator",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'test' not in st.session_state:
    st.session_state.test = None
if 'locked_questions' not in st.session_state:
    st.session_state.locked_questions = set()
if 'generation_params' not in st.session_state:
    st.session_state.generation_params = None

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
            temp_path = "temp_lookup_tables.xlsx"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.read())
            data_manager = DataManager(temp_path)
            st.success("✓ Custom data loaded")
        else:
            data_manager = DataManager("data/WorksheetMergeMasterSourceFile.xlsx")
            st.info("Using default data from repository")
    else:
        data_manager = DataManager("data/WorksheetMergeMasterSourceFile.xlsx")
    
    st.markdown("---")
    
    # Learning Outcomes
    st.subheader("Learning Outcomes")
    outcome_s1 = st.checkbox("12E5.S.1 - Measures of Central Tendency", value=True)
    outcome_s2 = st.checkbox("12E5.S.2 - Percentile Rank", value=HAS_PERCENTILE, disabled=not HAS_PERCENTILE)
    if not HAS_PERCENTILE:
        st.caption("⚠️ Percentile Rank coming soon")
    
    selected_outcomes = []
    if outcome_s1:
        selected_outcomes.append("12E5.S.1")
    if outcome_s2 and HAS_PERCENTILE:
        selected_outcomes.append("12E5.S.2")
    
    st.markdown("---")
    
    # Question Types
    st.subheader("Question Mix")
    
    num_mmm = st.slider(
        "Mean/Median/Mode",
        min_value=0,
        max_value=10,
        value=2,
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
        value=2 if HAS_WEIGHTED else 0,
        disabled=not HAS_WEIGHTED,
        help="Course grades or frequency data (2 marks each)" if HAS_WEIGHTED else "Coming soon"
    )
    
    num_percentile_calc = st.slider(
        "Percentile Rank (Calculation)",
        min_value=0,
        max_value=5,
        value=2 if HAS_PERCENTILE else 0,
        disabled=not HAS_PERCENTILE,
        help="Calculate PR using formula (2 marks each)" if HAS_PERCENTILE else "Coming soon"
    )
    
    num_percentile_concept = st.slider(
        "Percentile Rank (Conceptual)",
        min_value=0,
        max_value=3,
        value=1 if HAS_PERCENTILE else 0,
        disabled=not HAS_PERCENTILE,
        help="Understanding percentile vs percent (1 mark each)" if HAS_PERCENTILE else "Coming soon"
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
    else:
        seed_value = random.randint(1, 999999)


def generate_questions(data_manager, difficulty_range, num_mmm, num_trimmed, 
                       num_weighted, num_percentile_calc, num_percentile_concept):
    """Generate all questions based on parameters"""
    
    # Set seed
    random.seed(seed_value)
    
    # Initialize available generators
    mmm_gen = MeanMedianModeGenerator(data_manager)
    trimmed_gen = TrimmedMeanGenerator(data_manager)
    
    if HAS_WEIGHTED:
        weighted_gen = WeightedMeanGenerator(data_manager)
    
    if HAS_PERCENTILE:
        percentile_gen = PercentileRankGenerator(data_manager)
    
    # Generate questions
    questions = []
    
    # Mean/Median/Mode
    for i in range(num_mmm):
        diff = random.choice(difficulty_range)
        marks = random.choice([1, 2])
        q = mmm_gen.generate_question(difficulty=diff, marks=marks)
        questions.append(q)
    
    # Trimmed Mean
    for i in range(num_trimmed):
        diff = random.choice(difficulty_range)
        q = trimmed_gen.generate_question(difficulty=diff, marks=2)
        questions.append(q)
    
    # Weighted Mean (if available)
    if HAS_WEIGHTED:
        for i in range(num_weighted):
            diff = random.choice(difficulty_range)
            qtype = random.choice(["percentage", "frequency"])
            q = weighted_gen.generate_question(difficulty=diff, question_type=qtype)
            questions.append(q)
    
    # Percentile Rank (if available)
    if HAS_PERCENTILE:
        for i in range(num_percentile_calc):
            diff = random.choice(difficulty_range)
            q = percentile_gen.generate_question(difficulty=diff, question_type="calculation")
            questions.append(q)
        
        for i in range(num_percentile_concept):
            diff = random.choice([1, 2])
            q = percentile_gen.generate_question(difficulty=diff, question_type="conceptual")
            questions.append(q)
    
    # Shuffle questions
    random.shuffle(questions)
    
    return questions


# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Generate Test")
    
    # Generate new test button
    if st.button("🎲 Generate New Test", type="primary", use_container_width=True):
        if not selected_outcomes:
            st.error("Please select at least one learning outcome")
        elif (num_mmm + num_trimmed + num_weighted + num_percentile_calc + num_percentile_concept) == 0:
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
                
                # Save generation parameters for re-rolling
                st.session_state.generation_params = {
                    'difficulty_range': difficulty_range,
                    'num_mmm': num_mmm,
                    'num_trimmed': num_trimmed,
                    'num_weighted': num_weighted,
                    'num_percentile_calc': num_percentile_calc,
                    'num_percentile_concept': num_percentile_concept
                }
                
                # Generate questions
                questions = generate_questions(
                    data_manager, difficulty_range, num_mmm, num_trimmed,
                    num_weighted, num_percentile_calc, num_percentile_concept
                )
                
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
                st.session_state.locked_questions = set()  # Reset locks
                st.success(f"✓ Generated test with {len(questions)} questions!")
                st.rerun()
    
    # Re-roll unlocked questions button
    if st.session_state.test and st.session_state.generation_params:
        num_locked = len(st.session_state.locked_questions)
        num_unlocked = len(st.session_state.test.questions) - num_locked
        
        if num_unlocked > 0:
            if st.button(f"🔄 Re-roll {num_unlocked} Unlocked Question{'s' if num_unlocked != 1 else ''}", 
                        use_container_width=True):
                with st.spinner(f"Re-rolling {num_unlocked} questions..."):
                    # Get locked questions
                    locked_questions = [q for i, q in enumerate(st.session_state.test.questions) 
                                       if i in st.session_state.locked_questions]
                    
                    # Calculate how many new questions we need
                    total_needed = len(st.session_state.test.questions)
                    num_to_generate = total_needed - len(locked_questions)
                    
                    # Generate new questions
                    params = st.session_state.generation_params
                    
                    # Generate MORE questions than needed so we can shuffle and pick
                    all_new_questions = generate_questions(
                        data_manager,
                        params['difficulty_range'],
                        params['num_mmm'],
                        params['num_trimmed'],
                        params['num_weighted'],
                        params['num_percentile_calc'],
                        params['num_percentile_concept']
                    )
                    
                    # Pick the number we need
                    new_questions = all_new_questions[:num_to_generate]
                    
                    # Combine locked and new questions
                    all_questions = locked_questions + new_questions
                    
                    # Shuffle everything
                    random.shuffle(all_questions)
                    
                    # Update test
                    st.session_state.test.questions = all_questions
                    
                    # Reset locked indices (questions moved)
                    st.session_state.locked_questions = set()
                    
                    st.success(f"✓ Re-rolled {num_to_generate} questions!")
                    st.rerun()
    
    # Display test
    if st.session_state.test:
        test = st.session_state.test
        
        st.markdown("---")
        st.subheader("Test Preview")
        
        # Show lock/unlock controls
        if len(test.questions) > 0:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"""
**Test Information:**
- Version: {test.version_id}
- Questions: {len(test.questions)} ({len(st.session_state.locked_questions)} 🔒 locked)
- Total Marks: {test.total_marks}
- Estimated Time: {test.estimated_time_minutes} minutes
                """)
            with col_b:
                if st.button("🔓 Unlock All"):
                    st.session_state.locked_questions = set()
                    st.rerun()
        
        st.markdown("---")
        
        # Display questions with lock checkboxes
        for i, q in enumerate(test.questions, 1):
            # Lock checkbox in the expander header
            col_lock, col_question = st.columns([0.5, 9.5])
            
            with col_lock:
                is_locked = st.checkbox(
                    "🔒",
                    key=f"lock_{i}",
                    value=(i-1) in st.session_state.locked_questions,
                    help="Lock this question (won't change when re-rolling)"
                )
                
                # Update locked set
                if is_locked:
                    st.session_state.locked_questions.add(i-1)
                else:
                    st.session_state.locked_questions.discard(i-1)
            
            with col_question:
                lock_icon = "🔒 " if is_locked else ""
                with st.expander(f"{lock_icon}**Question {i}** {q.get_marks_display()}" + 
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
        
        # Show lock status
        num_locked = len(st.session_state.locked_questions)
        st.metric("🔒 Locked", num_locked)
        
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
        
        # PDF Export
        if HAS_PDF:
            st.markdown("**📄 PDF Export**")
            
            col_student, col_teacher = st.columns(2)
            
            with col_student:
                if st.button("📥 Student Copy", use_container_width=True):
                    with st.spinner("Generating PDF..."):
                        try:
                            pdf_builder = TestPDFBuilder()
                            pdf_bytes = pdf_builder.build_student_test(test)
                            
                            filename = f"EMA40S_Test_{test.version_id}_Student.pdf"
                            
                            st.download_button(
                                label="⬇️ Download Student PDF",
                                data=pdf_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                            st.success("✓ PDF ready!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            with col_teacher:
                if st.button("📥 Teacher Copy", use_container_width=True):
                    with st.spinner("Generating PDF..."):
                        try:
                            pdf_builder = TestPDFBuilder()
                            pdf_bytes = pdf_builder.build_teacher_test(test)
                            
                            filename = f"EMA40S_Test_{test.version_id}_Teacher.pdf"
                            
                            st.download_button(
                                label="⬇️ Download Teacher PDF",
                                data=pdf_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                            st.success("✓ PDF ready!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("📄 PDF export: Upload pdf_builder.py to enable")
        
        st.markdown("---")
        
        # Show version for reproducibility
        st.caption(f"Version: {test.version_id}")
        if use_seed:
            st.caption(f"Seed: {seed_value}")
        
        # Show feature status
        st.markdown("---")
        st.caption("**Features:**")
        st.caption(f"✅ Mean/Median/Mode")
        st.caption(f"✅ Trimmed Mean")
        st.caption(f"{'✅' if HAS_WEIGHTED else '⏳'} Weighted Mean")
        st.caption(f"{'✅' if HAS_PERCENTILE else '⏳'} Percentile Rank")
        st.caption(f"{'✅' if HAS_PDF else '⏳'} PDF Export")
        st.caption(f"✅ Question Locking 🆕")
    
    else:
        st.info("Generate a test to see statistics")
        
        # Help text about locking feature
        st.markdown("---")
        st.subheader("💡 Question Locking")
        st.markdown("""
**Lock questions you like, re-roll the rest!**

1. Generate a test
2. Check 🔒 on questions you want to keep
3. Click "🔄 Re-roll" to regenerate unlocked questions
4. Perfect your test!
        """)

st.markdown("---")
version = "0.3.0" if HAS_PDF else ("0.2.0" if (HAS_WEIGHTED and HAS_PERCENTILE) else "0.1.0")
st.caption(f"EMA40S Test Generator v{version} | Manitoba Education")
st.caption("🌐 [GitHub](https://github.com/milesmacfarlane/TestGenerator) | 📧 Feedback")
