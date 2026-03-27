# 🏰 Dark Castle: Ascensão

**Dark Castle: Ascensão** é um RPG Roguelike de fantasia sombria desenvolvido em Python. O projeto utiliza o **Streamlit** como motor de interface, elevando os limites da biblioteca ao integrar renderização de sprites em tempo real e manipulação direta de DOM para uma experiência de jogo fluida e imersiva.

---

## 🎨 Diferenciais Técnicos (Engine)

Diferente de aplicações Streamlit convencionais, o **Dark Castle** utiliza soluções de engenharia para contornar limitações de interface:

* **Renderização via Iframes (Sandboxing)**: O uso de `st.components.v1.html` permite que a arena de combate funcione de forma independente, evitando o *sanitizing* de HTML do Streamlit e garantindo que emojis e estruturas complexas sejam renderizados sem erros de "tag escapada".
* **Sprites em Pixel Art (CSS Box-Shadow)**: Personagens e monstros não utilizam arquivos de imagem externos. São renderizados puramente via código CSS usando a técnica de `box-shadow` múltiplo, garantindo carregamento instantâneo e uma estética 8-bit autêntica.
* **Sistema de Animação de Combate**: Implementação de *keyframes* complexos para simular ataques, magias, esquivas e efeitos de "screen shake" e "flash" durante o dano.

---

## 🎮 Funcionalidades do Jogo

### ⚔️ Sistema de Classes Único
Escolha entre quatro linhagens com mecânicas exclusivas:
* **Guerreiro**: Equilibrado, com alta sobrevivência e bloqueio passivo de 20% de dano.
* **Mago**: Especialista em dano místico; itens **RAROS** amplificam o poder das magias em +70%.
* **Berserker**: Entra em estado de **Fúria** (+90% de dano) quando a vida está abaixo de 20%.
* **Assassino**: Mestre da agilidade, com 30% de chance de esquiva e 25% de atordoamento (*stun*).

### 🛡️ Progressão e Economia
* **Mercado Dinâmico**: Sistema de compras que oferece equipamentos de ataque e defesa baseados no seu andar atual.
* **Gerenciamento de Inventário**: Venda itens antigos para obter ouro e gerencie seus recursos para sobreviver.
* **Dificuldade Escalonável**: O HP e ATK dos monstros aumentam em **22% por andar**.
* **Lore Imersiva**: Fragmentos de história que se revelam conforme você sobe os andares do castelo.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**: Lógica principal e gerenciamento de estado (`session_state`).
* **Streamlit**: Framework de interface web.
* **HTML5 / Modern CSS**: Customização da interface para uma estética *Dark Fantasy* e animações de combate.
* **Google Fonts**: Utilização das fontes *Cinzel Decorative* e *UnifrakturMaguntia*.

---

## 🚀 Como Executar o Projeto

1.  **Clone o repositório**:
    ```bash
    git clone [https://github.com/Gustavo-Meneses/firulas](https://github.com/Gustavo-Meneses/firulas)
    ```

2.  **Instale as dependências**:
    ```bash
    pip install streamlit
    ```

3.  **Inicie o jogo**:
    ```bash
    streamlit run jogo_medieval.py
    ```

---

## 📜 Regras de Combate

* **Dano**: O dano é calculado com base no seu atributo de Ataque somado a um fator aleatório. A Defesa do seu equipamento reduz o dano recebido.
* **Mana**: Recurso essencial para habilidades mágicas. Pode ser recuperada com itens específicos no mercado.
* **Permadeath**: No castelo, a morte é definitiva. O progresso é perdido ao morrer, desafiando o jogador a cada nova rodada.

---

### 🤝 Contribuições

Este projeto é um experimento de interface rica em ambientes de dados. Sugestões de novos itens, balanceamento de classes ou novos sprites em CSS são muito bem-vindas!

**Desenvolvido com ⚔️ e 🐍 por Gustavo Meneses.**
