"""
Home Design POC - Main Entry Point
Demonstrates multi-agent workflow for interior design planning
"""
import os
import sys
import json
from datetime import datetime
from agents.visual_assessor import VisualAssessor
from agents.project_coordinator import ProjectCoordinator
import config

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

def save_results(results: dict, output_dir: str = "output"):
    """Save POC results to JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"poc_results_{timestamp}.json")

    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {filepath}")
    return filepath

def run_poc(image_path: str, design_style: str = "modern minimalist", budget_range: str = "moderate"):
    """
    Run the complete POC workflow

    Args:
        image_path: Path to room photo
        design_style: Target design style
        budget_range: Budget category (low, moderate, high)
    """
    print("\n" + "="*70)
    print("🏠 HOME DESIGN POC - Multi-Agent Interior Design Planner")
    print("="*70)

    results = {
        "timestamp": datetime.now().isoformat(),
        "input_image": image_path,
        "target_style": design_style,
        "budget_range": budget_range,
        "workflow_steps": []
    }

    try:
        # STEP 1: Visual Assessment
        print("\n📍 STEP 1: Visual Assessment")
        print("-" * 70)

        assessor = VisualAssessor()
        analysis = assessor.analyze(image_path)

        if "error" in analysis:
            print(f"❌ Visual assessment failed: {analysis['error']}")
            results["error"] = analysis["error"]
            save_results(results)
            return results

        # Display summary
        summary = assessor.get_room_summary(analysis)
        print(summary)

        results["workflow_steps"].append({
            "step": "visual_assessment",
            "agent": "VisualAssessor",
            "output": analysis
        })

        # STEP 2: Project Coordination & Rendering
        print("\n📍 STEP 2: Project Coordination & Rendering Generation")
        print("-" * 70)

        coordinator = ProjectCoordinator()
        project_plan = coordinator.generate_project_plan(
            room_analysis=analysis,
            design_style=design_style,
            budget_range=budget_range,
            reference_image=image_path
        )

        print("\n✅ Project Plan Generated!")
        print(f"Design Style: {project_plan['design_style']}")
        print(f"Budget Range: {project_plan['budget_range']}")

        results["workflow_steps"].append({
            "step": "project_coordination",
            "agent": "ProjectCoordinator",
            "output": project_plan
        })

        # Display rendering description
        rendering = project_plan.get("rendering", {})
        if rendering.get("success"):
            print("\n🎨 RENDERING DESCRIPTION:")
            print("-" * 70)
            print(rendering.get("rendering_description", ""))

        # POC Complete
        print("\n" + "="*70)
        print("✅ POC WORKFLOW COMPLETE!")
        print("="*70)

        # Save results
        results["status"] = "success"
        output_file = save_results(results)

        # Summary
        print("\n📊 POC SUMMARY:")
        print(f"✓ Room analyzed: {analysis.get('raw_analysis', {}).get('room_type', 'Unknown')}")
        print(f"✓ Design style: {design_style}")
        print(f"✓ Project plan generated")
        print(f"✓ Results saved: {output_file}")

        return results

    except Exception as e:
        print(f"\n❌ POC Error: {str(e)}")
        results["status"] = "error"
        results["error"] = str(e)
        save_results(results)
        return results

def main():
    """Main entry point for POC"""
    # Example usage
    print("\n🚀 Starting Home Design POC...")

    # Check for test photos
    test_photos_dir = config.TEST_PHOTOS_DIR

    if not os.path.exists(test_photos_dir) or not os.listdir(test_photos_dir):
        print(f"\n⚠️  No test photos found in '{test_photos_dir}/'")
        print("\nPlease add some room photos to the test_photos/ directory and run again.")
        print("\nExample: Place a photo named 'living_room.jpg' in test_photos/")
        return

    # Get first image from test_photos directory
    photos = [f for f in os.listdir(test_photos_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not photos:
        print(f"\n⚠️  No image files found in '{test_photos_dir}/'")
        return

    test_image = os.path.join(test_photos_dir, photos[0])

    print(f"\nUsing test image: {test_image}")
    print("Design style: modern minimalist")
    print("Budget range: moderate\n")

    # Run POC
    results = run_poc(
        image_path=test_image,
        design_style="modern minimalist",
        budget_range="moderate"
    )

    # Interactive refinement option
    if results.get("status") == "success":
        print("\n" + "="*70)
        print("🔄 Optional: Test Iterative Refinement")
        print("="*70)
        print("\nExample refinement requests:")
        print("- 'make the colors warmer'")
        print("- 'add more plants'")
        print("- 'use lighter wood tones'")
        print("\nTo test refinement, modify this script to call coordinator.refine_design()")

if __name__ == "__main__":
    main()
