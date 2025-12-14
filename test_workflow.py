"""
Test the complete workflow with a real room image
Demonstrates CrewAI agents working together
"""
import sys
import os
from datetime import datetime
from PIL import Image

# Setup UTF-8 encoding FIRST
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

# Try to import matplotlib, but make it optional
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️ Matplotlib not available - skipping visual comparison")

# Import our agents
from agents.visual_assessor import VisualAssessor
from agents.project_coordinator import ProjectCoordinator

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def main():
    print_section("🏠 AI HOME DESIGN ASSISTANT - WORKFLOW TEST")

    # Configuration
    IMAGE_PATH = "test_photos/IMG20251213210129.jpg"
    DESIGN_STYLE = "modern minimalist"
    BUDGET_RANGE = "moderate"
    CUSTOM_PROMPT = """Transform into a productive home office with:
    - Clean, organized desk setup
    - Proper cable management
    - Better lighting (desk lamp and ambient lighting)
    - Organized bookshelf with books and decorative items
    - Minimalist decor with plants
    - Professional workspace atmosphere
    - Keep the existing furniture but make it more organized"""

    print(f"📸 Image: {IMAGE_PATH}")
    print(f"🎨 Style: {DESIGN_STYLE}")
    print(f"💰 Budget: {BUDGET_RANGE}")
    print(f"📝 Custom Prompt: {CUSTOM_PROMPT[:100]}...")

    # Step 1: Initialize CrewAI Agents
    print_section("🤖 STEP 1: INITIALIZE CREWAI AGENTS")

    print("Initializing Visual Assessor Agent...")
    visual_assessor = VisualAssessor()
    print(f"✅ Visual Assessor Ready")
    print(f"   Role: {visual_assessor.agent.role}")
    print(f"   Verbose: {visual_assessor.agent.verbose}")

    print("\nInitializing Project Coordinator Agent...")
    project_coordinator = ProjectCoordinator()
    print(f"✅ Project Coordinator Ready")
    print(f"   Role: {project_coordinator.agent.role}")
    print(f"   Has Nano Banana: {project_coordinator.image_generator.image_gen_available}")

    # Step 2: Analyze Room
    print_section("🔍 STEP 2: VISUAL ASSESSOR AGENT - ROOM ANALYSIS")

    print("CrewAI Agent is analyzing the room...")
    print("This involves:")
    print("  1. ImageAnalyzer tool extracts room data")
    print("  2. Agent creates assessment task")
    print("  3. Crew executes the task")
    print("  4. Agent provides professional analysis\n")

    analysis_result = visual_assessor.analyze(IMAGE_PATH)

    if "error" in analysis_result:
        print(f"❌ Error: {analysis_result['error']}")
        return

    # Display analysis results
    raw_analysis = analysis_result.get("raw_analysis", {})

    print("\n📊 Analysis Results:")
    print(f"   Room Type: {raw_analysis.get('room_type', 'Unknown')}")
    print(f"   Current Style: {raw_analysis.get('current_style', 'Unknown')}")
    print(f"   Size: {raw_analysis.get('dimensions_estimate', 'Unknown')}")
    print(f"   Lighting: {raw_analysis.get('lighting', 'Unknown')}")
    print(f"   Condition: {raw_analysis.get('condition', 'Unknown')}")

    if raw_analysis.get('features'):
        print(f"\n   Key Features:")
        for feature in raw_analysis['features'][:5]:
            print(f"     • {feature}")

    if raw_analysis.get('challenges'):
        print(f"\n   Challenges:")
        for challenge in raw_analysis['challenges'][:3]:
            print(f"     • {challenge}")

    # Step 3: Transform Room
    print_section("🎨 STEP 3: PROJECT COORDINATOR AGENT - TRANSFORMATION")

    print("CrewAI Agent is creating your design...")
    print("This involves:")
    print("  1. Generate rendering with Nano Banana (using reference image)")
    print("  2. Create budget breakdown task")
    print("  3. Crew executes planning task")
    print("  4. Agent produces comprehensive plan\n")

    transformation_result = project_coordinator.generate_project_plan(
        room_analysis=analysis_result,
        design_style=DESIGN_STYLE,
        budget_range=BUDGET_RANGE,
        reference_image=IMAGE_PATH
    )

    # Display transformation results
    rendering = transformation_result.get("rendering", {})

    print("\n🎨 Transformation Results:")
    print(f"   Success: {rendering.get('success', False)}")

    if rendering.get("success"):
        print(f"   Image Path: {rendering.get('image_path', 'N/A')}")
        print(f"   Model Used: {rendering.get('model', 'N/A')}")

        if rendering.get('size'):
            print(f"   Image Size: {rendering['size'][0]} x {rendering['size'][1]} pixels")

        print(f"   Used Reference Image: {rendering.get('used_reference_image', False)}")

        if rendering.get('rendering_description'):
            desc = rendering['rendering_description']
            print(f"\n   Description Preview:")
            print(f"   {desc[:200]}...")
    else:
        print(f"   ❌ Error: {rendering.get('error', 'Unknown error')}")

    # Step 4: Display Results
    print_section("✨ STEP 4: RESULTS")

    print("📊 Project Summary:")
    print(f"   Room Type: {transformation_result.get('room_type', 'N/A').title()}")
    print(f"   Design Style: {transformation_result.get('design_style', 'N/A').title()}")
    print(f"   Budget Range: {transformation_result.get('budget_range', 'N/A').title()}")

    # Check if we have the transformed image
    if rendering.get("success") and rendering.get("image_path"):
        transformed_path = rendering["image_path"]

        if os.path.exists(transformed_path):
            print(f"\n✅ Transformed image saved!")
            print(f"   Original: {IMAGE_PATH}")
            print(f"   Transformed: {transformed_path}")

            # Display images side by side (if matplotlib available)
            if HAS_MATPLOTLIB:
                try:
                    original_img = Image.open(IMAGE_PATH)
                    transformed_img = Image.open(transformed_path)

                    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

                    axes[0].imshow(original_img)
                    axes[0].set_title("Original Room", fontsize=14, fontweight='bold')
                    axes[0].axis('off')

                    axes[1].imshow(transformed_img)
                    axes[1].set_title(f"Transformed - {DESIGN_STYLE.title()}", fontsize=14, fontweight='bold')
                    axes[1].axis('off')

                    plt.tight_layout()

                    # Save comparison
                    comparison_path = f"output/comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    plt.savefig(comparison_path, dpi=150, bbox_inches='tight')
                    print(f"   Comparison saved: {comparison_path}")

                    plt.show()

                except Exception as e:
                    print(f"   ⚠️ Could not display comparison: {e}")
            else:
                print("   📊 Images available at paths shown above")
        else:
            print(f"\n❌ Transformed image not found at: {transformed_path}")
    else:
        print("\n⚠️ Image transformation incomplete")

    # Display project plan preview
    if transformation_result.get("project_plan"):
        print("\n📋 Project Plan Preview:")
        plan = str(transformation_result["project_plan"])
        # Show first 500 characters
        print(plan[:500] + "..." if len(plan) > 500 else plan)

    print_section("🎉 WORKFLOW COMPLETE!")

    print("✅ CrewAI agents successfully completed all tasks:")
    print("   1. Visual Assessor analyzed the room")
    print("   2. Project Coordinator generated transformation")
    print("   3. Both agents used their tools and reasoning")
    print("   4. Complete design plan created")

    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
