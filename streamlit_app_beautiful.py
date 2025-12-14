"""
Streamlit Home Design Assistant - Beautiful & Simplistic Edition
Upload an image and transform your space with AI
"""
import streamlit as st
import sys
import os
from PIL import Image
import io
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
    page_title="AI Home Designer",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Beautiful Custom CSS
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Content container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 1rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero p {
        font-size: 1.3rem;
        color: #555;
        margin-top: 0;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Image upload area */
    .stFileUploader {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Text areas and inputs */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(102, 126, 234, 0.1);
        padding: 1rem;
        border-radius: 10px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
        background: rgba(102, 126, 234, 0.05);
        border-radius: 10px;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    /* Images */
    img {
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
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

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temp directory"""
    try:
        temp_dir = os.path.join("temp", "uploads")
        os.makedirs(temp_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(temp_dir, f"upload_{timestamp}_{uploaded_file.name}")
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    except Exception as e:
        st.error(f"❌ Error saving file: {str(e)}")
        return None

def analyze_room(image_path):
    """Analyze the uploaded room image"""
    with st.spinner("🔍 Analyzing your room..."):
        try:
            assessor = VisualAssessor()
            analysis = assessor.analyze(image_path)
            
            if "error" in analysis:
                st.error(f"❌ Analysis failed: {analysis['error']}")
                return None
            
            return analysis
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            return None

def transform_room(analysis, design_prompt, design_style, budget_range, image_path):
    """Generate transformation with custom prompt"""
    with st.spinner("🎨 Creating your dream space..."):
        try:
            coordinator = ProjectCoordinator()
            
            project_plan = coordinator.generate_project_plan(
                room_analysis=analysis,
                design_style=design_style,
                budget_range=budget_range,
                reference_image=image_path
            )
            
            return project_plan
        except Exception as e:
            st.error(f"❌ Error during transformation: {str(e)}")
            return None

# Main App
def main():
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>🏠 AI Home Designer</h1>
        <p>Transform your space in seconds with AI-powered design</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Style Presets
    st.markdown("### ✨ Choose Your Style")
    
    style_presets = {
        "🛋️ Cozy Reading Nook": {
            "prompt": "Transform into a cozy reading nook with warm lighting, comfortable seating, built-in bookshelves filled with books, a plush reading chair with ottoman, soft ambient lighting, and warm earth tones",
            "style": "cozy bohemian"
        },
        "🌿 Minimalist Zen": {
            "prompt": "Create a minimalist zen space with natural materials, neutral colors, plants, clean lines, uncluttered surfaces, and calming atmosphere",
            "style": "modern minimalist"
        },
        "🎨 Creative Studio": {
            "prompt": "Design a creative studio with organized storage, good natural lighting, inspiring artwork, comfortable workspace, and vibrant accent colors",
            "style": "contemporary"
        },
        "☕ Coffee Bar Corner": {
            "prompt": "Set up a stylish coffee bar corner with open shelving, cafe-style lighting, coffee equipment display, and cozy seating area",
            "style": "industrial loft"
        },
        "🧘 Meditation Space": {
            "prompt": "Design a meditation space with soft lighting, comfortable floor cushions, natural elements, calming colors, and minimal distractions",
            "style": "scandinavian"
        },
        "✍️ Custom Design": {
            "prompt": "",
            "style": "modern minimalist"
        }
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛋️ Cozy Reading Nook", use_container_width=True):
            st.session_state.selected_preset = "🛋️ Cozy Reading Nook"
    
    with col2:
        if st.button("🌿 Minimalist Zen", use_container_width=True):
            st.session_state.selected_preset = "🌿 Minimalist Zen"
    
    with col3:
        if st.button("🎨 Creative Studio", use_container_width=True):
            st.session_state.selected_preset = "🎨 Creative Studio"
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("☕ Coffee Bar Corner", use_container_width=True):
            st.session_state.selected_preset = "☕ Coffee Bar Corner"
    
    with col5:
        if st.button("🧘 Meditation Space", use_container_width=True):
            st.session_state.selected_preset = "🧘 Meditation Space"
    
    with col6:
        if st.button("✍️ Custom Design", use_container_width=True):
            st.session_state.selected_preset = "✍️ Custom Design"
    
    # Get selected preset
    if 'selected_preset' not in st.session_state:
        st.session_state.selected_preset = "🛋️ Cozy Reading Nook"
    
    selected_preset = st.session_state.selected_preset
    preset_data = style_presets[selected_preset]
    
    st.markdown("---")
    
    # Custom Instructions (if Custom Design selected)
    if selected_preset == "✍️ Custom Design":
        st.markdown("### 📝 Describe Your Dream Space")
        custom_prompt = st.text_area(
            "Tell us exactly what you want:",
            placeholder="Example: Transform into a modern home office with standing desk, plants, natural light, organized storage, and motivational wall art...",
            height=120,
            help="Be specific about colors, furniture, lighting, and atmosphere"
        )
        
        design_style = st.selectbox(
            "Design Style:",
            ["Modern Minimalist", "Cozy Bohemian", "Industrial Loft", "Scandinavian", 
             "Contemporary", "Rustic Farmhouse", "Mid-Century Modern", "Coastal"]
        )
    else:
        st.info(f"**Selected Style:** {selected_preset}\n\n{preset_data['prompt']}")
        custom_prompt = preset_data['prompt']
        design_style = preset_data['style'].title()
    
    # Budget slider
    budget_range = st.select_slider(
        "💰 Budget Range:",
        options=["Low", "Moderate", "High"],
        value="Moderate"
    )
    
    st.markdown("---")
    
    # Main Content Area
    st.markdown("### 📸 Upload & Transform")
    
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("**Original Room**")
        uploaded_file = st.file_uploader(
            "Drop your room photo here",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            image_path = save_uploaded_file(uploaded_file)
            st.session_state.temp_image_path = image_path
            
            if image_path:
                st.success("✅ Image uploaded!")
    
    with col_right:
        st.markdown("**Transformed Design**")
        
        if st.session_state.transformation_result:
            rendering = st.session_state.transformation_result.get("rendering", {})
            
            if rendering.get("success") and rendering.get("image_path"):
                try:
                    transformed_image = Image.open(rendering["image_path"])
                    st.image(transformed_image, use_container_width=True)
                    
                    with open(rendering["image_path"], "rb") as f:
                        st.download_button(
                            label="📥 Download Design",
                            data=f,
                            file_name=f"transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                except Exception as e:
                    st.warning(f"⚠️ Could not display image: {str(e)}")
            else:
                st.info("✨ Your transformed design will appear here")
        else:
            st.info("✨ Your transformed design will appear here")
    
    # Transform Button
    if uploaded_file is not None and custom_prompt.strip():
        st.markdown("---")
        
        if st.button("🎨 Transform My Space Now", type="primary", use_container_width=True):
            # Analysis
            analysis = analyze_room(st.session_state.temp_image_path)
            
            if analysis:
                st.session_state.analysis_result = analysis
                
                # Show quick analysis
                with st.expander("📊 Room Analysis", expanded=False):
                    raw = analysis.get("raw_analysis", {})
                    
                    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
                    
                    with metrics_col1:
                        st.metric("Room Type", raw.get("room_type", "Unknown").title())
                    with metrics_col2:
                        st.metric("Current Style", raw.get("current_style", "Unknown").title())
                    with metrics_col3:
                        st.metric("Condition", raw.get("condition", "Good").title())
                    with metrics_col4:
                        st.metric("Lighting", raw.get("lighting", "Natural").title())
                
                # Transformation
                transformation = transform_room(
                    analysis,
                    custom_prompt,
                    design_style.lower(),
                    budget_range.lower(),
                    st.session_state.temp_image_path
                )
                
                if transformation:
                    st.session_state.transformation_result = transformation
                    
                    rendering = transformation.get("rendering", {})
                    
                    if rendering.get("success"):
                        st.balloons()
                        st.success("🎉 Your design is ready!")
                        
                        # Show details
                        with st.expander("📋 Design Details", expanded=False):
                            if rendering.get("rendering_description"):
                                st.markdown(rendering["rendering_description"])
                            
                            if transformation.get("project_plan"):
                                st.markdown("---")
                                st.markdown("**Complete Project Plan:**")
                                st.markdown(transformation["project_plan"])
                        
                        st.rerun()
                    else:
                        st.error(f"⚠️ Generation issue: {rendering.get('error', 'Unknown error')}")
    
    elif uploaded_file is not None and not custom_prompt.strip():
        st.warning("⚠️ Please select a style preset or write custom instructions above")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: white; padding: 1rem;'>
        <p style='font-size: 0.9rem; opacity: 0.8;'>Powered by Google Gemini Vision & Nano Banana AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()