import tempfile
import streamlit as st
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    st.sidebar.markdown("---")

def render_solution_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Image Upload
    with col1:
        st.subheader("📷 Upload LeetCode Question")
        uploaded_image = st.file_uploader(
            "Upload a screenshot of your LeetCode problem",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Solution Preferences
    with col2:
        st.subheader("💡 Solution Preferences")
        solution_language = st.selectbox(
            "Preferred programming language for the solution:",
            ["Python", "C++", "Java", "JavaScript"]
        )
        solution_style = st.selectbox(
            "Solution style:",
            ["Concise & efficient", "Detailed & step-by-step", "Beginner-friendly", "Best practices"]
        )

    # Column 3: Explanation Preferences
    with col3:
        st.subheader("📝 Explanation Preferences")
        explanation_depth = st.selectbox(
            "Explanation depth:",
            ["High-level summary", "Line-by-line walkthrough", "Concept-focused", "With sample test cases"]
        )
        extra_material = st.selectbox(
            "Would you like additional learning material?",
            ["No, just the explanation", "Relevant links", "Similar problems", "Time & space complexity analysis"]
        )

    return {
        "uploaded_image": uploaded_image,
        "solution_language": solution_language,
        "solution_style": solution_style,
        "explanation_depth": explanation_depth,
        "extra_material": extra_material
    }

def generate_solution(solution_preferences): 
    # Save uploaded image to a temporary file
    uploaded_image = solution_preferences["uploaded_image"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    solution_language = solution_preferences["solution_language"]
    solution_style = solution_preferences["solution_style"]
    explanation_depth = solution_preferences["explanation_depth"]
    extra_material = solution_preferences["extra_material"] 

    leetcode_solver_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="LeetCode Solver",
        role="Reads LeetCode problem screenshots and generates optimized solutions with explanations.",
        description=(
            "You're a coding assistant trained to interpret visual LeetCode problem statements "
            "from screenshots and generate clean, working solutions based on user preferences. "
            "You also explain the logic in a clear, instructional format."
        ),
        instructions=[
            "First, read and understand the problem shown in the uploaded image.",
            "Use the user's preferred programming language and solution style.",
            "Generate a correct, complete, and readable solution to the problem.",
            "After the code, include a clear explanation based on the selected explanation depth.",
            "If requested, include additional content like time and space complexity, similar problems, or external links.",
            "Format the output cleanly with markdown code blocks and bullet points where appropriate.",
            "Always structure your response using the following format:\n\n"
            "### 💻 Solution\n"
            "```<language>\n<your code here>\n```\n\n"
            "### 📘 Explanation\n"
            "<Step-by-step explanation or walkthrough here>",
            "Do not hallucinate or fabricate constraints or test cases not shown in the problem unless explicitly asked."
        ],
        markdown=True
    )

    prompt = f"""
    A user has uploaded a screenshot of a LeetCode problem and would like your help solving it.

    Please write a solution in **{solution_language}**, using a **{solution_style.lower()}** approach.

    After the solution, provide a(n) **{explanation_depth.lower()}** explanation of the logic.

    Also include **{extra_material.lower()}** if relevant.
    """

    response = leetcode_solver_agent.run(prompt.strip(), images=[Image(filepath=image_path)])
    solution = response.content 

    return solution

def main() -> None:
    # Page config
    st.set_page_config(page_title="LeetCode Solver Bot", page_icon="💻", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>💻 LeetCode Solver Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to LeetCode Solver Bot — a smart Streamlit tool that transforms LeetCode question screenshots into clean, optimized code solutions with step-by-step logic explanations to boost your problem-solving skills.",
        unsafe_allow_html=True
    )

    render_sidebar()
    solution_preferences = render_solution_preferences()

    st.markdown("---")

    # UI button to trigger solution generation
    if st.button("🚀 Generate Solution"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not solution_preferences["uploaded_image"]:
            st.error("Please upload a LeetCode problem screenshot to proceed.")
        else:
            with st.spinner("Generating solution and explanation..."):
                solution = generate_solution(solution_preferences)

                # Save results to session state
                st.session_state.solution = solution
                st.session_state.image = solution_preferences["uploaded_image"]

    # Display result if available
    if "solution" in st.session_state and "image" in st.session_state:
            
        st.markdown("## 🖼️ Uploaded Image")
        st.image(st.session_state.image, use_container_width=False)

        st.markdown("## 💡 Generated Solution & Explanation")
        st.markdown(st.session_state.solution)

        st.markdown("---")

        st.download_button(
            label="📥 Download Solution",
            data=st.session_state.solution,
            file_name="leetcode_solution.md",
            mime="text/markdown"
        )



if __name__ == "__main__":
    main()

