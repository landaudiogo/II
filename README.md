### Preferências:

Manu - PLC, MES
Gabi - MES, PLC
Ana - Indiferente
Diogo - Indiferente


### Diagramas (até 14.03)
- Classes 
	- Base de Dados
	- Processo
- Objetos
- Sequência


### PLC 
- mapeamento de endereços para cada componente (Gabi)
- desenho dos componentes simples (Diogo, Ana)
- desenho complexos (Gabi, Ana, Manu)



### MES 
- Interações com base de dados (Diogo)
- Comunicação com chão de fábrica (Manu)
- Comunicação ERP (Diogo, Gabi)
- Decisão de entrada de peça (Ana, Diogo)

##### Interações com a base de dados: 
Tarefas: 
1. Desenho do diagrama de classes para a base de dados
2. Mapeamento local Python da base de dados
3. Funções genéricas simples: get, add, remove, update
4. Funções genéricas complexas: 
	- get_objects_using_attrs: where clause restricted to the attributes
	- object_insert_or_nothing: insert an object in case it does not exist and in case it does exist don't do anything. All the nested objects are added in the same manner.
5. Converter xml para json

### Interface
- Desenvolver API
- Frontend
