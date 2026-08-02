"""Seed the database with initial content: tutorials, lessons, challenges, and badges.

Usage:
    python seed.py
"""
import json

from app import create_app, db
from app.models import Badge, Challenge, Lesson, Tutorial


def seed_tutorials():
    tutorials_data = [
        {
            "slug": "ai-fundamentals",
            "title": "AI Fundamentals",
            "description": "Understand what AI really is, its history, types, and real-world applications.",
            "icon": "🤖",
            "color": "#6366f1",
            "difficulty": "beginner",
            "order_index": 1,
            "estimated_minutes": 30,
            "lessons": [
                {
                    "title": "What is Artificial Intelligence?",
                    "slug": "what-is-ai",
                    "order_index": 1,
                    "estimated_minutes": 5,
                    "xp_reward": 20,
                    "content": """
<h2>Welcome to AI Fundamentals! 🚀</h2>
<p>Before we dive into code, let's answer the most important question: <strong>What is Artificial Intelligence (AI)?</strong></p>
<blockquote>Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think, learn, and make decisions.</blockquote>
<h3>Key Ideas</h3>
<ul>
    <li><strong>AI</strong> is a broad field focused on building intelligent machines.</li>
    <li>It includes subfields like <strong>Machine Learning</strong>, <strong>NLP</strong>, <strong>Computer Vision</strong>, and <strong>Robotics</strong>.</li>
    <li>AI systems learn from <strong>data</strong> to make predictions or decisions.</li>
</ul>
<h3>Examples You Use Every Day</h3>
<ul>
    <li>📱 <strong>Recommendation systems</strong> (Netflix, YouTube)</li>
    <li>🗣 <strong>Voice assistants</strong> (Siri, Alexa, Google Assistant)</li>
    <li>📧 <strong>Spam filters</strong> in your email</li>
    <li>🗺 <strong>Navigation apps</strong> that predict traffic</li>
</ul>
<h3>Types of AI</h3>
<table>
    <tr><th>Type</th><th>Description</th><th>Example</th></tr>
    <tr><td>Narrow AI</td><td>Specialized in one task</td><td>Chess engines, chatbots</td></tr>
    <tr><td>General AI</td><td>Human-level intelligence</td><td>Still theoretical</td></tr>
    <tr><td>Super AI</td><td>Beyond human intelligence</td><td>Science fiction</td></tr>
</table>
<p>Most of the AI we use today is <strong>Narrow AI</strong> — extremely good at one specific thing.</p>
<h3>Key Takeaway</h3>
<p>AI is about building systems that can <strong>perceive</strong>, <strong>reason</strong>, and <strong>act</strong>. Now that you understand the basics, let's explore how machines actually learn!</p>
""",
                },
                {
                    "title": "How Machines Learn",
                    "slug": "how-machines-learn",
                    "order_index": 2,
                    "estimated_minutes": 7,
                    "xp_reward": 25,
                    "content": """
<h2>How Do Machines Learn? 🧠</h2>
<p>The magic of modern AI comes from <strong>Machine Learning (ML)</strong> — the ability for computers to learn patterns from data <em>without being explicitly programmed</em>.</p>
<h3>The Traditional Approach</h3>
<p>In traditional programming, you write rules:</p>
<pre><code>if temperature > 30:
    print("It's hot!")
else:
    print("It's cool!")</code></pre>
<h3>The Machine Learning Approach</h3>
<p>In ML, you provide <strong>data</strong> and let the model figure out the rules:</p>
<pre><code># Input: many (temperature, feeling) examples
data = [(25, "cool"), (32, "hot"), (28, "hot"), (20, "cool")]

# The ML model learns the boundary automatically!</code></pre>
<h3>Three Types of ML</h3>
<ol>
    <li><strong>Supervised Learning</strong> — Learn from labeled examples (e.g., spam detection).</li>
    <li><strong>Unsupervised Learning</strong> — Find patterns in unlabeled data (e.g., customer grouping).</li>
    <li><strong>Reinforcement Learning</strong> — Learn by trial and error with rewards (e.g., game playing).</li>
</ol>
<h3>Key Concept: Features & Labels</h3>
<ul>
    <li><strong>Features</strong> are the inputs (what you observe).</li>
    <li><strong>Labels</strong> are the outputs (what you predict).</li>
</ul>
<pre><code># House price prediction
features = [area_sqft, bedrooms, location_quality]
label = price</code></pre>
<h3>Takeaway</h3>
<p>Machine learning = <strong>data + algorithm</strong>. The more quality data, the better the model — this is why data is often called "the new oil". 🛢️</p>
""",
                },
                {
                    "title": "Applications of AI",
                    "slug": "ai-applications",
                    "order_index": 3,
                    "estimated_minutes": 5,
                    "xp_reward": 20,
                    "content": """
<h2>AI Is Everywhere 🌍</h2>
<p>Let's look at real-world AI applications across different industries.</p>
<h3>🏥 Healthcare</h3>
<ul>
    <li>AI diagnoses diseases from medical images.</li>
    <li>Predicts patient outcomes and suggests treatments.</li>
    <li>Accelerates drug discovery.</li>
</ul>
<h3>💰 Finance</h3>
<ul>
    <li>Fraud detection in real-time transactions.</li>
    <li>Algorithmic trading and risk assessment.</li>
    <li>Personalized financial advice (robo-advisors).</li>
</ul>
<h3>🚗 Transportation</h3>
<ul>
    <li>Self-driving cars use computer vision + deep learning.</li>
    <li>Route optimization and traffic prediction.</li>
</ul>
<h3>🎮 Entertainment</h3>
<ul>
    <li>Game AI opponents (AlphaGo, chess engines).</li>
    <li>Content recommendation (Netflix, Spotify).</li>
    <li>Procedural content generation.</li>
</ul>
<h3>📚 Education (like this platform!)</h3>
<ul>
    <li>Personalized learning paths based on student progress.</li>
    <li>Automated grading and instant feedback.</li>
    <li>AI tutors available 24/7.</li>
</ul>
<h3>Key Takeaway</h3>
<p>AI is transforming every industry. Learning AI now positions you at the forefront of this revolution. 💪</p>
""",
                },
            ],
        },
        {
            "slug": "python-for-ai",
            "title": "Python for AI",
            "description": "Learn the Python essentials every AI developer needs — from variables to functions.",
            "icon": "🐍",
            "color": "#10b981",
            "difficulty": "beginner",
            "order_index": 2,
            "estimated_minutes": 35,
            "lessons": [
                {
                    "title": "Getting Started with Python",
                    "slug": "python-basics",
                    "order_index": 1,
                    "estimated_minutes": 6,
                    "xp_reward": 20,
                    "content": """
<h2>Python: The Language of AI 🐍</h2>
<p>Python is the most popular language for AI and data science. Here's why:</p>
<ul>
    <li>✅ Simple, readable syntax</li>
    <li>✅ Huge ecosystem (NumPy, Pandas, PyTorch, TensorFlow)</li>
    <li>✅ Great community and documentation</li>
</ul>
<h3>Your First Program</h3>
<pre><code># This is a comment
print("Hello World with AI!")  # Output: Hello World with AI!</code></pre>
<h3>Variables & Data Types</h3>
<pre><code>name = "Alice"        # string
age = 16              # integer
height = 5.7          # float
is_learning = True    # boolean

print(f"{name} is {age} years old")</code></pre>
<h3>Basic Operations</h3>
<pre><code># Arithmetic
sum = 10 + 5          # 15
diff = 10 - 5         # 5
prod = 10 * 5         # 50
quot = 10 / 5         # 2.0
power = 2 ** 3        # 8

# Comparison
print(10 > 5)         # True
print(10 == 5)        # False</code></pre>
<h3>Lists (very important in AI!)</h3>
<pre><code># A list of numbers
data = [1, 2, 3, 4, 5]
print(data[0])        # 1
print(data[-1])       # 5
data.append(6)        # [1, 2, 3, 4, 5, 6]
print(len(data))      # 6</code></pre>
<p>Data in AI is almost always stored as lists or arrays. Master them well!</p>
""",
                },
                {
                    "title": "Control Flow & Loops",
                    "slug": "control-flow",
                    "order_index": 2,
                    "estimated_minutes": 7,
                    "xp_reward": 25,
                    "content": """
<h2>Making Decisions & Repeating Tasks 🔁</h2>
<h3>If Statements</h3>
<pre><code>score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Your grade: {grade}")</code></pre>
<h3>For Loops</h3>
<pre><code># Iterate over a list
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
print(total)  # 15</code></pre>
<h3>While Loops</h3>
<pre><code>count = 0
while count < 5:
    print(count)
    count += 1</code></pre>
<h3>List Comprehensions (Pythonic!)</h3>
<pre><code># Get squares of even numbers
numbers = [1, 2, 3, 4, 5, 6]
squares = [n ** 2 for n in numbers if n % 2 == 0]
print(squares)  # [4, 16, 36]</code></pre>
<h3>Why This Matters for AI</h3>
<p>Loops are how we <strong>process datasets</strong> — iterating over training examples, features, and predictions. List comprehensions are especially common in ML code.</p>
""",
                },
                {
                    "title": "Functions & Modules",
                    "slug": "functions",
                    "order_index": 3,
                    "estimated_minutes": 7,
                    "xp_reward": 25,
                    "content": """
<h2>Reusable Code: Functions 📦</h2>
<p>Functions let you package logic into reusable blocks — essential for building ML models.</p>
<h3>Defining Functions</h3>
<pre><code>def greet(name):
    \"\"\"Return a greeting message.\"\"\"
    return f"Hello, {name}!"

print(greet("AI Learner"))  # Hello, AI Learner!</code></pre>
<h3>Default Parameters</h3>
<pre><code>def multiply(a, b=2):
    return a * b

print(multiply(5))    # 10 (b defaults to 2)
print(multiply(5, 3)) # 15</code></pre>
<h3>Lambda Functions</h3>
<pre><code># Short anonymous functions
square = lambda x: x ** 2
print(square(4))  # 16</code></pre>
<h3>Importing Modules</h3>
<pre><code>import math
print(math.sqrt(16))  # 4.0

from random import randint
print(randint(1, 6))  # random dice roll</code></pre>
<h3>Building a Simple Predictor</h3>
<pre><code>def predict_grade(hours_studied):
    if hours_studied >= 5:
        return "Great"
    elif hours_studied >= 3:
        return "Good"
    else:
        return "Needs work"

print(predict_grade(6))  # Great</code></pre>
<p>Functions are the building blocks of every AI library. Next, we'll build real AI models!</p>
""",
                },
            ],
        },
        {
            "slug": "machine-learning-basics",
            "title": "Machine Learning Basics",
            "description": "Core ML concepts: regression, classification, and the training workflow.",
            "icon": "📈",
            "color": "#f59e0b",
            "difficulty": "intermediate",
            "order_index": 3,
            "estimated_minutes": 40,
            "lessons": [
                {
                    "title": "Supervised Learning & Regression",
                    "slug": "regression-intro",
                    "order_index": 1,
                    "estimated_minutes": 8,
                    "xp_reward": 30,
                    "content": """
<h2>Predicting Numbers: Linear Regression 📈</h2>
<p><strong>Regression</strong> is a supervised learning task where we predict a <strong>continuous number</strong> — like price, temperature, or score.</p>
<h3>The Line Equation</h3>
<pre><code>y = m * x + b

# y = predicted value
# m = slope
# x = feature (input)
# b = intercept</code></pre>
<h3>Example: Predicting Study Score</h3>
<p>Given hours studied, predict exam score. The model learns the best <code>m</code> and <code>b</code>.</p>
<pre><code>hours = [1, 2, 3, 4, 5]
scores = [50, 55, 65, 70, 80]

# Best fit line (approximately): score = 7.5 * hours + 42.5
# For 6 hours: 7.5 * 6 + 42.5 = 87.5</code></pre>
<h3>How the Model "Learns"</h3>
<ol>
    <li>Start with random <code>m</code> and <code>b</code>.</li>
    <li>Make predictions and calculate the <strong>error</strong>.</li>
    <li>Adjust <code>m</code> and <code>b</code> to reduce error.</li>
    <li>Repeat until the error is small.</li>
</ol>
<h3>Measuring Quality: R² Score</h3>
<ul>
    <li><strong>R² = 1</strong>: perfect prediction.</li>
    <li><strong>R² = 0</strong>: model is no better than the mean.</li>
    <li><strong>R² < 0</strong>: model is worse than the mean.</li>
</ul>
<p>Try the <strong>Linear Regression demo</strong> in the AI Playground to see this in action!</p>
""",
                },
                {
                    "title": "Classification & the Perceptron",
                    "slug": "classification-perceptron",
                    "order_index": 2,
                    "estimated_minutes": 8,
                    "xp_reward": 30,
                    "content": """
<h2>Predicting Categories: Classification 🏷</h2>
<p><strong>Classification</strong> predicts a <strong>category</strong> — spam/not-spam, cat/dog, pass/fail.</p>
<h3>The Perceptron: The Simplest Neural Network</h3>
<p>A perceptron takes inputs, multiplies them by <strong>weights</strong>, adds a <strong>bias</strong>, and decides the output.</p>
<pre><code>def perceptron(inputs, weights, bias):
    total = bias + sum(w * x for w, x in zip(weights, inputs))
    return 1 if total >= 0 else 0</code></pre>
<h3>Learning the AND Gate</h3>
<table>
    <tr><th>Input 1</th><th>Input 2</th><th>AND Output</th></tr>
    <tr><td>0</td><td>0</td><td>0</td></tr>
    <tr><td>0</td><td>1</td><td>0</td></tr>
    <tr><td>1</td><td>0</td><td>0</td></tr>
    <tr><td>1</td><td>1</td><td>1</td></tr>
</table>
<p>The perceptron learns weights that produce this table. Try the <strong>Perceptron demo</strong> in the playground!</p>
<h3>Training Loop</h3>
<pre><code>for epoch in range(epochs):
    for inputs, label in training_data:
        prediction = perceptron(inputs, weights, bias)
        error = label - prediction
        # Update weights
        weights = [w + lr * error * x for w, x in zip(weights, inputs)]
        bias += lr * error</code></pre>
<h3>Limitations</h3>
<p>A single perceptron can only learn <strong>linearly separable</strong> patterns (like AND/OR). For complex patterns, we need <strong>deep neural networks</strong> with multiple layers — that's deep learning!</p>
""",
                },
                {
                    "title": "The ML Workflow",
                    "slug": "ml-workflow",
                    "order_index": 3,
                    "estimated_minutes": 6,
                    "xp_reward": 25,
                    "content": """
<h2>The Machine Learning Workflow 🔄</h2>
<p>Every ML project follows a similar pipeline. Understanding this workflow is key to building successful AI systems.</p>
<h3>Step 1: Gather Data 📊</h3>
<p>Collect high-quality, representative data. Remember: <strong>garbage in, garbage out</strong>.</p>
<h3>Step 2: Clean & Prepare Data 🧹</h3>
<ul>
    <li>Handle missing values.</li>
    <li>Remove duplicates.</li>
    <li>Scale/normalize features.</li>
    <li>Split into training / validation / test sets.</li>
</ul>
<h3>Step 3: Choose a Model 🧠</h3>
<p>Select an algorithm based on the problem type: regression, classification, clustering, etc.</p>
<h3>Step 4: Train the Model 🎯</h3>
<p>Feed training data to the model so it learns patterns by adjusting its parameters.</p>
<h3>Step 5: Evaluate 📏</h3>
<p>Test on <strong>unseen</strong> data to measure generalization using metrics like accuracy or R².</p>
<h3>Step 6: Deploy & Monitor 🚀</h3>
<p>Put the model into production and continuously monitor performance.</p>
<blockquote>Key Split: Train on 80%, validate on 10%, test on 10%. Never test on data the model has already seen!</blockquote>
<p>This workflow applies whether you're predicting house prices, detecting fraud, or building a chatbot!</p>
""",
                },
            ],
        },
        {
            "slug": "neural-networks-deep-learning",
            "title": "Neural Networks & Deep Learning",
            "description": "Discover how multi-layer neural networks power modern AI breakthroughs.",
            "icon": "🧠",
            "color": "#06b6d4",
            "difficulty": "advanced",
            "order_index": 4,
            "estimated_minutes": 45,
            "lessons": [
                {
                    "title": "Neural Networks Explained",
                    "slug": "neural-networks",
                    "order_index": 1,
                    "estimated_minutes": 9,
                    "xp_reward": 35,
                    "content": """
<h2>How Neural Networks Work 🧠</h2>
<p>Neural networks are inspired by the <strong>human brain</strong> — networks of connected "neurons" that learn from data.</p>
<h3>Anatomy of a Neural Network</h3>
<ol>
    <li><strong>Input Layer</strong>: receives features.</li>
    <li><strong>Hidden Layers</strong>: process information (this is where learning happens).</li>
    <li><strong>Output Layer</strong>: produces the prediction.</li>
</ol>
<h3>The Neuron</h3>
<pre><code># A single neuron
output = activation(weights * inputs + bias)

# Example with sigmoid activation
import math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

output = sigmoid(0.5 * 2 + 0.3 * 1 + 0.1)  # 0.73</code></pre>
<h3>Activation Functions</h3>
<ul>
    <li><strong>Sigmoid</strong>: outputs 0-1, great for probabilities.</li>
    <li><strong>ReLU</strong>: max(0, x), fast and popular for hidden layers.</li>
    <li><strong>Softmax</strong>: converts scores to probabilities for multi-class classification.</li>
</ul>
<h3>Why "Deep" Learning?</h3>
<p><strong>Deep</strong> networks have many hidden layers, allowing them to learn increasingly complex features — from edges → shapes → objects → faces.</p>
<h3>How They Learn</h3>
<ul>
    <li><strong>Forward propagation</strong>: pass inputs through the network to get a prediction.</li>
    <li><strong>Backpropagation</strong>: compute error and update weights backward through layers.</li>
    <li><strong>Gradient descent</strong>: optimize weights to minimize the loss.</li>
</ul>
<blockquote>Neural networks are powerful function approximators — with enough data and neurons, they can learn almost any pattern.</blockquote>
""",
                },
                {
                    "title": "Training & Backpropagation",
                    "slug": "training-backpropagation",
                    "order_index": 2,
                    "estimated_minutes": 9,
                    "xp_reward": 35,
                    "content": """
<h2>How Networks Learn: Backpropagation 🔄</h2>
<p>Backpropagation is the algorithm that makes deep learning possible.</p>
<h3>The Big Idea</h3>
<ol>
    <li>Make a prediction (forward pass).</li>
    <li>Calculate the loss (how wrong we were).</li>
    <li>Compute how much each weight contributed to the error.</li>
    <li>Adjust weights to reduce the error (backward pass).</li>
</ol>
<h3>Loss Functions</h3>
<ul>
    <li><strong>Mean Squared Error (MSE)</strong>: for regression.</li>
    <li><strong>Cross-Entropy</strong>: for classification.</li>
</ul>
<pre><code>def mse(predictions, actuals):
    n = len(predictions)
    return sum((p - a) ** 2 for p, a in zip(predictions, actuals)) / n

loss = mse([2.0, 3.5], [2.5, 3.0])  # 0.25</code></pre>
<h3>Gradient Descent</h3>
<p>We update weights in the direction that reduces loss, scaled by the <strong>learning rate</strong>:</p>
<pre><code># weight = weight - learning_rate * gradient
weights = [w - lr * grad for w, grad in zip(weights, gradients)]</code></pre>
<h3>Hyperparameters</h3>
<ul>
    <li><strong>Learning rate</strong>: how big each step is. Too big → overshoot; too small → slow.</li>
    <li><strong>Epochs</strong>: how many times we pass the whole dataset.</li>
    <li><strong>Batch size</strong>: how many samples per update.</li>
</ul>
<p>Choosing good hyperparameters is both science and art — it's called <strong>tuning</strong>!</p>
""",
                },
                {
                    "title": "Real-World Deep Learning",
                    "slug": "real-world-dl",
                    "order_index": 3,
                    "estimated_minutes": 7,
                    "xp_reward": 30,
                    "content": """
<h2>Deep Learning in the Real World 🌐</h2>
<h3>Computer Vision 👁</h3>
<ul>
    <li><strong>CNNs</strong> (Convolutional Neural Networks) power image recognition.</li>
    <li>Self-driving cars detect objects in real time.</li>
    <li>Medical imaging: detecting tumors in X-rays.</li>
</ul>
<h3>Natural Language Processing 💬</h3>
<ul>
    <li><strong>Transformers</strong> (like GPT) power modern language models.</li>
    <li>Machine translation, sentiment analysis, chatbots.</li>
    <li>Our AI Playground chatbot uses rules, but real chatbots use transformers!</li>
</ul>
<h3>Generative AI 🎨</h3>
<ul>
    <li><strong>GANs</strong> generate realistic images.</li>
    <li>Text-to-image models (DALL-E, Stable Diffusion).</li>
    <li>Text generation (ChatGPT, Claude, Gemini).</li>
</ul>
<h3>Popular Deep Learning Frameworks</h3>
<table>
    <tr><th>Framework</th><th>Best For</th></tr>
    <tr><td>PyTorch</td><td>Research, flexibility, dynamic graphs</td></tr>
    <tr><td>TensorFlow</td><td>Production, deployment, Keras API</td></tr>
    <tr><td>JAX</td><td>High-performance numerical computing</td></tr>
</table>
<h3>Key Takeaway</h3>
<p>Deep learning has revolutionized AI. You now understand the foundations — the next step is to build and experiment. Head to the <strong>Challenge Hub</strong> to test your skills!</p>
""",
                },
            ],
        },
    ]

    created = 0
    for t_data in tutorials_data:
        tutorial = Tutorial.query.filter_by(slug=t_data["slug"]).first()
        if tutorial:
            continue
        lessons_data = t_data.pop("lessons")
        tutorial = Tutorial(**t_data)
        for l_data in lessons_data:
            tutorial.lessons.append(Lesson(**l_data))
        db.session.add(tutorial)
        created += 1

    db.session.commit()
    print(f"  ✅ Seeded {created} tutorials")


def seed_challenges():
    challenges_data = [
        {
            "slug": "sum-two-numbers",
            "title": "Sum Two Numbers",
            "difficulty": "easy",
            "category": "python",
            "xp_reward": 30,
            "description": """
<p>Write a function <code>solve(a, b)</code> that returns the <strong>sum</strong> of two numbers.</p>
<pre><code>solve(3, 4)  # -> 7
solve(-1, 1) # -> 0</code></pre>
""",
            "starter_code": 'def solve(a, b):\n    # Your code here\n    return 0\n',
            "solution_code": 'def solve(a, b):\n    return a + b\n',
            "test_cases": [
                {"input": [3, 4], "expected": 7},
                {"input": [-1, 1], "expected": 0},
                {"input": [10, 20], "expected": 30},
                {"input": [0, 0], "expected": 0},
            ],
            "hints": ["Use the + operator.", "Return the result directly."],
        },
        {
            "slug": "is-even",
            "title": "Is It Even?",
            "difficulty": "easy",
            "category": "python",
            "xp_reward": 30,
            "description": """
<p>Write a function <code>solve(n)</code> that returns <code>True</code> if <code>n</code> is <strong>even</strong>, and <code>False</code> otherwise.</p>
<pre><code>solve(4)  # -> True
solve(7)  # -> False</code></pre>
""",
            "starter_code": 'def solve(n):\n    # Your code here\n    return False\n',
            "solution_code": 'def solve(n):\n    return n % 2 == 0\n',
            "test_cases": [
                {"input": 4, "expected": True},
                {"input": 7, "expected": False},
                {"input": 0, "expected": True},
                {"input": -3, "expected": False},
            ],
            "hints": ["Use the modulo operator %."],
        },
        {
            "slug": "reverse-string",
            "title": "Reverse a String",
            "difficulty": "easy",
            "category": "python",
            "xp_reward": 40,
            "description": """
<p>Write a function <code>solve(s)</code> that returns the <strong>reversed</strong> version of a string.</p>
<pre><code>solve("hello")  # -> "olleh"
solve("AI")     # -> "IA"</code></pre>
""",
            "starter_code": 'def solve(s):\n    # Your code here\n    return s\n',
            "solution_code": 'def solve(s):\n    return s[::-1]\n',
            "test_cases": [
                {"input": "hello", "expected": "olleh"},
                {"input": "AI", "expected": "IA"},
                {"input": "racecar", "expected": "racecar"},
                {"input": "", "expected": ""},
            ],
            "hints": ["Python slicing with [::-1] reverses a sequence.", "Or build it with a loop."],
        },
        {
            "slug": "max-of-list",
            "title": "Find the Maximum",
            "difficulty": "easy",
            "category": "python",
            "xp_reward": 40,
            "description": """
<p>Write a function <code>solve(nums)</code> that returns the <strong>largest</strong> number in a list.</p>
<pre><code>solve([3, 7, 2, 9])  # -> 9
solve([-1, -5, -2])  # -> -1</code></pre>
""",
            "starter_code": 'def solve(nums):\n    # Your code here\n    return 0\n',
            "solution_code": 'def solve(nums):\n    return max(nums)\n',
            "test_cases": [
                {"input": [3, 7, 2, 9], "expected": 9},
                {"input": [-1, -5, -2], "expected": -1},
                {"input": [42], "expected": 42},
                {"input": [5, 5, 5], "expected": 5},
            ],
            "hints": ["Use the built-in max() function.", "Or iterate manually with a loop."],
        },
        {
            "slug": "count-vowels",
            "title": "Count the Vowels",
            "difficulty": "medium",
            "category": "python",
            "xp_reward": 60,
            "description": """
<p>Write a function <code>solve(s)</code> that returns the number of <strong>vowels</strong> (a, e, i, o, u) in a string. Ignore case.</p>
<pre><code>solve("hello")  # -> 2 (e, o)
solve("AI")     # -> 2 (A, I)</code></pre>
""",
            "starter_code": 'def solve(s):\n    # Your code here\n    return 0\n',
            "solution_code": 'def solve(s):\n    vowels = set("aeiou")\n    return sum(1 for ch in s.lower() if ch in vowels)\n',
            "test_cases": [
                {"input": "hello", "expected": 2},
                {"input": "AI", "expected": 2},
                {"input": "xyz", "expected": 0},
                {"input": "Python Programming", "expected": 4},
            ],
            "hints": ["Convert to lowercase first.", "Check if each character is in 'aeiou'."],
        },
        {
            "slug": "fizzbuzz",
            "title": "FizzBuzz",
            "difficulty": "medium",
            "category": "python",
            "xp_reward": 60,
            "description": """
<p>Write a function <code>solve(n)</code> that returns a list of strings for numbers 1 to n:</p>
<ul>
    <li>Divisible by 3 → <code>"Fizz"</code></li>
    <li>Divisible by 5 → <code>"Buzz"</code></li>
    <li>Divisible by both → <code>"FizzBuzz"</code></li>
    <li>Otherwise → the number as a string</li>
</ul>
<pre><code>solve(3)  # -> ["1", "2", "Fizz"]</code></pre>
""",
            "starter_code": 'def solve(n):\n    # Your code here\n    return []\n',
            "solution_code": 'def solve(n):\n    result = []\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            result.append("FizzBuzz")\n        elif i % 3 == 0:\n            result.append("Fizz")\n        elif i % 5 == 0:\n            result.append("Buzz")\n        else:\n            result.append(str(i))\n    return result\n',
            "test_cases": [
                {"input": 3, "expected": ["1", "2", "Fizz"]},
                {"input": 5, "expected": ["1", "2", "Fizz", "4", "Buzz"]},
                {"input": 15, "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]},
            ],
            "hints": ["Check divisibility by 15 first (both).", "Use range(1, n+1).", "Append strings, not numbers."],
        },
        {
            "slug": "fibonacci",
            "title": "Fibonacci Sequence",
            "difficulty": "medium",
            "category": "python",
            "xp_reward": 70,
            "description": """
<p>Write a function <code>solve(n)</code> that returns the <code>n</code>-th Fibonacci number (0-indexed).</p>
<pre><code>solve(0)  # -> 0
solve(1)  # -> 1
solve(6)  # -> 8</code></pre>
<p>Fibonacci: 0, 1, 1, 2, 3, 5, 8, ...</p>
""",
            "starter_code": 'def solve(n):\n    # Your code here\n    return 0\n',
            "solution_code": 'def solve(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n',
            "test_cases": [
                {"input": 0, "expected": 0},
                {"input": 1, "expected": 1},
                {"input": 6, "expected": 8},
                {"input": 10, "expected": 55},
            ],
            "hints": ["Handle base cases n=0 and n=1.", "Use two variables to track the last two numbers."],
        },
        {
            "slug": "is-palindrome",
            "title": "Is It a Palindrome?",
            "difficulty": "hard",
            "category": "python",
            "xp_reward": 90,
            "description": """
<p>Write a function <code>solve(s)</code> that returns <code>True</code> if a string reads the same forward and backward (ignoring spaces, punctuation, and case), and <code>False</code> otherwise.</p>
<pre><code>solve("racecar")        # -> True
solve("A man a plan a canal Panama")  # -> True
solve("hello")          # -> False</code></pre>
""",
            "starter_code": 'def solve(s):\n    # Your code here\n    return False\n',
            "solution_code": 'import re\ndef solve(s):\n    clean = re.sub(r"[^a-zA-Z0-9]", "", s).lower()\n    return clean == clean[::-1]\n',
            "test_cases": [
                {"input": "racecar", "expected": True},
                {"input": "A man a plan a canal Panama", "expected": True},
                {"input": "hello", "expected": False},
                {"input": "No 'x' in Nixon", "expected": True},
            ],
            "hints": ["Remove non-alphanumeric characters.", "Convert to lowercase.", "Compare with its reverse."],
        },
    ]

    created = 0
    for ch_data in challenges_data:
        challenge = Challenge.query.filter_by(slug=ch_data["slug"]).first()
        if challenge:
            continue
        # db.JSON handles serialization automatically - pass the list directly
        challenge = Challenge(**ch_data)
        db.session.add(challenge)
        created += 1

    db.session.commit()
    print(f"  ✅ Seeded {created} challenges")


def seed_badges():
    badges_data = [
        {"slug": "first-steps", "name": "First Steps", "description": "Complete your first lesson.", "icon": "👣", "criteria_type": "lessons_completed", "criteria_value": 1},
        {"slug": "quick-learner", "name": "Quick Learner", "description": "Complete 5 lessons.", "icon": "⚡", "criteria_type": "lessons_completed", "criteria_value": 5},
        {"slug": "bookworm", "name": "Bookworm", "description": "Complete 10 lessons.", "icon": "📚", "criteria_type": "lessons_completed", "criteria_value": 10},
        {"slug": "scholar", "name": "Scholar", "description": "Complete 20 lessons.", "icon": "🎓", "criteria_type": "lessons_completed", "criteria_value": 20},
        {"slug": "problem-solver", "name": "Problem Solver", "description": "Solve your first challenge.", "icon": "🧩", "criteria_type": "challenges_solved", "criteria_value": 1},
        {"slug": "challenge-master", "name": "Challenge Master", "description": "Solve 5 challenges.", "icon": "🏆", "criteria_type": "challenges_solved", "criteria_value": 5},
        {"slug": "ai-hero", "name": "AI Hero", "description": "Solve 10 challenges.", "icon": "🦸", "criteria_type": "challenges_solved", "criteria_value": 10},
        {"slug": "xp-100", "name": "Century", "description": "Earn 100 XP.", "icon": "💯", "criteria_type": "total_xp", "criteria_value": 100},
        {"slug": "xp-500", "name": "Power Learner", "description": "Earn 500 XP.", "icon": "🚀", "criteria_type": "total_xp", "criteria_value": 500},
        {"slug": "xp-1000", "name": "AI Legend", "description": "Earn 1000 XP.", "icon": "👑", "criteria_type": "total_xp", "criteria_value": 1000},
        {"slug": "streak-3", "name": "On a Roll", "description": "Maintain a 3-day streak.", "icon": "🔥", "criteria_type": "streak", "criteria_value": 3},
        {"slug": "streak-7", "name": "Unstoppable", "description": "Maintain a 7-day streak.", "icon": "⚡", "criteria_type": "streak", "criteria_value": 7},
        {"slug": "level-5", "name": "Rising Star", "description": "Reach level 5.", "icon": "🌟", "criteria_type": "level", "criteria_value": 5},
        {"slug": "level-10", "name": "AI Master", "description": "Reach level 10.", "icon": "🧠", "criteria_type": "level", "criteria_value": 10},
    ]

    created = 0
    for b_data in badges_data:
        badge = Badge.query.filter_by(slug=b_data["slug"]).first()
        if badge:
            continue
        db.session.add(Badge(**b_data))
        created += 1

    db.session.commit()
    print(f"  ✅ Seeded {created} badges")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("🌱 Seeding database...")
        seed_tutorials()
        seed_challenges()
        seed_badges()
        print("🎉 Seed complete!")

