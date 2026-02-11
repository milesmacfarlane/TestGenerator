"""
Basic tests for Test Generator
Run with: python -m pytest tests/
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from statistics_calculator import StatisticsCalculator
from data_manager import DataManager
from question_models import Question, QuestionType, AnswerFormat


def test_statistics_calculator_mean():
    """Test mean calculation"""
    calc = StatisticsCalculator()
    data = [1, 2, 3, 4, 5]
    assert calc.calculate_mean(data) == 3.0


def test_statistics_calculator_median():
    """Test median calculation"""
    calc = StatisticsCalculator()
    
    # Odd number of values
    assert calc.calculate_median([1, 2, 3, 4, 5]) == 3.0
    
    # Even number of values
    assert calc.calculate_median([1, 2, 3, 4]) == 2.5


def test_statistics_calculator_mode():
    """Test mode calculation"""
    calc = StatisticsCalculator()
    
    # Single mode
    assert calc.calculate_mode([1, 2, 2, 3]) == "2"
    
    # Multiple modes
    result = calc.calculate_mode([1, 1, 2, 2, 3])
    assert "1" in result and "2" in result
    
    # No mode
    assert calc.calculate_mode([1, 2, 3, 4]) == "no mode"


def test_statistics_calculator_trimmed_mean():
    """Test trimmed mean calculation"""
    calc = StatisticsCalculator()
    data = [1, 2, 3, 4, 5, 100]  # 100 is outlier
    
    # Remove 1 from each end
    trimmed = calc.calculate_trimmed_mean(data, num_to_remove=1)
    
    # Should be mean of [2, 3, 4, 5] = 3.5
    assert trimmed == 3.5


def test_statistics_calculator_percentile_rank():
    """Test percentile rank calculation"""
    calc = StatisticsCalculator()
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Value 5: 4 values below it, 10 total
    # PR = (4/10) * 100 = 40
    assert calc.percentile_rank(5, data) == 40.0


def test_data_manager_fallback():
    """Test data manager with fallback data"""
    dm = DataManager("nonexistent.xlsx")
    
    # Should create fallback data
    name = dm.get_name()
    assert 'full_name' in name
    assert 'first_name' in name
    
    place = dm.get_place_cdn()
    assert 'city' in place
    assert 'province' in place


def test_question_model_creation():
    """Test creating a Question object"""
    q = Question(
        id="TEST_001",
        unit="Statistics",
        outcomes=["12E5.S.1"],
        question_type=QuestionType.CALCULATION,
        difficulty=2,
        total_marks=2,
        mark_breakdown={"process": 1.0, "answer": 1.0},
        context="Test context",
        question_text="Test question",
        given_data={"test": "data"},
        answer=42,
        answer_format=AnswerFormat.NUMERIC
    )
    
    assert q.id == "TEST_001"
    assert q.unit == "Statistics"
    assert q.total_marks == 2
    assert q.get_marks_display() == "[2 marks]"


def test_question_auto_id():
    """Test automatic ID generation"""
    q = Question(
        id="",  # Empty ID should auto-generate
        unit="Statistics",
        outcomes=["12E5.S.1"],
        question_type=QuestionType.CALCULATION,
        difficulty=1,
        total_marks=1,
        mark_breakdown={"answer": 1.0},
        context="Test",
        question_text="Test",
        given_data={},
        answer=0
    )
    
    assert q.id.startswith("STAT_")
    assert len(q.id) == 10  # STAT_XXXXX


if __name__ == "__main__":
    # Run tests manually
    print("Running tests...")
    
    test_statistics_calculator_mean()
    print("✓ Mean test passed")
    
    test_statistics_calculator_median()
    print("✓ Median test passed")
    
    test_statistics_calculator_mode()
    print("✓ Mode test passed")
    
    test_statistics_calculator_trimmed_mean()
    print("✓ Trimmed mean test passed")
    
    test_statistics_calculator_percentile_rank()
    print("✓ Percentile rank test passed")
    
    test_data_manager_fallback()
    print("✓ Data manager test passed")
    
    test_question_model_creation()
    print("✓ Question model test passed")
    
    test_question_auto_id()
    print("✓ Auto ID test passed")
    
    print("\n✅ All tests passed!")
