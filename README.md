# API de Detecção e Decodificação de QR/Barcode

Esta é uma API de alta performance construída com FastAPI que detecta e decodifica códigos QR e outros tipos de códigos de barras a partir de um arquivo de imagem.

A ideia é simular o funcionamento de um serviço como o ML Kit do Google, onde um *frame* (imagem) é enviado e o conteúdo do código de barras é retornado.

O projeto utiliza uma abordagem de duas etapas para maior precisão e velocidade:
1.  **Detecção**: Um modelo YOLOv8 (`YOLOV8s_Barcode_Detection.pt`) é usado para localizar a posição dos códigos de barras na imagem.
2.  **Decodificação**: A biblioteca `pyzbar` é usada para ler o conteúdo apenas da área recortada onde o código foi detectado.

## Pré-requisitos

*   Python 3.11+
*   Docker (para execução via contêiner)

## Arquivos do Projeto

*   `main.py`: O código principal da aplicação FastAPI.
*   `requirements.txt`: As dependências Python necessárias para o projeto.
*   `Dockerfile`: As instruções para construir a imagem Docker da aplicação.
*   `YOLOV8s_Barcode_Detection.pt`: O modelo de machine learning treinado para detectar códigos de barras.

## Configuração e Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-diretorio>
    ```

2.  **Instale as dependências:**
    Certifique-se de que o arquivo `YOLOV8s_Barcode_Detection.pt` está no mesmo diretório.
    ```bash
    pip install -r requirements.txt
    ```

## Como Executar a Aplicação

Você pode executar a API de duas maneiras:

### 1. Localmente com Uvicorn

Execute o seguinte comando no seu terminal:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
A API estará disponível em `http://127.0.0.1:8000`.

### 2. Usando Docker

O `Dockerfile` fornecido facilita a conteinerização da aplicação.

1.  **Construa a imagem Docker:**
    ```bash
    docker build -t qr-decoder-api .
    ```

2.  **Execute o contêiner:**
    ```bash
    docker run -p 8000:8000 qr-decoder-api
    ```
    A API estará disponível em `http://127.0.0.1:8000`.

### 3. Usando a Imagem do Docker Hub (Recomendado)

A imagem Docker é construída e enviada automaticamente para o Docker Hub através de uma pipeline de CI/CD.

1.  **Puxe a imagem mais recente:**
    ```bash
    docker pull leandrofreires/qr-decoder-api:latest
    ```

2.  **Execute o contêiner:**
    ```bash
    docker run -p 8000:8000 leandrofreires/qr-decoder-api:latest
    ```

## Como Usar a API

### Endpoint: `POST /decode_qr/`

Este endpoint aceita o upload de um arquivo de imagem (`multipart/form-data`) e retorna os dados decodificados dos códigos de barras encontrados.

**Exemplo de requisição com `curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/decode_qr/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/para/sua/imagem.png"
```

**Exemplo de Resposta de Sucesso:**
```json
{
  "decoded_qrs": [
    {
      "type": "QRCODE",
      "data": "Conteúdo do QR Code aqui"
    }
  ]
}
```

**Exemplo de Resposta (Código não encontrado):**
```json
{
  "message": "No QR code found or could not be decoded."
}
```
