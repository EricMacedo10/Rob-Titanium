                    target['store'],
                    keyword=term  # Passa palavra-chave para ML
                )
                
                products_found.append(product)
            else:
                print(f"❌ Preço alto ({price_integer} > {max_price_integer}). Ignorando.")
        else:
             print(f"💨 Produto não encontrado ou erro na busca.")




    # 5. Salvar JSON Local
    local_path = 'site/data.json'
    print("\n" + "="*60)
    if products_found:
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(products_found, f, indent=4, ensure_ascii=False)
        print(f"💾 Arquivo {local_path} atualizado com {len(products_found)} ofertas reais.")
    else:
        print("⚠ Nenhuma oferta nova encontrada. Arquivo data.json mantido.")




    # 6. Upload FTP para Hostinger
    if products_found:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        ftp_host = os.getenv('FTP_HOST')
        ftp_user = os.getenv('FTP_USER')
        ftp_pass = os.getenv('FTP_PASS')
        
        if ftp_host and ftp_user and ftp_pass:
            print("\n🌐 Iniciando upload para Hostinger...")
            upload_success = upload_to_hostinger(
                local_file_path=local_path,
                ftp_host=ftp_host,
                ftp_user=ftp_user,
                ftp_pass=ftp_pass,
                remote_path='public_html/data.json'
            )
            if upload_success:
                print("🎉 Site atualizado com sucesso!")
            else:
                print("⚠️ Upload falhou, mas arquivo local foi salvo.")
        else:
            print("⚠️ Credenciais FTP não configuradas. Apenas salvando localmente.")
    
    # 7. Resumo da Execução
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print("📊 RESUMO DA EXECUÇÃO")
    print("=" * 60)
    print(f"✅ Produtos encontrados: {len(products_found)}")
    print(f"❌ Erros encontrados: {len(errors)}")
    print(f"⏱️  Tempo total: {duration:.1f}s ({duration/60:.1f} min)")
    print(f"📅 Finalizado em: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if errors:
        print("\n⚠️  ERROS DETALHADOS:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    print("=" * 60)
    print("🎉 Robô Titanium finalizado!")
    print("=" * 60)




if __name__ == "__main__":
    main()
