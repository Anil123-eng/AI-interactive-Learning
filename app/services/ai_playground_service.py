"""AI Playground service - interactive AI demos (Application Layer).

Provides small, self-contained machine-learning / NLP demos that run
entirely in-process so students can experiment without external APIs.
"""
import math
import re


class RuleBasedChatbot:
    """A simple rule-based chatbot demonstrating pattern matching."""

    RESPONSES = [
        (r"\b(hello|hi|hey)\b", [
            "Hello! 👋 I'm EduBot, your AI learning assistant. Ask me about AI, machine learning, or Python!",
            "Hi there! Ready to learn something new about AI today?",
        ]),
        (r"\b(what is|define|meaning of)\b.*\b(ai|artificial intelligence)\b", [
            "AI (Artificial Intelligence) is the simulation of human intelligence in machines "
            "that are programmed to think, learn, and make decisions.",
            "Artificial Intelligence is about building systems that can perform tasks that "
            "normally require human intelligence — like understanding language or recognizing images.",
        ]),
        (r"\b(machine learning|ml|supervised learning|unsupervised learning|reinforcement learning)\b", [
            "Machine Learning is a subset of AI where computers learn patterns from data instead of "
            "being explicitly programmed. Types: Supervised, Unsupervised, and Reinforcement Learning!",
            "ML = Teaching computers to learn from examples. Like teaching a child to recognize cats by showing many cat pictures!",
        ]),
        (r"\b(neural network|neural networks|deep learning)\b", [
            "Neural Networks are computing systems inspired by the brain. They consist of layers of "
            "'neurons' that learn patterns from data — the basis of Deep Learning!",
        ]),
        (r"\b(python|programming|code|coding)\b", [
            "Python is the most popular language for AI development — simple syntax + powerful libraries like NumPy, PyTorch, and TensorFlow!",
        ]),
        (r"\b(how|where|what)\b.*\b(learn|start|begin|study|course|tutorial)\b|\b(recommend|roadmap)\b", [
            "Great question! Start here: 1) Learn Python basics, 2) Take our AI Fundamentals tutorial, "
            "3) Try the challenges in the Challenge Hub, 4) Experiment in this playground!",
        ]),
        (r"\b(thank|thanks|thank you)\b", [
            "You're welcome! 🎉 Keep learning and don't forget to check out the Challenge Hub.",
            "Happy to help! Learning AI is a journey — you're doing great!",
        ]),
        (r"\b(bye|goodbye|see you)\b", [
            "Goodbye! 👋 Come back soon to continue your AI journey!",
        ]),
    ]

    FALLBACKS = [
        "I don't have a lesson on that exact topic yet. Try asking about AI, machine learning, Python, or neural networks.",
        "That is outside my current offline knowledge. I can explain the tutorials, coding challenges, and the AI concepts covered here.",
    ]

    def respond(self, message: str) -> str:
        if not isinstance(message, str):
            return "Please send your question as text. 😊"
        text = re.sub(r"\s+", " ", message.lower()).strip()
        if not text:
            return "Please type a message so I can help you! 😊"
        for pattern, replies in self.RESPONSES:
            if re.search(pattern, text):
                # Rotate by message content so repeated requests are not random,
                # while different questions can receive different explanations.
                return replies[sum(ord(char) for char in text) % len(replies)]
        return self.FALLBACKS[sum(ord(char) for char in text) % len(self.FALLBACKS)]


class SentimentAnalyzer:
    """A simple lexicon-based sentiment analyzer."""

    POSITIVE_WORDS = {
        "good", "great", "excellent", "amazing", "awesome", "happy", "love", "wonderful",
        "fantastic", "best", "positive", "joy", "beautiful", "perfect", "nice", "helpful",
        "impressive", "delighted", "glad", "brilliant", "superb", "outstanding", "cool",
    }
    NEGATIVE_WORDS = {
        "bad", "terrible", "awful", "hate", "sad", "worst", "negative", "angry", "horrible",
        "poor", "ugly", "useless", "disappointed", "annoying", "boring", "frustrating",
        "error", "fail", "broken", "awful", "unhappy", "awful",
    }
    INTENSIFIERS = {"very", "really", "extremely", "so", "super", "incredibly"}

    def analyze(self, text: str) -> dict:
        words = re.findall(r"[a-zA-Z']+", text.lower())
        if not words:
            return {"score": 0.0, "label": "Neutral", "positive": 0, "negative": 0}

        score = 0.0
        pos_count = 0
        neg_count = 0
        for i, word in enumerate(words):
            multiplier = 1.0
            if i > 0 and words[i - 1] in self.INTENSIFIERS:
                multiplier = 1.5
            if word in self.POSITIVE_WORDS:
                score += 1.0 * multiplier
                pos_count += 1
            elif word in self.NEGATIVE_WORDS:
                score -= 1.0 * multiplier
                neg_count += 1

        # Normalize to [-1, 1]
        max_count = max(pos_count, neg_count, 1)
        normalized = max(-1.0, min(1.0, score / (max_count * 1.5)))

        if normalized > 0.15:
            label = "Positive 😊"
        elif normalized < -0.15:
            label = "Negative 😞"
        else:
            label = "Neutral 😐"

        return {
            "score": round(normalized, 3),
            "label": label,
            "positive": pos_count,
            "negative": neg_count,
        }


class LinearRegression:
    """Simple linear regression trained with least squares / gradient descent."""

    def fit(self, x_values: list[float], y_values: list[float]) -> dict:
        n = len(x_values)
        if n == 0 or n != len(y_values):
            return {"error": "X and Y must have the same non-zero length."}
        mean_x = sum(x_values) / n
        mean_y = sum(y_values) / n
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        denominator = sum((x - mean_x) ** 2 for x in x_values)
        if denominator == 0:
            return {"error": "X values are constant — cannot fit a slope."}
        slope = numerator / denominator
        intercept = mean_y - slope * mean_x
        predictions = [slope * x + intercept for x in x_values]
        r2 = self._r_squared(y_values, predictions)
        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "equation": f"y = {slope:.2f}x + {intercept:.2f}",
            "r2": round(r2, 4),
            "predictions": [round(p, 2) for p in predictions],
        }

    @staticmethod
    def _r_squared(y: list[float], pred: list[float]) -> float:
        mean_y = sum(y) / len(y)
        ss_res = sum((yi - pi) ** 2 for yi, pi in zip(y, pred))
        ss_tot = sum((yi - mean_y) ** 2 for yi in y)
        if ss_tot == 0:
            return 0.0
        return 1 - ss_res / ss_tot


class Perceptron:
    """A single-layer perceptron for linearly separable binary classification."""

    def __init__(self, learning_rate: float = 0.1, epochs: int = 100):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = []
        self.bias = 0.0

    def fit(self, features: list[list[float]], labels: list[int]) -> dict:
        if len(features) == 0 or len(features) != len(labels):
            return {"error": "Features and labels must be aligned and non-empty."}
        n_features = len(features[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            errors = 0
            for x, y in zip(features, labels):
                prediction = self._predict_raw(x)
                error = y - prediction
                if error != 0:
                    errors += 1
                    for i in range(n_features):
                        self.weights[i] += self.lr * error * x[i]
                    self.bias += self.lr * error
            if errors == 0:
                break

        # Accuracy
        correct = sum(1 for x, y in zip(features, labels) if self._predict_raw(x) == y)
        accuracy = correct / len(labels)
        return {
            "weights": [round(w, 4) for w in self.weights],
            "bias": round(self.bias, 4),
            "accuracy": round(accuracy, 4),
            "epochs_used": self.epochs,
        }

    def predict(self, features: list[float]) -> int:
        if not self.weights:
            raise RuntimeError("Model not trained yet.")
        return self._predict_raw(features)

    def _predict_raw(self, features: list[float]) -> int:
        total = self.bias + sum(w * f for w, f in zip(self.weights, features))
        return 1 if total >= 0 else 0

