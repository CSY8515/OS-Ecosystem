from ai_hub.domain.predictions import UsagePrediction, predict_usage_limit


class UsagePredictionService:
    def predict(self, **evidence) -> UsagePrediction:
        return predict_usage_limit(**evidence)
