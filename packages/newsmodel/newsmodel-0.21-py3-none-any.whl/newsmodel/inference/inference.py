import torch
from mlflow.tracking import MlflowClient
from transformers import AutoTokenizer

import mlflow
import torch.nn as nn
from transformers import AutoModel


class SentimentClassifier(nn.Module):
    """torch의 nn.Module을 사용해서 분류기 클래스의 기본적인 구조가 들어있는 모듈
    ---------
    """

    # caution: 코드가 중복되지 않게 pretrained_model_name만을 사용해서 할 수는 없을까?

    def __init__(self, pretrained_model_name, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = AutoModel.from_pretrained(
            pretrained_model_name, return_dict=False
        )
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.bert(
            input_ids=input_ids, attention_mask=attention_mask
        )
        output = self.drop(pooled_output)
        return self.out(output)


def embedding(input_text, PRE_TRAINED_MODEL_NAME):
    """input text가 들어오면 모델에 inference할 text를 torch model이 사용할 수 있게, input text를 embedding하는 함수.

    Parameters
    ---------
    input_text: str
        사용자가 넣을 문장 정보.
    PRE_TRAINED_MODEL_NAME: str
        tokenizer가 사용할 PRE_TRAINED_MODEL_NAME의 이름. 사용할 모델과 PRE_TRAINED_MODEL_NAME의 정보가 맞아야 한다.
        참고: https://huggingface.co/transformers/v3.0.2/model_doc/auto.html

    Return
    ---------
    input_ids: tensor
        encoding된 단어들이 숫자로 표현된 결과
    attention_mask: tensor
        단어가 있는지의 여부를 표시하는 결과, 문장이 있으면 1, 문자가 없고 padding이 되어 있으면 0으로 표시된다.
    """
    device = "cpu"

    tokenizer = AutoTokenizer.from_pretrained(
        PRE_TRAINED_MODEL_NAME, return_dict=False
    )

    encoded_review = tokenizer.encode_plus(
        input_text,
        max_length=512,
        add_special_tokens=True,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors="pt",
    )
    input_ids = encoded_review["input_ids"].to(device)
    attention_mask = encoded_review["attention_mask"].to(device)

    return input_ids, attention_mask


def load_model(model_name):
    """mlflow 저장된 모델에서 되어 있는 모델을 불러오는 함수

    Parameters
    ---------
    model_name: str
        model runs에 들어갈 model 이름. mlflow server에서 사용자가 지정한 model_runs의 이름
    tracking_ip: str
        mlflow sever가 저장되어 있는 ip주소
    current_state: str
        가져오고 있는 모델의 상태. ex) Production

    Return
    ---------
    model: torch.nn
        사전에 학습된 pytorch model
    """
    model = SentimentClassifier(model_name, 2)
    model.load_state_dict(torch.load('mobileBert.pt', map_location="cpu"))
    model = model.to("cpu")

    return model


def inference(model, input_ids, attention_mask):
    """
    pytorch 모델과 embedding된 문장을 사용해서 문장이 긍정적인지, 부정적인지 분류한다.

    Parameters
    ---------
    model: torch.nn
        사전에 학습된 pytorch model
    input_ids: tensor
        encoding된 단어들이 숫자로 표현된 결과
    attention_mask: tensor
        단어가 있는지의 여부를 표시하는 결과, 문장이 있으면 1, 문자가 없고 padding이 되어 있으면 0으로 표시된다.

    Returns
        softmax_prob: tensor
            문장이 긍정적인지 부정적인지 확률로 나타낸 결과
        prediction: tensor
            문장이 긍정적인지 부정적인지 0 혹은 1로 나타낸 결과
    ---------
    """
    logits = model(input_ids, attention_mask)
    softmax_prob = torch.nn.functional.softmax(logits, dim=1)
    _, prediction = torch.max(softmax_prob, dim=1)

    return softmax_prob, prediction


def inference_sentence(
    input_text: str
):
    """inference 함수를 사용해서, 문장 단위로 문장이 긍정적인지, 부정적인지 보여준다.

    Parameters
    ---------
    input_text: str
        모델에 사용하고자 하는 문장
    PRE_TRAINED_MODEL_NAME: str
        tokenizer가 사용할 PRE_TRAINED_MODEL_NAME의 이름. 사용할 모델과 PRE_TRAINED_MODEL_NAME의 정보가 맞아야 한다.
        참고: https://huggingface.co/transformers/v3.0.2/model_doc/auto.html
    model_name: str
        model runs에 들어갈 model 이름. mlflow server에서 사용자가 지정한 model_runs의 이름
    tracking_ip: str
        mlflow sever가 저장되어 있는 ip주소
    current_state: str
        가져오고 있는 모델의 상태. ex) Production

    Returns
    ---------
    softmax_prob: tensor
        문장이 긍정적인지 부정적인지 확률로 나타낸 결과
    prediction: tensor
        문장이 긍정적인지 부정적인지 0 혹은 1로 나타낸 결과
    ---------
    """
    input_ids, attention_mask = embedding(
        input_text, "google/mobilebert-uncased")
    model = load_model("google/mobilebert-uncased")
    class_prob, pred = inference(model, input_ids, attention_mask)
    return (
        class_prob.detach().cpu().numpy()[0],
        pred.detach().cpu().numpy()[0],
    )
