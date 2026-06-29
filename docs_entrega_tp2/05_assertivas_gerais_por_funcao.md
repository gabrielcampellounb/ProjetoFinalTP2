# 05 — Assertivas gerais por função

Esta tabela consolida funções e métodos relevantes encontrados no código da aplicação. Funções auxiliares privadas foram incluídas quando sustentam validações ou persistência importantes. Quando o teste específico não foi localizado de forma direta, foi indicado o teste de integração mais próximo ou “teste não localizado”.

## Grupo 1 — Autenticação, usuários, sessão e perfis

| Assinatura | Arquivo | Grupo | Integrantes | Entrada esperada | Saída garantida | Invariante | Argumento de corretude | Requisito | Teste |
|---|---|---|---|---|---|---|---|---|---|
| `User.__init__(name, email, password_hash, role, user_id=None)` | `app/domain/user.py` | G1 | Gabriel Balder; Anabel Mendes | atributos válidos | instância `User` | papel em `user/admin` | valida cada campo antes de atribuir | RQ-G1-001 | `test_user.py` |
| `User._validate_user_id(user_id)` | `app/domain/user.py` | G1 | Gabriel Balder; Anabel Mendes | `None` ou int | id normalizado | bool não aceito | impede id inválido persistido | RQ-G1-001 | `test_user.py` |
| `User._validate_name(name)` | `app/domain/user.py` | G1 | Gabriel Balder; Anabel Mendes | string não vazia | nome stripado | sem nome vazio | normaliza entrada | RQ-G1-001 | `test_user.py` |
| `User._validate_email(email)` | `app/domain/user.py` | G1 | Gabriel Balder; Anabel Mendes | string com `@` | e-mail minúsculo | único no repo | rejeita formato mínimo inválido | RQ-G1-001 | `test_user.py` |
| `User._validate_password_hash(password_hash)` | `app/domain/user.py` | G1 | Gabriel Balder; Anabel Mendes | hash string | hash aceito | não vazio | impede credencial vazia | RQ-G1-002 | `test_user.py` |
| `User._validate_role(role)` | `app/domain/user.py` | G1 | Gabriel Balder; Anabel Mendes | `user` ou `admin` | papel | conjunto fechado | sustenta autorização | RQ-G1-005 | `test_user.py` |
| `UserService.__init__(user_repository)` | `app/application/user_service.py` | G1 | Gabriel Balder; Anabel Mendes | repo com add/get | serviço | dependência injetada | separa aplicação e infra | RQ-G1-001 | `test_user_service.py` |
| `UserService.create_user(name, email, password, role='user')` | `app/application/user_service.py` | G1 | dados cadastrais | `User` persistido | senha vira hash | verifica duplicidade antes de persistir | RQ-G1-001/002 | `test_user_service.py` |
| `UserService.authenticate_user(email, password)` | `app/application/user_service.py` | G1 | credenciais | `User` autenticado | senha compara hash | só retorna se e-mail e senha conferem | RQ-G1-003 | `test_auth_routes.py` |
| `UserService._validate_password(password)` | `app/application/user_service.py` | G1 | string | senha aceita | não vazia | evita hash de valor inválido | RQ-G1-002 | `test_user_service.py` |
| `SQLiteUserRepository.create_table()` | `app/infrastructure/user_repository.py` | G1 | conexão aberta | tabela `users` | e-mail único; role com CHECK | DDL define restrições | RQ-G1-001 | `test_user_repository.py` |
| `SQLiteUserRepository.add_user(user)` | `app/infrastructure/user_repository.py` | G1 | `User` válido | id preenchido | duplicidade controlada | converte `IntegrityError` em erro de domínio | RQ-G1-001 | `test_user_repository.py` |
| `SQLiteUserRepository.get_user_by_email(email)` | `app/infrastructure/user_repository.py` | G1 | e-mail | `User` ou `None` | busca case-insensitive | retorna domínio, não row cru | RQ-G1-003 | `test_user_repository.py` |
| `create_auth_blueprint(user_service)` | `app/web/auth_routes.py` | G1 | serviço | blueprint | rotas sem SQL direto | delega ao serviço | RQ-G1-001/003/004 | `test_auth_routes.py` |
| `_serialize_user(user)` | `app/web/auth_routes.py` | G1 | `User` | dict público | hash não exposto | omite `password_hash` | RQ-G1-002 | `test_auth_routes.py` |
| `authenticated_required(view_function)` | `app/web/authorization.py` | G1 | view | wrapper | sem `user_id` retorna 401 | verifica sessão antes da view | RQ-G1-005 | testes de rotas protegidas |
| `admin_required(view_function)` | `app/web/authorization.py` | G1 | view | wrapper | role admin obrigatório | diferencia 401 e 403 | RQ-G1-005 | `test_product_routes.py` |
| `create_html_blueprint(...)` | `app/web/html_routes.py` | G1/G2/G3 | todos | serviços inicializados | blueprint HTML | rotas chamam serviços | integra camadas | vários | `test_html_routes.py` |
| `_start_session(user)` | `app/web/html_routes.py` | G1 | `User` | sessão atualizada | `user_id` e `role` presentes | limpa sessão antes | RQ-G1-003 | `test_html_routes.py` |

## Grupo 2 — Catálogo, produtos, estoque e administração

| Assinatura | Arquivo | Grupo | Integrantes | Entrada esperada | Saída garantida | Invariante | Argumento de corretude | Requisito | Teste |
|---|---|---|---|---|---|---|---|---|---|
| `Product.__init__(name, brand, price, bar_code)` | `app/domain/product.py` | G2 | Dionilton; Jhonny | dados válidos | `Product` | preço não negativo | valida antes de atribuir | RQ-G2-001 | `test_product.py` |
| `Product._validate_text(value, field_label, article, empty_adjective)` | `app/domain/product.py` | G2 | Dionilton; Jhonny | texto | texto stripado | não vazio | centraliza validação | RQ-G2-001 | `test_product.py` |
| `validate_quantity(quantity)` | `app/domain/quantity.py` | G2/G3 | Dionilton; Jhonny | inteiro não negativo | inteiro | bool rejeitado | impede estoque negativo | RQ-G2-005 | `test_product_service.py` |
| `ProductService.create_product(name, brand, price, bar_code, quantity)` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | dados produto | `Product` | repo recebe entidade e quantidade | domínio valida dados | RQ-G2-001 | `test_product_routes.py` |
| `ProductService.search_products(query)` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | string | lista | query vazia sem consulta | evita busca ampla indevida no método | RQ-G2-002 | `test_product_service.py` |
| `ProductService.list_products()` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | repo pronto | lista | ativos | delega ao repo | RQ-G2-002 | teste indireto HTML |
| `ProductService.list_products_page(query, page, page_size)` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | paginação | página e totais | page >= 1 | calcula offset e total | RQ-G2-002 | `test_html_routes.py` |
| `ProductService.get_product(bar_code)` | `app/application/product_service.py` | G2/G3 | Dionilton; Jhonny | código | produto/quantidade | erro se ausente | usa `_get_product_or_raise` | RQ-G2-002 | vários |
| `ProductService.update_product(bar_code, name, brand, price)` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | dados editáveis | produto atualizado | código preservado | reconstrói domínio válido | RQ-G2-003 | `test_product_service.py` |
| `ProductService.deactivate_product(bar_code)` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | código existente | None | remoção lógica | consulta antes de inativar | RQ-G2-004 | `test_product_service.py` |
| `ProductService.update_stock(bar_code, quantity)` | `app/application/product_service.py` | G2 | Dionilton; Jhonny | quantidade válida | produto/quantidade | estoque não negativo | valida antes de persistir | RQ-G2-005 | `test_product_service.py` |
| `SQLiteProductRepository.create_table()` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | conexão | tabela | coluna `active` | cria/migra schema | RQ-G2-001/004 | `test_product_repository.py` |
| `SQLiteProductRepository.add_product(product, quantity)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | produto e quantidade | registro | PK por `bar_code` | verifica duplicidade | RQ-G2-001 | `test_product_repository.py` |
| `SQLiteProductRepository.get_product_by_bar_code(bar_code)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | código | tupla ou None | converte para domínio | SELECT único por PK | RQ-G2-002 | `test_product_repository.py` |
| `SQLiteProductRepository.search_products_by_text(query)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | texto | lista | `active=1` | usa LIKE nome/marca | RQ-G2-002 | `test_product_repository.py` |
| `SQLiteProductRepository.list_active_products()` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | tabela | lista | só ativos | filtro SQL | RQ-G2-002/004 | testes HTML |
| `SQLiteProductRepository.list_active_products_page(query, limit, offset)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | paginação | lista parcial | LIMIT/OFFSET | SQL paginado | RQ-G2-002 | `test_html_routes.py` |
| `SQLiteProductRepository.count_active_products(query)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | texto | int | mesmo filtro da página | suporta paginação correta | RQ-G2-002 | `test_html_routes.py` |
| `SQLiteProductRepository.update_product(product)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | Product | commit | não altera PK | UPDATE campos editáveis | RQ-G2-003 | `test_product_repository.py` |
| `SQLiteProductRepository.deactivate_product(bar_code)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | código | commit | `active=0` | sem DELETE físico | RQ-G2-004 | `test_product_repository.py` |
| `SQLiteProductRepository.update_stock(bar_code, quantity)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | quantidade | commit | não negativa | chama `validate_quantity` | RQ-G2-005 | `test_product_repository.py` |
| `SQLiteProductRepository._ensure_active_column()` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | tabela antiga | coluna ativa | compatibilidade | usa PRAGMA e ALTER | RQ-G2-004 | `test_product_repository.py` |
| `SQLiteProductRepository._to_product_with_quantity(row)` | `app/infrastructure/product_repository.py` | G2 | Dionilton; Jhonny | row | `(Product,int)` | domínio reconstruído | evita rows fora da infra | RQ-G2-002 | indireto |
| `AdminMetricsService.get_metrics()` | `app/application/admin_metrics_service.py` | G2 | Dionilton; Jhonny | repo | dict | chaves fixas | delega contagem | RQ-G2-007 | `test_admin_metrics_repository.py` |
| `SQLiteAdminMetricsRepository.get_metrics()` | `app/infrastructure/admin_metrics_repository.py` | G2 | Dionilton; Jhonny | conexão | dict contagens | 4 totais | SQL único retorna métricas | RQ-G2-007 | `test_admin_metrics_repository.py` |
| `create_product_blueprint(product_service)` | `app/web/routes.py` | G2 | Dionilton; Jhonny | serviço | blueprint | admin nas mutações | rotas finas | RQ-G2-001..006 | `test_product_routes.py` |
| `create_admin_metrics_blueprint(metrics_service)` | `app/web/admin_metrics_routes.py` | G2 | Dionilton; Jhonny | serviço | blueprint | admin obrigatório | decorator protege | RQ-G2-007 | `test_admin_metrics_routes.py` |
| `serialize_product(product, quantity)` | `app/web/serializers.py` | G2/G3 | Dionilton; Jhonny | Product/quantidade | dict JSON | contrato da API | padroniza resposta | RQ-G2-001/002 | rotas de produto |

## Grupo 3 — Listas, carrinho, preços, locais e total

| Assinatura | Arquivo | Grupo | Integrantes | Entrada esperada | Saída garantida | Invariante | Argumento de corretude | Requisito | Teste |
|---|---|---|---|---|---|---|---|---|---|
| `ShoppingList.__init__(list_id, user_id, name, created_at, favorite=False)` | `domain/shopping_list.py` | G3 | Gabriel Dylan; Gabriel Campello; Luiz Otávio | dados lista | lista | user_id positivo; nome não vazio | valida campos | RQ-G3-001/002 | `test_shopping_list.py` |
| `ShoppingListItem.__init__(list_id, bar_code, quantity)` | `domain/shopping_list.py` | G3 | Gabriel Dylan; Gabriel Campello; Luiz Otávio | item | item | quantidade > 0 | valida item antes do repo | RQ-G3-003 | `test_shopping_list_service.py` |
| `ShoppingListService.create_shopping_list(user_id, name)` | `application/shopping_list_service.py` | G3 | idem | user/nome | lista | user_id da sessão | clock gera data | RQ-G3-001 | `test_shopping_list_service.py` |
| `ShoppingListService.list_shopping_lists(user_id)` | `application/shopping_list_service.py` | G3 | idem | user_id | listas | só do usuário | repo filtra por user_id | RQ-G3-001 | `test_shopping_list_service.py` |
| `ShoppingListService.mark_as_favorite(user_id, list_id)` | `application/shopping_list_service.py` | G3 | idem | lista própria | favorita | uma favorita | valida posse antes | RQ-G3-002 | `test_shopping_list_service.py` |
| `ShoppingListService.add_item(user_id, list_id, bar_code, quantity)` | `application/shopping_list_service.py` | G3 | idem | produto/lista/qtd | item | lista própria/produto existente | valida dependências | RQ-G3-003 | `test_shopping_list_routes.py` |
| `ShoppingListService.get_shopping_list_details(user_id, list_id)` | `application/shopping_list_service.py` | G3 | idem | lista própria | lista e produtos | não vaza lista alheia | resolve produtos por repo | RQ-G3-003 | `test_html_routes.py` |
| `ShoppingListService.update_item(user_id, list_id, bar_code, quantity)` | `application/shopping_list_service.py` | G3 | idem | item existente | item atualizado | qtd > 0 | checa existência | RQ-G3-003 | `test_shopping_list_service.py` |
| `ShoppingListService.remove_item(user_id, list_id, bar_code)` | `application/shopping_list_service.py` | G3 | idem | item existente | None | lista própria | checa antes de remover | RQ-G3-003 | `test_shopping_list_service.py` |
| `SQLiteShoppingListRepository.create_table()` | `infrastructure/shopping_list_repository.py` | G3 | idem | conexão | tabelas | favorite existe | cria/migra schema | RQ-G3-001/002 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.add_shopping_list(shopping_list)` | `infrastructure/shopping_list_repository.py` | G3 | idem | lista | id | id autoincremento | INSERT e lastrowid | RQ-G3-001 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.set_favorite(user_id, list_id)` | `infrastructure/shopping_list_repository.py` | G3 | idem | user/list | commit | uma favorita | transação desfavorita outras | RQ-G3-002 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.add_item(item)` | `infrastructure/shopping_list_repository.py` | G3 | idem | item | commit | chave composta | impede duplicidade no SQLite | RQ-G3-003 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.get_item(list_id, bar_code)` | `infrastructure/shopping_list_repository.py` | G3 | idem | ids | item/None | busca composta | retorna domínio | RQ-G3-003 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.list_items(list_id)` | `infrastructure/shopping_list_repository.py` | G3 | idem | list_id | itens | ordenado por bar_code | filtro por lista | RQ-G3-003 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.update_item(item)` | `infrastructure/shopping_list_repository.py` | G3 | idem | item | commit | altera só quantidade | UPDATE por chave composta | RQ-G3-003 | `test_shopping_list_repository.py` |
| `SQLiteShoppingListRepository.remove_item(list_id, bar_code)` | `infrastructure/shopping_list_repository.py` | G3 | idem | ids | commit | remove item específico | DELETE composto | RQ-G3-003 | `test_shopping_list_repository.py` |
| `CartService.add_item(cart, bar_code, quantity)` | `application/cart_service.py` | G3 | idem | dict/qtd | dict mutado | qtd > 0 | valida e grava | RQ-G3-004 | `test_cart_routes.py` |
| `CartService.update_item(cart, bar_code, quantity)` | `application/cart_service.py` | G3 | idem | item existente | dict mutado | item existe | `_ensure_item_exists` | RQ-G3-004 | `test_cart_routes.py` |
| `CartService.remove_item(cart, bar_code)` | `application/cart_service.py` | G3 | idem | item existente | dict mutado | chave removida | erro se ausente | RQ-G3-004 | `test_cart_routes.py` |
| `CartService.get_items(cart)` | `application/cart_service.py` | G3 | idem | dict sessão | lista itens | cada bar_code resolvido | usa `ProductService` | RQ-G3-004 | `test_cart_routes.py` |
| `CartService.calculate_total(items)` | `application/cart_service.py` | G3 | idem | lista produto/qtd | total float | soma correta | itera e acumula | RQ-G3-005 | `test_cart_service.py` |
| `Store.__init__(store_id, name, address, observation, latitude, longitude)` | `domain/store.py` | G3 | idem | dados local | Store | coordenadas válidas/juntas | valida limites geográficos | RQ-G3-006/008 | `test_store.py` |
| `StoreService.create_store(name, address, observation, latitude, longitude)` | `application/store_service.py` | G3 | idem | dados | Store persistido | valida antes | domínio + repo | RQ-G3-006 | `test_store_service.py` |
| `StoreService.list_stores()` | `application/store_service.py` | G3 | idem | repo | lista | ordenação do repo | delega | RQ-G3-006 | `test_store_routes.py` |
| `StoreService.get_store(store_id)` | `application/store_service.py` | G3 | idem | id | Store/None | sem exceção | consulta repo | RQ-G3-006 | testes HTML |
| `StoreService.find_nearest_store(latitude, longitude)` | `application/store_service.py` | G3 | idem | coordenadas | Store/distância | menor distância | compara todos geolocalizados com `geopy` | RQ-G3-008 | `test_store_service.py` |
| `StoreService._validate_user_location(latitude, longitude)` | `application/store_service.py` | G3 | idem | coordenadas | tupla float | limites de Store | reutiliza validação de domínio | RQ-G3-008 | `test_store_service.py` |
| `SQLiteStoreRepository.create_table()` | `infrastructure/store_repository.py` | G3 | idem | conexão | tabela | latitude/longitude existem | cria/migra schema | RQ-G3-006/008 | `test_store_repository.py` |
| `SQLiteStoreRepository.add_store(store)` | `infrastructure/store_repository.py` | G3 | idem | Store | id | persiste coordenadas | INSERT completo | RQ-G3-006 | `test_store_repository.py` |
| `SQLiteStoreRepository.list_stores()` | `infrastructure/store_repository.py` | G3 | idem | tabela | lista | ordenação por nome/id | SELECT e conversão | RQ-G3-006 | `test_store_repository.py` |
| `SQLiteStoreRepository.get_store_by_id(store_id)` | `infrastructure/store_repository.py` | G3 | idem | id | Store/None | id único | SELECT por PK | RQ-G3-006 | `test_store_repository.py` |
| `SQLiteStoreRepository.update_store_coordinates(store_id, latitude, longitude)` | `infrastructure/store_repository.py` | G3 | idem | id/coordenadas | commit | coordenadas atualizadas | usado pelo seed | RQ-G3-008 | `test_demo_seed.py` |
| `ProductPrice.__init__(product_bar_code, store_id, user_id, price, created_at)` | `domain/product_price.py` | G3 | idem | dados preço | ProductPrice | preço não negativo | valida ids e data | RQ-G3-007 | `test_product_price_service.py` |
| `ProductPriceService.register_price(product_bar_code, store_id, user_id, price)` | `application/product_price_service.py` | G3 | idem | dados | ProductPrice | produto/local existem | checa repos antes | RQ-G3-007 | `test_product_price_routes.py` |
| `ProductPriceService.list_product_prices(product_bar_code)` | `application/product_price_service.py` | G3 | idem | produto | preços | produto existe | evita consulta de produto ausente | RQ-G3-007 | `test_product_price_service.py` |
| `ProductPriceService.list_product_price_details(product_bar_code)` | `application/product_price_service.py` | G3 | idem | produto | preço+loja | resolve loja | agrega detalhes | RQ-G3-007 | `test_mvp_html_routes.py` |
| `ProductPriceService.list_store_products_page(store_id, query, page, page_size)` | `application/product_price_service.py` | G3 | idem | loja/query/página | produtos/totais | loja existe | pagina preços por loja | RQ-G3-007 | `test_mvp_html_routes.py` |
| `SQLiteProductPriceRepository.create_table()` | `infrastructure/product_price_repository.py` | G3 | idem | conexão | tabela/index | histórico independente | cria índice por produto | RQ-G3-007 | `test_product_price_repository.py` |
| `SQLiteProductPriceRepository.add_price(product_price)` | `infrastructure/product_price_repository.py` | G3 | idem | ProductPrice | commit | histórico preservado | sempre INSERT | RQ-G3-007 | `test_product_price_repository.py` |
| `SQLiteProductPriceRepository.list_prices_by_product(product_bar_code)` | `infrastructure/product_price_repository.py` | G3 | idem | código | lista | mais recente primeiro | ORDER BY data/id | RQ-G3-007 | `test_product_price_repository.py` |
| `create_shopping_list_blueprint(shopping_list_service)` | `web/shopping_list_routes.py` | G3 | idem | serviço | blueprint | usa sessão | rotas finas | RQ-G3-001..003 | `test_shopping_list_routes.py` |
| `create_cart_blueprint(cart_service)` | `web/cart_routes.py` | G3 | idem | serviço | blueprint | carrinho em sessão | rotas delegam ao serviço | RQ-G3-004/005 | `test_cart_routes.py` |
| `create_store_blueprint(store_service)` | `web/store_routes.py` | G3 | idem | serviço | blueprint | admin para POST | rotas de loja/GPS | RQ-G3-006/008 | `test_store_routes.py` |
| `create_product_price_blueprint(product_price_service)` | `web/product_price_routes.py` | G3 | idem | serviço | blueprint | autenticado | rotas delegam | RQ-G3-007 | `test_product_price_routes.py` |
| `_optional_float(value)` | `web/html_routes.py` | G3 | idem | string opcional | float/None | campo vazio vira None | suporta formulário de loja | RQ-G3-006/008 | teste indireto HTML |

## Módulos transversais

| Assinatura | Arquivo | Grupo | Integrantes | Entrada esperada | Saída garantida | Invariante | Argumento de corretude | Requisito | Teste |
|---|---|---|---|---|---|---|---|---|---|
| `create_app(connection)` | `app/web/app.py` | G1/G2/G3 | todos | conexão SQLite | aplicação Flask | blueprints e handlers registrados | inicializa tabelas e serviços | vários | `test_web_dependencies.py`, integrações |
| `_register_error_handlers(flask_app)` | `app/web/app.py` | G1/G2/G3 | todos | app Flask | handlers | erros de domínio viram HTTP | centraliza respostas | vários | testes de rotas |
| `initialize_*` | `app/web/dependencies.py` | G1/G2/G3 | todos | conexão/serviços | serviços prontos | composição fora das rotas | cria repositórios/tabelas | vários | `test_web_dependencies.py` |
| `seed_demo_data(connection)` | `app/infrastructure/demo_seed.py` | G1/G2/G3 | todos | conexão | resumo de criação | idempotente | verifica existentes antes de inserir | DEMO | `test_demo_seed.py` |
| `seed_demo_database(database_path)` | `app/infrastructure/demo_seed.py` | G1/G2/G3 | todos | caminho SQLite | resumo | fecha conexão | encapsula seed local | DEMO | `test_demo_seed.py` |

