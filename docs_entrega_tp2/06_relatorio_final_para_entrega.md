# 06 — Relatório final para entrega

## Introdução

Este relatório documenta a análise técnica do projeto “Sistema de Gerência de Compras e Compartilhamento de Preços”, desenvolvido em Python com Flask, SQLite e testes automatizados com `unittest`. O objetivo da documentação é apoiar a entrega acadêmica da disciplina Técnicas de Programação 2, fornecendo visão geral, rastreabilidade, assertivas de corretude e descrições textuais para geração posterior de diagramas UML e DFD.

## Metodologia de análise do código

A análise foi realizada a partir da estrutura real do repositório. Foram inspecionados:

- árvore principal do projeto;
- módulos Python das camadas `domain`, `application`, `infrastructure` e `web`;
- rotas Flask JSON e HTML;
- templates Jinja2;
- repositórios SQLite e instruções de criação de tabelas;
- testes unitários e de integração;
- docstrings e marcadores de estórias/requisitos no código e nos testes.

Não foram alterados arquivos de lógica da aplicação. A documentação foi construída somente com base em evidência existente no código.

## Divisão de responsabilidades em 3 grupos

| Grupo | Responsabilidade | Integrantes |
|---|---|---|
| Grupo 1 | Autenticação, usuários, sessão, perfis e segurança básica. | Gabriel Balder; Anabel Mendes |
| Grupo 2 | Catálogo, produtos, estoque, remoção lógica e painel administrativo. | Dionilton Oliveira Silva; Jhonny Rodrigues de Sousa |
| Grupo 3 | Listas de compras, carrinho, total, locais, preços, GPS e mapa. | Gabriel Dylan; Gabriel Campello; Luiz Otávio |

## Resumo dos diagramas produzidos

Cada documento de grupo contém descrições textuais e blocos compatíveis com PlantUML ou Mermaid para:

- Diagrama de Casos de Uso;
- Diagrama de Fluxo de Dados;
- Diagrama de Classes;
- Diagrama de Atividades.

Os diagramas refletem a implementação real observada. Por exemplo:

- o Grupo 1 mostra o fluxo de cadastro, login, logout e autorização por sessão;
- o Grupo 2 mostra manutenção de produtos, estoque e métricas administrativas;
- o Grupo 3 mostra listas, carrinho, total, locais, preços e busca da loja mais próxima por GPS.

## Resumo das assertivas

As assertivas foram organizadas em duas camadas:

1. Assertivas específicas dentro de cada documento de grupo, diretamente relacionadas ao escopo funcional.
2. Tabela consolidada no arquivo `05_assertivas_gerais_por_funcao.md`, agrupada por módulo e grupo.

As assertivas documentam:

- entrada esperada;
- saída garantida;
- invariantes estruturais;
- argumento curto de corretude;
- efeitos colaterais;
- exceções ou erros tratados;
- requisitos e testes relacionados.

## Resumo da rastreabilidade

A rastreabilidade foi construída em dois níveis:

- matrizes por grupo, associando estória, requisito, caso de uso, DFD, classe, atividade, código, função/rota e teste;
- matriz geral em `04_matriz_rastreabilidade_geral.md`, consolidando US01–US07 e AD01–AD05.

Foram localizados no código os marcadores:

- `US01`, `US02`, `US03`, `US04`, `US05`, `US06`;
- `AD01`, `AD02`, `AD03`, `AD04`;
- `RNF02`;
- marcadores auxiliares `WEB`, `DEMO` e `QA`.

Não foram localizados marcadores ou implementações para:

- `US07`;
- `AD05`.

Esses itens foram registrados como “não localizado”, sem inventar funcionalidades.

## Limitações encontradas

- A edição e remoção de produtos existem como API JSON, mas não foi localizada tela HTML específica para editar/remover produto.
- A atualização de estoque existe como API JSON, mas não foi localizada tela HTML específica para estoque.
- A autenticação é baseada em sessão simples do Flask; não há uso de Flask-Login, recuperação de senha ou autenticação multifator.
- A autorização administrativa é implementada em decorators simples na camada web.
- Não há paginação avançada nem filtros complexos no histórico de preços.
- O mapa usa Leaflet com tiles externos do OpenStreetMap; para funcionar plenamente no navegador, depende de acesso à internet e permissão de geolocalização.
- US07 e AD05 não foram encontrados no código ou nos testes.

## Observação sobre integrantes e implementação

A divisão documental principal foi mantida conforme solicitado no enunciado do pedido. Entretanto, a estrutura real do código mostra integração entre grupos, especialmente em:

- `app/web/html_routes.py`, que concentra fluxos HTML de autenticação, catálogo, listas, carrinho, locais, preços e dashboards;
- `app/web/dependencies.py`, que compõe serviços de todos os grupos;
- `app/web/app.py`, que registra todos os blueprints e handlers globais.

Portanto, embora cada grupo tenha responsabilidade documental própria, alguns arquivos são transversais.

## Conclusão

O projeto apresenta uma arquitetura simples e coerente com o escopo acadêmico: domínio, aplicação, infraestrutura SQLite e camada web Flask. A implementação cobre autenticação, autorização administrativa, catálogo, estoque, listas, carrinho, total estimado, locais de compra, preços compartilhados e mapa da loja mais próxima.

A cobertura de testes é ampla e utiliza `unittest`, com testes unitários e de integração. A documentação gerada permite transformar os textos em diagramas UML/DFD por ferramentas como PlantUML, Mermaid, Draw.io ou Lucidchart. Os requisitos ausentes foram explicitamente marcados como não localizados, preservando a fidelidade à implementação real.

## Arquivos desta entrega

- `docs_entrega_tp2/00_visao_geral_do_sistema.md`
- `docs_entrega_tp2/grupo_1_autenticacao_usuarios.md`
- `docs_entrega_tp2/grupo_2_catalogo_admin_estoque.md`
- `docs_entrega_tp2/grupo_3_listas_carrinho_precos.md`
- `docs_entrega_tp2/04_matriz_rastreabilidade_geral.md`
- `docs_entrega_tp2/05_assertivas_gerais_por_funcao.md`
- `docs_entrega_tp2/06_relatorio_final_para_entrega.md`

