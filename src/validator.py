from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field

class UserStory(BaseModel):
    id: str = Field(description="Unique identifier, e.g., US-001")
    title: str = Field(description="Short, descriptive title of the user story")
    user_story: str = Field(description="Format: As a [user], I want [feature], so that [benefit]")
    acceptance_criteria: List[str] = Field(description="List of testable acceptance criteria using Given/When/Then")
    priority: Literal["High", "Medium", "Low"] = Field(description="Assigned priority based on business value")
    estimate_points: int = Field(description="Fibonacci story points (1, 2, 3, 5, 8, 13)")
    tags: List[str] = Field(description="Relevant technical or functional tags")

class BacklogOutput(BaseModel):
    project_summary: str = Field(description="Executive summary of requirements processed")
    identified_risks: List[str] = Field(description="Potential technical risks or missing edge cases")
    user_stories: List[UserStory]
    generated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp of generation")