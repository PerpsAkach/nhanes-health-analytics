from src.evaluation import challenger_decision


def test_challenger_requires_all_guardrails():
    benchmark = {"roc_auc": 0.66, "pr_auc": 0.50, "brier": 0.22, "ece10": 0.07}
    challenger = {"roc_auc": 0.68, "pr_auc": 0.53, "brier": 0.21, "ece10": 0.05}
    assert challenger_decision(benchmark, challenger, [])["keep"] is True
    assert challenger_decision(benchmark, challenger, ["male recall degraded"])["keep"] is False
