"""
Interactive Home Design Tool
Upload an image and provide a custom prompt to transform your interior design
"""
import os
import sys
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

def get_image_path():
    """Prompt user for image path"""
    print("\n" + "="*70)
    print("📸 IMAGE SELECTION")
    print("="*70)

    # Show available images in test_photos
    test_photos_dir = config.TEST_PHOTOS_DIR
    if os.path.exists(test_photos_dir):
        photos = [f for f in os.listdir(test_photos_dir)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if photos:
            print("\nAvailable images in test_photos/:")
            for i, photo in enumerate(photos, 1):
                print(f"  {i}. {photo}")

    print("\nOptions:")
    print("  1. Enter full path to your image")
    print("  2. Enter filename from test_photos/")
    print("  3. Enter number from list above")

    choice = input("\nYour choice: ").strip()

    # Handle numeric selection
    if choice.isdigit() and photos:
        idx = int(choice) - 1
        if 0 <= idx < len(photos):
            return os.path.join(test_photos_dir, photos[idx])

    # Handle filename or full path
    if os.path.exists(choice):
        return choice

    # Try as filename in test_photos
    test_path = os.path.join(test_photos_dir, choice)
    if os.path.exists(test_path):
        return test_path

    print(f"❌ Could not find image: {choice}")
    return None

def get_design_prompt():
    """Get custom design prompt from user"""
    print("\n" + "="*70)
    print("✨ DESIGN TRANSFORMATION PROMPT")
    print("="*70)

    print("\nDescribe how you want to transform this space.")
    print("Be specific about:")
    print("  - Style (modern, minimalist, cozy, industrial, etc.)")
    print("  - Colors you want")
    print("  - Furniture changes")
    print("  - Lighting preferences")
    print("  - Any specific elements (plants, artwork, etc.)")

    print("\nExamples:")
    print("  'Modern minimalist with warm wood tones and lots of plants'")
    print("  'Cozy bohemian style with earthy colors and natural textures'")
    print("  'Industrial loft with exposed brick, metal accents, and Edison bulbs'")

    print("\n" + "-"*70)
    prompt = input("Your design prompt: ").strip()

    if not prompt:
        print("Using default: modern minimalist design")
        return "modern minimalist design", "modern minimalist"

    return prompt, extract_style(prompt)

def extract_style(prompt):
    """Extract design style from prompt"""
    style_keywords = {
        'modern': 'modern',
        'minimalist': 'minimalist',
        'contemporary': 'contemporary',
        'industrial': 'industrial',
        'bohemian': 'bohemian',
        'scandinavian': 'scandinavian',
        'rustic': 'rustic',
        'farmhouse': 'farmhouse',
        'traditional': 'traditional',
        'mid-century': 'mid-century modern',
        'coastal': 'coastal',
        'vintage': 'vintage'
    }

    prompt_lower = prompt.lower()
    for keyword, style in style_keywords.items():
        if keyword in prompt_lower:
            return style

    return prompt.split()[0] if prompt else "custom"

def get_budget():
    """Get budget preference from user"""
    print("\n" + "="*70)
    print("💰 BUDGET RANGE")
    print("="*70)

    print("\nSelect your budget range:")
    print("  1. Low ($1,000 - $3,000)")
    print("  2. Moderate ($3,000 - $7,000)")
    print("  3. High ($7,000+)")

    choice = input("\nYour choice (1-3): ").strip()

    budget_map = {
        '1': 'low',
        '2': 'moderate',
        '3': 'high'
    }

    return budget_map.get(choice, 'moderate')

def save_results(results: dict, output_dir: str = "output"):
    """Save results to JSON file"""
    import json
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"interactive_results_{timestamp}.json")

    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {filepath}")
    return filepath

def run_interactive_design():
    """Run interactive design transformation"""
    print("\n" + "="*70)
    print("🏠 INTERACTIVE HOME DESIGN ASSISTANT")
    print("="*70)
    print("\nTransform your space with AI-powered interior design suggestions!")

    # Get inputs
    image_path = get_image_path()
    if not image_path:
        return

    design_prompt, design_style = get_design_prompt()
    budget_range = get_budget()

    # Confirm selections
    print("\n" + "="*70)
    print("📋 YOUR SELECTIONS")
    print("="*70)
    print(f"Image: {image_path}")
    print(f"Design prompt: {design_prompt}")
    print(f"Style: {design_style}")
    print(f"Budget: {budget_range}")

    confirm = input("\nProceed with these selections? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    # Initialize results
    results = {
        "timestamp": datetime.now().isoformat(),
        "input_image": image_path,
        "design_prompt": design_prompt,
        "target_style": design_style,
        "budget_range": budget_range,
        "workflow_steps": []
    }

    try:
        # STEP 1: Visual Assessment
        print("\n" + "="*70)
        print("📍 STEP 1: Analyzing Your Space")
        print("="*70)

        assessor = VisualAssessor()
        analysis = assessor.analyze(image_path)

        if "error" in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            results["error"] = analysis["error"]
            save_results(results)
            return

        # Display summary
        summary = assessor.get_room_summary(analysis)
        print(summary)

        results["workflow_steps"].append({
            "step": "visual_assessment",
            "agent": "VisualAssessor",
            "output": analysis
        })

        # STEP 2: Generate Transformation with Custom Prompt
        print("\n" + "="*70)
        print("📍 STEP 2: Creating Your Custom Design Transformation")
        print("="*70)

        coordinator = ProjectCoordinator()

        # Create custom design brief incorporating user's prompt
        raw_analysis = analysis.get("raw_analysis", {})
        custom_brief = f"""Transform this space based on the following request:

USER'S VISION: {design_prompt}

Current room details:
- Type: {raw_analysis.get('room_type', 'room')}
- Size: {raw_analysis.get('dimensions_estimate', 'medium')}
- Current condition: {raw_analysis.get('condition', 'needs refresh')}
- Key features: {', '.join(raw_analysis.get('features', []))}

Create a design that:
1. Fulfills the user's specific vision: "{design_prompt}"
2. Works with the existing space and features
3. Stays within {budget_range} budget range
4. Provides specific, actionable recommendations"""

        project_plan = coordinator.generate_project_plan(
            room_analysis=analysis,
            design_style=design_style,
            budget_range=budget_range,
            reference_image=image_path
        )

        print("\n✅ Custom Design Plan Generated!")
        print(f"Design Style: {project_plan['design_style']}")
        print(f"Budget Range: {project_plan['budget_range']}")

        results["workflow_steps"].append({
            "step": "custom_design_transformation",
            "agent": "ProjectCoordinator",
            "custom_prompt": design_prompt,
            "output": project_plan
        })

        # Display rendering description if available
        rendering = project_plan.get("rendering", {})
        if rendering.get("success"):
            print("\n" + "="*70)
            print("🎨 YOUR TRANSFORMED SPACE")
            print("="*70)
            print(rendering.get("rendering_description", ""))

        # Workflow Complete
        print("\n" + "="*70)
        print("✅ DESIGN TRANSFORMATION COMPLETE!")
        print("="*70)

        results["status"] = "success"
        output_file = save_results(results)

        # Summary
        print("\n📊 SUMMARY:")
        print(f"✓ Room analyzed: {raw_analysis.get('room_type', 'Unknown')}")
        print(f"✓ Your vision: {design_prompt}")
        print(f"✓ Design style: {design_style}")
        print(f"✓ Custom transformation plan generated")
        print(f"✓ Results saved: {output_file}")

        return results

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        results["status"] = "error"
        results["error"] = str(e)
        save_results(results)
        return results

def main():
    """Main entry point"""
    try:
        run_interactive_design()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
