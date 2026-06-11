"""
TITANIUM AUTO-REFRESH TOKEN
============================
Roda no GitHub Actions. Lê o token atual dos env vars (GitHub Secrets),
renova via API Meta, atualiza os PHPs e faz deploy via FTP.
Também escreve o novo token em GITHUB_OUTPUT para o workflow salvar no Secret.
"""
import os, sys, re, ftplib, requests

def main():
    print("=" * 60)
    print("TITANIUM TOKEN MANAGER — Auto-Refresh (CI/CD)")
    print("=" * 60)

    APP_ID     = os.environ.get('APP_ID', '')
    APP_SECRET = os.environ.get('APP_SECRET', '')
    OLD_TOKEN  = os.environ.get('IG_ACCESS_TOKEN', '')
    FTP_HOST   = os.environ.get('FTP_HOST', '')
    FTP_USER   = os.environ.get('FTP_USER', '')
    FTP_PASS   = os.environ.get('FTP_PASS', '')

    if not all([APP_ID, APP_SECRET, OLD_TOKEN]):
        print("ERRO FATAL: Secrets ausentes no GitHub!")
        print(f"  APP_ID: {'OK' if APP_ID else 'AUSENTE'}")
        print(f"  APP_SECRET: {'OK' if APP_SECRET else 'AUSENTE'}")
        print(f"  IG_ACCESS_TOKEN: {'OK' if OLD_TOKEN else 'AUSENTE'}")
        print()
        print("ACAO NECESSARIA: Adicione estes secrets em:")
        print("  GitHub > Settings > Secrets and variables > Actions")
        sys.exit(1)

    # PASSO 1: Renovar o token via API Meta
    print(f"\n[1] Renovando token via API Meta...")
    resp = requests.get(
        "https://graph.facebook.com/v21.0/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": OLD_TOKEN
        },
        timeout=30
    )
    data = resp.json()

    if 'access_token' not in data:
        print(f"ERRO ao renovar token: {data}")
        sys.exit(1)

    NEW_TOKEN  = data['access_token']
    expires_in = data.get('expires_in', 0)
    print(f"   Novo token obtido! Valido por {int(expires_in)//86400} dias.")
    print(f"   Token (inicio): {NEW_TOKEN[:25]}...")

    # PASSO 2: Verificar que o token funciona
    print(f"\n[2] Verificando novo token...")
    verify = requests.get(
        "https://graph.facebook.com/v21.0/me",
        params={"access_token": NEW_TOKEN, "fields": "id,name"},
        timeout=15
    ).json()
    if 'error' in verify:
        print(f"ERRO na verificacao: {verify}")
        sys.exit(1)
    print(f"   Conta: {verify.get('name')} (ID: {verify.get('id')})")

    # PASSO 3: Atualizar bot_instagram.php (Moda)
    print(f"\n[3] Atualizando social/bot_instagram.php (Moda)...")
    php_path = 'social/bot_instagram.php'
    with open(php_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\$USER_TOKEN\s*=\s*"[^"]*"', f'$USER_TOKEN = "{NEW_TOKEN}"', content)
    with open(php_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("   Moda: OK")

    # PASSO 4: Atualizar bot_instagram_pesca.php (Pesca)
    print(f"\n[4] Atualizando pesca/bot_instagram_pesca.php (Pesca)...")
    pesca_path = 'pesca/bot_instagram_pesca.php'
    with open(pesca_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\$USER_TOKEN\s*=\s*"[^"]*"', f'$USER_TOKEN = "{NEW_TOKEN}"', content)
    with open(pesca_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("   Pesca: OK")

    # PASSO 5: Deploy via FTP
    print(f"\n[5] Deploy FTP -> Hostinger...")
    if FTP_HOST and FTP_USER and FTP_PASS:
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS, timeout=30)
        with open(php_path, 'rb') as f:
            ftp.storbinary('STOR bot_instagram.php', f)
        print("   bot_instagram.php (Moda) -> OK")
        with open(pesca_path, 'rb') as f:
            ftp.storbinary('STOR bot_instagram_pesca.php', f)
        print("   bot_instagram_pesca.php (Pesca) -> OK")
        ftp.quit()
    else:
        print("   AVISO: Secrets FTP ausentes. Deploy FTP ignorado.")

    # PASSO 6: Escrever novo token no GITHUB_OUTPUT
    # (O workflow vai pegar isso e salvar de volta no GitHub Secret)
    print(f"\n[6] Salvando novo token no GitHub Output...")
    gh_output = os.environ.get('GITHUB_OUTPUT', '')
    if gh_output:
        with open(gh_output, 'a') as f:
            f.write(f"new_token={NEW_TOKEN}\n")
        print("   GITHUB_OUTPUT atualizado!")
    else:
        print("   (GITHUB_OUTPUT nao disponivel - rodando localmente)")

    print()
    print("=" * 60)
    print("AUTO-REFRESH COMPLETO!")
    print(f"Ambos os robos operacionais por mais {int(expires_in)//86400} dias.")
    print("=" * 60)

if __name__ == '__main__':
    main()
