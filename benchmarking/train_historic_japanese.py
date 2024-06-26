import pandas as pd
import pickle
import numpy as np
import linktransformer as lt
import os


###run as script

if __name__ == "__main__":
     ##Load the data
    dataset_path = os.path.join(lt.DATA_DIR_PATH, "jp_pr_tkv2.csv")

    ##Load the data
    df = pd.read_csv(dataset_path)

    ##Drop if tk_truth!=0 or 1
    df = df[df['tk_truth'].isin([0,1])]
    
    ##Print some dataset stats
    ## size of dataset
    print(df.shape)
    ## number of positives
    print(df[df["tk_truth"]==1].shape[0])
    ## number of negatives
    print(df[df["tk_truth"]==0].shape[0])
    

    loss_type="supcon"
   # Call the train_model function
    saved_model_path = lt.train_model(
        model_path="oshizo/sbert-jsnli-luke-japanese-base-lite",
        data=df,
        left_col_names=["source_firm_title","source_address",
                        "source_product",
                        "source_est_date",
                        "source_capital",
                        "source_bank",
                        "source_shareholder",
                        ],
        right_col_names=["tk_firm_title","tk_address",
                        "tk_product",
                        "tk_est_date",
                        "tk_capital",
                        "tk_bank",
                        "tk_shareholder"],
        label_col_name="tk_truth",
        left_id_name=['source'],
        right_id_name=['tk_path_value'],
        log_wandb=True,
        training_args={"num_epochs": 200,
                        "warm_up_perc": 1,
                        "learning_rate": 2e-5,
                       "test_at_end": True,
                       "save_val_test_pickles": True,
                       "model_save_name": f"lt-historicjapanesecompanies-comp-prod-ind_{loss_type}_full",
                       "opt_model_description": "This model was trained on a dataset of historic Japanese companies, products, industry, addresses, and shareholders. Take a look at our paper for more details. The task is to link indices of japanese companies",
                       "opt_model_lang":"ja",
                       "loss_type":loss_type,
                       "val_perc":0.2,
                       "loss_params":{},
                        "wandb_names":{
                                     "id": "econabhishek",
                                    "run": f"lt-historicjapanesecompanies-comp-prod-ind_{loss_type}_full",
                                    "project": "linkage",
                                    "entity": "econabhishek" },}
    )


    # ###Save the model to hub
    best_model=lt.load_model(saved_model_path)

    best_model.save_to_hub(repo_name = "lt-historicjapanesecompanies", ##Write model name here
            organization= "dell-research-harvard",
            private = None,
            commit_message = "Add new LinkTransformer model.",
            local_model_path = None,
            exist_ok = True,
            replace_model_card = True,
            )


    
