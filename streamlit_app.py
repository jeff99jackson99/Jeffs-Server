import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Business Management Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .task-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Review Q3 commission reports", "department": "Commissions", "priority": "High", "status": "Pending", "created": datetime.now() - timedelta(days=2)},
        {"id": 2, "title": "Process cancellation request #789", "department": "Cancellations", "priority": "Medium", "status": "In Progress", "created": datetime.now() - timedelta(days=1)},
        {"id": 3, "title": "Update contract templates", "department": "Contract Admin", "priority": "Low", "status": "Pending", "created": datetime.now() - timedelta(hours=6)},
        {"id": 4, "title": "Investigate claim #45678", "department": "Claims", "priority": "Urgent", "status": "In Progress", "created": datetime.now() - timedelta(hours=3)},
        {"id": 5, "title": "Schedule team training session", "department": "Contract Admin", "priority": "Medium", "status": "Pending", "created": datetime.now() - timedelta(hours=1)}
    ]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Main header
st.markdown('<h1 class="main-header">🏢 Business Management Dashboard</h1>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Dashboard", "Task Management", "AI Assistant", "Analytics", "Settings"]
)

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t["status"] == "Completed"])
    pending_tasks = len([t for t in st.session_state.tasks if t["status"] == "Pending"])
    urgent_tasks = len([t for t in st.session_state.tasks if t["priority"] == "Urgent"])
    
    with col1:
        st.metric(
            label="📋 Total Tasks",
            value=total_tasks,
            delta=f"+{total_tasks - 5}"
        )
    
    with col2:
        st.metric(
            label="✅ Completed",
            value=completed_tasks,
            delta=f"+{completed_tasks - 2}"
        )
    
    with col3:
        st.metric(
            label="⏳ Pending",
            value=pending_tasks,
            delta=f"-{pending_tasks - 3}"
        )
    
    with col4:
        st.metric(
            label="🚨 Urgent",
            value=urgent_tasks,
            delta=f"+{urgent_tasks - 1}"
        )
    
    st.markdown("---")
    
    # Recent activity and charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Task Status Distribution")
        
        # Create task status data
        status_data = pd.DataFrame({
            'Status': ['Pending', 'In Progress', 'Completed'],
            'Count': [
                len([t for t in st.session_state.tasks if t["status"] == "Pending"]),
                len([t for t in st.session_state.tasks if t["status"] == "In Progress"]),
                len([t for t in st.session_state.tasks if t["status"] == "Completed"])
            ]
        })
        
        st.bar_chart(status_data.set_index('Status'))
    
    with col2:
        st.subheader("🎯 Priority Breakdown")
        
        priority_data = pd.DataFrame({
            'Priority': ['Low', 'Medium', 'High', 'Urgent'],
            'Count': [
                len([t for t in st.session_state.tasks if t["priority"] == "Low"]),
                len([t for t in st.session_state.tasks if t["priority"] == "Medium"]),
                len([t for t in st.session_state.tasks if t["priority"] == "High"]),
                len([t for t in st.session_state.tasks if t["priority"] == "Urgent"])
            ]
        })
        
        st.bar_chart(priority_data.set_index('Priority'))
    
    # Recent tasks
    st.subheader("📋 Recent Tasks")
    
    recent_tasks = sorted(st.session_state.tasks, key=lambda x: x["created"], reverse=True)[:5]
    
    for task in recent_tasks:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.write(f"**{task['title']}**")
                st.caption(f"Created: {task['created'].strftime('%Y-%m-%d %H:%M')}")
            
            with col2:
                st.write(f"📁 {task['department']}")
            
            with col3:
                priority_colors = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Urgent": "🔴"}
                st.write(f"{priority_colors.get(task['priority'], '⚪')} {task['priority']}")
            
            with col4:
                status_colors = {"Pending": "⏳", "In Progress": "🔄", "Completed": "✅"}
                st.write(f"{status_colors.get(task['status'], '❓')} {task['status']}")

# Task Management Page
elif page == "Task Management":
    st.header("📝 Task Management")
    
    # Create new task
    with st.expander("➕ Create New Task", expanded=True):
        with st.form("task_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                task_title = st.text_input("Task Title", placeholder="Enter task title...")
                task_description = st.text_area("Description", placeholder="Enter task description...")
            
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                department = st.selectbox("Department", ["Claims", "Commissions", "Contract Admin", "Cancellations"])
                due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=7))
            
            submitted = st.form_submit_button("Create Task", type="primary")
            
            if submitted:
                if task_title:
                    new_task = {
                        "id": max([t["id"] for t in st.session_state.tasks]) + 1,
                        "title": task_title,
                        "description": task_description,
                        "department": department,
                        "priority": priority,
                        "status": "Pending",
                        "due_date": due_date,
                        "created": datetime.now()
                    }
                    st.session_state.tasks.append(new_task)
                    st.success(f"✅ Task '{task_title}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a task title")
    
    st.markdown("---")
    
    # Filter and display tasks
    st.subheader("📋 Current Tasks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_dept = st.selectbox("Filter by Department", ["All", "Claims", "Commissions", "Contract Admin", "Cancellations"])
    
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Urgent"])
    
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed"])
    
    # Apply filters
    filtered_tasks = st.session_state.tasks
    
    if filter_dept != "All":
        filtered_tasks = [t for t in filtered_tasks if t["department"] == filter_dept]
    
    if filter_priority != "All":
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == filter_priority]
    
    if filter_status != "All":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == filter_status]
    
    # Display tasks
    if filtered_tasks:
        for task in filtered_tasks:
            with st.container():
                with st.expander(f"📋 {task['title']} - {task['department']}", expanded=False):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**Description:** {task.get('description', 'No description')}")
                        if 'due_date' in task:
                            st.write(f"**Due Date:** {task['due_date']}")
                        st.write(f"**Created:** {task['created'].strftime('%Y-%m-%d %H:%M')}")
                    
                    with col2:
                        priority_colors = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Urgent": "🔴"}
                        st.write(f"{priority_colors.get(task['priority'], '⚪')} **{task['priority']}**")
                    
                    with col3:
                        status_colors = {"Pending": "⏳", "In Progress": "🔄", "Completed": "✅"}
                        st.write(f"{status_colors.get(task['status'], '❓')} **{task['status']}**")
                    
                    with col4:
                        if task['status'] != "Completed":
                            if st.button("Complete", key=f"complete_{task['id']}"):
                                task['status'] = "Completed"
                                st.success(f"✅ Task '{task['title']}' completed!")
                                st.rerun()
                        else:
                            st.write("✅ Completed")
    else:
        st.info("No tasks match the selected filters.")

# AI Assistant Page
elif page == "AI Assistant":
    st.header("🤖 AI Assistant")
    
    st.markdown("Ask me anything about your business processes, contracts, or policies!")
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response based on keywords
        with st.chat_message("assistant"):
            response = generate_ai_response(prompt)
            st.markdown(response)
        
        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 How do I process a new claim?"):
            response = """
            **Claim Processing Steps:**
            1. 📄 Receive claim documentation
            2. ✅ Verify policy coverage
            3. 🔢 Assign claim number
            4. 👨‍💼 Review by adjuster
            5. 💰 Process payment (5-7 business days)
            """
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("💰 What's the commission rate?"):
            response = """
            **Commission Rates:**
            - 🥉 Standard: 12.5%
            - 🥈 Premium: 15.0%
            - 🔄 Renewal: 10.0%
            - 🆕 New Business: 20.0%
            """
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📝 Contract modification process?"):
            response = """
            **Contract Modifications:**
            1. 📝 Submit modification request
            2. ⚖️ Legal team review (2-3 days)
            3. ✅ Client approval required
            4. 📊 Update system records
            5. 📧 Send confirmation
            """
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Analytics Page
elif page == "Analytics":
    st.header("📊 Analytics & Reports")
    
    # Department performance
    st.subheader("🏢 Department Performance")
    
    dept_data = {}
    for task in st.session_state.tasks:
        dept = task["department"]
        if dept not in dept_data:
            dept_data[dept] = {"total": 0, "completed": 0, "pending": 0}
        dept_data[dept]["total"] += 1
        if task["status"] == "Completed":
            dept_data[dept]["completed"] += 1
        else:
            dept_data[dept]["pending"] += 1
    
    if dept_data:
        dept_df = pd.DataFrame(dept_data).T
        dept_df["completion_rate"] = (dept_df["completed"] / dept_df["total"] * 100).round(1)
        
        st.dataframe(dept_df)
        
        # Chart
        st.subheader("📈 Completion Rates by Department")
        st.bar_chart(dept_df["completion_rate"])
    
    # Task trends
    st.subheader("📅 Task Creation Trends")
    
    # Create sample trend data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    trend_data = pd.DataFrame({
        'Date': dates,
        'Tasks Created': [max(1, int(pd.np.random.normal(3, 1))) for _ in range(len(dates))],
        'Tasks Completed': [max(0, int(pd.np.random.normal(2.5, 1))) for _ in range(len(dates))]
    })
    
    st.line_chart(trend_data.set_index('Date'))

# Settings Page
elif page == "Settings":
    st.header("⚙️ Settings")
    
    st.subheader("🎨 Appearance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Theme", ["Light", "Dark", "Auto"])
        st.selectbox("Language", ["English", "Spanish", "French"])
    
    with col2:
        st.selectbox("Timezone", ["UTC", "EST", "PST", "CST"])
        st.number_input("Items per page", min_value=10, max_value=100, value=25)
    
    st.markdown("---")
    
    st.subheader("🔔 Notifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Email notifications", value=True)
        st.checkbox("Task reminders", value=True)
    
    with col2:
        st.checkbox("Weekly reports", value=False)
        st.checkbox("Urgent task alerts", value=True)
    
    st.markdown("---")
    
    st.subheader("🗑️ Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Chat History", type="secondary"):
            st.session_state.messages = []
            st.success("Chat history cleared!")
    
    with col2:
        if st.button("Reset All Tasks", type="secondary"):
            st.session_state.tasks = []
            st.success("All tasks reset!")
            st.rerun()

# Helper function for AI responses
def generate_ai_response(prompt):
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["contract", "agreement"]):
        return """
        **Contract Information:**
        
        I can help you with contract-related questions! Here's what I know:
        
        📋 **Standard Contract Types:**
        - Service agreements
        - Insurance policies
        - Commission contracts
        - Cancellation agreements
        
        ⏱️ **Processing Times:**
        - New contracts: 3-5 business days
        - Modifications: 2-3 business days
        - Renewals: 1-2 business days
        
        📞 **Need Help?** Contact the legal team for complex contract questions.
        """
    
    elif any(word in prompt_lower for word in ["commission", "payment", "money"]):
        return """
        **Commission Information:**
        
        💰 **Current Commission Structure:**
        - Standard policies: 12.5%
        - Premium policies: 15.0%
        - Renewals: 10.0%
        - New business: 20.0%
        
        📊 **Payment Schedule:**
        - Monthly commission runs: 15th of each month
        - Processing time: 3-5 business days
        - Minimum payout: $100
        
        📈 **Performance Bonuses:**
        - Quarterly targets: 10% bonus
        - Annual targets: 25% bonus
        """
    
    elif any(word in prompt_lower for word in ["claim", "damage", "loss"]):
        return """
        **Claims Processing:**
        
        🚨 **Urgent Claims (< 24 hours):**
        - Fire damage
        - Water damage
        - Theft/loss
        
        ⏱️ **Standard Processing:**
        - Initial review: 24-48 hours
        - Investigation: 5-7 business days
        - Payment processing: 3-5 business days
        
        📋 **Required Documentation:**
        - Incident report
        - Police report (if applicable)
        - Photos/videos
        - Repair estimates
        
        📞 **Need Assistance?** Contact the claims department.
        """
    
    elif any(word in prompt_lower for word in ["cancel", "terminate", "end"]):
        return """
        **Cancellation Process:**
        
        📝 **Cancellation Types:**
        - Policyholder request
        - Non-payment
        - Fraud
        - Policy violation
        
        ⏱️ **Processing Time:**
        - Standard cancellation: 3-5 business days
        - Refund processing: 5-7 business days
        
        💰 **Refund Calculation:**
        - Pro-rated refund based on unused coverage
        - Minus any fees or penalties
        - Processing fee: $25
        
        📞 **Questions?** Contact the cancellations department.
        """
    
    else:
        return """
        **General Business Information:**
        
        I'm here to help with your business questions! I can assist with:
        
        📋 **Task Management**
        📊 **Analytics & Reporting**
        💰 **Commission Information**
        📝 **Contract Procedures**
        🚨 **Claims Processing**
        ❌ **Cancellation Procedures**
        
        Feel free to ask me anything specific about these areas, or use the quick action buttons above for common questions!
        """

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🏢 **Business Management Dashboard** | Built with Streamlit | Version 2.0 | 
    <a href='#' style='color: #1f77b4;'>Help</a> | 
    <a href='#' style='color: #1f77b4;'>Support</a>
</div>
""", unsafe_allow_html=True)
