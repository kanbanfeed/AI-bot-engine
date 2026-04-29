from modules.comment_builder import create_comment

# mock account (simulate DB row)
account = {
    "account_id": 1,
    "opener_position": 1,
    "closer_position": 1
}

phase_ii = """You have not admitted to yourself that your manager may not view you as a candidate for promotion at all, which directly impacts your confidence in seeking a raise or advancement. This judgment from your manager is not about your skills or potential, but rather their perception of your performance and fit within the team's goals. What does it mean for your future at this company if you are not even on their radar for promotion?"""

result, error = create_comment(account, phase_ii)

if error:
    print("ERROR:", error)
else:
    print("\nCOMMENT:\n")
    print(result["comment"])