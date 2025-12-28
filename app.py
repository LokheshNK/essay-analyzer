import os
import random
from flask import Flask, render_template, request, jsonify
from google import genai  # New SDK import

app = Flask(__name__)

# Use environment variable for security (recommended)
# Or keep hard-coded for quick testing (remove in production!)
client = genai.Client()  # and set $env:GEMINI_API_KEY in PowerShell

# Configure Gemini API (set your API key as an environment variable: export GEMINI_API_KEY='your_api_key_here')

# List of 50 diverse essay topics (sourced from various categories)
topics = [
    "AI in Classrooms: Help or Hindrance?",
    "Teen Mental Health and Social Media Algorithms",
    "Fast Fashion vs. Sustainability: Who Pays the Real Price?",
    "Financial Literacy: Should It Be a Required High School Course?",
    "Remote & Hybrid Learning: What Should Stay?",
    "Data Privacy: How Much Should Apps Know About Us?",
    "E-Sports in Schools: Hobby or Legitimate Sport?",
    "Climate Action: Individual Choices vs. Policy Change",
    "News Literacy: Can Students Spot Misinformation?",
    "Gig Work & Micro-Internships: A New Path for Students?",
    "The Role of Drones in Modern Society",
    "How Video Games Influence Problem-Solving Skills",
    "Should Self-Driving Cars Be Allowed on All Roads?",
    "The Future of Artificial Organs in Medicine",
    "How Wearable Devices Affect Health Awareness",
    "The Impact of Space Tourism on Society",
    "Should Genetic Data Be Shared with Governments?",
    "How Coding Has Become a Modern Literacy Skill",
    "The Role of Robotics in Disaster Relief",
    "How Renewable Tech Is Changing Home Design",
    "Should Zoos Be Replaced by Wildlife Sanctuaries?",
    "The Impact of Urban Air Pollution on Children",
    "How Community Gardens Promote Sustainability",
    "Should Plastic Bags Be Completely Banned?",
    "The Role of Oceans in Regulating Global Climate",
    "How Wildfires Affect Local Communities",
    "Should Meat Consumption Be Reduced for the Planet?",
    "The Importance of Reforestation Programs",
    "How Renewable Energy Shapes Rural Economies",
    "Should Littering Fines Be Increased Worldwide?",
    "How Street Art Reflects Social Issues",
    "Should Schools Teach More About Local Folklore?",
    "The Role of Storytelling in Preserving History",
    "How Sports Celebrities Influence Teen Culture",
    "Should TV Shows Have Cultural Sensitivity Guidelines?",
    "The Impact of Cultural Festivals on Tourism",
    "How Photography Changes Perceptions of Reality",
    "Should More Schools Encourage Debate Clubs?",
    "The Role of Humor in Bringing Cultures Together",
    "How Fashion Reflects Social Identity",
    "Should Student Voting Be Allowed in School Decisions?",
    "How Political Debates Affect Young Voters",
    "The Role of Education in Reducing Poverty",
    "Should Teachers Have More Say in Policy-Making?",
    "How Scholarships Encourage Equal Access to Education",
    "The Role of Political Campaigns in Shaping Opinions",
    "Should More Schools Offer Classes on Media Literacy?",
    "How Education Systems Prepare Students for Democracy",
    "The Importance of Fair Representation in Politics",
    "Should International Students Pay the Same Fees as Locals?"
]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_topic', methods=['GET'])
def get_topic():
    topic = random.choice(topics)
    return jsonify({'topic': topic})

# ... (keep everything at the top the same: imports, app, client, topics list, routes / and /get_topic)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    essay = data.get('essay')
    topic = data.get('topic', '')  # Get the current topic from frontend

    if not essay:
        return jsonify({'error': 'No essay provided'}), 400
    
    # Build prompt with topic for better relevance checking
    prompt = (
        "Analyze this student essay in detail. The essay topic is: \"{topic}\"\n\n"
        "Output ONLY valid JSON with these exact keys:\n"
        "{\n"
        "  'ratings': {\n"
        "    'grammar': number,\n"
        "    'structure': number,\n"
        "    'content': number,\n"
        "    'coherence': number,\n"
        "    'originality': number,\n"
        "    'topic_relevance': number,  // NEW: How well the essay stays on/sticks to the given topic (0-10)\n"
        "    'overall': number\n"
        "  },\n"
        "  'strengths': [ /* 3-7 bullet points */ ],\n"
        "  'weaknesses': [ /* 3-7 bullet points */ ],\n"
        "  'detailed_comments': {\n"
        "    'grammar': 'string',\n"
        "    'structure': 'string',\n"
        "    'content': 'string',\n"
        "    'coherence': 'string',\n"
        "    'originality': 'string',\n"
        "    'topic_relevance': 'Detailed feedback on how well the essay addresses the topic'\n"
        "  },\n"
        "  'suggestions': [ /* 4-6 strings */ ],\n"
        "  'word_count_feedback': 'string',\n"
        "  'key_insights': [ /* 2-4 strings */ ]\n"
        "}\n\n"
        "Essay:\n" + essay
    ).format(topic=topic)  # Inject the actual topic

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Stable & fast
            contents=prompt
        )
        analysis_json = response.text.strip()
        if analysis_json.startswith('```json'):
            analysis_json = analysis_json[7:-3].strip()

        return jsonify({'analysis': analysis_json})
    except Exception as e:
        return jsonify({'analysis': f"Error from Gemini API: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=8001)