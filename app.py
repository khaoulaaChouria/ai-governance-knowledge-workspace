import json
import streamlit as st

from services.pdf_reader import extract_text
from services.entity_extractor import extract_entities
from services.storage import save_entities
from services.knowledge_repository import get_documents
from services.knowledge_explorer import (
    get_all_entities,
    search_entities
)
from services.rag_service import ask_knowledge_base
from services.dashboard_service import get_dashboard_data

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Governance Knowledge Workspace",
    layout="wide"
)

st.title("AI Governance Knowledge Workspace")

st.write(
    "Upload business documents to build your organization's governance knowledge base."
)

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Upload Document",
        "📚 Knowledge Repository",
        "🧠 Knowledge Explorer",
        "🤖 AI Assistant"
    ]
)

# ==================================================
# PAGE 0 - Dashboard
# ==================================================

if page == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    st.write(
        "Welcome to the AI Governance Knowledge Workspace."
    )

    dashboard = get_dashboard_data()

    # ---------------------------------------------
    # Metrics
    # ---------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📄 Documents",
        dashboard["total_documents"]
    )

    col2.metric(
        "🧠 Entities",
        dashboard["total_entities"]
    )

    col3.metric(
        "📂 Categories",
        dashboard["total_categories"]
    )

    col4.metric(
        "🤖 AI Assistant",
        "Ready"
    )

    st.divider()

    # ---------------------------------------------
    # Knowledge Distribution
    # ---------------------------------------------

    st.subheader("📊 Knowledge Distribution")

    if dashboard["category_distribution"]:

        st.bar_chart(
            dashboard["category_distribution"]
        )

    else:

        st.info("No knowledge available yet.")

    st.divider()

    # ---------------------------------------------
    # Recent Documents
    # ---------------------------------------------

    st.subheader("📚 Recent Documents")

    if dashboard["recent_documents"]:

        for document in reversed(
            dashboard["recent_documents"]
        ):

            st.write(f"📄 {document}")

    else:

        st.info("No documents uploaded yet.")

    st.divider()

    # ---------------------------------------------
    # Quick Actions
    # ---------------------------------------------

    st.subheader("🚀 Quick Actions")

    st.info(
        """
• Upload governance documents

• Explore extracted knowledge

• Search governance entities

• Ask the AI Assistant questions
"""
    )

# ==================================================
# PAGE 1 - Upload Document
# ==================================================

if page == "📄 Upload Document":

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success(f"Uploaded: {uploaded_file.name}")

        with st.spinner("Extracting text..."):
            text = extract_text(uploaded_file)

        with st.spinner("Extracting governance knowledge..."):
            entities = extract_entities(text)

        save_entities(uploaded_file.name, entities)

        st.success("Knowledge extracted successfully.")

        st.subheader("Extracted Entities")

        st.json(entities)

        st.download_button(
            label="📥 Download Knowledge Base (JSON)",
            data=json.dumps(
                entities,
                indent=4,
                ensure_ascii=False
            ),
            file_name=f"{uploaded_file.name.replace('.pdf', '')}.json",
            mime="application/json"
        )

# ==================================================
# PAGE 2 - Knowledge Repository
# ==================================================

elif page == "📚 Knowledge Repository":

    st.header("📚 Knowledge Repository")

    documents = get_documents()

    if not documents:
        st.info("No knowledge documents found.")

    else:

        st.success(f"{len(documents)} document(s) found.")

        for document in documents:

            data = document["data"]

            total_entities = sum(
                len(items)
                for items in data.values()
                if isinstance(items, list)
            )

            non_empty_categories = sum(
                1
                for items in data.values()
                if isinstance(items, list) and len(items) > 0
            )

            with st.expander(f"📄 {document['name']}"):

                st.write(f"**Total Entities:** {total_entities}")
                st.write(f"**Categories Used:** {non_empty_categories}")

                st.divider()

                st.subheader("Category Summary")

                for category, items in data.items():

                    if isinstance(items, list) and len(items) > 0:

                        st.write(f"**{category}** : {len(items)}")

                st.divider()

                st.subheader("Extracted JSON")

                st.json(data)

# ==================================================
# PAGE 3 - Knowledge Explorer
# ==================================================

elif page == "🧠 Knowledge Explorer":

    st.header("🧠 Knowledge Explorer")

    # ------------------------------
    # Search
    # ------------------------------

    search = st.text_input(
        "🔍 Search",
        placeholder="Search by entity name or description..."
    )

    if search:

        knowledge = search_entities(search)

    else:

        knowledge = get_all_entities()

    if not knowledge:

        st.info("No matching knowledge found.")

    else:

        # ------------------------------
        # Sidebar Category Filter
        # ------------------------------

        categories = ["All Categories"] + sorted(knowledge.keys())

        selected_category = st.sidebar.selectbox(
            "📂 Browse Categories",
            categories
        )

        if selected_category != "All Categories":

            knowledge = {
                selected_category: knowledge[selected_category]
            }

        total_entities = sum(
            len(items)
            for items in knowledge.values()
        )

        st.success(
            f"{len(knowledge)} categories • {total_entities} entities"
        )

        # ------------------------------
        # Display Knowledge
        # ------------------------------

        for category, entities in knowledge.items():

            st.subheader(
                f"{category.replace('_', ' ').title()} ({len(entities)})"
            )

            for entity in entities:

                with st.container(border=True):

                    st.markdown(
                        f"### {entity['name']}"
                    )

                    st.markdown("**Description**")

                    st.write(entity["description"])

                    st.markdown("**Source Documents**")

                    for document in entity["documents"]:

                        st.write(f"• {document}")

                    if entity.get("source_text"):

                        with st.expander("📄 View Source Text"):

                            st.write(entity["source_text"])

            st.divider()



# ==================================================
# PAGE 4 - AI Governance Assistant
# ==================================================

elif page == "🔍 Semantic Search":

    st.header("🤖 AI Governance Assistant")

    st.write(
        "Ask questions about your organization's AI governance knowledge base."
    )

    st.divider()

    # --------------------------------------------
    # Chat History
    # --------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous conversation

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and "sources" in message
                and message["sources"]
            ):

                with st.expander("📚 Sources Used"):

                    for source in message["sources"]:

                        with st.container(border=True):

                            st.markdown(
                                f"### {source['name']}"
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(
                                    f"**Category:** {source['category']}"
                                )

                            with col2:
                                st.write(
                                    f"**Document:** {source['document']}"
                                )

                            st.write(
                                f"**Description:** {source['description']}"
                            )

                            if source.get("source_text"):

                                with st.expander("View Source Text"):

                                    st.write(source["source_text"])

                            st.caption(
                                f"Similarity Distance: {source['distance']:.3f}"
                            )

    # --------------------------------------------
    # Chat Input
    # --------------------------------------------

    query = st.chat_input(
        "Ask a question about AI governance..."
    )

    if query:

        # -------------------------
        # User Message
        # -------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):

            st.markdown(query)

        # -------------------------
        # Assistant Response
        # -------------------------

        with st.chat_message("assistant"):

            with st.spinner("Searching the knowledge base..."):

                result = ask_knowledge_base(query)

            st.markdown(result["answer"])

            if result["sources"]:

                with st.expander("📚 Sources Used"):

                    for source in result["sources"]:

                        with st.container(border=True):

                            st.markdown(
                                f"### {source['name']}"
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(
                                    f"**Category:** {source['category']}"
                                )

                            with col2:
                                st.write(
                                    f"**Document:** {source['document']}"
                                )

                            st.write(
                                f"**Description:** {source['description']}"
                            )

                            if source.get("source_text"):

                                with st.expander("View Source Text"):

                                    st.write(source["source_text"])

                            st.caption(
                                f"Similarity Distance: {source['distance']:.3f}"
                            )

        # -------------------------
        # Save Assistant Response
        # -------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"]
            }
        )