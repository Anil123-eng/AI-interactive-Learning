"""AI Playground routes - interactive AI demos (Presentation Layer)."""
from flask import Blueprint, jsonify, render_template, request

from ..services.ai_playground_service import (
    LinearRegression,
    MentorChatbot,
    Perceptron,
    SentimentAnalyzer,
)

playground_bp = Blueprint("playground", __name__)

_chatbot = MentorChatbot()
_sentiment = SentimentAnalyzer()


@playground_bp.route("/playground")
def playground_home():
    return render_template("playground/index.html")


@playground_bp.route("/playground/chatbot", methods=["POST"])
def chatbot_endpoint():
    """POST {message: string} -> chatbot reply."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not isinstance(message, str) or len(message) > 1000:
        return jsonify({"error": "Message must be text and no longer than 1000 characters."}), 400
    reply = _chatbot.respond(message)
    return jsonify({"reply": reply})


@playground_bp.route("/playground/sentiment", methods=["POST"])
def sentiment_endpoint():
    """POST {text: string} -> sentiment analysis result."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not isinstance(text, str) or len(text) > 5000:
        return jsonify({"error": "Text must be text and no longer than 5000 characters."}), 400
    result = _sentiment.analyze(text)
    return jsonify(result)


@playground_bp.route("/playground/regression", methods=["POST"])
def regression_endpoint():
    """POST {x: [], y: []} -> linear regression fit."""
    data = request.get_json(silent=True) or {}
    x_values = data.get("x", [])
    y_values = data.get("y", [])
    if not isinstance(x_values, list) or not isinstance(y_values, list):
        return jsonify({"error": "X and Y must be lists of numbers."}), 400
    try:
        x_values = [float(v) for v in x_values]
        y_values = [float(v) for v in y_values]
    except (TypeError, ValueError):
        return jsonify({"error": "X and Y must be lists of numbers."}), 400
    result = LinearRegression().fit(x_values, y_values)
    return jsonify(result), 400 if "error" in result else 200


@playground_bp.route("/playground/perceptron", methods=["POST"])
def perceptron_endpoint():
    """POST {features: [[...]], labels: []} -> train perceptron.

    Also supports the built-in AND/OR demo when given a demo key.
    """
    data = request.get_json(silent=True) or {}

    # Built-in demo datasets
    if data.get("demo") == "and":
        features = [[0, 0], [0, 1], [1, 0], [1, 1]]
        labels = [0, 0, 0, 1]
    elif data.get("demo") == "or":
        features = [[0, 0], [0, 1], [1, 0], [1, 1]]
        labels = [0, 1, 1, 1]
    else:
        features = data.get("features", [])
        labels = data.get("labels", [])
        try:
            if not isinstance(features, list) or not isinstance(labels, list):
                raise ValueError
            features = [[float(v) for v in row] for row in features]
            labels = [int(v) for v in labels]
            if (
                not features
                or any(not row or len(row) != len(features[0]) for row in features)
                or any(label not in (0, 1) for label in labels)
            ):
                raise ValueError
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid features/labels format."}), 400

    model = Perceptron(learning_rate=0.1, epochs=100)
    result = model.fit(features, labels)

    # Show predictions on the training set
    if "error" not in result:
        predictions = [model.predict(row) for row in features]
        result["predictions"] = predictions
        result["demo_data"] = {"features": features, "labels": labels, "predictions": predictions}
    return jsonify(result), 400 if "error" in result else 200


@playground_bp.route("/playground/data", methods=["GET"])
def demo_data():
    """Provide sample datasets for the playground."""
    return jsonify(
        {
            "regression": {
                "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "y": [2.1, 4.2, 5.9, 8.1, 9.8, 12.0, 13.9, 16.2, 17.8, 20.1],
            },
            "sentiment_samples": [
                "I love learning about AI! It's absolutely amazing and wonderful!",
                "This is the worst experience ever. I'm so frustrated and disappointed.",
                "The weather today is quite normal.",
                "Machine learning is very interesting and extremely helpful!",
            ],
        }
    )

