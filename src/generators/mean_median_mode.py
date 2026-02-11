"""
Mean, Median, Mode Generator
Generates questions for outcome 12E5.S.1
"""

import random
import sys
from pathlib import Path

# Ensure parent directory is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from question_models import Question, QuestionType, AnswerFormat
from statistics_calculator import StatisticsCalculator
from data_manager import DataManager


class MeanMedianModeGenerator:
    """
    Generate mean/median/mode questions matching provincial exam patterns
    
    Provincial Exam: 1-2 marks
    Student Booklet: Lesson 1
    """
    
    CONTEXT_TEMPLATES = [
        {
            "id": "concert_attendance",
            "template": "{name} tracked nightly attendance at {venue} in {city} over {period} nights.",
            "uses": ["name", "venue", "city", "period"]
        },
        {
            "id": "quiz_scores",
            "template": "{name} recorded quiz scores for students taking {course}.",
            "uses": ["name", "course"]
        },
        {
            "id": "job_earnings",
            "template": "{name} tracked daily earnings from {job} over {period} days.",
            "uses": ["name", "job", "period"]
        },
        {
            "id": "tips_received",
            "template": "{name} works as a server and received the following tips during one shift.",
            "uses": ["name"]
        },
        {
            "id": "product_sales",
            "template": "{name} manages {business} and recorded daily sales over {period} days.",
            "uses": ["name", "business", "period"]
        }
    ]
    
    PHRASING_VARIANTS = [
        "Calculate the mean, median, and mode.",
        "Determine the measures of central tendency.",
        "Find the mean (average), median (middle value), and mode (most frequent value)."
    ]
    
    def __init__(self, data_manager: DataManager):
        self.data = data_manager
        self.calc = StatisticsCalculator()
    
    def generate_question(self, difficulty: int = 2, marks: int = 2) -> Question:
        """Generate a mean/median/mode question"""
        
        # Generate dataset
        dataset = self._generate_dataset(difficulty)
        
        # Calculate answers
        mean_val = self.calc.calculate_mean(dataset)
        median_val = self.calc.calculate_median(dataset)
        mode_val = self.calc.calculate_mode(dataset)
        
        # Select and populate context
        context_template = random.choice(self.CONTEXT_TEMPLATES)
        context_str = self._populate_context(context_template, dataset)
        
        # Format dataset
        dataset_str = ", ".join(map(str, dataset))
        
        # Select phrasing
        phrasing = random.choice(self.PHRASING_VARIANTS)
        
        # Build question
        question_text = f"{context_str} The values recorded were:\n\n{dataset_str}\n\n{phrasing}"
        
        # Build solution
        solution_steps = [
            f"Dataset: {dataset_str}",
            f"Mean: {' + '.join(map(str, dataset))} ÷ {len(dataset)} = {mean_val:.1f}",
            f"Median: {median_val:.1f} (middle value when sorted)",
            f"Mode: {mode_val}"
        ]
        
        # Mark breakdown
        if marks == 1:
            mark_breakdown = {"answer": 1.0}
        else:
            mark_breakdown = {"calculations": 1.0, "answer": 1.0}
        
        return Question(
            id="",
            unit="Statistics",
            outcomes=["12E5.S.1"],
            question_type=QuestionType.CALCULATION,
            difficulty=difficulty,
            total_marks=marks,
            mark_breakdown=mark_breakdown,
            context=context_str,
            question_text=question_text,
            given_data={"dataset": dataset, "context_template": context_template["id"]},
            answer={
                "mean": round(mean_val, 1),
                "median": round(median_val, 1) if median_val != int(median_val) else int(median_val),
                "mode": mode_val
            },
            answer_format=AnswerFormat.MULTIPLE_VALUES,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_dataset(self, difficulty: int):
        """Generate dataset based on difficulty level"""
        if difficulty == 1:
            size = random.randint(5, 7)
            values = [random.randint(0, 10) for _ in range(size)]
            mode_value = random.choice(values)
            values.append(mode_value)
            random.shuffle(values)
            return values
        
        elif difficulty == 2:
            size = random.randint(7, 10)
            return [random.randint(0, 20) for _ in range(size)]
        
        elif difficulty == 3:
            size = random.randint(8, 12)
            return [random.randint(10, 100) for _ in range(size)]
        
        elif difficulty == 4:
            size = random.randint(8, 10)
            if random.random() < 0.5:
                return [round(random.uniform(10, 100), 1) for _ in range(size)]
            else:
                return [random.randint(50, 200) for _ in range(size)]
        
        else:  # difficulty == 5
            size = random.randint(10, 15)
            if random.random() < 0.5:
                return sorted(random.sample(range(10, 100), size))
            else:
                return [round(random.uniform(10, 100), 2) for _ in range(size)]
    
    def _populate_context(self, template: dict, dataset: list) -> str:
        """Populate context template with data"""
        context = template["template"]
        uses = template["uses"]
        
        replacements = {}
        
        if "name" in uses:
            name_data = self.data.get_name(with_title=True)
            replacements["{name}"] = name_data["full_name"]
        
        if "venue" in uses:
            replacements["{venue}"] = self.data.get_theater()
        
        if "city" in uses:
            place = self.data.get_place_cdn()
            replacements["{city}"] = place["full_name"]
        
        if "course" in uses:
            replacements["{course}"] = self.data.get_course()
        
        if "job" in uses:
            replacements["{job}"] = self.data.get_summer_job()
        
        if "business" in uses:
            replacements["{business}"] = self.data.get_business()
        
        if "period" in uses:
            replacements["{period}"] = str(len(dataset))
        
        for key, value in replacements.items():
            context = context.replace(key, value)
        
        return context
