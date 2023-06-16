import gradio as gr
import pandas as pd
import pickle

import os
MAIN_FOLDER = os.path.dirname(__file__)

# Define params names
PARAMS_NAME = [
    "orderAmount",
    "orderState",
    "paymentMethodRegistrationFailure",
    "paymentMethodType",
    "paymentMethodProvider",
    "paymentMethodIssuer",
    "transactionAmount",
    "transactionFailed",
    "emailDomain",
    "emailProvider",
    "customerIPAddressSimplified",
    "sameCity"
]

# Load model
with open("model/modelo_proyecto_final.pkl", "rb") as f:
    model = pickle.load(f)

# Columnas
COLUMNS_PATH = "model/categories_ohe_without_fraudulent.pickle"
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

BINS_ORDER = os.path.join(MAIN_FOLDER, "model/saved_bins_order.pickle")
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

BINS_TRANSACTION = os.path.join(MAIN_FOLDER, "model/saved_bins_transaction.pickle")
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)

def predict(*args):
    answer_dict = {}

    for i in range(len(PARAMS_NAME)):
        answer_dict[PARAMS_NAME[i]] = [args[i]]

    # Crear dataframe
    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
    single_instance["orderAmount"] = pd.cut(single_instance['orderAmount'],
                                 bins=new_saved_bins_order, 
                                 include_lowest=True)

    single_instance["transactionAmount"] = single_instance["transactionAmount"].astype(int)
    single_instance["transactionAmount"] = pd.cut(single_instance['transactionAmount'],
                                 bins=new_saved_bins_order, 
                                 include_lowest=True)

    # One hot encoding
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)

    prediction = model.predict(single_instance_ohe)

    # Cast numpy.int64 to just a int
    type_of_fraud = int(prediction[0])

    # Adaptación respuesta
    response = "Error parsing value"
    if type_of_fraud == 0:
        response = "False"
    if type_of_fraud == 1:
        response = "True"
    if type_of_fraud == 2:
        response = "Warning"

    return response


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Prevención de Fraude 👀🔍 
        """
    )

    with gr.Row():
        with gr.Column():

            gr.Markdown(
                """
                ## Predecir si un cliente es fraudulento o no.
                """
            )
            
            orderAmount = gr.Slider(label="Order amount", minimum=0, maximum=355, step=2, randomize=True)

            orderState = gr.Radio(
                label="Order state",
                choices=["fulfilled", "failed", "pending"],
                value="failed"
                )

            paymentMethodRegistrationFailure = gr.Radio(
                label="Payment method registration failure",
                choices=["False", "True"],
                value="True"
                )

            paymentMethodType = gr.Radio(
                label="Payment method type",
                choices=["card", "apple pay ", "paypal", "bitcoin"],
                value="bitcoin"
                )

            paymentMethodProvider = gr.Dropdown(
                label="Payment method provider",
                choices=["JCB 16 digit", "VISA 16 digit", "Voyager", "Diners Club / Carte Blanche", "Maestro", "VISA 13 digit", "Discover", "American Express", "JCB 15 digit", "Mastercard"],
                multiselect=False,
                value="American Express"
                )
            
            paymentMethodIssuer = gr.Dropdown(
                label="Payment method issuer",
                choices=["Her Majesty Trust", "Vertex Bancorp", "Fountain Financial Inc.", "His Majesty Bank Corp.", "Bastion Banks", "Bulwark Trust Corp.", "weird", "Citizens First Banks", "Grand Credit Corporation", "Solace Banks", "Rose Bancshares"],
                multiselect=False,
                value="Bastion Banks"
                )
            
            transactionAmount = gr.Slider(label="Transaction amount", minimum=0, maximum=355, step=2, randomize=True)

            transactionFailed = gr.Radio(
                label="Transaction failed",
                choices=["False", "True"],
                value="False"
                )

            emailDomain = gr.Radio(
                label="Email domain",
                choices=["com", "biz", "org", "net", "info", "weird"],
                value="com"
                )

            emailProvider = gr.Radio(
                label="Email provider",
                choices=["gmail", "hotmail", "yahoo", "other", "weird"],
                value="gmail"
                )

            customerIPAddressSimplified = gr.Radio(
                label="Customer IP Address",
                choices=["only_letters", "digits_and_letters"],
                value="only_letter"
                )

            sameCity = gr.Radio(
                label="Same city",
                choices=["unknown", "no", "yes"],
                value="unknown"
                )

        with gr.Column():

            gr.Markdown(
                """
                ## Predicción
                """
            )

            label = gr.Label(label="Score")
            predict_btn = gr.Button(value="Evaluar")
            predict_btn.click(
            predict,
            inputs=[
                orderAmount,
                orderState,
                paymentMethodRegistrationFailure,
                paymentMethodType,
                paymentMethodProvider,
                paymentMethodIssuer,
                transactionAmount,
                transactionFailed,
                emailDomain,
                emailProvider,
                customerIPAddressSimplified,
                sameCity,
            ],
            outputs=[label],
            api_name="prediccion"
            )
    gr.Markdown(
        """
        <p style='text-align: center'>
            <a >Proyecto Final Kari 🤟🏻
            </a>
        </p>
        """
    )

demo.launch(share=True)
