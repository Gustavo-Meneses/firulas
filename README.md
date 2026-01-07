--

# 🏰 Dark Castle: Ascensão

**Dark Castle: Ascensão** é um RPG de aventura *roguelike* desenvolvido em Python com a biblioteca Streamlit. Enfrente perigos constantes, gerencie seus recursos e suba os andares de um castelo amaldiçoado em busca de glória.

## 🎮 Funcionalidades do Jogo

* **Sistema de Classes Único**: Escolha entre quatro linhagens com mecânicas exclusivas:
* **Guerreiro**: Equilibrado, com alta defesa e sobrevivência.
* **Mago**: Especialista em dano místico, com bônus de 70% em magias ao usar itens raros.
* **Berserker**: Entra em estado de **Fúria** (+90% de dano) quando a vida está criticamente baixa.
* **Assassino**: Mestre da agilidade, com chances reais de esquiva e atordoamento (*stun*) de inimigos.


* **Mercado Dinâmico**: Um sistema de compras que oferece sempre uma opção de ataque e uma de defesa (proporção 50/50).
* **Gerenciamento de Inventário**: Venda itens antigos para obter ouro ou equipe novos achados para melhorar seus atributos.
* **Progressão por Andares**: A dificuldade escala conforme você sobe. Derrote o número necessário de inimigos para avançar.
* **Exploração e Sorte**: 50% de chance de encontrar baús de tesouro durante a exploração das salas.

## 🛠️ Tecnologias Utilizadas

* **Python**: Linguagem principal.
* **Streamlit**: Framework utilizado para a interface web e gerenciamento de estado da sessão.
* **HTML/CSS**: Customização da interface para uma estética *Dark/Retro*.

## 🚀 Como Executar o Projeto

1. **Clone o repositório**:
```bash
git clone https://github.com/Gustavo-Meneses/firulas

```


2. **Instale as dependências**:
```bash
pip install streamlit

```


3. **Inicie o jogo**:
```bash
streamlit run jogo_medieval.py

```



## 📜 Regras de Combate e Atributos

* **Combate**: O dano é calculado com base no seu atributo de Ataque somado a um fator aleatório. A Defesa reduz o dano recebido dos monstros.
* **Mana**: Essencial para classes mágicas realizarem habilidades especiais. Pode ser recuperada com poções no mercado.
* **Morte**: O progresso é perdido ao morrer (*permadeath*), desafiando o jogador a cada nova rodada.

---

### 🤝 Contribuições

Sugestões de novos itens, classes ou balanceamento são sempre bem-vindas! Sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

---

**Desenvolvido com ⚔️ e 🐍.**

---

**Dica de amigo:** Gostaria que eu criasse uma seção específica de "Lore" (história do jogo) para deixar o README ainda mais imersivo?
