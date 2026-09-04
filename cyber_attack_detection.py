import numpy as np
import pandas as pd
import mysql.connector

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ==========================================
# 1. CREATE SAMPLE DATA FOR ML MODEL
# ==========================================

np.random.seed(42)

normal_data = np.column_stack((
    np.random.randint(100, 1000, 500),   # Packet Size
    np.random.randint(10, 300, 500),     # Connection Duration
    np.random.randint(0, 3, 500),        # Failed Login Attempts
    np.random.randint(10, 500, 500)      # Number of Packets
))

attack_data = np.column_stack((
    np.random.randint(1000, 10000, 500),
    np.random.randint(1, 1000, 500),
    np.random.randint(3, 20, 500),
    np.random.randint(500, 10000, 500)
))

X = np.vstack((normal_data, attack_data))

y = np.array(
    [0] * len(normal_data) +
    [1] * len(attack_data)
)


# ==========================================
# 2. TRAIN MACHINE LEARNING MODEL
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)


# ==========================================
# 3. MYSQL DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MASHOOD09",
        database="cyberguard_db"
    )

    return connection


# ==========================================
# 4. PREDICT CYBER ATTACK
# ==========================================

def predict_attack(
    packet_size,
    connection_duration,
    failed_login_attempts,
    number_of_packets
):

    features = np.array([[
        packet_size,
        connection_duration,
        failed_login_attempts,
        number_of_packets
    ]])

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0]

    confidence = round(
        max(probability) * 100,
        2
    )

    # ------------------------------------------
    # DETERMINE ATTACK TYPE
    # ------------------------------------------

    if prediction == 0:

        result = "Normal"
        attack_type = "No Attack"

    else:

        result = "Attack"

        # DoS / DDoS Detection
        if number_of_packets > 5000:
            attack_type = "Possible DoS/DDoS Attack"

        # Brute Force Detection
        elif failed_login_attempts >= 5:
            attack_type = "Possible Brute Force Attack"

        # Suspicious Traffic
        elif packet_size > 5000:
            attack_type = "Suspicious High Packet Traffic"

        else:
            attack_type = "Suspicious Network Activity"

    return {
        "prediction": result,
        "attack_type": attack_type,
        "confidence": confidence
    }


# ==========================================
# 5. SAVE PREDICTION TO MYSQL
# ==========================================

def save_prediction(
    packet_size,
    connection_duration,
    failed_login_attempts,
    number_of_packets,
    prediction,
    attack_type,
    confidence
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO attack_history
        (
            packet_size,
            connection_duration,
            failed_login_attempts,
            number_of_packets,
            prediction,
            attack_type,
            confidence
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        """

        values = (
            float(packet_size),
            float(connection_duration),
            int(failed_login_attempts),
            int(number_of_packets),
            prediction,
            attack_type,
            float(confidence)
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

    except mysql.connector.Error as error:

        print("MySQL Error:", error)

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ==========================================
# 6. GET PREDICTION HISTORY
# ==========================================

def get_prediction_history():

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT *
        FROM attack_history
        ORDER BY created_at DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        return data

    except mysql.connector.Error as error:

        print("MySQL Error:", error)

        return []

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ==========================================
# 7. TEST THE BACKEND
# ==========================================

if __name__ == "__main__":

    print("CyberGuard AI Backend Started")
    print(
        f"Model Accuracy: {accuracy * 100:.2f}%"
    )

    result = predict_attack(
        packet_size=500,
        connection_duration=100,
        failed_login_attempts=0,
        number_of_packets=100
    )

    print("Test Result:")
    print(result)