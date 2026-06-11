from collections.abc import Callable

from fastapi import Request

from app.config import get_settings

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "World Cup Pool 2026": "World Cup Pool 2026",
        "Welcome to the betting pool for the 2026 FIFA World Cup.": (
            "Welcome to the betting pool for the 2026 FIFA World Cup."
        ),
        "FIFA World Cup 2026": "FIFA World Cup 2026",
        "Predict. Compete. Celebrate.": "Predict. Compete. Celebrate.",
        "Join the pool": "Join the pool",
        "Log in": "Log in",
        "Log out": "Log out",
        "Sign up": "Sign up",
        "This username is already taken.": "This username is already taken.",
        "Invalid username or password.": "Invalid username or password.",
        "This account is inactive.": "This account is inactive.",
        "Pick every score": "Pick every score",
        "Submit your predictions before kickoff and chase the perfect scoreline.": (
            "Submit your predictions before kickoff and chase the perfect scoreline."
        ),
        "Climb the table": "Climb the table",
        "Earn points for exact scores and correct results. Track your rank live.": (
            "Earn points for exact scores and correct results. Track your rank live."
        ),
        "Play with friends": "Play with friends",
        "A private bolão built for your crew across Brazil, the USA, and beyond.": (
            "A private bolão built for your crew across Brazil, the USA, and beyond."
        ),
        "Trionda spirit": "Trionda spirit",
        "United across three nations. One tournament.": "United across three nations. One tournament.",
        "Home": "Home",
        "Matches": "Matches",
        "Leaderboard": "Leaderboard",
        "Your dashboard": "Your dashboard",
        "Welcome back": "Welcome back",
        "The group stage opens soon. Place your bets and follow the leaderboard.": (
            "The group stage opens soon. Place your bets and follow the leaderboard."
        ),
        "Upcoming matches": "Upcoming matches",
        "Coming soon": "Coming soon",
        "Match cards with HTMX bet forms will appear here once the schedule is loaded.": (
            "Match cards with HTMX bet forms will appear here once the schedule is loaded."
        ),
        "Rankings update after each final whistle.": "Rankings update after each final whistle.",
        "Invite your friends": "Invite your friends",
        "Share the pool and compete across every stage of the tournament.": (
            "Share the pool and compete across every stage of the tournament."
        ),
        "Account": "Account",
        "Enter your credentials to access your predictions.": (
            "Enter your credentials to access your predictions."
        ),
        "Username": "Username",
        "Your username": "Your username",
        "Password": "Password",
        "No account yet?": "No account yet?",
        "Create one": "Create one",
        "Create your account and join the 2026 pool.": "Create your account and join the 2026 pool.",
        "Display name": "Display name",
        "How friends will see you": "How friends will see you",
        "Choose a username": "Choose a username",
        "At least 8 characters": "At least 8 characters",
        "Confirm password": "Confirm password",
        "Repeat your password": "Repeat your password",
        "Create account": "Create account",
        "Already have an account?": "Already have an account?",
        "Passwords do not match.": "Passwords do not match.",
        "Save Bet": "Save Bet",
        "API": "API",
        "Health": "Health",
        "Admin": "Admin",
        "Group": "Group",
        "Match day": "Match day",
        "Match day navigation": "Match day navigation",
        "Previous day": "Previous day",
        "Next day": "Next day",
        "No matches on this day.": "No matches on this day.",
    },
    "pt_BR": {
        "World Cup Pool 2026": "Bolão Copa do Mundo 2026",
        "Welcome to the betting pool for the 2026 FIFA World Cup.": (
            "Bem-vindo ao bolão da Copa do Mundo FIFA 2026."
        ),
        "FIFA World Cup 2026": "Copa do Mundo FIFA 2026",
        "Predict. Compete. Celebrate.": "Palpite. Compita. Comemore.",
        "Join the pool": "Entrar no bolão",
        "Log in": "Entrar",
        "Log out": "Sair",
        "Sign up": "Cadastrar",
        "This username is already taken.": "Este usuário já está em uso.",
        "Invalid username or password.": "Usuário ou senha inválidos.",
        "This account is inactive.": "Esta conta está inativa.",
        "Pick every score": "Palpite cada placar",
        "Submit your predictions before kickoff and chase the perfect scoreline.": (
            "Envie seus palpites antes do apito inicial e busque o placar perfeito."
        ),
        "Climb the table": "Suba na tabela",
        "Earn points for exact scores and correct results. Track your rank live.": (
            "Ganhe pontos por placar exato e resultado correto. Acompanhe sua posição ao vivo."
        ),
        "Play with friends": "Jogue com amigos",
        "A private bolão built for your crew across Brazil, the USA, and beyond.": (
            "Um bolão privado para sua galera no Brasil, EUA e além."
        ),
        "Trionda spirit": "Espírito Trionda",
        "United across three nations. One tournament.": "Três nações unidas. Um só torneio.",
        "Home": "Início",
        "Matches": "Jogos",
        "Leaderboard": "Classificação",
        "Your dashboard": "Seu painel",
        "Welcome back": "Bem-vindo de volta",
        "The group stage opens soon. Place your bets and follow the leaderboard.": (
            "A fase de grupos começa em breve. Faça seus palpites e acompanhe a classificação."
        ),
        "Upcoming matches": "Próximos jogos",
        "Coming soon": "Em breve",
        "Match cards with HTMX bet forms will appear here once the schedule is loaded.": (
            "Os cartões de jogos com formulários HTMX aparecerão aqui quando a tabela for carregada."
        ),
        "Rankings update after each final whistle.": (
            "A classificação é atualizada após cada apito final."
        ),
        "Invite your friends": "Convide seus amigos",
        "Share the pool and compete across every stage of the tournament.": (
            "Compartilhe o bolão e dispute em todas as fases do torneio."
        ),
        "Account": "Conta",
        "Enter your credentials to access your predictions.": (
            "Informe suas credenciais para acessar seus palpites."
        ),
        "Username": "Usuário",
        "Your username": "Seu usuário",
        "Password": "Senha",
        "No account yet?": "Ainda não tem conta?",
        "Create one": "Crie uma",
        "Create your account and join the 2026 pool.": "Crie sua conta e entre no bolão 2026.",
        "Display name": "Nome de exibição",
        "How friends will see you": "Como seus amigos verão você",
        "Choose a username": "Escolha um usuário",
        "At least 8 characters": "Mínimo de 8 caracteres",
        "Confirm password": "Confirmar senha",
        "Repeat your password": "Repita sua senha",
        "Create account": "Criar conta",
        "Already have an account?": "Já tem uma conta?",
        "Passwords do not match.": "As senhas não coincidem.",
        "Save Bet": "Salvar Palpite",
        "API": "API",
        "Health": "Status",
        "Admin": "Administração",
        "Group": "Grupo",
        "Match day": "Dia de jogos",
        "Match day navigation": "Navegação por dia",
        "Previous day": "Dia anterior",
        "Next day": "Próximo dia",
        "No matches on this day.": "Nenhum jogo neste dia.",
    },
}


def get_locale_from_request(request: Request) -> str:
    settings = get_settings()
    query_locale = request.query_params.get("lang")
    if query_locale and query_locale in settings.locale_list:
        return query_locale

    accept_language = request.headers.get("accept-language", "")
    for part in accept_language.split(","):
        candidate = part.split(";")[0].strip()
        if candidate in settings.locale_list:
            return candidate
        if candidate.startswith("pt") and "pt_BR" in settings.locale_list:
            return "pt_BR"

    return settings.default_locale


def get_translator(locale: str) -> Callable[[str], str]:
    catalog = TRANSLATIONS.get(locale, TRANSLATIONS["en"])

    def translate(message: str) -> str:
        return catalog.get(message, message)

    return translate
