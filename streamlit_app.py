"""
Streamlit Home Design Assistant
Upload an image and transform your space with AI
"""
import streamlit as st
import sys
import os
from PIL import Image
import io
import tempfile
from datetime import datetime

# Fix UTF-8 encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

# Import our agents
from agents.visual_assessor import VisualAssessor
from agents.project_coordinator import ProjectCoordinator

# Page config
st.set_page_config(
    page_title="AI Home Design Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'transformation_result' not in st.session_state:
    st.session_state.transformation_result = None
if 'temp_image_path' not in st.session_state:
    st.session_state.temp_image_path = None
if 'agent_responses' not in st.session_state:
    st.session_state.agent_responses = {}

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temp directory"""
    try:
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join("temp", "uploads")
        os.makedirs(temp_dir, exist_ok=True)

        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(temp_dir, f"upload_{timestamp}_{uploaded_file.name}")

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def analyze_room(image_path):
    """Analyze the uploaded room image"""
    with st.spinner("🔍 Analyzing your room..."):
        try:
            assessor = VisualAssessor()
            analysis = assessor.analyze(image_path)

            if "error" in analysis:
                st.error(f"Analysis failed: {analysis['error']}")
                return None

            return analysis
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            return None

def transform_room(analysis, design_prompt, design_style, budget_range, image_path):
    """Generate transformation with custom prompt"""
    with st.spinner("🎨 Generating your transformed design..."):
        try:
            coordinator = ProjectCoordinator()

            # Generate transformation
            project_plan = coordinator.generate_project_plan(
                room_analysis=analysis,
                design_style=design_style,
                budget_range=budget_range,
                reference_image=image_path
            )

            return project_plan
        except Exception as e:
            st.error(f"Error during transformation: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return None

# Main App
def main():
    # Header
    st.markdown('<div class="main-header">🏠 AI Home Design Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform your space with AI-powered design suggestions</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Additional Settings")

        # Design style
        design_style = st.selectbox(
            "Design Style",
            [
                "Modern Minimalist",
                "Cozy Bohemian",
                "Industrial Loft",
                "Scandinavian",
                "Contemporary",
                "Rustic Farmhouse",
                "Mid-Century Modern",
                "Coastal",
                "Traditional"
            ],
            help="This will be combined with your custom instructions"
        )

        # Budget range
        budget_range = st.select_slider(
            "Budget Range",
            options=["low", "moderate", "high"],
            value="moderate",
            help="Affects the cost estimates in the project plan"
        )

        st.divider()

        # Info
        st.info("""
        **How it works:**
        1. ✍️ Describe your dream space (above)
        2. 📸 Upload a room photo
        3. ⚙️ Adjust settings here
        4. ✨ Click 'Transform My Space'
        5. 🎉 View your transformation!
        """)

        st.divider()

        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Model", "Nano Banana")
        st.metric("Resolution", "1024x1024")
        st.metric("Format", "PNG")

    # Instructions Section - Make it prominent
    st.header("✍️ Describe Your Dream Space")

    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["🎨 Quick Styles", "✨ Custom Instructions", "💡 Examples"])

    with tab1:
        st.write("**Choose a pre-made transformation style:**")
        quick_style_options = {
            "🛋️ Cozy Reading Nook": "Transform into a cozy reading nook with warm lighting, comfortable seating, built-in bookshelves filled with books, a plush reading chair with ottoman, soft ambient lighting, and warm earth tones",
            "🌿 Minimalist Zen": "Create a minimalist zen space with natural materials, neutral colors, plants, clean lines, uncluttered surfaces, and calming atmosphere",
            "🎨 Creative Studio": "Design a creative studio with organized storage, good natural lighting, inspiring artwork, comfortable workspace, and vibrant accent colors",
            "☕ Coffee Bar Corner": "Set up a stylish coffee bar corner with open shelving, cafe-style lighting, coffee equipment display, and cozy seating area",
            "🏋️ Home Gym": "Transform into a home gym with rubber flooring, wall-mounted mirrors, organized equipment storage, motivational decor, and proper ventilation",
            "🎮 Gaming Setup": "Create a gaming setup with ergonomic furniture, RGB lighting, cable management, display mounting, and comfortable seating",
            "🧘 Meditation Space": "Design a meditation space with soft lighting, comfortable floor cushions, natural elements, calming colors, and minimal distractions",
            "👶 Kids Play Area": "Transform into a kids play area with colorful storage, soft flooring, educational displays, creative stations, and safety features"
        }

        selected_quick_style = st.selectbox(
            "Select a transformation style:",
            list(quick_style_options.keys()),
            key="quick_style"
        )

        custom_prompt = quick_style_options[selected_quick_style]
        st.info(f"**Instructions:** {custom_prompt}")

    with tab2:
        st.write("**Write your own transformation instructions:**")
        st.markdown("""
        Describe exactly how you want your space to look. Be specific about:
        - 🎨 **Colors & Materials:** "White walls with warm wood accents"
        - 🪑 **Furniture:** "Comfortable reading chair with ottoman"
        - 💡 **Lighting:** "Soft ambient lighting with task lamps"
        - 🌿 **Decor:** "Lots of plants and natural textures"
        - 🎯 **Purpose:** "Perfect for relaxation and reading"
        """)

        custom_prompt = st.text_area(
            "Your transformation instructions:",
            value="",
            placeholder="Example: Transform into a cozy reading nook with warm lighting, comfortable seating, built-in bookshelves filled with books, a plush reading chair with ottoman, soft ambient lighting, and warm earth tones",
            height=150,
            key="custom_instructions",
            help="The more detailed your instructions, the better the AI can transform your space!"
        )

        if not custom_prompt.strip():
            st.warning("⚠️ Please provide instructions for how you'd like to transform your space")

    with tab3:
        st.write("**Get inspired by these example transformations:**")

        col_ex1, col_ex2 = st.columns(2)

        with col_ex1:
            st.markdown("""
            **🛏️ Bedroom Examples:**
            - "Serene minimalist bedroom with white linens, natural wood furniture, hanging plants, and soft morning light"
            - "Cozy bohemian bedroom with macrame wall hangings, layered textiles, warm fairy lights, and abundant plants"
            - "Modern industrial bedroom with exposed brick, metal accents, Edison bulbs, and concrete floors"

            **🏠 Living Room Examples:**
            - "Scandinavian living room with light wood floors, white walls, cozy textiles, and statement lighting"
            - "Mid-century modern living room with vintage furniture, geometric patterns, and warm wood tones"
            - "Coastal living room with white and blue palette, natural textures, and beach-inspired decor"
            """)

        with col_ex2:
            st.markdown("""
            **💼 Office Examples:**
            - "Productive home office with ergonomic desk, organized shelving, plants, natural light, and inspiring artwork"
            - "Creative studio with large worktable, art supplies organization, gallery wall, and bright task lighting"
            - "Executive office with dark wood furniture, leather chairs, built-in bookshelves, and sophisticated decor"

            **🍳 Kitchen Examples:**
            - "Modern farmhouse kitchen with white shaker cabinets, butcher block island, subway tile, and vintage accents"
            - "Contemporary kitchen with sleek cabinets, quartz counters, stainless appliances, and minimalist design"
            - "Rustic kitchen with reclaimed wood, open shelving, farmhouse sink, and warm lighting"
            """)

        if st.button("💡 Use a random example"):
            examples = [
                "Cozy reading nook with floor-to-ceiling bookshelves, comfortable armchair, warm lighting, and soft throw blankets",
                "Productive workspace with standing desk, organized storage, plants, natural light, and motivational wall art",
                "Zen meditation corner with floor cushions, soft lighting, minimal decor, plants, and calming neutral colors",
                "Vintage coffee bar with open shelving, cafe lighting, espresso machine, and cozy seating area",
                "Modern minimalist bedroom with platform bed, floating nightstands, warm wood accents, and statement lighting"
            ]
            import random
            custom_prompt = random.choice(examples)
            st.success(f"✨ Try this: {custom_prompt}")
            st.session_state.example_prompt = custom_prompt

    st.divider()

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📸 Upload Your Room Photo")

        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of your room to get started"
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Original Room", use_container_width=True)

            # Save to temp file
            image_path = save_uploaded_file(uploaded_file)
            st.session_state.temp_image_path = image_path

            if image_path:
                st.success("✅ Image uploaded successfully!")

    with col2:
        st.header("🎨 Transformed Design")

        if st.session_state.transformation_result:
            # Display transformed image if available
            rendering = st.session_state.transformation_result.get("rendering", {})

            if rendering.get("success") and rendering.get("image_path"):
                try:
                    transformed_image = Image.open(rendering["image_path"])
                    st.image(transformed_image, caption="Your Transformed Space", use_container_width=True)

                    # Download button
                    with open(rendering["image_path"], "rb") as f:
                        st.download_button(
                            label="📥 Download Transformed Image",
                            data=f,
                            file_name=f"transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.warning(f"Could not load transformed image: {str(e)}")
            else:
                st.info("Transformed image will appear here after generation")
        else:
            st.info("Upload an image and click 'Transform My Space' to see your AI-generated design!")

    # Transform button
    if uploaded_file is not None:
        st.divider()

        # Show current instructions
        if 'custom_prompt' in locals() and custom_prompt and custom_prompt.strip():
            with st.expander("📝 Your Transformation Instructions", expanded=False):
                st.info(f"**You requested:** {custom_prompt}")
                st.write(f"**Design Style:** {design_style}")
                st.write(f"**Budget Range:** {budget_range}")

        # Validate instructions
        has_instructions = 'custom_prompt' in locals() and custom_prompt and custom_prompt.strip()

        if st.button("✨ Transform My Space", type="primary", disabled=not has_instructions):
            if not has_instructions:
                st.error("⚠️ Please provide transformation instructions in the tabs above!")
            else:
                # Step 1: Analyze room
                st.header("📊 Analysis & Transformation")

                analysis = analyze_room(st.session_state.temp_image_path)

                if analysis:
                    st.session_state.analysis_result = analysis

                    # Display analysis
                    with st.expander("🔍 Room Analysis", expanded=True):
                        raw_analysis = analysis.get("raw_analysis", {})

                        col_a, col_b, col_c = st.columns(3)

                        with col_a:
                            st.metric("Room Type", raw_analysis.get("room_type", "Unknown").title())
                            st.metric("Size", raw_analysis.get("dimensions_estimate", "Unknown").title())

                        with col_b:
                            st.metric("Current Style", raw_analysis.get("current_style", "Unknown").title())
                            st.metric("Condition", raw_analysis.get("condition", "Unknown").replace("_", " ").title())

                        with col_c:
                            st.metric("Lighting", raw_analysis.get("lighting", "Unknown").title())

                        # Features
                        if raw_analysis.get("features"):
                            st.subheader("Key Features")
                            features_text = ", ".join(raw_analysis["features"])
                            st.write(features_text)

                        # Challenges
                        if raw_analysis.get("challenges"):
                            st.subheader("Challenges")
                            for challenge in raw_analysis["challenges"]:
                                st.write(f"• {challenge}")

                        # Opportunities
                        if raw_analysis.get("opportunities"):
                            st.subheader("Opportunities")
                            for opportunity in raw_analysis["opportunities"]:
                                st.write(f"• {opportunity}")

                    # Professional Assessment
                    if analysis.get("professional_assessment"):
                        with st.expander("👨‍💼 Professional Assessment"):
                            st.markdown(analysis["professional_assessment"])

                    # Store agent response for later display
                    if 'agent_responses' not in st.session_state:
                        st.session_state.agent_responses = {}
                    st.session_state.agent_responses['visual_assessor'] = analysis.get("professional_assessment", "")

                    # Step 2: Generate transformation
                    transformation = transform_room(
                        analysis,
                        custom_prompt,
                        design_style.lower(),
                        budget_range,
                        st.session_state.temp_image_path
                    )

                    if transformation:
                        st.session_state.transformation_result = transformation

                        # Store project coordinator response
                        st.session_state.agent_responses['project_coordinator'] = transformation.get("project_plan", "")

                        # Display rendering description
                        rendering = transformation.get("rendering", {})

                        if rendering.get("success"):
                            st.success("✅ Transformation complete!")

                            # Display transformed image
                            if rendering.get("image_path"):
                                st.subheader("🎨 Your Transformed Space")
                                try:
                                    transformed_image = Image.open(rendering["image_path"])
                                    st.image(transformed_image, use_container_width=True)
                                except Exception as e:
                                    st.warning(f"Image saved but display failed: {str(e)}")

                            # Description
                            if rendering.get("rendering_description"):
                                with st.expander("📝 Transformation Description", expanded=True):
                                    st.markdown(rendering["rendering_description"])
                        else:
                            st.warning(f"Image generation issue: {rendering.get('error', 'Unknown error')}")

                        # Project Plan
                        if transformation.get("project_plan"):
                            with st.expander("📋 Complete Project Plan", expanded=False):
                                st.markdown(transformation["project_plan"])

                        # Agent Responses Section
                        if 'agent_responses' in st.session_state and st.session_state.agent_responses:
                            st.divider()
                            st.subheader("🤖 Agent Analysis & Planning")

                            agent_tab1, agent_tab2 = st.tabs([
                                "👁️ Visual Assessment Specialist",
                                "📋 Design Project Coordinator"
                            ])

                            with agent_tab1:
                                st.markdown("### Professional Room Assessment")
                                st.info("This is the detailed analysis from our Visual Assessment Specialist agent.")
                                if 'visual_assessor' in st.session_state.agent_responses:
                                    st.markdown(st.session_state.agent_responses['visual_assessor'])
                                else:
                                    st.write("No assessment available yet.")

                            with agent_tab2:
                                st.markdown("### Complete Project Plan")
                                st.info("This is the comprehensive project plan from our Design Project Coordinator agent.")
                                if 'project_coordinator' in st.session_state.agent_responses:
                                    st.markdown(st.session_state.agent_responses['project_coordinator'])
                                else:
                                    st.write("No project plan available yet.")

                        # Budget summary
                        st.divider()
                        st.subheader("💰 Project Summary")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Design Style", transformation.get("design_style", "N/A").title())

                        with col2:
                            st.metric("Budget Range", transformation.get("budget_range", "N/A").title())

                        with col3:
                            st.metric("Room Type", transformation.get("room_type", "N/A").title())

                        # Success message
                        st.balloons()
                        st.success("🎉 Your personalized home design is ready!")

                        # Rerun to update the image in the right column
                        st.rerun()

# Example images section
with st.expander("💡 See Example Transformations"):
        st.write("Here are some example prompts you can try:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**🛋️ Living Room**")
            st.code("Modern minimalist living room with neutral tones, clean lines, and natural light")

        with col2:
            st.write("**🛏️ Bedroom**")
            st.code("Cozy bohemian bedroom with warm earth tones, plants, and textured fabrics")

        with col3:
            st.write("**🏢 Home Office**")
            st.code("Productive workspace with ergonomic furniture, good lighting, and organized storage")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>Powered by Google Gemini Vision & Nano Banana</p>
        <p style='font-size: 0.9rem;'>Upload your room photo and transform it with AI! 🏠✨</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
        main()
