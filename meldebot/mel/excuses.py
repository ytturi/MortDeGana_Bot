from random import choice, randint

EXCUSES = [
    f"Fa {randint(2,30)} anys plovia",
    f"Tinc hora a la pelu, que només hi vaig {randint(1,20)} cops per setmana",
    f"Vaig al gym, la idea és anar-hi {randint(1,20)} cops per setmana",
    "Aquest dia justament vaig a donar sang",
    "Casum l'olla! Tinc un dinar familiar",
    "Demà haig d'anar a passar la itv",
    "El metge m'ha dit que no puc menjar aliments rics en sodi",
    "És que em guardo dies de vacances",
    "És que se m'ha punxat la roda de la bici estàtica i l'he de canviar",
    "És que vai demanar un paquet i crec que m'arribarà llavors",
    "És que fa molt de sol i no tinc crema",
    "És que he d'anar a treure la marmota a passejar",
    "Estic esperant a que el Jefe em doni el contracte que m'ha dit que ara me'l porta",
    "Estic esperant la corda i tamboret que m'he demanat a amazon",
    "He quedat per fer una muntanya",
    "Jo vindria, però és que se m'ha espatllat el GPS del mòbil",
    "Jo vindria, però m'agrada fer motos",
    "Jo vindria, però és que s'em morirà el peix que vaig a comprar ara",
    "Justament aquest dia he quedat per jugar a arrancar cebes",
    "M'he endescuidat de regar el cactus de Gisce",
    "Mha semblat veure una gota a la carretera",
    "No puc venir pk la dona m'ha dit que anes a la platja de palafrugell i em quedés un parell d'hores sota l'aigua",
    "No puc venir que he d'afegir excuses de moto al bot",
    "Plou i fa sol, em quedo a casa sol",
    "Se m'ha mort el PC i li fem un funeral. Tenia una 3080ti",
    "Se m'ha mort la PS5 i li fem un funeral. Poques que n'hi han...",
    "Soc un mort de gana",
    "Tinc el rellotge en format 24h",
    "Tinc un conegut que fa casi un any que no veig que té corona, així que faig quarentena per si de cas.",
    "Tu que m'acaben de trucar que d'aqui 20min anem a fer una implantació i no sé quan tornaré.",
    "Volia venir pro no soy 1000itar",
    "Volia venir pro no soy 1000itante",
    "Volia venir pro no soy 100tifiko",
    "Ho sento sóc simracer",
    "He d'anar a agafar l'AVE",
    "M'he equivocat i he anat al Pagès Original",
    "Sóc vegetarià i fan tapes amb carn",
    f"Estic en remot i visc {randint(1,50)} km lluny",
    "M'estic preparant pel proper canvi de tarifes",
    "Treballo als Països Baixos",
    "He quedat per anar al cine, la peli es diu 'No tinc ganes de venir'. Diuen que és molt bona!",
    f"Haig d'anar a plantar {randint(2,50)} regues de cebes, {randint(2,50)} de cols, {randint(2,50)} d'alls i {randint(2,50)} de brocolis",
    "Tinc un problema i no puc venir",
    "Es que he anat a donar sang i no m'arrba al creelllkakakak",
    f"Ara acabo de recordar que vaig al rocodrom, intento anar {randint(2,50)} vegades per setmana",
    "Brumm brummmmm",
    "Vindria però no bec cervesa",
    "No puc venir perque m'agrada anar per l'autopista, ara que son gratuites",
    "He d'anar a casa a simular indexades",
    "El meu horòscop em diu que he de menjar 44 peces de fruita diàries i avui vaig tard",
    "No puc deixar sola la serp que tinc a casa o es menjarà el hàmster",
    "Començo un curs de ganxet a Udemy i em fa molta il·lusió",
    "He llegit a Twitter que avui tinc que holdear BTC",
    "Tinc que anar a posar pinso a les gallines. No obren fins dilluns que ve",
    "He tingut que marxar de la ciutat per un temps i no sé quan podré tornar. M'han dit que millor no expliqui perquè.",
    "M'han detingut per no recollir una caca de gos. Envia 2.000€ a freemortdegana.com per treure'm d'aquí.",
    "M'he comprat un yo-yo i estic recuperant la meva infància. Seré al parc de sota de casa, berenant pa amb xocolata",
    "M'encantaria, però no em ve de gust",
    "La meva religió no em permet quedar avui amb persones que tinguin noms que continguin vocals. Vinc a la propera!",
    "És que fa temps que estic enfadat amb vosaltres i no recordo perquè. No us vull veure fins que s'em passi.",
    "Uff, impossible. Just tenia pensat trucar a Movistar per a donar-me de baixa. Us veig l'any que ve.",
    "Quan acabi amb les excuses del bot, n'he d'afegir també a unes declaracions del Rajoy. A veure si colen!",
    "Mmm... no sé si arribaria a temps. Estic esperant que acabi la sèrie One Piece. Després estaré disponible.",
    "És que aquesta tarda entra eòlica al mix i volia aprofitar per a carregar el rellotge i els mòbils.",
    f"Avui no puc venir. Algú m'ha robat les tovalloles del safareig i les estic rastrejant. Són a {randint(2,10)} km de casa meva.",
    "He de pagar el lloguer i només tinc la meitat. Així que vaig al casino per a intentar duplicar els meus diners.",
    "Ahir em vaig desatascar les orelles i amb l'esquerra vaig entrar massa el bastonet. Com que dormo amb el despertador a l'esquerra, no l'he sentit fins ara.",
    "Vindria, però he de canviar el filtre i la bombeta del forn.",
    "Ho sento, m'he tingut que barallar al carrer amb uns nois que deien que no ereu els millors companys per anar a fer un Pagès avui.",
    "Em sap greu. Avui no puc caminar gaire, m'he lesionat un dit fent un bugfix de l'ERP.",
    "Un altre dia, companys, tinc que rentar els plats i trigo una mica perquè sóc alèrgic a l'aigua calenta.",
    "No podré venir... el tren que em porta fins aquí deu minuts tard, ha arribat deu minuts tard.",
    "Un corb m'ha robat les claus. Estic perseguint-lo amb un dron, així que potser trigaré una mica.",
    "Ho sento, però he d'entrenar el meu dron perquè pugui servir-me cafè. Si no ho aconsegueixo, no sé com sobreviviré a la programació d'avui.",
    "No podré venir, el meu ordinador ha decidit que és un artista i està pintant un mural de codi. He de veure si el resultat és net.",
    "Em sap greu, però he d'ajudar un Jedi a reparar el seu sabre de llum. Els circuits de la força són més complicats del que semblen.",
    "Avui em trobo atrapant l'error més difícil de la meva vida: el meu gats s'han convertit en NPCs i s'han escapat del sistema.",
    "Estic en plena batalla contra un bug que s'ha disfressat de mascota de companyia. Necessito fer una auditoria del meu codi.",
    "No podré venir... la meva connexió a Internet ha decidit fer una escapada a les Maldives. Estic intentant fer servir la força per recuperar-la.",
    "He de fer neteja de codi, però el meu teclat ha començat a comunicar-se amb mi en binari i no sé si estic preparat per a aquesta conversa.",
    "Ahir vaig fer un viatge intergalàctic amb el meu ordinador i ara no sé com tornar. Necessito un 'warp drive' d'urgència!",
    "M'he compromès a fer una revisió del meu perfil de Steam amb un llum d'ull de tigré. El meu avatar no es va actualitzar des de l'era de la programació en C.",
    "Em sap greu, però he d'enfrontar-me a una batalla de tauler amb uns 'minions' que han decidit que el meu codi és el seu nou habitatge.",
    "Ho sento, però el meu ordinador ha decidit fer un 'break' i necessita una 'reboot' emocional. No puc deixar-lo sol!",
    "No podré venir... he de fer un 'commit' amb la meva consola de jocs abans que s'enfadi i es converteixi en un 'rollback'.",
    "Avui no puc, estic atrapat en un 'loop' de videojocs que no em deixa sortir. Necessito un 'escape key'!",
    "Em sap greu, però he de 'debuguejar' la meva vida social. Els meus amics són com variables no inicialitzades, necessiten atenció.",
    "No puc vindre, estic en una 'quest' per trobar el 'level up' de la meva motivació. Els 'XP' no s'acumulen sols!",
    "Estic atrapat en un 'merge conflict' amb els meus plans i no sé com resoldre-ho. Necessito un 'git' de solucions!",
    "Ho sento, el meu equip de programadors ha decidit fer una 'synchronization' de codi i necessito ser-hi per evitar un 'data loss'.",
    "Avui he de fer un 'patch' de la meva rutina diària, que està plena de 'bugs' incontrolables.",
    "No podré vindre, estic intentant trobar l'algorisme que m'ajudi a sortir de la meva zona de confort. Les funcions no sempre són fàcils!",
    "Em sap greu, però el meu cervell s'ha penjat en mode 'buffering' mentre intentava processar totes les opcions d'avui. Necessito un reinici!",
]


def get_random_excuse() -> str:
    """Generate a random text for motos

    Returns:
        str: Moto quote
    """
    return choice(EXCUSES)
