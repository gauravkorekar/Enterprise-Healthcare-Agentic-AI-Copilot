from Backend.Evaluation.judge import judge
from Backend.Evaluation.metrics import calculate_average

from Backend.Logs.logger import logger


class EvaluationAgent:

    def run(
        self,
        question,
        context,
        answer
    ):

        scores = judge.evaluate(
            question,
            context,
            answer
        )

        average = calculate_average(scores)

        logger.info(
            f"[EVALUATION] {scores}"
        )

        logger.info(
            f"[EVALUATION] Average Score : {average}"
        )

        return {
            "scores": scores,
            "average_score": average
        }


evaluation_agent = EvaluationAgent()