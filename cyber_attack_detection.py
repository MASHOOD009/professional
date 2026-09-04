import pandas as pd
import mysql.connector

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ==========================================
# 1. CREATE NETWORK TRAFFIC DATASET
# ==========================================

data = {
    "Packet_Size": [
        120, 1500, 200, 1800, 300, 1600, 250, 2000,
        180, 1700, 350, 1900, 400, 2100, 220, 1750,
        280, 1850, 320, 1950
    ],

    "Connection_Duration": [
        10, 300, 15, 450, 20, 500, 12, 600,
        18, 550, 25, 650, 30, 700, 14, 480,
        22, 520, 28, 580
    ],

    "Failed_Login_Attempts": [
        0, 5, 0, 8, 1, 7, 0, 10,
        0, 6, 1, 9, 0, 11, 0, 7,
        1, 8, 0, 10
    ],

    "Number_of_Packets": [
        10, 500, 15, 800, 20, 700, 12, 1000,
        18, 750, 25, 900, 30, 1100, 14, 650,
        22, 780, 28, 850
    ],

    # 0 = Normal Traffic
    # 1 = Cyber Attack
    "Attack": [
        0, 1, 0, 1, 0, 1, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1,
        0, 1, 0, 1
    ]
}


# ==========================================
# 2. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(data)


# ==========================================
# 3. FEATURES AND TARGET
# ==========================================

X = df.drop("Attack", axis=1)
y = df["Attack"]


# ==========================================
# 4. TRAIN AND TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# 5. TRAIN RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# ==========================================
# 6. MODEL EVALUATION
# ==========================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)


# ==========================================
# 7. MYSQL DATABASE CONNECTION
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
# 8. SAVE PREDICTION TO MYSQL
# ==========================================

def save_prediction(
    packet_size,
    connection_duration,
    failed_login_attempts,
    number_of_packets,
    result
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO prediction_history
    (
        packet_size,
        connection_duration,
        failed_login_attempts,
        number_of_packets,
        result
    )
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        packet_size,
        connection_duration,
        failed_login_attempts,
        number_of_packets,
        result
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================
# 9. GET PREDICTION HISTORY
# ==========================================

def get_prediction_history():

    connection = get_connection()

    query = """
    SELECT *
    FROM prediction_history
    ORDER BY prediction_time DESC
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df


# ==========================================
# 10. PREDICT CYBER ATTACK
# ==========================================

def predict_attack(
    packet_size,
    connection_duration,
    failed_login_attempts,
    number_of_packets
):

    input_data = pd.DataFrame({
        "Packet_Size": [packet_size],
        "Connection_Duration": [connection_duration],
        "Failed_Login_Attempts": [failed_login_attempts],
        "Number_of_Packets": [number_of_packets]
    })

    prediction = model.predict(input_data)[0]

    result = (
        "Cyber Attack"
        if prediction == 1
        else "Normal Traffic"
    )

    # Save prediction automatically in MySQL
    save_prediction(
        packet_size,
        connection_duration,
        failed_login_attempts,
        number_of_packets,
        result
    )

    return prediction


# ==========================================
# 11. DISPLAY MODEL EVALUATION
# ==========================================

if __name__ == "__main__":

    print("\n===== CYBERGUARD AI =====")

    print("\n----- MODEL EVALUATION -----")

    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall: {recall * 100:.2f}%")
    print(f"F1 Score: {f1 * 100:.2f}%")