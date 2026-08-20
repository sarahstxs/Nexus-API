import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/router", tags=["router"])

@router.get("/meu-endpoint-integrado")
async def buscar_dados_externos():
    url_da_api_externa = "https://comicvine.gamespot.com/api/characters/?api_key=d415fd62e1a91e2650bdd88329ed51dc2ce534c5&format=json&filter=name:Spider-Man"

    headers = {
        "User-Agent": "MeuAplicativoDeQuadrinhos_v1.0"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resposta = await client.get(url_da_api_externa, headers=headers)
        
    if resposta.status_code != 200:
        raise HTTPException(
            status_code=resposta.status_code, 
            detail=f"A API externa falhou. Código: {resposta.status_code}"
        )
        
    # Transforma a resposta em um dicionário Python
    dados = resposta.json()
    
    # 1. Acessamos a chave "results", que contém a lista de personagens encontrados
    lista_resultados = dados.get("results", [])
    
    # 2. Verificamos se a API realmente encontrou alguém para não dar erro
    if len(lista_resultados) == 0:
        return {"mensagem": "Nenhum personagem encontrado com esse nome."}
        
    # 3. Pegamos o primeiro personagem da lista (posição 0)
    primeiro_personagem = lista_resultados[0]
    
    # 4. Extraímos apenas os campos específicos que queremos desse personagem!
    nome_personagem = primeiro_personagem.get("name")
    resumo_personagem = primeiro_personagem.get("deck") # 'deck' é o resumo na Comic Vine
    imagem_url = primeiro_personagem.get("image", {}).get("original_url")
    
    # 5. Devolvemos uma resposta limpa e enxuta para quem chamou a nossa API
    return {
        "nome": nome_personagem,
        "resumo": resumo_personagem,
        "imagem": imagem_url
    }