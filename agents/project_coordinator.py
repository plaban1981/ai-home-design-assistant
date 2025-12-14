"""
Project Coordinator Agent
Generates photorealistic renderings, budget breakdowns, and project timelines
"""
from crewai import Agent, Task, Crew, LLM
from tools.image_generator import ImageGenerator
from typing import Dict, Any
import json
import config

# Configure LLM to use Google AI Studio (not Vertex AI)
llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=config.GOOGLE_API_KEY
)
class ProjectCoordinator:
    """Agent responsible for coordinating design execution and rendering generation"""

    def __init__(self):
        self.image_generator = ImageGenerator()
        self.agent = Agent(
            role="Design Project Coordinator",
            goal="Generate photorealistic renderings and comprehensive project plans including budget and timeline",
            backstory="""You are a seasoned project coordinator with expertise in
            interior design execution. You translate design visions into actionable
            plans with realistic budgets and timelines. You work with contractors,
            understand material costs, and ensure projects stay on track.""",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    def generate_project_plan(
        self,
        room_analysis: Dict[str, Any],
        design_style: str = "modern minimalist",
        budget_range: str = "moderate",
        reference_image: str = None
    ) -> Dict[str, Any]:
        """
        Generate complete project plan including rendering, budget, and timeline

        Args:
            room_analysis: Analysis from VisualAssessor
            design_style: Target design style
            budget_range: low, moderate, high
            reference_image: Optional reference photo

        Returns:
            Complete project plan
        """
        print(f"\n🎨 Project Coordinator creating plan for {design_style} design...")

        # Extract room details
        raw_analysis = room_analysis.get("raw_analysis", {})
        room_type = raw_analysis.get("room_type", "room")
        size = raw_analysis.get("dimensions_estimate", "medium")

        # Create design brief
        design_brief = f"""Transform this {room_type} into a {design_style} space.

Current condition: {raw_analysis.get('condition', 'needs refresh')}
Room size: {size}
Key features to maintain: {', '.join(raw_analysis.get('features', []))}

Design goals:
- Update to {design_style} aesthetic
- Improve lighting and atmosphere
- Maximize functionality
- Stay within {budget_range} budget range
"""

        # Generate rendering
        rendering = self.image_generator.generate_rendering(
            room_analysis=raw_analysis,
            design_brief=design_brief,
            style=design_style,
            reference_image_path=reference_image
        )

        # Create budget and timeline task
        task = Task(
            description=f"""Based on this design rendering:
            {json.dumps(rendering, indent=2)}

            For a {size} {room_type} with {budget_range} budget, create:

            1. BUDGET BREAKDOWN
               - Materials (paint, flooring, fixtures)
               - Furniture and decor
               - Labor costs
               - Contingency (10-15%)
               - Total estimated cost

            2. PROJECT TIMELINE
               - Planning phase
               - Material sourcing
               - Installation/construction
               - Styling and finishing
               - Total estimated duration

            3. CONTRACTOR RECOMMENDATIONS
               - Types of contractors needed
               - Skills required
               - Estimated labor hours

            4. SHOPPING LIST
               - Key items needed
               - Suggested retailers
               - Priority order for purchases""",
            agent=self.agent,
            expected_output="Structured project plan with budget and timeline"
        )

        # Execute task using Crew
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        project_details = crew.kickoff()

        return {
            "rendering": rendering,
            "project_plan": str(project_details),
            "design_style": design_style,
            "budget_range": budget_range,
            "room_type": room_type
        }

    def refine_design(
        self,
        previous_plan: Dict[str, Any],
        refinement_request: str
    ) -> Dict[str, Any]:
        """
        Refine design based on user feedback

        Args:
            previous_plan: Previous project plan
            refinement_request: Natural language refinement (e.g., "make cabinets cream instead of white")

        Returns:
            Refined project plan
        """
        print(f"\n✨ Refining design: {refinement_request}")

        # Refine rendering
        refined_rendering = self.image_generator.refine_rendering(
            previous_rendering=previous_plan.get("rendering", {}),
            refinement_request=refinement_request
        )

        return {
            "rendering": refined_rendering,
            "refinement_applied": refinement_request,
            "version": previous_plan.get("version", 1) + 1,
            "original_style": previous_plan.get("design_style")
        }
