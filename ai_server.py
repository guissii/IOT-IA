from flask import Flask, request, jsonify
from collections import deque
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

history_temp = deque(maxlen=50)
history_time = deque(maxlen=50)
tick = [0]

def detect_anomaly(value):
    if len(history_temp) < 5:
        return False, 0.0
    arr  = np.array(history_temp)
    mean = np.mean(arr)
    std  = np.std(arr)
    if std == 0:
        return False, 0.0
    z = abs((value - mean) / std)
    return bool(z > 2.5), round(float(z), 2)

def predict_next(temps, times):
    if len(temps) < 5:
        return None
    X = np.array(times).reshape(-1, 1)
    y = np.array(temps)
    model = LinearRegression().fit(X, y)
    next_t = times[-1] + 300
    return round(float(model.predict([[next_t]])[0]), 1)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temp = data.get('temperature')
    hum  = data.get('humidity')

    if temp is None:
        return jsonify({"error": "missing temperature"}), 400

    tick[0] += 30
    history_temp.append(temp)
    history_time.append(tick[0])

    is_anomaly, z_score = detect_anomaly(temp)
    predicted = predict_next(list(history_temp), list(history_time))

    result = {
        "anomaly"       : is_anomaly,
        "z_score"       : z_score,
        "temperature"   : temp,
        "humidity"      : hum,
        "predicted_temp": predicted,
        "in_minutes"    : 5,
        "history_size"  : len(history_temp)
    }

    print(f"[IA] T={temp} H={hum} | anomalie={is_anomaly}"
          f" z={z_score} | pred={predicted}")
    return jsonify(result)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status"      : "running",
        "history_size": len(history_temp),
        "last_temp"   : list(history_temp)[-1] if history_temp else None
    })

if __name__ == '__main__':
    print("Serveur IA démarré → http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
