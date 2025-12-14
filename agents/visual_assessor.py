"""
Visual Assessor Agent
Analyzes room photos and inspiration images to provide detailed assessment
"""
from crewai import Agent, Task, Crew, LLM
from tools.image_analyzer import ImageAnalyzer
from typing import Dict, Any
import json
import config

# Configure LLM to use Google AI Studio (not Vertex AI)
llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=config.GOOGLE_API_KEY
)
class VisualAssessor:
    """Agent responsible for visual analysis of room photos"""

    def __init__(self):
        self.image_analyzer = ImageAnalyzer()
        self.agent = Agent(
            role="Visual Assessment Specialist",
            goal="Analyze room photos to extract detailed information about space, style, and design opportunities",
            backstory="""You are an expert interior designer with 15 years of experience
            analyzing spaces. You have a keen eye for identifying room characteristics,
            design challenges, and opportunities. You can assess a room's potential and
            provide actionable insights for transformation.""",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    def analyze(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a room photo and return comprehensive assessment

        Args:
            image_path: Path to room photo

        Returns:
            Detailed analysis dictionary
        """
        print(f"\n🔍 Visual Assessor analyzing: {image_path}")

        # Use ImageAnalyzer tool
        analysis = self.image_analyzer.analyze_room(image_path)

        if "error" in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return analysis

        # Create assessment task for the agent
        task = Task(
            description=f"""Based on this room analysis:
            {json.dumps(analysis, indent=2)}

            Provide a professional assessment including:
            1. Overall impression of the space
            2. Key strengths to build upon
            3. Design challenges to address
            4. Recommendations for transformation
            5. Budget-conscious suggestions""",
            agent=self.agent,
            expected_output="Structured assessment with recommendations"
        )

        # Execute task using Crew
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()

        # Combine tool analysis with agent assessment
        return {
            "raw_analysis": analysis,
            "professional_assessment": str(result),
            "image_path": image_path
        }

    def get_room_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the analysis"""
        raw = analysis.get("raw_analysis", {})

        room_type = raw.get("room_type", "Unknown")
        style = raw.get("current_style", "Unknown")
        condition = raw.get("condition", "Unknown")
        size = raw.get("dimensions_estimate", "Unknown")

        summary = f"""
📊 ROOM ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━
Room Type: {room_type}
Current Style: {style}
Size: {size}
Condition: {condition}

Features: {', '.join(raw.get('features', []))}
Colors: {', '.join(raw.get('colors', []))}
Lighting: {raw.get('lighting', 'Unknown')}

Challenges: {', '.join(raw.get('challenges', []))}
Opportunities: {', '.join(raw.get('opportunities', []))}
"""
        return summary
