"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import os

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    input_folder = "./files/input/"

    dataframes = []

    # Iterar sobre todos los archivos en la carpeta
    for filename in os.listdir(input_folder):
        if filename.endswith(".zip"):
            filepath = os.path.join(input_folder, filename)
            df = pd.read_csv(
                filepath,
                index_col=False,
                compression="zip"
            )
            dataframes.append(df)
    df_completo = pd.concat(dataframes, ignore_index=True)

    df_client = df_completo[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']]
    #Falta 'last_contact_date'
    df_campaign = df_completo[['client_id', 'number_contacts','contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'month', 'day']]
    df_economics = df_completo[['client_id', 'cons_price_idx', 'euribor_three_months']]

    df_campaign.iloc[:, 4] = (df_campaign.iloc[:, 4] == 'success').astype(int)
    df_campaign.iloc[:, 5] = (df_campaign.iloc[:, 5] == 'yes').astype(int)
    # Diccionario para mapear las abreviaturas a números
    meses_dict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 
                'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    df_campaign.iloc[:, 6] = df_campaign.iloc[:, 6].map(meses_dict)    
    df_campaign['last_contact_date'] = pd.to_datetime({'year': 2022, 'month': df_campaign['month'], 'day': df_campaign['day']})
    df_campaign.drop(['month', 'day'], axis=1, inplace=True)

    df_client.iloc[:, 2] = df_client.iloc[:, 2].str.replace('.', '').str.replace('-', '_')
    df_client.iloc[:, 4] = df_client.iloc[:, 4].str.replace('.', '_').replace('unknown', pd.NA)
    df_client.iloc[:, 5] = (df_client.iloc[:, 5] == 'yes').astype(int)
    df_client.iloc[:, 6] = (df_client.iloc[:, 6] == 'yes').astype(int)

    dataframes = [
        (df_client, 'client.csv'),
        (df_campaign, 'campaign.csv'),
        (df_economics, 'economics.csv')
    ]

    output_dir = './files/output/'

    os.makedirs(output_dir, exist_ok=True)

    for df, filename in dataframes:
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)

