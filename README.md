# Genius 💡- T1
Este projeto consiste no desenvolvimento de um sistema embarcado que tem como inspiração o jogo da memória clássico Genius, um disco que dispõe de 4 cores diferentes que acendem em uma ordem aleatória e o jogador precisa adivinhar a sequência correta das cores, utilizando-se de 4 LEDs e  4 botões para representar a sequência reproduzida e a ser inserida pelo jogador.

# Componentes do sistema ⚙
- Microcontrolador Raspberry Pi Pico
- 4 botões "push"
- 6 LEDs difusos 5mm
- Jumpers Macho Macho e Macho Fêmea
- Protoboard

# Requisitos
- UR01: Ser composto por módulos prontos e de fácil acesso 

- UR02: Captar a ordem em que os LEDs são acesos corretamente 

- UR03: Permitir que ao apertar um dos botões, o LED correspondente ao botão seja aceso 

- UR04: Gravar a sequência apertada pelo jogador em um vetor de dados 

- UR05: Utilizar Python como linguagem de programação que configura o ambiente de desenvolvimento (RaspBerry Pi Pico) 

# Funcionalidades 🕹
- 4 LEDs com cores diferentes acendem em ordem aleatória e incremental (um LED pisca primeiro, depois dois, e assim por diante)
- Após os LEDs piscarem, um LED é aceso para indicar ao jogador que é a sua vez de apertar os botões na ordem em que os LEDs piscaram
- Caso o jogador aperte os botões na ordem correta em que os LEDs piscaram, outro LED acende indicando que o jogador passou para a próxima fase
- Caso contrário, todos os LEDs acendem simultaneamente, indicando que o jogador perdeu a rodada e então o jogo é encerrado

# Diagrama de Blocos 
![Diagrama de Blocos Genius](./T1/DiagramaGeniusdrawio.jpg)

# Genius 💡- T2
Este projeto consiste no desenvolvimento de um sistema embarcado que tem como inspiração o jogo da memória clássico Genius, um disco que dispõe de 4 cores diferentes que acendem em uma ordem aleatória e o jogador precisa adivinhar a sequência correta das cores, utilizando-se de uma interface gráfica em um display touch simulando virtualmente o minigame, com o jogador tendo que pressionar os botões na mesma sequência que estes acenderam.

# Componentes do sistema ⚙
- Microcomputador Raspberry Pi
- Display touch Raspberry Pi
- Dispositivo Buzzer 5V 
- Jumpers Macho/Macho e Macho/Fêmea
- Protoboard 170 pontos
- Cartão de memória SD 128GB

# Requisitos
- UR01: O cartão de memória deve estar configurado no ambiente do Rasberry Pi corretamente, com conexão com internet e visualização dos arquivos clara

- UR02: Ter uma interface gráfica intuitiva e acessível para os jogadores

- UR03: Exibir na tela a sequência aleatória que os botões acendem e armazená-la em um vetor de dados

- UR04: Captar a sequência dos botões pressionados pelo jogador e armazená-la em um vetor de dados

- UR05: Comparar o vetor de dados da sequência dos botões pressionados pelo jogador com o vetor de dados da sequência em que os botões acenderam

- UR06: Utilizar Python como linguagem de programação e demais bibliotecas de suporte, como GPIO Zero para conectar com as portas do Raspberry Pi e Tkinter, para estilização da interface gráfica

- UR07: Disparar o buzzer como um alerta toda vez que o jogador pressionar o botão errado da sequência

# Funcionalidades 🕹
- O jogo se inicia com quatro botões quadriculados serem acesos em uma sequência aleatória e incremental a cada rodada (um botão acende na primeira, dois na segunda, e assim sucessivamente), além dos botões quadriculares, há dois botões circulares: um para indicar que o jogador passou para a próxima rodada e outro indicando que o jogador perdeu a rodada. Há também um contador indicando a rodada que o jogador está
- Após os botões acenderem, o jogador deve pressionar os botões na sequência correta em que acenderam 
- Ao acertar a sequência, o jogador pasa para a próxima rodada, o botão circular verde acende e o contador incrementa para o número da próxima rodada (ex: jogador passou da rodada 1 para rodada 2)
- Caso pressione algum botão errado da sequência, o buzzer dispara um som, o botão circular vermelho acende e o jogador encerra a rodada. Uma mensagem é exibida indicando a rodada em que o jogador conseguiu avançar

# Diagrama de Blocos
![Diagrama de Blocos T2](./T2/DiagramaT2Microcontroladores.drawio.png)

# Integrantes 👷‍♂️
- Felipe Kenzo Ohara Sakae | RA: 22.00815-2
- Lucas Gozze Crapino | RA: 22.00667-2
- Vinicius Garcia Imendes Dechechi | RA: 22.01568-0
![Foto dos membros](./FotoMembrosMicrocontroladores.jpeg)
