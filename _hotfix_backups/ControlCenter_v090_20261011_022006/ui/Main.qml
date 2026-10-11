import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

ApplicationWindow {
    id: win
    width: 1500; height: 920
    minimumWidth: 1100; minimumHeight: 700
    visible: true
    title: "NONIVERUS PosterTile Luxury Studio v0.9.0.1  /  " + studio.editionName
    color: (win.light ? "#E7E3DB" : "#080E19")
    property var dictionary: {"pt-PT": {"Cria sem limites.": "Cria sem limites.", "Precisão profissional em cada folha.": "Precisão profissional em cada folha.", "＋   IMPORTAR IMAGEM": "＋   IMPORTAR IMAGEM", "FORMATO FINAL": "FORMATO FINAL", "Altura (cm)": "Altura (cm)", "Largura (cm)": "Largura (cm)", "PROPORÇÃO PRESERVADA": "PROPORÇÃO PRESERVADA", "Sem deformar a imagem original": "Sem deformar a imagem original", "PAPEL DE IMPRESSÃO  /  SELEÇÃO MANUAL": "PAPEL DE IMPRESSÃO  /  SELEÇÃO MANUAL", "02  /  PRINT ENGINE": "02  /  PRINT ENGINE", "OCULTAR  −": "OCULTAR  −", "AVANÇADO  ＋": "AVANÇADO  ＋", "Método de montagem": "Método de montagem", "Margem (mm)": "Margem (mm)", "Sobreposição (mm)": "Sobreposição (mm)", "PLANO DE IMPRESSÃO": "PLANO DE IMPRESSÃO", "EXPORTAR PDF  ↗": "EXPORTAR PDF  ↗", "O teu projeto, em grande.": "O teu projeto, em grande.", "◇   VISTA PLANA": "◇   VISTA PLANA", "◇   PERSPETIVA": "◇   PERSPETIVA", "＋\\n\\nIMPORTA A TUA IMAGEM\\nPARA COMEÇAR": "＋\\n\\nIMPORTA A TUA IMAGEM\\nPARA COMEÇAR", "Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas": "Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas", "●  VISTA DE MONTAGEM": "●  VISTA DE MONTAGEM", "PÁGINAS": "PÁGINAS", "01  /  PROJECT SETUP": "01  /  PROJECT SETUP"}, "en": {"Cria sem limites.": "Create without limits.", "Precisão profissional em cada folha.": "Professional precision on every sheet.", "＋   IMPORTAR IMAGEM": "＋   IMPORT IMAGE", "FORMATO FINAL": "FINAL SIZE", "Altura (cm)": "Height (cm)", "Largura (cm)": "Width (cm)", "PROPORÇÃO PRESERVADA": "ASPECT RATIO LOCKED", "Sem deformar a imagem original": "Original image not distorted", "PAPEL DE IMPRESSÃO  /  SELEÇÃO MANUAL": "PRINT PAPER  /  MANUAL SELECTION", "02  /  PRINT ENGINE": "02  /  PRINT ENGINE", "OCULTAR  −": "HIDE  −", "AVANÇADO  ＋": "ADVANCED  ＋", "Método de montagem": "Assembly method", "Margem (mm)": "Margin (mm)", "Sobreposição (mm)": "Overlap (mm)", "PLANO DE IMPRESSÃO": "PRINT PLAN", "EXPORTAR PDF  ↗": "EXPORT PDF  ↗", "O teu projeto, em grande.": "Your project, larger than life.", "◇   VISTA PLANA": "◇   FLAT VIEW", "◇   PERSPETIVA": "◇   PERSPECTIVE", "＋\\n\\nIMPORTA A TUA IMAGEM\\nPARA COMEÇAR": "＋\\n\\nIMPORT AN IMAGE\\nTO START", "Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas": "Illustrative preview · PDF uses precise physical coordinates", "●  VISTA DE MONTAGEM": "●  ASSEMBLY VIEW", "PÁGINAS": "PAGES", "01  /  PROJECT SETUP": "01  /  PROJECT SETUP"}, "es": {"Cria sem limites.": "Crea sin límites.", "Precisão profissional em cada folha.": "Precisión profesional en cada hoja.", "＋   IMPORTAR IMAGEM": "＋   IMPORTAR IMAGEN", "FORMATO FINAL": "TAMAÑO FINAL", "Altura (cm)": "Altura (cm)", "Largura (cm)": "Anchura (cm)", "PROPORÇÃO PRESERVADA": "PROPORCIÓN CONSERVADA", "Sem deformar a imagem original": "Sin deformar la imagen", "PAPEL DE IMPRESSÃO  /  SELEÇÃO MANUAL": "PAPEL DE IMPRESIÓN  /  SELECCIÓN", "02  /  PRINT ENGINE": "02  /  MOTOR DE IMPRESIÓN", "OCULTAR  −": "OCULTAR  −", "AVANÇADO  ＋": "AVANZADO  ＋", "Método de montagem": "Método de montaje", "Margem (mm)": "Margen (mm)", "Sobreposição (mm)": "Solapamiento (mm)", "PLANO DE IMPRESSÃO": "PLAN DE IMPRESIÓN", "EXPORTAR PDF  ↗": "EXPORTAR PDF  ↗", "O teu projeto, em grande.": "Tu proyecto, a lo grande.", "◇   VISTA PLANA": "◇   VISTA PLANA", "◇   PERSPETIVA": "◇   PERSPECTIVA", "＋\\n\\nIMPORTA A TUA IMAGEM\\nPARA COMEÇAR": "＋\\n\\nIMPORTA UNA IMAGEN\\nPARA EMPEZAR", "Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas": "Vista ilustrativa · El PDF usa coordenadas físicas exactas", "●  VISTA DE MONTAGEM": "●  VISTA DE MONTAJE", "PÁGINAS": "PÁGINAS", "01  /  PROJECT SETUP": "01  /  CONFIGURACIÓN"}, "fr": {"Cria sem limites.": "Créez sans limites.", "Precisão profissional em cada folha.": "Précision professionnelle sur chaque feuille.", "＋   IMPORTAR IMAGEM": "＋   IMPORTER UNE IMAGE", "FORMATO FINAL": "FORMAT FINAL", "Altura (cm)": "Hauteur (cm)", "Largura (cm)": "Largeur (cm)", "PROPORÇÃO PRESERVADA": "PROPORTIONS CONSERVÉES", "Sem deformar a imagem original": "Image originale non déformée", "PAPEL DE IMPRESSÃO  /  SELEÇÃO MANUAL": "PAPIER  /  SÉLECTION MANUELLE", "02  /  PRINT ENGINE": "02  /  MOTEUR D’IMPRESSION", "OCULTAR  −": "MASQUER  −", "AVANÇADO  ＋": "AVANCÉ  ＋", "Método de montagem": "Méthode d’assemblage", "Margem (mm)": "Marge (mm)", "Sobreposição (mm)": "Chevauchement (mm)", "PLANO DE IMPRESSÃO": "PLAN D’IMPRESSION", "EXPORTAR PDF  ↗": "EXPORTER PDF  ↗", "O teu projeto, em grande.": "Votre projet en grand.", "◇   VISTA PLANA": "◇   VUE PLANE", "◇   PERSPETIVA": "◇   PERSPECTIVE", "＋\\n\\nIMPORTA A TUA IMAGEM\\nPARA COMEÇAR": "＋\\n\\nIMPORTEZ UNE IMAGE\\nPOUR COMMENCER", "Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas": "Aperçu illustratif · Le PDF utilise des coordonnées physiques exactes", "●  VISTA DE MONTAGEM": "●  VUE D’ASSEMBLAGE", "PÁGINAS": "PAGES", "01  /  PROJECT SETUP": "01  /  CONFIGURATION"}, "it": {"Cria sem limites.": "Crea senza limiti.", "Precisão profissional em cada folha.": "Precisione professionale su ogni foglio.", "＋   IMPORTAR IMAGEM": "＋   IMPORTA IMMAGINE", "FORMATO FINAL": "FORMATO FINALE", "Altura (cm)": "Altezza (cm)", "Largura (cm)": "Larghezza (cm)", "PROPORÇÃO PRESERVADA": "PROPORZIONI CONSERVATE", "Sem deformar a imagem original": "Immagine originale non deformata", "PAPEL DE IMPRESSÃO  /  SELEÇÃO MANUAL": "CARTA  /  SCELTA MANUALE", "02  /  PRINT ENGINE": "02  /  MOTORE DI STAMPA", "OCULTAR  −": "NASCONDI  −", "AVANÇADO  ＋": "AVANZATE  ＋", "Método de montagem": "Metodo di montaggio", "Margem (mm)": "Margine (mm)", "Sobreposição (mm)": "Sovrapposizione (mm)", "PLANO DE IMPRESSÃO": "PIANO DI STAMPA", "EXPORTAR PDF  ↗": "ESPORTA PDF  ↗", "O teu projeto, em grande.": "Il tuo progetto in grande.", "◇   VISTA PLANA": "◇   VISTA PIANA", "◇   PERSPETIVA": "◇   PROSPETTIVA", "＋\\n\\nIMPORTA A TUA IMAGEM\\nPARA COMEÇAR": "＋\\n\\nIMPORTA UN’IMMAGINE\\nPER INIZIARE", "Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas": "Anteprima illustrativa · Il PDF usa coordinate fisiche esatte", "●  VISTA DE MONTAGEM": "●  VISTA MONTAGGIO", "PÁGINAS": "PAGINE", "01  /  PROJECT SETUP": "01  /  CONFIGURAZIONE"}}
    property var extraTranslations: ({
      "en": {"CALIBRAR":"CALIBRATE","Calibração não selecionada":"No calibration selected","ATELIER  /  LIVE CANVAS":"STUDIO  /  LIVE CANVAS","PROFESSIONAL OUTPUT":"PROFESSIONAL OUTPUT","PDF pronto:":"PDF ready:","Personalizado":"Custom","vertical":"portrait","horizontal":"landscape","Sobrepor":"Overlap","Cortar e unir":"Trim and join","SELECIONADO: ":"SELECTED: "," · podes alterar a orientação em baixo.":" · orientation can be changed below.","AUTO: escolhe A4 ou A3 pela menor quantidade de folhas.":"AUTO: chooses A4 or A3 to minimise sheets.","01  /  ORIGEM DO PROJETO":"01  /  PROJECT SOURCE","IMAGEM":"IMAGE","TEXTO GIGANTE":"LARGE TEXT","Cria uma frase usando as fontes do teu computador.":"Create a message using fonts installed on your computer."},
      "es": {"CALIBRAR":"CALIBRAR","Calibração não selecionada":"Calibración no seleccionada","ATELIER  /  LIVE CANVAS":"TALLER  /  LIENZO EN VIVO","PROFESSIONAL OUTPUT":"SALIDA PROFESIONAL","PDF pronto:":"PDF listo:","Personalizado":"Personalizado","vertical":"vertical","horizontal":"horizontal","Sobrepor":"Superponer","Cortar e unir":"Cortar y unir","SELECIONADO: ":"SELECCIONADO: "," · podes alterar a orientação em baixo.":" · cambia la orientación abajo.","AUTO: escolhe A4 ou A3 pela menor quantidade de folhas.":"AUTO: elige A4 o A3 para reducir las hojas.","01  /  ORIGEM DO PROJETO":"01  /  ORIGEN DEL PROYECTO","IMAGEM":"IMAGEN","TEXTO GIGANTE":"TEXTO GIGANTE","Cria uma frase usando as fontes do teu computador.":"Crea una frase usando las fuentes de tu ordenador."},
      "fr": {"CALIBRAR":"ÉTALONNER","Calibração não selecionada":"Aucun étalonnage sélectionné","ATELIER  /  LIVE CANVAS":"ATELIER  /  APERÇU EN DIRECT","PROFESSIONAL OUTPUT":"EXPORTATION PROFESSIONNELLE","PDF pronto:":"PDF prêt :","Personalizado":"Personnalisé","vertical":"portrait","horizontal":"paysage","Sobrepor":"Superposer","Cortar e unir":"Découper et assembler","SELECIONADO: ":"SÉLECTIONNÉ : "," · podes alterar a orientação em baixo.":" · changez l’orientation ci-dessous.","AUTO: escolhe A4 ou A3 pela menor quantidade de folhas.":"AUTO : choisit A4 ou A3 pour réduire le nombre de feuilles.","01  /  ORIGEM DO PROJETO":"01  /  SOURCE DU PROJET","IMAGEM":"IMAGE","TEXTO GIGANTE":"TEXTE GÉANT","Cria uma frase usando as fontes do teu computador.":"Créez un texte avec les polices installées."},
      "it": {"CALIBRAR":"CALIBRA","Calibração não selecionada":"Nessuna calibrazione selezionata","ATELIER  /  LIVE CANVAS":"ATELIER  /  ANTEPRIMA LIVE","PROFESSIONAL OUTPUT":"OUTPUT PROFESSIONALE","PDF pronto:":"PDF pronto:","Personalizado":"Personalizzato","vertical":"verticale","horizontal":"orizzontale","Sobrepor":"Sovrapponi","Cortar e unir":"Taglia e unisci","SELECIONADO: ":"SELEZIONATO: "," · podes alterar a orientação em baixo.":" · modifica l’orientamento qui sotto.","AUTO: escolhe A4 ou A3 pela menor quantidade de folhas.":"AUTO: sceglie A4 o A3 per ridurre i fogli.","01  /  ORIGEM DO PROJETO":"01  /  ORIGINE PROGETTO","IMAGEM":"IMMAGINE","TEXTO GIGANTE":"TESTO GIGANTE","Cria uma frase usando as fontes do teu computador.":"Crea una frase usando i font installati."}
    })
    function choice(text) {
        if (text === "Auto") return text
        if (text === "Personalizado") return t(text)
        if (text === "Sobrepor" || text === "Cortar e unir") return t(text)
        return text.replace("vertical",t("vertical")).replace("horizontal",t("horizontal"))
    }
    property var panelTranslations: {"pt-PT": {"01  /  CONFIGURAÇÃO": "01  /  CONFIGURAÇÃO", "02  /  ORIGEM DO PROJETO": "02  /  ORIGEM DO PROJETO", "03  /  FORMATO FINAL": "03  /  FORMATO FINAL", "04  /  PAPEL E IMPRESSÃO": "04  /  PAPEL E IMPRESSÃO", "EDITAR TEXTO": "EDITAR TEXTO", "PROFESSIONAL OUTPUT": "PROFESSIONAL OUTPUT"}, "en": {"01  /  CONFIGURAÇÃO": "01  /  PROJECT SETUP", "02  /  ORIGEM DO PROJETO": "02  /  PROJECT SOURCE", "03  /  FORMATO FINAL": "03  /  FINAL SIZE", "04  /  PAPEL E IMPRESSÃO": "04  /  PAPER & PRINTING", "EDITAR TEXTO": "EDIT TEXT", "PROFESSIONAL OUTPUT": "PROFESSIONAL OUTPUT"}, "es": {"01  /  CONFIGURAÇÃO": "01  /  CONFIGURACIÓN", "02  /  ORIGEM DO PROJETO": "02  /  ORIGEN DEL PROYECTO", "03  /  FORMATO FINAL": "03  /  TAMAÑO FINAL", "04  /  PAPEL E IMPRESSÃO": "04  /  PAPEL E IMPRESIÓN", "EDITAR TEXTO": "EDITAR TEXTO", "PROFESSIONAL OUTPUT": "SALIDA PROFESIONAL"}, "fr": {"01  /  CONFIGURAÇÃO": "01  /  CONFIGURATION", "02  /  ORIGEM DO PROJETO": "02  /  SOURCE DU PROJET", "03  /  FORMATO FINAL": "03  /  FORMAT FINAL", "04  /  PAPEL E IMPRESSÃO": "04  /  PAPIER ET IMPRESSION", "EDITAR TEXTO": "MODIFIER LE TEXTE", "PROFESSIONAL OUTPUT": "EXPORTATION PROFESSIONNELLE"}, "it": {"01  /  CONFIGURAÇÃO": "01  /  CONFIGURAZIONE", "02  /  ORIGEM DO PROJETO": "02  /  ORIGINE DEL PROGETTO", "03  /  FORMATO FINAL": "03  /  FORMATO FINALE", "04  /  PAPEL E IMPRESSÃO": "04  /  CARTA E STAMPA", "EDITAR TEXTO": "MODIFICA TESTO", "PROFESSIONAL OUTPUT": "OUTPUT PROFESSIONALE"}}
    function t(key) {
        var override = panelTranslations[studio.language]
        if (override && override[key]) return override[key]
        var entry = dictionary[studio.language]
        return (entry && entry[key]) || (extraTranslations[studio.language] && extraTranslations[studio.language][key]) || key
    }
    property int centerPage: 0
    function centerLabel(key) {
        var labels = {
            "pt-PT": {settings:"DEFINIÇÕES",help:"AJUDA",about:"SOBRE",printers:"Impressoras e calibração",intro:"Preferências gerais",help1:"Primeiros passos: importar imagem ou criar texto gigante.",help2:"Montagem: imprimir a 100%, sem ajustar à página.",help3:"Para montar: seguir as referências de corte de cada folha.",aboutInfo:"Informações sobre a aplicação e direitos."},
            "en": {settings:"SETTINGS",help:"HELP",about:"ABOUT",printers:"Printers and calibration",intro:"General preferences",help1:"Getting started: import an image or create large text.",help2:"Assembly: print at 100%, without fit to page.",help3:"Follow the cutting references on every sheet.",aboutInfo:"Application information and rights."},
            "es": {settings:"AJUSTES",help:"AYUDA",about:"ACERCA DE",printers:"Impresoras y calibración",intro:"Preferencias generales",help1:"Primeros pasos: importa una imagen o crea texto gigante.",help2:"Montaje: imprime al 100 %, sin ajustar a la página.",help3:"Sigue las marcas de corte de cada hoja.",aboutInfo:"Información de la aplicación y derechos."},
            "fr": {settings:"PARAMÈTRES",help:"AIDE",about:"À PROPOS",printers:"Imprimantes et étalonnage",intro:"Préférences générales",help1:"Démarrage : importez une image ou créez un grand texte.",help2:"Assemblage : imprimez à 100 %, sans adapter à la page.",help3:"Suivez les repères de découpe de chaque feuille.",aboutInfo:"Informations sur l'application et droits."},
            "it": {settings:"IMPOSTAZIONI",help:"AIUTO",about:"INFO",printers:"Stampanti e calibrazione",intro:"Preferenze generali",help1:"Per iniziare: importa un'immagine o crea testo gigante.",help2:"Montaggio: stampa al 100%, senza adattare alla pagina.",help3:"Segui i riferimenti di taglio su ogni foglio.",aboutInfo:"Informazioni e diritti dell'applicazione."}
        }
        return (labels[studio.language] || labels["pt-PT"])[key] || key
    }
    function controlLabel(key) {
        var translations = {
          "pt-PT": {theme:"TEMA VISUAL", language:"IDIOMA", printerHint:"Perfis guardados por impressora e formato. Imprime a 100% e confirma as medidas numa impressora física.", notification:"NOTIFICAÇÃO"},
          "en": {theme:"APPEARANCE", language:"LANGUAGE", printerHint:"Profiles are saved per printer and paper format. Print at 100% and check the physical measurements.", notification:"NOTIFICATION"},
          "es": {theme:"APARIENCIA", language:"IDIOMA", printerHint:"Perfiles guardados por impresora y formato. Imprime al 100 % y verifica las medidas.", notification:"NOTIFICACIÓN"},
          "fr": {theme:"APPARENCE", language:"LANGUE", printerHint:"Profils enregistrés par imprimante et format. Imprimez à 100 % et vérifiez les mesures.", notification:"NOTIFICATION"},
          "it": {theme:"ASPETTO", language:"LINGUA", printerHint:"Profili salvati per stampante e formato. Stampa al 100% e verifica le misure.", notification:"NOTIFICA"}
        }
        return (translations[studio.language] || translations["pt-PT"])[key] || key
    }
    property bool light: studio.theme === "Pearl Titanium"
    property color ink: (win.light ? "#25364A" : "#EEF3FB")
    property color muted: (win.light ? "#576879" : "#8795AD")
    property color line: (win.light ? "#BBC4CC" : "#273449")
    property color gold: (win.light ? "#B97543" : "#E9A66B")
    property color blue: (win.light ? "#4772AE" : "#5E92EC")
    property bool details: false
    property int mode: 0
    property bool perspective: true
    property real tileZoom: 1

    component Caption: Text {
        color: (win.light ? "#63758B" : "#899BB7"); font.pixelSize: 11; font.weight: Font.DemiBold
        font.letterSpacing: 2.1
    }
    component ActionButton: Button {
        id: ab
        property bool primary: false
        implicitHeight: 46
        background: Rectangle {
            radius: 12
            color: ab.down ? (win.light ? "#A96B40" : "#CE8F5B") : (ab.primary ? (win.light ? "#B97543" : "#E9A66B") : (ab.hovered ? (win.light ? "#C7D2DA" : "#23334B") : (win.light ? "#D7DEE2" : "#1A283D")))
            border.color: ab.primary ? (win.light ? "#BD814E" : "#F5BF8A") : (win.light ? "#A7B5C0" : "#34465E")
            border.width: 1
            Behavior on color { ColorAnimation { duration: 150 } }
        }
        contentItem: Text {
            text: ab.text; font.pixelSize: 13; font.weight: Font.DemiBold
            color: ab.primary ? (win.light ? "#18283C" : "#1B1720") : (win.light ? "#263B53" : "#EAF1FC")
            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
        }
    }
    // Navegação do Control Center: largura mínima zero para não extravasar
    // a barra lateral quando o texto traduzido é comprido (Private Preview).
    component CenterNavButton: Button {
        id: cnb
        property bool primary: false
        implicitWidth: 0
        implicitHeight: 54
        Layout.minimumWidth: 0
        background: Rectangle {
            radius: 12
            color: cnb.down ? (win.light ? "#A96B40" : "#CE8F5B")
                : (cnb.primary ? (win.light ? "#B97543" : "#E9A66B")
                : (cnb.hovered ? (win.light ? "#C7D2DA" : "#23334B")
                : (win.light ? "#D7DEE2" : "#1A283D")))
            border.color: cnb.primary ? (win.light ? "#BD814E" : "#F5BF8A")
                : (win.light ? "#A7B5C0" : "#34465E")
            border.width: 1
            Behavior on color { ColorAnimation { duration: 150 } }
        }
        contentItem: Text {
            text: cnb.text
            color: cnb.primary ? (win.light ? "#18283C" : "#1B1720")
                : (win.light ? "#263B53" : "#EAF1FC")
            font.pixelSize: 12
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.WordWrap
            maximumLineCount: 2
            elide: Text.ElideRight
            leftPadding: 8
            rightPadding: 8
            clip: true
        }
    }
    component StudioField: TextField {
        color: (win.light ? "#25364A" : "#EFF4FF"); selectedTextColor: (win.light ? "#FFFFFF" : "#FFFFFF"); selectionColor: (win.light ? "#7594B8" : "#385F9E")
        font.pixelSize: 15
        padding: 12
        background: Rectangle { color: (win.light ? "#E0E5E7" : "#0C1728"); radius: 11; border.color: parent.activeFocus ? (win.light ? "#B97543" : "#E9A66B") : (win.light ? "#9AAAB8" : "#35445B") }
    }
    component LuxuryCombo: ComboBox {
        id: cb
        property bool localizeChoices: false
        implicitHeight: 44
        font.pixelSize: 13
        background: Rectangle {
            color: (win.light ? "#D7DFE3" : "#101F32"); border.color: cb.activeFocus ? (win.light ? "#B97543" : "#E9A66B") : (win.light ? "#A5B2BF" : "#36475E"); radius: 10
        }
        contentItem: Text { leftPadding: 14; rightPadding: 28; text: cb.localizeChoices ? win.choice(cb.currentText) : cb.displayText; color: (win.light ? "#26384A" : "#EAF0FB"); verticalAlignment: Text.AlignVCenter; font.pixelSize: 13; elide: Text.ElideRight }
        indicator: Text { text: "⌄"; color: (win.light ? "#B97543" : "#E9A66B"); font.pixelSize: 20; anchors.right: parent.right; anchors.rightMargin: 13; anchors.verticalCenter: parent.verticalCenter }
        popup: Popup {
            y: cb.height+5; width: cb.width; implicitHeight: contentItem.implicitHeight+8
            padding: 4
            background: Rectangle { color: (win.light ? "#E1E5E8" : "#18283E"); radius: 9; border.color: (win.light ? "#A5B3C1" : "#445670") }
            contentItem: ListView {
                implicitHeight: contentHeight
                model: cb.popup.visible ? cb.delegateModel : null
                currentIndex: cb.highlightedIndex
                clip: true
            }
        }
        delegate: ItemDelegate {
            width: cb.width-8; height: 38
            contentItem: Text { text: cb.localizeChoices ? win.choice(modelData) : modelData; color: (win.light ? "#26384A" : "#EAF0FB"); font.pixelSize: 13; verticalAlignment: Text.AlignVCenter; leftPadding: 10 }
            background: Rectangle { radius: 6; color: highlighted ? (win.light ? "#C7D7E4" : "#34537A") : "transparent" }
            highlighted: cb.highlightedIndex===index
        }
    }

    Rectangle {
        id: glow
        width: 730; height: 730; radius: 365
        x: win.width-450; y: -440
        color: (win.light ? "#D9E0E4" : "#15294A"); opacity: .32
    }
    ColumnLayout {
        anchors.fill: parent; anchors.margins: 26; spacing: 17
        // Top bar
        RowLayout {
            Layout.fillWidth: true; Layout.preferredHeight: 65; spacing: 16
            Rectangle {
                width: 46; height: 46; radius: 15
                color: (win.light ? "#D1DADE" : "#14253A"); border.color: (win.light ? "#A3B3C2" : "#395372")
                Image { anchors.fill: parent; anchors.margins: 1; source: "../assets/branding/postertile_icon.png"; fillMode: Image.PreserveAspectFit; smooth: true }
            }
            ColumnLayout {
                spacing: 1
                Text { text: "NONIVERUS"; color: (win.light ? "#25364A" : "#F6F8FE"); font.family: "Georgia"; font.pixelSize: 25; font.letterSpacing: 3.7 }
                Caption { text: "POSTERTILE  /  LUXURY STUDIO" }
            }
            Item { Layout.fillWidth: true }
            Rectangle { width: 7; height: 7; radius: 4; color: (win.light ? "#AF7045" : "#DFA36F") }
            Text { text: "PRECISION PRINTING"; color: muted; font.pixelSize: 11; font.letterSpacing: 2 }
            Rectangle { width: 1; height: 26; color: line; Layout.leftMargin: 14; Layout.rightMargin: 14 }
            ActionButton { text: "⚙  " + win.centerLabel("settings"); onClicked: centerDialog.open() }
            Text { text: "v0.9.0.1  /  " + studio.editionName; color: (win.light ? "#516477" : "#CBD6E8"); font.pixelSize: 11 }
        }
        Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: (win.light ? "#B4C1CA" : "#25334A") }

        RowLayout {
            Layout.fillWidth: true; Layout.fillHeight: true; spacing: 18
            // Left workspace
            Rectangle {
                Layout.preferredWidth: 356; Layout.fillHeight: true
                color: (win.light ? "#D5DCE0" : "#101B2D"); radius: 20; border.color: (win.light ? "#B3BEC7" : "#2A3A50")
                Flickable {
                    anchors.fill: parent
                    anchors.margins: 10
                    anchors.bottomMargin: 94
                    contentWidth: width
                    contentHeight: controls.implicitHeight + 24
                    clip: true
                    boundsBehavior: Flickable.StopAtBounds
                    ScrollBar.vertical: ScrollBar {
                         policy: ScrollBar.AsNeeded
                         width: 7
                         contentItem: Rectangle {
                             implicitWidth: 5
                             radius: 3
                             color: (win.light ? "#899CA9" : "#49647F")
                             opacity: 0.7
                         }
                         background: Rectangle { color: "transparent" }
                     }
                    ColumnLayout {
                    id: controls
                    x: 12; y: 12
                    width: parent.width - 32
                    spacing: 16
                    Caption { text: win.t("01  /  CONFIGURAÇÃO") }
                    Text { text: win.t("Cria sem limites."); color: ink; font.pixelSize: 24; font.family: "Georgia" }
                    Text { text: win.t("Precisão profissional em cada folha."); color: muted; font.pixelSize: 12 }
                    Caption { text: win.t("02  /  ORIGEM DO PROJETO") }
                    RowLayout {
                        Layout.fillWidth: true; spacing: 8
                        ActionButton { Layout.fillWidth: true; text: "▧  " + win.t("IMAGEM"); primary: studio.sourceMode === "image"; onClicked: studio.chooseImage() }
                        ActionButton { Layout.fillWidth: true; text: "T  " + win.t("TEXTO GIGANTE"); primary: studio.sourceMode === "text"; onClicked: studio.createText() }
                    }
                    ActionButton { Layout.fillWidth: true; text: win.compositionLabel(); primary: studio.sourceMode === "composition"; onClicked: studio.composeImageText() }
                    ActionButton { visible: studio.sourceMode === "composition"; Layout.fillWidth: true; text: win.editCompositionLabel(); onClicked: studio.composeImageText() }
                    Text { visible: studio.sourceMode === "text"; Layout.fillWidth: true; text: win.t("Cria uma frase usando as fontes do teu computador."); color: muted; font.pixelSize: 10; wrapMode: Text.WordWrap }
                    ActionButton { visible: studio.sourceMode === "text"; Layout.fillWidth: true; text: win.t("EDITAR TEXTO"); onClicked: studio.createText() }
                     Text { text: studio.filename; color: (win.light ? "#52667B" : "#B9C7DC"); font.pixelSize: 11; elide: Text.ElideMiddle; Layout.fillWidth: true }
                    Rectangle { Layout.fillWidth: true; height: 1; color: line }
                    Caption { text: win.t("03  /  FORMATO FINAL") }
                    LuxuryCombo {
                        id: format
                        Layout.fillWidth: true
                        model: ["Personalizado", "A3 horizontal (2 A4)", "A3 vertical (2 A4)", "A3 horizontal", "A3 vertical", "A2 horizontal", "A2 vertical", "A1 horizontal", "A1 vertical"]
                        onActivated: { studio.setFormat(currentText); a3Mode.currentIndex=0; heightInput.text=studio.heightCm.toFixed(1); widthInput.text=studio.widthCm.toFixed(1) }
                    }
                    RowLayout {
                        Layout.fillWidth: true; spacing: 12
                        ColumnLayout {
                            Layout.fillWidth: true; spacing: 6
                            Text { text: win.t("Altura (cm)"); color: muted; font.pixelSize: 12 }
                            StudioField { id: heightInput; Layout.fillWidth: true; text: studio.heightCm.toFixed(1); validator: DoubleValidator { bottom: 0.1; top: 1000 } onEditingFinished: { studio.setHeight(text); widthInput.text=studio.widthCm.toFixed(1); text=studio.heightCm.toFixed(1); format.currentIndex=0 } }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true; spacing: 6
                            Text { text: win.t("Largura (cm)"); color: muted; font.pixelSize: 12 }
                            StudioField { id: widthInput; Layout.fillWidth: true; text: studio.widthCm.toFixed(1); validator: DoubleValidator { bottom: 0.1; top: 1000 } onEditingFinished: { studio.setWidth(text); heightInput.text=studio.heightCm.toFixed(1); text=studio.widthCm.toFixed(1); format.currentIndex=0 } }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true; height: 56; radius: 11
                        color: (win.light ? "#CBD7DD" : "#192C43"); border.color: (win.light ? "#A7B5C0" : "#314761")
                        RowLayout {
                            anchors.fill: parent; anchors.margins: 13; spacing: 7
                            Text { text: "◇"; color: gold; font.pixelSize: 25 }
                            ColumnLayout {
                                spacing: 4
                                Text { text: win.t("PROPORÇÃO PRESERVADA"); color: (win.light ? "#3B4A58" : "#F5E2D0"); font.pixelSize: 11; font.weight: Font.DemiBold }
                                Text { text: win.t("Sem deformar a imagem original"); color: (win.light ? "#5D6E80" : "#99ACC7"); font.pixelSize: 10 }
                            }
                        }
                    }
                    Rectangle { Layout.fillWidth: true; height: 1; color: line }
                    Caption { text: win.framingLabel("heading") }
                    Text {
                        Layout.fillWidth: true; wrapMode: Text.WordWrap
                        text: win.framingLabel("intro")
                        color: win.muted; font.pixelSize: 11
                    }
                    LuxuryCombo {
                        id: framingMode
                        Layout.fillWidth: true
                        model: [
                            win.framingLabel("fit"),
                            win.framingLabel("fill"),
                            win.framingLabel("custom")
                        ]
                        currentIndex: studio.fitMode === "Ajustar" ? 0 :
                                      (studio.fitMode === "Preencher" ? 1 : 2)
                        onActivated: studio.setFitMode(["Ajustar","Preencher","Personalizado"][currentIndex])
                    }
                    Text {
                        Layout.fillWidth: true
                        text: studio.fitMode === "Ajustar" ? win.framingLabel("fitInfo") :
                              (studio.fitMode === "Preencher" ? win.framingLabel("fillInfo") :
                               win.framingLabel("customInfo"))
                        color: win.muted; font.pixelSize: 11; wrapMode: Text.WordWrap
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        visible: studio.fitMode === "Personalizado"
                        spacing: 4
                        RowLayout {
                            Layout.fillWidth: true
                            Text { text: win.framingLabel("horiz"); color: win.ink; font.pixelSize: 11 }
                            Item { Layout.fillWidth: true }
                            Text { text: Math.round(studio.focalX) + "%"; color: win.gold; font.pixelSize: 11 }
                        }
                        Slider {
                            id: horizontalFocus
                            Layout.fillWidth: true
                            from: 0; to: 100; stepSize: 1
                            value: studio.focalX
                            onMoved: studio.setFocalPosition(value,studio.focalY)
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            Text { text: win.framingLabel("vert"); color: win.ink; font.pixelSize: 11 }
                            Item { Layout.fillWidth: true }
                            Text { text: Math.round(studio.focalY) + "%"; color: win.gold; font.pixelSize: 11 }
                        }
                        Slider {
                            id: verticalFocus
                            Layout.fillWidth: true
                            from: 0; to: 100; stepSize: 1
                            value: studio.focalY
                            onMoved: studio.setFocalPosition(studio.focalX,value)
                        }
                        ActionButton {
                            Layout.fillWidth: true
                            text: win.framingLabel("center")
                            onClicked: studio.setFocalPosition(50,50)
                        }
                    }
                    Rectangle { Layout.fillWidth: true; height: 1; color: line }
                    Caption { text: win.t("04  /  PAPEL E IMPRESSÃO") }
                    ColumnLayout {
                        visible: studio.a3TwoEnabled
                        Layout.fillWidth: true
                        spacing: 8
                        Rectangle {
                            Layout.fillWidth: true; implicitHeight: 104; radius: 12
                            color: (win.light ? "#D1DBDF" : "#1A2C40")
                            border.color: (win.light ? "#B97543" : "#D69A69")
                            ColumnLayout {
                                anchors.fill: parent; anchors.margins: 12; spacing: 6
                                Text {
                                    Layout.fillWidth: true
                                    text: studio.language==="pt-PT" ? "A3 EM 2 FOLHAS A4" :
                                          studio.language==="en" ? "A3 ON TWO A4 SHEETS" :
                                          studio.language==="es" ? "A3 EN DOS HOJAS A4" :
                                          studio.language==="fr" ? "A3 SUR DEUX FEUILLES A4" :
                                          "A3 SU DUE FOGLI A4"
                                    font.pixelSize: 12; font.bold: true; color: win.gold
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: studio.language==="pt-PT" ? "O PDF terá sempre 2 folhas A4. Escolhe como tratar as margens da tua impressora." :
                                          studio.language==="en" ? "The PDF always has 2 A4 pages. Choose how to handle your printer margins." :
                                          studio.language==="es" ? "El PDF tendrá 2 páginas A4. Elige cómo gestionar los márgenes." :
                                          studio.language==="fr" ? "Le PDF aura 2 pages A4. Choisissez comment gérer les marges." :
                                          "Il PDF avrà 2 pagine A4. Scegli come gestire i margini."
                                    font.pixelSize: 11; color: win.ink; wrapMode: Text.WordWrap
                                }
                            }
                        }
                        LuxuryCombo {
                            id: a3Mode
                            Layout.fillWidth: true
                            model: studio.language==="pt-PT" ?
                                ["Com margens (A3 reduzido)", "Sem margens (A3 exato)"] :
                                studio.language==="en" ?
                                ["Safe margins (smaller than A3)", "Borderless (exact A3)"] :
                                studio.language==="es" ?
                                ["Con márgenes (menor que A3)", "Sin márgenes (A3 exacto)"] :
                                studio.language==="fr" ?
                                ["Avec marges (moins que A3)", "Sans marges (A3 exact)"] :
                                ["Con margini (minore di A3)", "Senza margini (A3 esatto)"]
                            currentIndex: 0
                            onActivated: studio.setA3TwoMode(currentIndex===0 ? "safe" : "borderless")
                        }
                        Text {
                            Layout.fillWidth: true
                            text: studio.a3TwoMode==="borderless" ?
                                (studio.language==="pt-PT" ? "A3 exato: exige impressão A4 sem margens (borderless), a 100%." :
                                 studio.language==="en" ? "Exact A3: requires borderless A4 printing at 100%." :
                                 studio.language==="es" ? "A3 exacto: requiere impresión A4 sin márgenes al 100%." :
                                 studio.language==="fr" ? "A3 exact : impression A4 sans marges à 100 % requise." :
                                 "A3 esatto: richiede stampa A4 senza margini al 100%.") :
                                (studio.language==="pt-PT" ? "Impressora comum: recorta as margens interiores e une. A imagem final fica ligeiramente menor que A3." :
                                 studio.language==="en" ? "Standard printer: trim inner white margins and join. Finished image is smaller than A3." :
                                 studio.language==="es" ? "Impresora normal: recorta los márgenes interiores y une. La imagen queda menor que A3." :
                                 studio.language==="fr" ? "Imprimante standard : coupez les marges intérieures et assemblez. Image plus petite que A3." :
                                 "Stampante normale: taglia i margini interni e unisci. Immagine più piccola di A3.")
                            color: win.muted; font.pixelSize: 11; wrapMode: Text.WordWrap
                        }
                    }
                    RowLayout {
                        visible: !studio.a3TwoEnabled
                        Layout.fillWidth: true; spacing: 7
                        Repeater {
                            model: ["A4", "A3", "AUTO"]
                            delegate: Rectangle {
                                required property string modelData
                                readonly property bool selected: modelData === "AUTO"
                                    ? paper.currentIndex === 0
                                    : paper.currentText.indexOf(modelData) === 0
                                Layout.fillWidth: true
                                implicitHeight: 40
                                radius: 9
                                color: selected ? (win.light ? "#C39A78" : "#A97045") : (win.light ? "#D7DFE3" : "#15283D")
                                border.color: selected ? gold : line
                                Text {
                                    anchors.centerIn: parent
                                    text: modelData
                                    font.pixelSize: 13; font.bold: true
                                    color: selected ? (win.light ? "#1A2B3D" : "#091525") : ink
                                }
                                MouseArea {
                                    anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        paper.currentIndex = modelData === "A4" ? 1 : (modelData === "A3" ? 3 : 0)
                                        applyConfig()
                                    }
                                }
                            }
                        }
                    }
                    Text {
                        visible: !studio.a3TwoEnabled
                        Layout.fillWidth: true
                        text: paper.currentIndex === 0
                            ? win.t("AUTO: escolhe A4 ou A3 pela menor quantidade de folhas.")
                            : win.t("SELECIONADO: ") + win.choice(paper.currentText) + win.t(" · podes alterar a orientação em baixo.")
                        font.pixelSize: 10; color: muted; wrapMode: Text.WordWrap
                    }
                    LuxuryCombo {
                        id: paper; localizeChoices: true; Layout.fillWidth: true; currentIndex: 1
                        visible: !studio.a3TwoEnabled
                        model: ["Auto","A4 vertical","A4 horizontal","A3 vertical","A3 horizontal"]
                        onActivated: applyConfig()
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        Caption { text: win.t("02  /  PRINT ENGINE") }
                        Item { Layout.fillWidth: true }
                        Text { text: details ? win.t("OCULTAR  −") : win.t("AVANÇADO  ＋"); color: gold; font.pixelSize: 11
                            MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: details=!details }
                        }
                    }
                    ColumnLayout {
                        visible: details; Layout.fillWidth: true; spacing: 9
                        Text { text: win.t("Método de montagem"); color: muted; font.pixelSize: 11 }
                        LuxuryCombo { id: assembly; localizeChoices: true; Layout.fillWidth: true; model: ["Sobrepor","Cortar e unir"]; onActivated: applyConfig() }
                        RowLayout {
                            Layout.fillWidth: true; spacing: 10
                            ColumnLayout {
                                Layout.fillWidth: true
                                Text { text: win.t("Margem (mm)"); color: muted; font.pixelSize: 11 }
                                StudioField { id: marginField; Layout.fillWidth: true; text: "8"; onEditingFinished: applyConfig() }
                            }
                            ColumnLayout {
                                Layout.fillWidth: true
                                Text { text: win.t("Sobreposição (mm)"); color: muted; font.pixelSize: 11 }
                                StudioField { id: overlapField; Layout.fillWidth: true; text: "10"; onEditingFinished: applyConfig() }
                            }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true; height: 85; radius: 14
                        color: (win.light ? "#D3DCE1" : "#19283A"); border.color: (win.light ? "#A9B7C2" : "#33455C")
                        ColumnLayout {
                            anchors.fill: parent; anchors.margins: 14; spacing: 6
                            Caption { text: win.t("PLANO DE IMPRESSÃO") }
                            Text { text: studio.summary; color: (win.light ? "#26384B" : "#F5F7FD"); font.pixelSize: 13; font.weight: Font.DemiBold; wrapMode: Text.Wrap }
                        }
                    }
                    }
                }
                Rectangle {
                    anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: parent.bottom
                    anchors.margins: 10; height: 76; radius: 13
                    color: (win.light ? "#D5DCE0" : "#101B2D")
                    ColumnLayout {
                        anchors.fill: parent; spacing: 4
                        ActionButton { Layout.fillWidth: true; Layout.preferredHeight: 52; primary: true; text: win.t("EXPORTAR PDF  ↗"); onClicked: { applyConfig(); studio.export() } }
                        Text { Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; text: "A4 / A3  ·  100%"; color: win.muted; font.pixelSize: 10 }
                    }
                }
            }
            // Main stage
            Rectangle {
                Layout.fillWidth: true; Layout.fillHeight: true; color: (win.light ? "#D5DCE0" : "#101C2C"); radius: 20; border.color: (win.light ? "#ACBAC4" : "#2A3B50")
                ColumnLayout {
                    anchors.fill: parent; anchors.margins: 20; spacing: 12
                    RowLayout {
                        Layout.fillWidth: true
                        ColumnLayout {
                            Caption { text: win.t("ATELIER  /  LIVE CANVAS") }
                            Text { text: win.t("O teu projeto, em grande."); color: ink; font.family: "Georgia"; font.pixelSize: 23 }
                        }
                        Item { Layout.fillWidth: true }
                        ActionButton { text: perspective ? win.t("◇   VISTA PLANA") : win.t("◇   PERSPETIVA"); onClicked: perspective=!perspective }
                        ActionButton { text: "−"; onClicked: tileZoom=Math.max(0.6,tileZoom-0.15) }
                        ActionButton { text: "+"; onClicked: tileZoom=Math.min(1.8,tileZoom+0.15) }
                    }
                    Rectangle {
                        id: canvasBox
                        Layout.fillWidth: true; Layout.fillHeight: true
                        radius: 16; clip: true
                        color: (win.light ? "#E1E6E8" : "#0B1422"); border.color: (win.light ? "#A5B4C1" : "#24364A")
                        // Subtle stage glow
                        Rectangle { width: parent.width*.80; height: parent.height*.75; anchors.centerIn: parent; radius: width/2; color: (win.light ? "#CFDBE1" : "#152C46"); opacity: .5 }
                        Item {
                            id: stage
                            width: Math.min(canvasBox.width*0.78,canvasBox.height*0.80*(studio.previewRatio))
                            height: Math.min(canvasBox.height*0.78,canvasBox.width*0.78*(1/Math.max(0.01,studio.previewRatio)))
                            anchors.centerIn: parent
                            scale: tileZoom
                            rotation: perspective ? -2.5 : 0
                            Behavior on rotation { NumberAnimation { duration: 350; easing.type: Easing.OutCubic } }
                            Rectangle { anchors.fill: parent; anchors.leftMargin: 11; anchors.topMargin: 14; radius: 6; color: (win.light ? "#C4D0D8" : "#03070F"); opacity: .78 }
                            Rectangle { anchors.fill: parent; color: (win.light ? "#CED6DB" : "#121A27"); border.color: (win.light ? "#6D7E8D" : "#566D87"); border.width: 1; radius: 5 }
                            Image {
                                id: artwork
                                anchors.fill: parent; anchors.margins: 3
                                source: studio.framedPreviewUrl
                                fillMode: Image.PreserveAspectFit
                                cache: false; asynchronous: true
                                visible: studio.imageUrl.length>0
                            }
                            Text {
                                visible: studio.imageUrl.length===0
                                anchors.centerIn: parent
                                text: win.t("＋\n\nIMPORTA A TUA IMAGEM\nPARA COMEÇAR")
                                font.pixelSize: 15; font.letterSpacing: 2
                                color: (win.light ? "#627486" : "#8395AD"); horizontalAlignment: Text.AlignHCenter
                            }
                            Repeater {
                                model: Math.max(0,studio.columns-1)
                                Rectangle { x: (index+1)*stage.width/studio.columns; y: 0; height: stage.height; width: 1; color: (win.light ? "#B97543" : "#E9A66B"); opacity: .75 }
                            }
                            Repeater {
                                model: Math.max(0,studio.rows-1)
                                Rectangle { y: (index+1)*stage.height/studio.rows; x: 0; width: stage.width; height: 1; color: (win.light ? "#B97543" : "#E9A66B"); opacity: .75 }
                            }
                        }
                        Rectangle {
                            anchors.left: parent.left; anchors.top: parent.top; anchors.margins: 20
                            color: (win.light ? "#CBD7DF" : "#172940"); radius: 9; width: labelPreview.width+24; height: 32
                            Text { id: labelPreview; anchors.centerIn: parent; text: win.t("●  VISTA DE MONTAGEM"); color: (win.light ? "#50667A" : "#AFC2DD"); font.pixelSize: 10; font.letterSpacing: 1.5 }
                        }
                        Text {
                            anchors.bottom: parent.bottom; anchors.horizontalCenter: parent.horizontalCenter; anchors.bottomMargin: 18
                            text: win.t("Visualização ilustrativa  ·  O PDF usa coordenadas físicas exatas")
                            color: (win.light ? "#667A8F" : "#8093AC"); font.pixelSize: 11
                        }
                    }
                    RowLayout {
                        Layout.fillWidth: true; Layout.preferredHeight: 56
                        Text { text: "◈"; color: gold; font.pixelSize: 23 }
                        ColumnLayout {
                            spacing: 4
                            Text { text: win.t("PROFESSIONAL OUTPUT"); color: (win.light ? "#273A50" : "#EDF1FC"); font.pixelSize: 11; font.weight: Font.DemiBold; font.letterSpacing: 1.5 }
                            Text { text: studio.status.replace("PDF pronto:",win.t("PDF pronto:")); color: (win.light ? "#637689" : "#8EA2BC"); font.pixelSize: 11; elide: Text.ElideMiddle; Layout.maximumWidth: 670 }
                        }
                        Item { Layout.fillWidth: true }
                        Text { text: studio.pageCount+" "+win.t("PÁGINAS"); color: (win.light ? "#AD7044" : "#E8AF7E"); font.pixelSize: 13; font.weight: Font.DemiBold }
                    }
                }
            }
        }
        RowLayout {
            Layout.fillWidth: true; Layout.preferredHeight: 18
            Text { text: "NONIVERUS   /   SOFTWARE WITHOUT STRINGS."; color: (win.light ? "#687B8E" : "#6D809B"); font.pixelSize: 10; font.letterSpacing: 1 }
            Item { Layout.fillWidth: true }
            Text { text: "LUXURY STUDIO  ·  EDITION 06"; color: (win.light ? "#687A8C" : "#8496AC"); font.pixelSize: 10; font.letterSpacing: 1 }
        }
    }
    // NONIVERUS Control Center — painel nativo, sem cabeçalho/rodapé de Dialog
    Popup {
        id: centerDialog
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        parent: Overlay.overlay
        x: Math.max(0, win.width - width)
        y: 0
        width: Math.min(825, win.width * 0.85)
        height: win.height
        padding: 0
        background: Rectangle {
            color: win.light ? "#E7E3DB" : "#101A2B"
            border.color: win.line
            border.width: 1
        }
        Overlay.modal: Rectangle { color: "#080F1D"; opacity: 0.50 }
        contentItem: ColumnLayout {
            spacing: 0
            Rectangle {
                Layout.fillWidth: true; Layout.preferredHeight: 115
                color: win.light ? "#DBE0E2" : "#14233A"
                ColumnLayout {
                    anchors.fill: parent; anchors.margins: 25; spacing: 8
                    RowLayout {
                        Layout.fillWidth: true
                        Caption { text: "NONIVERUS  /  LUXURY STUDIO" }
                        Item { Layout.fillWidth: true }
                        ActionButton { text: "×"; onClicked: centerDialog.close() }
                    }
                    Text { text: "Control Center"; color: win.ink; font.family: "Georgia"; font.pixelSize: 27 }
                }
            }
            RowLayout {
                Layout.fillWidth: true; Layout.fillHeight: true; spacing: 0
                Rectangle {
                    // 240px em ecrãs normais; adapta-se a janelas pequenas.
                    Layout.preferredWidth: Math.min(240, Math.max(195, centerDialog.width * 0.29))
                    Layout.minimumWidth: 195
                    Layout.fillHeight: true
                    clip: true
                    color: win.light ? "#D2DADE" : "#112035"
                    ColumnLayout {
                        anchors.fill: parent; anchors.margins: 15; spacing: 9
                        CenterNavButton { Layout.fillWidth: true; text: "⚙  " + win.centerLabel("settings"); primary: win.centerPage === 0; onClicked: win.centerPage = 0 }
                        CenterNavButton { Layout.fillWidth: true; text: "▤  " + win.centerLabel("printers"); primary: win.centerPage === 1; onClicked: win.centerPage = 1 }
                        CenterNavButton { Layout.fillWidth: true; text: "?  " + win.centerLabel("help"); primary: win.centerPage === 2; onClicked: win.centerPage = 2 }
                        CenterNavButton { Layout.fillWidth: true; text: "ⓘ  " + win.centerLabel("about"); primary: win.centerPage === 3; onClicked: win.centerPage = 3 }
                        Item { Layout.fillHeight: true }
                        Text {
                            Layout.fillWidth: true
                            Layout.minimumWidth: 0
                            text: "v0.9.0.1  /  " + studio.editionName
                            color: win.light ? "#63758B" : "#899BB7"
                            font.pixelSize: 10
                            font.weight: Font.DemiBold
                            font.letterSpacing: 1.0
                            wrapMode: Text.WordWrap
                            maximumLineCount: 2
                            elide: Text.ElideRight
                        }
                    }
                }
                Rectangle {
                    Layout.fillWidth: true; Layout.fillHeight: true
                    color: win.light ? "#E7E3DB" : "#101A2B"
                    Flickable {
                        anchors.fill: parent; anchors.margins: 28
                        contentWidth: width
                        contentHeight: centerContents.implicitHeight + 24
                        clip: true
                        ScrollBar.vertical: ScrollBar { }
                        ColumnLayout {
                            id: centerContents
                            width: parent.width
                            spacing: 16
                            ColumnLayout {
                                visible: win.centerPage === 0
                                Layout.fillWidth: true; spacing: 15
                                Text { text: win.centerLabel("intro"); color: win.ink; font.family: "Georgia"; font.pixelSize: 22 }
                                Rectangle { Layout.fillWidth: true; height: 1; color: win.line }
                                Caption { text: win.controlLabel("theme") }
                                LuxuryCombo {
                                    Layout.fillWidth: true
                                    model: ["Midnight Sapphire", "Pearl Titanium"]
                                    Component.onCompleted: currentIndex = (studio.theme === "Pearl Titanium" ? 1 : 0)
                                    onActivated: studio.setTheme(currentText)
                                }
                                Caption { text: win.controlLabel("language") }
                                LuxuryCombo {
                                    Layout.fillWidth: true
                                    model: ["Português", "English", "Español", "Français", "Italiano"]
                                    Component.onCompleted: currentIndex = Math.max(0, ["pt-PT","en","es","fr","it"].indexOf(studio.language))
                                    onActivated: studio.setLanguage(["pt-PT","en","es","fr","it"][currentIndex])
                                }
                            }
                            ColumnLayout {
                                visible: win.centerPage === 1
                                Layout.fillWidth: true; spacing: 16
                                Text { text: win.centerLabel("printers"); color: win.ink; font.family: "Georgia"; font.pixelSize: 22 }
                                Rectangle { Layout.fillWidth: true; height: 1; color: win.line }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: win.controlLabel("printerHint"); color: win.muted; font.pixelSize: 13 }
                                ActionButton { Layout.fillWidth: true; text: win.t("CALIBRAR"); onClicked: studio.calibrationDialog() }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: studio.calibrationStatus === "Calibração não selecionada" ? win.t("Calibração não selecionada") : studio.calibrationStatus; color: win.muted; font.pixelSize: 12 }
                            }
                            ColumnLayout {
                                visible: win.centerPage === 2
                                Layout.fillWidth: true; spacing: 16
                                Text { text: win.centerLabel("help"); color: win.ink; font.family: "Georgia"; font.pixelSize: 22 }
                                Rectangle { Layout.fillWidth: true; height: 1; color: win.line }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: win.centerLabel("help1"); color: win.ink; font.pixelSize: 14 }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: win.centerLabel("help2"); color: win.ink; font.pixelSize: 14 }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: win.centerLabel("help3"); color: win.ink; font.pixelSize: 14 }
                            }
                            ColumnLayout {
                                visible: win.centerPage === 3
                                Layout.fillWidth: true
                                spacing: 17
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 132
                                    radius: 12
                                    color: win.light ? "#DBE0E2" : "#172941"
                                    border.color: win.line
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 18
                                        spacing: 16
                                        Rectangle {
                                            Layout.preferredWidth: 76
                                            Layout.preferredHeight: 76
                                            color: "transparent"
                                            Image {
                                                anchors.fill: parent
                                                source: "../assets/branding/noniverus_logo.png"
                                                fillMode: Image.PreserveAspectFit
                                                smooth: true
                                            }
                                        }
                                        ColumnLayout {
                                            Layout.fillWidth: true
                                            spacing: 5
                                            Text { text: "NONIVERUS"; color: win.ink; font.family: "Georgia"; font.pixelSize: 23; font.letterSpacing: 2.2 }
                                            Text { text: "POSTERTILE  /  LUXURY STUDIO"; color: win.gold; font.pixelSize: 11; font.letterSpacing: 1.5 }
                                            Text { text: "PRECISION PRINTING"; color: win.muted; font.pixelSize: 10; font.letterSpacing: 1.1 }
                                        }
                                    }
                                }
                                Text { text: win.aboutText("product"); color: win.ink; font.family: "Georgia"; font.pixelSize: 22 }
                                Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: win.line }
                                Caption { text: win.aboutText("version") }
                                Text { text: "v0.9.0.1  /  " + studio.editionName; color: win.ink; font.pixelSize: 14 }
                                Caption { text: win.aboutText("description") }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: win.centerLabel("aboutInfo"); color: win.ink; font.pixelSize: 13 }
                                Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: win.line }
                                Text { text: win.aboutText("contact"); color: win.ink; font.family: "Georgia"; font.pixelSize: 20 }
                                Text { Layout.fillWidth: true; text: "contact@noniverus.com"; color: win.ink; font.pixelSize: 14; font.bold: true }
                                Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: win.line }
                                Caption { text: win.aboutText("legal") }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: "© 2026 NONIVERUS. All rights reserved."; color: win.ink; font.pixelSize: 12 }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: win.aboutText("legalInfo"); color: win.muted; font.pixelSize: 12 }
                                Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: "Python  ·  PySide6 / Qt Quick  ·  Pillow  ·  ReportLab"; color: win.muted; font.pixelSize: 11 }
                            }
                            Item { Layout.fillHeight: true }
                        }
                    }
                }
            }
        }
    }

    // Mensagens de exportação e erro, no tema do produto (sem QMessageBox do SO).
    property string toastMessage: ""
    Popup {
        id: noticePopup
        modal: false
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        parent: Overlay.overlay
        x: Math.max(12, (win.width - width) / 2)
        y: Math.max(12, win.height - height - 58)
        width: Math.min(560, win.width - 36)
        padding: 20
        background: Rectangle {
            radius: 15
            color: win.light ? "#E8E5DD" : "#18253A"
            border.color: win.gold; border.width: 1
        }
        contentItem: ColumnLayout {
            spacing: 12
            RowLayout {
                Layout.fillWidth: true
                Text { text: "NONIVERUS  /  " + win.controlLabel("notification"); color: win.gold; font.pixelSize: 11; font.weight: Font.DemiBold; font.letterSpacing: 1.2 }
                Item { Layout.fillWidth: true }
                ActionButton { text: "×"; onClicked: noticePopup.close() }
            }
            Text {
                Layout.fillWidth: true
                color: win.ink
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                text: win.toastMessage
            }
        }
    }
    Connections {
        target: studio
        function onNotice(message) {
            win.toastMessage = message
            noticePopup.open()
        }
    }
    Dialog {
        id: aboutDialog
        modal: true
        anchors.centerIn: parent
        width: Math.min(590, win.width-70)
        title: "NONIVERUS PosterTile Luxury Studio"
        standardButtons: Dialog.Close
        background: Rectangle { color: win.light ? "#E7E3DB" : "#101C2C"; radius: 16; border.color: win.light ? "#A6B5C1" : "#35465E" }
        header: Rectangle {
            implicitHeight: 74; color: "transparent"
            Text { anchors.centerIn: parent; text: "NONIVERUS  /  POSTERTILE"; color: win.ink; font.family: "Georgia"; font.pixelSize: 23; font.letterSpacing: 2 }
        }
        contentItem: ColumnLayout {
            spacing: 13
            Text { Layout.fillWidth: true; text: "LUXURY STUDIO  ·  VERSION 0.8.12"; color: win.gold; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter }
            Rectangle { Layout.fillWidth: true; height: 1; color: win.line }
            Text {
                Layout.fillWidth: true; wrapMode: Text.WordWrap; color: win.ink; font.pixelSize: 13
                text: studio.language === "pt-PT" ?
                    "Software de paginação e impressão de grande formato em folhas A4/A3. Desenvolvido sob a identidade NONIVERUS." :
                    studio.language === "en" ? "Large-format poster tiling software for A4/A3 sheets. Developed under the NONIVERUS identity." :
                    studio.language === "es" ? "Software de impresión de gran formato en hojas A4/A3. Desarrollado bajo la identidad NONIVERUS." :
                    studio.language === "fr" ? "Logiciel d'impression grand format sur feuilles A4/A3. Développé sous l'identité NONIVERUS." :
                    "Software per stampe di grande formato su fogli A4/A3. Sviluppato con identità NONIVERUS."
            }
            Text { Layout.fillWidth: true; text: "© 2026 NONIVERUS. All rights reserved."; color: win.ink; font.pixelSize: 12 }
            Text {
                Layout.fillWidth: true; wrapMode: Text.WordWrap; color: win.muted; font.pixelSize: 12
                text: studio.language === "pt-PT" ?
                    "NONIVERUS e os respetivos elementos de identidade são utilizados como sinais distintivos da marca. A sua utilização por terceiros não é autorizada sem consentimento. Este aviso não constitui prova de registo de marca." :
                    studio.language === "en" ? "NONIVERUS and its brand elements are used as distinctive identifiers. Third-party use requires permission. This notice is not proof of trademark registration." :
                    studio.language === "es" ? "NONIVERUS y sus elementos identifican la marca. Su uso por terceros requiere autorización. Este aviso no acredita el registro de la marca." :
                    studio.language === "fr" ? "NONIVERUS et ses éléments identifient la marque. Leur usage par des tiers nécessite une autorisation. Cet avis ne prouve pas un dépôt de marque." :
                    "NONIVERUS e gli elementi del marchio sono segni distintivi. L'uso da parte di terzi richiede autorizzazione. Questo avviso non prova la registrazione del marchio."
            }
            Text { Layout.fillWidth: true; wrapMode: Text.WordWrap; text: "Python · PySide6 / Qt Quick · Pillow · ReportLab"; color: win.muted; font.pixelSize: 11 }
            Text { Layout.fillWidth: true; text: "https://gptonline.ai/"; visible: false }
            Text { Layout.fillWidth: true; text: "NONIVERUS · Software without strings."; color: win.gold; font.pixelSize: 11 }
        }
    }
    function framingLabel(key) {
        const labels = {
            "pt-PT": {
                heading:"ENQUADRAMENTO",intro:"Escolhe como a imagem ocupa as medidas finais, sem a deformar.",
                fit:"Ajustar · imagem inteira",fill:"Preencher · cortar excesso",
                custom:"Personalizado · mover recorte",
                fitInfo:"Mantém toda a imagem. Podem surgir faixas brancas.",
                fillInfo:"Preenche o formato e corta o excesso ao centro.",
                customInfo:"Preenche o formato. Move o foco para escolher a zona visível.",
                horiz:"Foco horizontal",vert:"Foco vertical",center:"CENTRAR ENQUADRAMENTO"
            },
            "en": {
                heading:"IMAGE FRAMING",intro:"Choose how the image fills the final size without distortion.",
                fit:"Fit · entire image",fill:"Fill · crop excess",
                custom:"Custom · move crop",
                fitInfo:"Keeps the full image. White bands may appear.",
                fillInfo:"Fills the poster and crops the overflow at the centre.",
                customInfo:"Fills the poster. Move the focus to choose the visible area.",
                horiz:"Horizontal focus",vert:"Vertical focus",center:"CENTRE FRAMING"
            },
            "es": {
                heading:"ENCUADRE",intro:"Elige cómo ocupar el formato final sin deformar la imagen.",
                fit:"Ajustar · imagen completa",fill:"Rellenar · recortar",
                custom:"Personalizado · mover recorte",
                fitInfo:"Muestra la imagen completa. Puede dejar franjas blancas.",
                fillInfo:"Rellena el formato y recorta el exceso desde el centro.",
                customInfo:"Rellena el formato. Desplaza el foco para elegir la zona visible.",
                horiz:"Foco horizontal",vert:"Foco vertical",center:"CENTRAR ENCUADRE"
            },
            "fr": {
                heading:"CADRAGE",intro:"Choisissez le cadrage au format final sans déformer l’image.",
                fit:"Adapter · image entière",fill:"Remplir · recadrer",
                custom:"Personnalisé · déplacer",
                fitInfo:"Conserve l’image entière. Des bandes blanches peuvent apparaître.",
                fillInfo:"Remplit le format et recadre l’excédent au centre.",
                customInfo:"Remplit le format. Déplacez le point focal pour choisir la zone visible.",
                horiz:"Point focal horizontal",vert:"Point focal vertical",center:"CENTRER LE CADRAGE"
            },
            "it": {
                heading:"INQUADRATURA",intro:"Scegli come occupare il formato finale senza deformare l’immagine.",
                fit:"Adatta · immagine intera",fill:"Riempi · ritaglia",
                custom:"Personalizzato · sposta",
                fitInfo:"Mostra tutta l’immagine. Possono comparire fasce bianche.",
                fillInfo:"Riempie il formato e ritaglia l’eccesso al centro.",
                customInfo:"Riempie il formato. Sposta il fuoco per scegliere l’area visibile.",
                horiz:"Fuoco orizzontale",vert:"Fuoco verticale",center:"CENTRA INQUADRATURA"
            }
        }
        return (labels[studio.language] || labels["pt-PT"])[key] || key
    }
    function compositionLabel() {
        return ({"pt-PT":"▧  IMAGEM + TEXTO","en":"▧  IMAGE + TEXT","es":"▧  IMAGEN + TEXTO","fr":"▧  IMAGE + TEXTE","it":"▧  IMMAGINE + TESTO"})[studio.language] || "▧  IMAGEM + TEXTO"
    }
    function editCompositionLabel() {
        return ({"pt-PT":"EDITAR COMPOSIÇÃO","en":"EDIT COMPOSITION","es":"EDITAR COMPOSICIÓN","fr":"MODIFIER LA COMPOSITION","it":"MODIFICA COMPOSIZIONE"})[studio.language] || "EDITAR COMPOSIÇÃO"
    }
    function aboutText(key) {
        const labels = {
            "pt-PT": { product:"Informações da aplicação", version:"VERSÃO / EDIÇÃO", description:"O PRODUTO", contact:"Contacto e suporte", noEmail:"Email oficial ainda não configurado", emailHint:"Indica o email oficial NONIVERUS. Fica guardado apenas neste computador.", saveEmail:"GUARDAR EMAIL", legal:"INFORMAÇÃO LEGAL", legalInfo:"NONIVERUS e os elementos de identidade são sinais distintivos da marca. Este aviso não comprova um registo de marca." },
            "en": { product:"Application information", version:"VERSION / EDITION", description:"THE PRODUCT", contact:"Contact and support", noEmail:"Official email not configured", emailHint:"Enter the official NONIVERUS email. Stored on this computer only.", saveEmail:"SAVE EMAIL", legal:"LEGAL INFORMATION", legalInfo:"NONIVERUS and its branding are distinctive identifiers. This notice does not establish trademark registration." },
            "es": { product:"Información de la aplicación", version:"VERSIÓN / EDICIÓN", description:"EL PRODUCTO", contact:"Contacto y soporte", noEmail:"Correo oficial sin configurar", emailHint:"Introduce el correo oficial NONIVERUS. Se guarda solo en este equipo.", saveEmail:"GUARDAR CORREO", legal:"INFORMACIÓN LEGAL", legalInfo:"NONIVERUS y sus elementos de identidad son distintivos de marca. Este aviso no acredita un registro de marca." },
            "fr": { product:"Informations sur l’application", version:"VERSION / ÉDITION", description:"LE PRODUIT", contact:"Contact et assistance", noEmail:"Adresse officielle non configurée", emailHint:"Saisissez l’adresse officielle NONIVERUS. Conservée sur cet ordinateur.", saveEmail:"ENREGISTRER L’ADRESSE", legal:"INFORMATIONS JURIDIQUES", legalInfo:"NONIVERUS et son identité constituent des signes distinctifs. Cette mention ne prouve pas un dépôt de marque." },
            "it": { product:"Informazioni sull’applicazione", version:"VERSIONE / EDIZIONE", description:"IL PRODOTTO", contact:"Contatti e assistenza", noEmail:"Email ufficiale non configurata", emailHint:"Inserisci l’email ufficiale NONIVERUS. Resta salvata su questo computer.", saveEmail:"SALVA EMAIL", legal:"INFORMAZIONI LEGALI", legalInfo:"NONIVERUS e la sua identità sono segni distintivi. Questa nota non costituisce prova di registrazione del marchio." }
        }
        const loc = labels[studio.language] || labels["pt-PT"]
        return loc[key] || key
    }
    function applyConfig() { studio.configure(paper.currentText,assembly.currentText,marginField.text,overlapField.text) }
}
