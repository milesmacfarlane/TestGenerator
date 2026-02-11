"""
Trimmed Mean Generator
Generates questions for outcome 12E5.S.1 (trimmed means)
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from question_models import Question, QuestionType, AnswerFormat, QuestionPart
from statistics_calculator import StatisticsCalculator
from data_manager import DataManager


class TrimmedMeanGenerator:
    """
    Generate trimmed mean questions
    
    Provincial Exam: 1-2 marks
    Student Booklet: Lesson 2
    """
    
    CONTEXT_TEMPLATES = [
        {
            "id": "employee_salaries",
            "template": "The annual salaries for employees at {business} are shown below.",
            "uses": ["business"],
            "unit": "dollars"
        },
        {
            "id": "product_times",
            "template": "{name} tracked the time to complete each item over {period} items.",
            "uses": ["name", "period"],
            "unit": "hours"
        },
        {
            "id": "temperature_data",
            "template": "Daily high temperatures in {city} during one week in January are shown below.",
            "uses": ["city"],
            "unit": "°C"
        },
        {
            "id": "test_scores",
            "template": "{name} recorded quiz scores for students in {course}.",
            "uses": ["name", "course"],
            "unit": "points"
        }
    ]
    
    def __init__(self, data_manager: DataManager):
        self.data = data_manager
        self.calc = StatisticsCalculator()
    
    def generate_question(self, difficulty: int = 2, marks: int = 2) -> Question:
        """Generate trimmed mean question"""
        
        # Generate dataset with outliers
        dataset = self._generate_dataset_with_outliers(difficulty)
        
        # Calculate values
        arithmetic_mean = self.calc.calculate_mean(dataset)
        sorted_data = sorted(dataset)
        
        outlier_low = sorted_data[0]
        outlier_high = sorted_data[-1]
        trimmed_mean = self.calc.calculate_trimmed_mean(dataset, num_to_remove=1)
        
        # Select context
        context_template = random.choice(self.CONTEXT_TEMPLATES)
        context_str = self._populate_context(context_template, dataset)
        unit = context_template.get("unit", "")
        
        # Format dataset
        dataset_str = ", ".join(map(str, dataset))
        
        # Build question
        question_text = f"""{context_str} The values are:

{dataset_str}

a) Calculate the arithmetic mean.
b) Identify any outliers and calculate the trimmed mean."""
        
        # Build solution
        solution_steps = [
            f"a) Arithmetic mean: {' + '.join(map(str, dataset))} ÷ {len(dataset)} = {arithmetic_mean:.1f} {unit}",
            f"b) Sorted data: {', '.join(map(str, sorted_data))}",
            f"   Outliers: {outlier_low} (low) and {outlier_high} (high)",
            f"   Trimmed data: {', '.join(map(str, sorted_data[1:-1]))}",
            f"   Trimmed mean: {trimmed_mean:.1f} {unit}"
        ]
        
        # Create parts
        parts = [
            QuestionPart(
                letter="a",
                instruction="Calculate the arithmetic mean.",
                marks=1.0,
                answer=round(arithmetic_mean, 1),
                answer_format=AnswerFormat.NUMERIC_WITH_UNIT,
                solution_steps=[solution_steps[0]]
            ),
            QuestionPart(
                letter="b",
                instruction="Identify any outliers and calculate the trimmed mean.",
                marks=1.0,
                answer=round(trimmed_mean, 1),
                answer_format=AnswerFormat.NUMERIC_WITH_UNIT,
                solution_steps=solution_steps[1:]
            )
        ]
        
        return Question(
            id="",
            unit="Statistics",
            outcomes=["12E5.S.1"],
            question_type=QuestionType.MIXED,
            difficulty=difficulty,
            total_marks=marks,
            mark_breakdown={"arithmetic_mean": 1.0, "trimmed_mean": 1.0},
            context=context_str,
            question_text=question_text,
            given_data={"dataset": dataset, "unit": unit},
            parts=parts,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_dataset_with_outliers(self, difficulty: int):
        """Generate dataset with deliberate outliers"""
        if difficulty <= 2:
            cluster_size = random.randint(6, 8)
            cluster_min = random.randint(20, 40)
            cluster_max = cluster_min + random.randint(10, 20)
            
            cluster = [random.randint(cluster_min, cluster_max) for _ in range(cluster_size)]
            
            low_outlier = random.randint(cluster_min // 3, cluster_min - 10)
            high_outlier = random.randint(cluster_max + 30, cluster_max * 2)
            
            dataset = cluster + [low_outlier, high_outlier]
            random.shuffle(dataset)
            return dataset
        
        elif difficulty == 3:
            cluster_size = random.randint(7, 10)
            cluster_min = random.randint(100, 150)
            cluster_max = cluster_min + random.randint(30, 50)
            
            cluster = [random.randint(cluster_min, cluster_max) for _ in range(cluster_size)]
            
            low_outlier = random.randint(cluster_min // 2, cluster_min - 30)
            high_outlier = random.randint(cluster_max + 50, cluster_max * 2)
            
            dataset = cluster + [low_outlier, high_outlier]
            random.shuffle(dataset)
            return dataset
        
        else:
            cluster_size = random.randint(8, 12)
            
            if random.random() < 0.5:
                cluster_min = round(random.uniform(50, 100), 1)
                cluster = [round(random.uniform(cluster_min, cluster_min + 30), 1) 
                          for _ in range(cluster_size)]
                low_outlier = round(cluster_min / 2, 1)
                high_outlier = round(cluster_min * 2, 1)
            else:
                cluster_min = random.randint(-5, 5)
                cluster = [random.randint(cluster_min, cluster_min + 10) 
                          for _ in range(cluster_size)]
                low_outlier = random.randint(-20, cluster_min - 5)
                high_outlier = random.randint(cluster_min + 20, cluster_min + 40)
            
            dataset = cluster + [low_outlier, high_outlier]
            random.shuffle(dataset)
            return dataset
    
    def _populate_context(self, template: dict, dataset: list) -> str:
        """Populate context template"""
        context = template["template"]
        uses = template["uses"]
        
        replacements = {}
        
        if "name" in uses:
            name_data = self.data.get_name(with_title=True)
            replacements["{name}"] = name_data["full_name"]
        
        if "business" in uses:
            replacements["{business}"] = self.data.get_business()
        
        if "city" in uses:
            place = self.data.get_place_cdn()
            replacements["{city}"] = place["city"]
        
        if "course" in uses:
            replacements["{course}"] = self.data.get_course()
        
        if "period" in uses:
            replacements["{period}"] = str(len(dataset))
        
        for key, value in replacements.items():
            context = context.replace(key, value)
        
        return context
