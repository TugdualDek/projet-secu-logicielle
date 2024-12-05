import zxcvbn

class PasswordVulnerabilityScanner:
    @staticmethod
    def estimate_password_strength(password: str):
        result = zxcvbn.zxcvbn(password)
        score = result.get('score', 0)  # 0-4, 4 étant le plus fort
        if score < 2:
            print(f"Mot de passe faible. Score : {score}/4")
            print(f"Suggestions : {result['feedback']['suggestions']}")
        return score
