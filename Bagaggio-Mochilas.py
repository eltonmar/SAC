import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar o Selenium para usar o ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Iniciar a contagem de tempo
start_time = time.time()

# Contador de requisições
request_count = 0

# Lista para armazenar títulos de produtos
product_titles = []

# Função para extrair informações de produtos em uma página
def extract_product_info():
    products = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-container')
    for product in products:
        try:
            # Extrair o título
            title_element = product.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')
            product_title = title_element.text.strip()

            # Verificar se o título não está vazio
            if not product_title:
                continue

            # Adicionar o título à lista
            product_titles.append(product_title)

            # Extrair a URL da imagem
            try:
                image_element = product.find_element(By.CSS_SELECTOR, '.vtex-product-summary-2-x-imageContainer img')
                product_image_url = image_element.get_attribute('src')
            except:
                product_image_url = 'URL da imagem não encontrada'

            # Extrair o preço original
            try:
                original_price_element = product.find_element(By.CLASS_NAME, 'vtex-product-price-1-x-listPriceValue')
                product_original_price = original_price_element.text
            except:
                product_original_price = 'Preço original não encontrado'

            # Extrair o preço com desconto
            try:
                discount_price_element = product.find_element(By.CLASS_NAME, 'vtex-product-price-1-x-spotPriceValue')
                product_discount_price = discount_price_element.text
            except:
                product_discount_price = 'Preço com desconto não encontrado'

            # Extrair as tags
            tag_elements = product.find_elements(By.CLASS_NAME, 'vtex-product-highlights-2-x-productHighlightText')
            product_tags = [tag.text for tag in tag_elements]

            # Imprimir as informações do produto
            print(f'Título: {product_title}')
            print(f'URL da Imagem: {product_image_url}')
            print(f'Preço Original: {product_original_price}')
            print(f'Preço com Desconto: {product_discount_price}')
            print(f'Tags: {", ".join(product_tags)}')
            print(f'DIV HTML:\n{product.get_attribute("outerHTML")}\n')

        except Exception as e:
            print(f'Erro ao extrair informações de um produto: {e}')

# Iterar sobre as páginas
for page in range(1, 2):
    url = f'https://www.bagaggio.com.br/todos-produtos?page={page}'
    driver.get(url)
    request_count += 1

    # Aguardar carregar a página
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Extrair informações dos produtos
    extract_product_info()

# Fechar o navegador
driver.quit()

# Calcular o tempo total
end_time = time.time()
total_time = end_time - start_time

# Aviso sobre o número de requisições e o tempo total
print(f'Número total de requisições feitas: {request_count}')
print(f'Tempo total gasto: {total_time:.2f} segundos')

# Informar quantos produtos diferentes foram encontrados
unique_product_titles = set(product_titles)
print(f'Número total de produtos diferentes encontrados: {len(unique_product_titles)}')
